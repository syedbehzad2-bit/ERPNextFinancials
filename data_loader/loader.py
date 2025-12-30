"""
Main DataLoader - handles file loading with validation and auto-detection.
"""
import os
from typing import Optional, Dict, Any, Union
from pathlib import Path
from datetime import datetime

import pandas as pd

from models.base import DataType, DataQualityReport, SchemaMatch
from data_loader.validators import DataValidator
from data_loader.schema_detector import SchemaDetector
from data_loader.cleaners import DataCleaner
from config import settings


class DataLoader:
    """
    Handles CSV/Excel file uploads with validation, cleaning, and auto-detection.
    Brutally honest about data quality - no hiding problems.
    """

    SUPPORTED_EXTENSIONS = ('.csv', '.xlsx', '.xls')

    def __init__(self):
        self.validator = DataValidator()
        self.schema_detector = SchemaDetector()
        self.cleaner = DataCleaner()

        # State
        self._raw_data: Optional[pd.DataFrame] = None
        self._cleaned_data: Optional[pd.DataFrame] = None
        self._data_type: Optional[DataType] = None
        self._schema_match: Optional[SchemaMatch] = None
        self._quality_report: Optional[DataQualityReport] = None
        self._file_name: Optional[str] = None

    @property
    def file_name(self) -> Optional[str]:
        return self._file_name

    @property
    def raw_data(self) -> Optional[pd.DataFrame]:
        return self._raw_data

    @property
    def cleaned_data(self) -> Optional[pd.DataFrame]:
        return self._cleaned_data

    @property
    def data_type(self) -> Optional[DataType]:
        return self._data_type

    @property
    def schema_match(self) -> Optional[SchemaMatch]:
        return self._schema_match

    @property
    def quality_report(self) -> Optional[DataQualityReport]:
        return self._quality_report

    @property
    def is_usable(self) -> bool:
        """Return False if data has critical issues that prevent analysis."""
        return self._quality_report is not None and self._quality_report.is_usable

    @property
    def data_summary(self) -> Dict[str, Any]:
        """Get summary of loaded data."""
        if self._raw_data is None:
            return {}

        return {
            'file_name': self._file_name,
            'rows': len(self._raw_data),
            'columns': len(self._raw_data.columns),
            'data_type': self._data_type.value if self._data_type else 'unknown',
            'is_usable': self.is_usable,
            'quality_issues_count': self._quality_report.issue_count if self._quality_report else 0,
            'critical_issues': self._quality_report.has_critical_issues if self._quality_report else False
        }

    def load_file(
        self,
        file_path: Optional[Union[str, Path]] = None,
        file_obj=None,
        file_name: Optional[str] = None
    ) -> pd.DataFrame:
        """
        Load data from file path or Streamlit file object.

        Args:
            file_path: Path to CSV or Excel file
            file_obj: Streamlit uploaded file object
            file_name: Name of the file (required for file_obj)

        Returns:
            Cleaned DataFrame
        """
        # Reset state
        self._raw_data = None
        self._cleaned_data = None
        self._data_type = None
        self._schema_match = None
        self._quality_report = None

        # Load data
        if file_obj is not None:
            df = self._load_from_streamlit(file_obj, file_name)
        elif file_path is not None:
            df = self._load_from_path(file_path)
        else:
            raise ValueError("Either file_path or file_obj must be provided")

        if df is None or df.empty:
            raise ValueError("Could not load data from file")

        self._raw_data = df.copy()
        self._file_name = file_name or str(file_path)

        # Auto-detect data type
        self._data_type = self.schema_detector.detect_data_type(df)
        self._schema_match = self.schema_detector.create_schema_match(df, self._data_type)

        # Normalize column names
        normalized_df = self.schema_detector.normalize_columns(df, self._data_type)

        # Validate data
        self._quality_report = self.validator.validate(normalized_df, self._data_type)

        # Clean data
        cleaned_df, cleaning_issues = self.cleaner.clean(normalized_df)
        self._cleaned_data = cleaned_df

        # Update quality report with cleaning results
        if cleaning_issues:
            self._quality_report.issues.extend(cleaning_issues)

        return self._cleaned_data

    def _load_from_path(self, file_path: Union[str, Path]) -> Optional[pd.DataFrame]:
        """Load data from file path."""
        path = Path(file_path)

        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        if path.suffix.lower() not in self.SUPPORTED_EXTENSIONS:
            raise ValueError(f"Unsupported file type: {path.suffix}. Supported: {self.SUPPORTED_EXTENSIONS}")

        try:
            if path.suffix.lower() == '.csv':
                df = pd.read_csv(path, encoding='utf-8')
            else:
                df = pd.read_excel(path)

            return df
        except Exception as e:
            raise ValueError(f"Error reading file: {str(e)}")

    def _load_from_streamlit(self, file_obj, file_name: Optional[str]) -> Optional[pd.DataFrame]:
        """Load data from Streamlit uploaded file."""
        self._file_name = file_name or file_obj.name

        try:
            if file_obj.name.endswith('.csv'):
                df = pd.read_csv(file_obj)
            else:
                df = pd.read_excel(file_obj)

            return df
        except Exception as e:
            raise ValueError(f"Error reading uploaded file: {str(e)}")

    def get_column_mapping_report(self) -> Dict[str, Any]:
        """
        Get detailed report of column mappings.
        """
        if self._schema_match is None:
            return {'status': 'no_data'}

        return {
            'detected_type': self._data_type.value if self._data_type else 'unknown',
            'confidence': self._schema_match.confidence,
            'matched_columns': self._schema_match.matched_columns,
            'missing_columns': self._schema_match.missing_columns,
            'column_mappings': [
                {
                    'original': m.column_name,
                    'mapped_to': m.expected_field,
                    'confidence': m.confidence
                }
                for m in self._schema_match.column_mappings
            ]
        }

    def get_quality_summary(self) -> Dict[str, Any]:
        """
        Get quality summary for display.
        """
        if self._quality_report is None:
            return {'status': 'not_validated'}

        return {
            'is_usable': self._quality_report.is_usable,
            'total_rows': self._quality_report.total_rows,
            'total_columns': self._quality_report.total_columns,
            'issue_count': self._quality_report.issue_count,
            'critical_issues': [i.model_dump() for i in self._quality_report.issues if i.severity == 'critical'],
            'high_issues': [i.model_dump() for i in self._quality_report.issues if i.severity == 'high'],
            'missing_data': self._quality_report.missing_percentage,
            'duplicate_rows': self._quality_report.duplicate_rows
        }

    def preview_data(self, n_rows: int = 10) -> pd.DataFrame:
        """
        Get preview of cleaned data.
        """
        if self._cleaned_data is None:
            raise ValueError("No data loaded. Call load_file() first.")

        return self._cleaned_data.head(n_rows)

    def get_data_for_analysis(self) -> Dict[str, Any]:
        """
        Get all data needed for analysis.
        """
        return {
            'data_frame': self._cleaned_data,
            'data_type': self._data_type,
            'quality_report': self._quality_report,
            'column_mapping': self.get_column_mapping_report(),
            'schema_match': self._schema_match
        }
