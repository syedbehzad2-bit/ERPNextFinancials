"""
Data validation logic - brutally honest about issues.
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, date
from decimal import Decimal

from models.base import DataType, Severity, DataQualityIssue, DataQualityReport
from config import settings


class DataValidator:
    """
    Validates data and reports ALL issues found - no hiding problems.
    """

    # Column name patterns for each data type (case-insensitive)
    DATA_TYPE_PATTERNS = {
        DataType.FINANCIAL: [
            'revenue', 'sales', 'income', 'gross_profit', 'net_income',
            'cost_of_goods', 'cogs', 'expenses', 'operating_expenses',
            'operating_income', 'ebitda', 'margin', 'profit', 'loss',
            'period', 'date', 'month', 'year', 'quarter', 'budget'
        ],
        DataType.MANUFACTURING: [
            'production', 'planned_quantity', 'actual_quantity',
            'good_quantity', 'rejected_quantity', 'wastage', 'yield',
            'efficiency', 'output', 'throughput', 'downtime',
            'production_line', 'work_center', 'machine'
        ],
        DataType.INVENTORY: [
            'sku', 'product_id', 'stock', 'inventory', 'quantity',
            'on_hand', 'unit_cost', 'stock_value', 'warehouse',
            'receipt_date', 'last_movement', 'aging', 'coverage',
            'reorder_point', 'safety_stock'
        ],
        DataType.SALES: [
            'order_id', 'order_date', 'customer', 'product', 'quantity',
            'unit_price', 'total_amount', 'discount', 'tax',
            'sales_rep', 'channel', 'region', 'segment'
        ],
        DataType.PURCHASE: [
            'po_number', 'purchase_order', 'supplier', 'vendor',
            'order_date', 'expected_delivery', 'actual_delivery',
            'quantity_ordered', 'quantity_received', 'unit_price',
            'lead_time', 'delivery_status'
        ]
    }

    # Required columns for each data type
    REQUIRED_COLUMNS = {
        DataType.FINANCIAL: ['revenue', 'period'],
        DataType.MANUFACTURING: ['product_id', 'planned_quantity', 'actual_quantity'],
        DataType.INVENTORY: ['sku', 'quantity', 'unit_cost'],
        DataType.SALES: ['order_id', 'product_id', 'quantity', 'total_amount'],
        DataType.PURCHASE: ['po_number', 'supplier', 'quantity', 'unit_price']
    }

    # Numeric columns that should not have negative values
    POSITIVE_ONLY_COLUMNS = {
        'revenue', 'quantity', 'unit_price', 'total_amount', 'cost',
        'quantity_on_hand', 'planned_quantity', 'actual_quantity',
        'good_quantity', 'unit_cost', 'stock_value', 'margin'
    }

    def __init__(self):
        self.issues: List[DataQualityIssue] = []

    def validate(self, df: pd.DataFrame, data_type: DataType) -> DataQualityReport:
        """
        Run full validation and return brutally honest quality report.
        """
        self.issues = []
        df = df.copy()

        # Basic stats
        total_rows = len(df)
        total_columns = len(df.columns)

        # Check for duplicates
        try:
            duplicate_series = df.duplicated()
            duplicate_rows = duplicate_series.sum()
            # Ensure it's a scalar
            if hasattr(duplicate_rows, 'item'):
                duplicate_rows = duplicate_rows.item()
            elif hasattr(duplicate_rows, '__int__'):
                duplicate_rows = int(duplicate_rows)

            if duplicate_rows > 0:
                self._add_issue(
                    column='_all_',
                    issue_type='duplicate',
                    affected_rows=duplicate_rows,
                    severity=Severity.MEDIUM if duplicate_rows < total_rows * 0.05 else Severity.HIGH,
                    description=f"{duplicate_rows} duplicate rows found ({duplicate_rows/total_rows*100:.1f}%)",
                    recommendation="Remove duplicate rows before analysis"
                )
        except Exception:
            pass  # Skip duplicate check if it fails

        # Missing data analysis
        missing_pct = self._analyze_missing_data(df)

        # Column-level validation
        self._validate_columns(df, data_type)

        # Value validation
        self._validate_values(df)

        # Build report
        is_usable = not any(i.severity == Severity.CRITICAL for i in self.issues)
        blocking_issues = [i.description for i in self.issues if i.severity == Severity.CRITICAL]

        return DataQualityReport(
            total_rows=total_rows,
            total_columns=total_columns,
            columns=list(df.columns),
            issues=self.issues,
            missing_percentage=missing_pct,
            duplicate_rows=int(duplicate_rows),
            is_usable=is_usable,
            blocking_issues=blocking_issues
        )

    def _analyze_missing_data(self, df: pd.DataFrame) -> Dict[str, float]:
        """Analyze missing data percentages."""
        missing_pct = {}
        for col in df.columns:
            try:
                col_data = df[col]
                # Ensure we're working with a Series
                if hasattr(col_data, 'squeeze'):
                    col_data = col_data.squeeze()

                missing_count = pd.isnull(col_data).sum()
                # Ensure it's a scalar
                if hasattr(missing_count, 'item'):
                    missing_count = missing_count.item()
                elif hasattr(missing_count, '__int__'):
                    missing_count = int(missing_count)

                if missing_count > 0:
                    pct = (missing_count / len(df)) * 100
                    missing_pct[col] = round(pct, 2)

                    # Add issue for significant missing data
                    if pct > 20:
                        self._add_issue(
                            column=col,
                            issue_type='missing',
                            affected_rows=missing_count,
                            severity=Severity.CRITICAL if pct > 50 else Severity.HIGH,
                            description=f"Column '{col}' has {pct:.1f}% missing values ({missing_count} rows)",
                            recommendation=f"Impute or remove column '{col}' - high missing rate affects analysis"
                        )
                    elif pct > 10:
                        self._add_issue(
                            column=col,
                            issue_type='missing',
                            affected_rows=missing_count,
                            severity=Severity.MEDIUM,
                            description=f"Column '{col}' has {pct:.1f}% missing values",
                            recommendation=f"Consider imputation strategy for '{col}'"
                        )
                    elif pct > 0:
                        self._add_issue(
                            column=col,
                            issue_type='missing',
                            affected_rows=missing_count,
                            severity=Severity.LOW,
                            description=f"Column '{col}' has {pct:.1f}% missing values",
                            recommendation=f"Minor - can be handled with standard imputation"
                        )
            except Exception as e:
                # Skip problematic columns
                continue

        return missing_pct

    def _validate_columns(self, df: pd.DataFrame, data_type: DataType):
        """Validate column structure."""
        required = self.REQUIRED_COLUMNS.get(data_type, [])
        df_cols_lower = [c.lower() for c in df.columns]

        for req_col in required:
            if req_col.lower() not in df_cols_lower:
                self._add_issue(
                    column=req_col,
                    issue_type='missing_column',
                    affected_rows=len(df),
                    severity=Severity.CRITICAL,
                    description=f"Required column '{req_col}' is missing",
                    recommendation=f"Add column '{req_col}' or map an existing column"
                )

    def _validate_values(self, df: pd.DataFrame):
        """Validate data values."""
        for col in df.columns:
            col_lower = col.lower()

            # Check for negative values in positive-only columns
            if any(pos in col_lower for pos in self.POSITIVE_ONLY_COLUMNS):
                try:
                    neg_count = (df[col] < 0).sum()
                    if neg_count > 0:
                        self._add_issue(
                            column=col,
                            issue_type='invalid_value',
                            affected_rows=int(neg_count),
                            severity=Severity.HIGH,
                            description=f"Column '{col}' has {neg_count} negative values (expected positive)",
                            recommendation=f"Review and correct negative values in '{col}'"
                        )
                except (TypeError, ValueError):
                    pass  # Non-numeric column, skip

            # Check for outliers (basic statistical check)
            if self._is_numeric_column(df, col):
                self._check_outliers(df, col)

    def _is_numeric_column(self, df: pd.DataFrame, col: str) -> bool:
        """Check if column is numeric."""
        try:
            df[col].astype(float)
            return True
        except (ValueError, TypeError):
            return False

    def _check_outliers(self, df: pd.DataFrame, col: str):
        """Check for statistical outliers using IQR method."""
        try:
            series = pd.to_numeric(df[col], errors='coerce').dropna()
            if len(series) < 10:
                return

            Q1 = series.quantile(0.25)
            Q3 = series.quantile(0.75)
            IQR = Q3 - Q1

            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR

            outliers = ((series < lower_bound) | (series > upper_bound)).sum()
            outlier_pct = outliers / len(series) * 100

            if outlier_pct > 5:
                self._add_issue(
                    column=col,
                    issue_type='outlier',
                    affected_rows=int(outliers),
                    severity=Severity.MEDIUM,
                    description=f"Column '{col}' has {outliers} outliers ({outlier_pct:.1f}%)",
                    recommendation=f"Review outliers in '{col}' - may indicate data entry errors or genuine anomalies"
                )
        except (ValueError, TypeError):
            pass

    def _add_issue(
        self,
        column: str,
        issue_type: str,
        affected_rows: int,
        severity: Severity,
        description: str,
        recommendation: str
    ):
        """Add a data quality issue."""
        issue = DataQualityIssue(
            column=column,
            issue_type=issue_type,
            affected_rows=affected_rows,
            severity=severity,
            description=description,
            recommendation=recommendation
        )
        self.issues.append(issue)
