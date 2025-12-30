"""
Schema detection - auto-detects data type and maps columns intelligently.
"""
import pandas as pd
import re
from typing import Dict, List, Tuple, Optional, Any
from collections import Counter

from models.base import DataType, SchemaMatch, ColumnMapping


class SchemaDetector:
    """
    Intelligently detects data type and maps columns to expected fields.
    Supports flexible column naming conventions.
    """

    # Column name mappings (common variations -> expected field)
    COLUMN_MAPPINGS = {
        # Financial
        'revenue': ['revenue', 'sales', 'total_revenue', 'gross_sales', 'turnover'],
        'cost_of_goods_sold': ['cogs', 'cost_of_goods', 'cost_of_sales', 'direct_costs'],
        'gross_profit': ['gross_profit', 'gross_margin', 'gross_earnings'],
        'operating_expenses': ['operating_expenses', 'opex', 'operating_costs', 'operating_overhead'],
        'operating_income': ['operating_income', 'operating_profit', 'ebit'],
        'net_income': ['net_income', 'net_profit', 'net_earnings', 'bottom_line', 'profit_after_tax'],
        'period': ['period', 'date', 'month', 'year', 'quarter', 'fiscal_period', 'posting_date'],
        'budget': ['budget', 'budgeted', 'planned', 'forecast'],

        # Manufacturing
        'product_id': ['product_id', 'product_code', 'item_code', 'material_code', 'sku'],
        'product_name': ['product_name', 'item_name', 'description', 'material_description'],
        'planned_quantity': ['planned_quantity', 'planned_output', 'target_quantity', 'planned'],
        'actual_quantity': ['actual_quantity', 'actual_output', 'produced', 'actual'],
        'good_quantity': ['good_quantity', 'good_units', 'conforming', 'first_pass'],
        'rejected_quantity': ['rejected_quantity', 'rejections', 'scrap', 'non_conforming'],
        'wastage_quantity': ['wastage', 'waste', '损耗'],
        'production_line': ['production_line', 'line', 'work_center', 'machine', 'equipment'],
        'efficiency': ['efficiency', 'efficiency_rate', 'oee', 'utilization'],

        # Inventory
        'sku': ['sku', 'product_code', 'item_code', 'material_code', 'product_id'],
        'quantity': ['quantity', 'qty', 'on_hand', 'stock', 'inventory_qty'],
        'unit_cost': ['unit_cost', 'cost_per_unit', 'standard_cost', 'avg_cost'],
        'unit_price': ['unit_price', 'selling_price', 'price', 'retail_price'],
        'receipt_date': ['receipt_date', 'received_date', 'doc_date', 'posting_date'],
        'last_movement_date': ['last_movement', 'last_issue', 'last_sale', 'last_activity'],
        'warehouse': ['warehouse', 'warehouse_id', 'location', 'site', 'plant'],

        # Sales
        'order_id': ['order_id', 'order_number', 'order_no', 'sales_order', 'so_number'],
        'customer_id': ['customer_id', 'customer_code', 'client_id', 'account'],
        'customer_name': ['customer_name', 'customer', 'client', 'account_name', 'company'],
        'order_date': ['order_date', 'order_dt', 'sales_date', 'transaction_date'],
        'discount': ['discount', 'discount_amount', 'disc', 'allowance'],

        # Purchase
        'po_number': ['po_number', 'purchase_order', 'po_no', 'purchase_order_no'],
        'supplier_id': ['supplier_id', 'vendor_id', 'supplier_code', 'vendor_code'],
        'supplier_name': ['supplier_name', 'vendor', 'supplier', 'vendor_name'],
        'quantity_ordered': ['quantity_ordered', 'ordered_qty', 'po_quantity'],
        'quantity_received': ['quantity_received', 'received_qty', 'receipt_qty'],
        'expected_delivery_date': ['expected_delivery', 'delivery_date', 'promised_date'],
        'actual_delivery_date': ['actual_delivery', 'delivery_received', 'received_date'],
    }

    # Data type detection keywords
    TYPE_KEYWORDS = {
        DataType.FINANCIAL: [
            'revenue', 'profit', 'margin', 'expense', 'income', 'cogs', 'budget', 'forecast',
            'gross', 'net', 'operating', 'ebitda', 'ebit'
        ],
        DataType.MANUFACTURING: [
            'production', 'planned', 'actual', 'good', 'rejected', 'wastage', 'yield',
            'efficiency', 'output', 'throughput', 'downtime', 'oee'
        ],
        DataType.INVENTORY: [
            'sku', 'stock', 'inventory', 'quantity', 'on_hand', 'warehouse', 'receipt',
            'movement', 'aging', 'coverage', 'reorder', 'safety'
        ],
        DataType.SALES: [
            'order', 'customer', 'sales', 'discount', 'tax', 'channel', 'region',
            'segment', 'sales_rep', 'rep'
        ],
        DataType.PURCHASE: [
            'po', 'purchase_order', 'supplier', 'vendor', 'lead_time', 'delivery',
            'receipt', 'supplier'
        ]
    }

    def detect_data_type(self, df: pd.DataFrame) -> DataType:
        """
        Auto-detect the type of data based on column names and content.
        """
        scores = {dt: 0 for dt in DataType}

        # Normalize column names
        cols_lower = [c.lower().replace(' ', '_').replace('-', '_') for c in df.columns]

        # Score each data type
        for data_type, keywords in self.TYPE_KEYWORDS.items():
            for col in cols_lower:
                for keyword in keywords:
                    if keyword in col:
                        scores[data_type] += 1

        # Also check content patterns
        for col in df.columns:
            col_values = str(df[col].dropna().head(10).tolist())
            for data_type, keywords in self.TYPE_KEYWORDS.items():
                for keyword in keywords:
                    if keyword in col_values.lower():
                        scores[data_type] += 0.5

        # Return highest scoring type
        max_score = max(scores.values())
        if max_score == 0:
            return DataType.UNKNOWN

        for dt, score in scores.items():
            if score == max_score:
                return dt

        return DataType.UNKNOWN

    def detect_with_confidence(self, df: pd.DataFrame) -> Tuple[DataType, float]:
        """
        Detect data type with confidence score.
        """
        scores = {dt: 0 for dt in DataType if dt != DataType.UNKNOWN}

        cols_lower = [c.lower().replace(' ', '_').replace('-', '_') for c in df.columns]
        col_count = len(cols_lower)

        if col_count == 0:
            return DataType.UNKNOWN, 0.0

        for data_type, keywords in self.TYPE_KEYWORDS.items():
            for col in cols_lower:
                for keyword in keywords:
                    if keyword in col:
                        scores[data_type] += 1

        max_score = max(scores.values()) if scores else 0
        confidence = min(max_score / max(3, col_count * 0.5), 1.0)

        if max_score == 0:
            return DataType.UNKNOWN, 0.0

        for dt, score in scores.items():
            if score == max_score:
                return dt, round(confidence, 2)

        return DataType.UNKNOWN, 0.0

    def create_schema_match(self, df: pd.DataFrame, data_type: DataType) -> SchemaMatch:
        """
        Create schema match with column mappings and missing columns.
        """
        if data_type == DataType.UNKNOWN:
            return SchemaMatch(
                data_type=DataType.UNKNOWN,
                confidence=0.0,
                matched_columns=[],
                missing_columns=list(df.columns),
                column_mappings=[],
                suggested_fields={}
            )

        # Detect column mappings
        column_mappings = []
        matched_cols = []
        suggested_fields = {}

        for col in df.columns:
            mapping = self._map_column(col, data_type)
            if mapping:
                column_mappings.append(mapping)
                matched_cols.append(col)
                suggested_fields[col] = mapping.expected_field

        # Find missing required columns
        required_fields = self._get_required_fields(data_type)
        matched_fields = [m.expected_field for m in column_mappings]
        missing_fields = [f for f in required_fields if f not in matched_fields]

        # Calculate confidence
        matched_count = len(matched_fields)
        required_count = len(required_fields)
        required_matched = len([f for f in required_fields if f in matched_fields])

        # Confidence based on required fields match
        if required_count > 0:
            required_confidence = required_matched / required_count
        else:
            required_confidence = matched_count / 10 if matched_count > 0 else 0

        total_confidence = min(0.5 + (required_confidence * 0.5), 1.0)

        return SchemaMatch(
            data_type=data_type,
            confidence=round(total_confidence, 2),
            matched_columns=matched_cols,
            missing_columns=missing_fields,
            column_mappings=column_mappings,
            suggested_fields=suggested_fields
        )

    def _map_column(self, col_name: str, data_type: DataType) -> Optional[ColumnMapping]:
        """
        Map a column to its expected field.
        """
        col_lower = col_name.lower().replace(' ', '_').replace('-', '_')

        for expected_field, variations in self.COLUMN_MAPPINGS.items():
            for variation in variations:
                # Check for exact match first
                if col_lower == variation:
                    return ColumnMapping(
                        column_name=col_name,
                        expected_field=expected_field,
                        confidence=1.0
                    )

                # Check for word boundary match (variation should not be embedded in a longer word)
                # Use regex with word boundaries
                import re
                if re.search(r'\b' + re.escape(variation) + r'\b', col_lower):
                    return ColumnMapping(
                        column_name=col_name,
                        expected_field=expected_field,
                        confidence=0.9
                    )

                # For short patterns (<= 4 chars), require exact match or prefix
                if len(variation) <= 4 and (col_lower.startswith(variation) or col_lower.endswith(variation)):
                    return ColumnMapping(
                        column_name=col_name,
                        expected_field=expected_field,
                        confidence=0.8
                    )

        return None

    def _get_required_fields(self, data_type: DataType) -> List[str]:
        """
        Get required fields for each data type.
        Uses flexible field matching - if ANY variation exists, it counts.
        """
        required_map = {
            DataType.FINANCIAL: ['revenue', 'period'],
            DataType.MANUFACTURING: ['product_id', 'planned_quantity', 'actual_quantity'],
            DataType.INVENTORY: ['sku', 'quantity', 'unit_cost'],
            DataType.SALES: ['order_id', 'product_id', 'quantity', 'total_amount'],
            DataType.PURCHASE: ['po_number', 'supplier_id', 'quantity_ordered', 'unit_price']
        }
        return required_map.get(data_type, [])

    def normalize_columns(self, df: pd.DataFrame, data_type: DataType) -> pd.DataFrame:
        """
        Normalize column names to standard field names.
        """
        df = df.copy()
        rename_map = {}
        used_targets = set()

        for col in df.columns:
            mapping = self._map_column(col, data_type)
            if mapping:
                target = mapping.expected_field
                # Skip if this target is already used AND column name is different
                if target in used_targets and col.lower() != target:
                    continue
                # Also skip if we're trying to rename to the same name
                if col.lower() == target:
                    continue
                rename_map[col] = target
                used_targets.add(target)

        if rename_map:
            # For each rename, we need to handle duplicates specially
            for old_col, new_col in rename_map.items():
                if new_col in df.columns:
                    # New column already exists, drop the old one
                    df = df.drop(columns=[old_col])
                else:
                    # Safe to rename
                    df = df.rename(columns={old_col: new_col})

        return df

    def suggest_column_types(self, df: pd.DataFrame) -> Dict[str, str]:
        """
        Suggest data types for each column.
        """
        type_suggestions = {}

        for col in df.columns:
            col_lower = col.lower()

            # Date patterns
            if any(p in col_lower for p in ['date', 'time', 'period']):
                type_suggestions[col] = 'datetime64'
                continue

            # Numeric candidates
            if any(p in col_lower for p in ['amount', 'revenue', 'cost', 'price', 'quantity',
                                             'qty', 'count', 'rate', 'pct', 'margin', 'profit']):
                try:
                    # Check if column contains mostly numeric values
                    numeric_count = pd.to_numeric(df[col], errors='coerce').notna().sum()
                    if numeric_count / len(df) > 0.5:
                        type_suggestions[col] = 'float64'
                        continue
                except:
                    pass

            # ID patterns (string)
            if any(p in col_lower for p in ['id', 'code', 'number', 'no']):
                type_suggestions[col] = 'str'
                continue

            # Default
            type_suggestions[col] = str(df[col].dtype)

        return type_suggestions
