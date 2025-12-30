"""
Data cleaning utilities - with full audit trail of changes.
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, date
import re

from models.base import DataQualityIssue, Severity


class DataCleaner:
    """
    Cleans data with full audit trail of what was changed.
    """

    def __init__(self):
        self.changes_log: List[Dict[str, Any]] = []

    def clean(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, List[DataQualityIssue]]:
        """
        Apply cleaning transformations with audit trail.
        Returns cleaned DataFrame and list of issues found/resolved.
        """
        df = df.copy()
        issues: List[DataQualityIssue] = []

        # Remove completely empty rows
        original_rows = len(df)
        df = df.dropna(how='all')
        rows_removed = original_rows - len(df)
        if rows_removed > 0:
            self._log_change('remove_empty_rows', rows_removed, f"Removed {rows_removed} empty rows")

        # Remove duplicate rows
        original_rows = len(df)
        try:
            before_dup = len(df)
            df = df.drop_duplicates()
            after_dup = len(df)
            duplicates_removed = before_dup - after_dup
        except Exception:
            duplicates_removed = 0

        if duplicates_removed > 0:
            self._log_change('remove_duplicates', duplicates_removed, f"Removed {duplicates_removed} duplicate rows")
            issues.append(DataQualityIssue(
                column='_all_',
                issue_type='duplicate',
                affected_rows=duplicates_removed,
                severity=Severity.MEDIUM,
                description=f"Found and removed {duplicates_removed} duplicate rows",
                recommendation="Data cleaned - duplicates removed"
            ))

        # Clean column names
        df = self._clean_column_names(df)

        # Convert date columns
        df = self._convert_dates(df)

        # Clean numeric columns
        df = self._clean_numerics(df)

        # Handle missing values
        df = self._handle_missing_values(df)

        return df, issues

    def _log_change(self, change_type: str, affected_count: int, description: str):
        """Log a cleaning change."""
        self.changes_log.append({
            'type': change_type,
            'affected_rows': affected_count,
            'description': description,
            'timestamp': datetime.now()
        })

    def _clean_column_names(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Standardize column names: lowercase, replace spaces with underscores.
        """
        rename_map = {}
        for col in df.columns:
            new_name = col.lower().strip()
            new_name = re.sub(r'[\s\-/]+', '_', new_name)
            new_name = re.sub(r'[^\w_]', '', new_name)
            if new_name != col:
                rename_map[col] = new_name

        if rename_map:
            df = df.rename(columns=rename_map)
            self._log_change('rename_columns', len(rename_map), f"Renamed columns: {list(rename_map.values())}")

        return df

    def _convert_dates(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Convert date-like columns to datetime.
        """
        date_patterns = ['date', 'time', 'period']

        for col in df.columns:
            col_lower = col.lower()
            if any(p in col_lower for p in date_patterns):
                try:
                    original_nulls = df[col].isnull().sum()
                    df[col] = pd.to_datetime(df[col], errors='coerce')
                    new_nulls = df[col].isnull().sum()
                    if new_nulls > original_nulls:
                        self._log_change(
                            'date_conversion',
                            new_nulls - original_nulls,
                            f"Column '{col}': {new_nulls - original_nulls} rows became invalid dates"
                        )
                except Exception as e:
                    self._log_change('date_conversion_error', 0, f"Could not convert '{col}': {str(e)}")

        return df

    def _clean_numerics(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean numeric columns - remove currency symbols, commas, etc.
        """
        numeric_patterns = ['amount', 'revenue', 'cost', 'price', 'quantity', 'qty',
                           'total', 'margin', 'profit', 'rate', 'pct', 'percent']

        for col in df.columns:
            col_lower = col.lower()
            if any(p in col_lower for p in numeric_patterns):
                try:
                    # Check if column is object type but contains numbers
                    if df[col].dtype == 'object':
                        # Try to clean currency/percentage symbols
                        original_values = df[col].copy()

                        # Remove currency symbols and commas
                        cleaned = df[col].astype(str).str.replace(r'[$,\s]', '', regex=True)
                        cleaned = cleaned.str.replace(r'([0-9])\(([0-9])\)', r'-\1\2', regex=True)
                        cleaned = cleaned.str.replace(r'\(([0-9]+)\)', r'-\1', regex=True)
                        cleaned = cleaned.str.replace(r'%', '', regex=False)

                        # Try to convert
                        numeric = pd.to_numeric(cleaned, errors='coerce')
                        non_null_original = df[col].notna().sum()
                        non_null_numeric = numeric.notna().sum()

                        if non_null_numeric > non_null_original * 0.5:
                            df[col] = numeric
                            self._log_change(
                                'clean_numeric',
                                non_null_original,
                                f"Column '{col}': cleaned currency/formatting, {non_null_numeric} valid values"
                            )
                except Exception as e:
                    pass

        return df

    def _handle_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Handle missing values with appropriate strategies.
        """
        for col in df.columns:
            try:
                col_data = df[col]
                if hasattr(col_data, 'squeeze'):
                    col_data = col_data.squeeze()

                missing_count = pd.isnull(col_data).sum()
                # Ensure it's a scalar
                if hasattr(missing_count, 'item'):
                    missing_count = missing_count.item()
                elif hasattr(missing_count, '__int__'):
                    missing_count = int(missing_count)

                if missing_count == 0:
                    continue

                missing_pct = missing_count / len(df) * 100

                # For numeric columns with low missing rate, fill with median
                if pd.api.types.is_numeric_dtype(df[col]) and missing_pct < 10:
                    median_val = df[col].median()
                    if pd.notna(median_val):
                        df[col] = df[col].fillna(median_val)
                        self._log_change(
                            'fillna_median',
                            missing_count,
                            f"Column '{col}': filled {missing_count} missing values with median ({median_val})"
                        )

                # For categorical columns, fill with 'Unknown'
                elif df[col].dtype == 'object' or pd.api.types.is_categorical_dtype(df[col]):
                    df[col] = df[col].fillna('Unknown')
                    self._log_change(
                        'fillna_unknown',
                        missing_count,
                        f"Column '{col}': filled {missing_count} missing values with 'Unknown'"
                    )
            except Exception:
                continue  # Skip problematic columns

        return df

    def get_changes_summary(self) -> Dict[str, Any]:
        """
        Get summary of all cleaning changes made.
        """
        return {
            'changes_count': len(self.changes_log),
            'changes': self.changes_log
        }
