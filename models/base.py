"""
Base Pydantic models and enums for the ERP Intelligence Agent.
"""
from enum import Enum
from typing import Optional, List, Dict, Any
from datetime import datetime, date
from decimal import Decimal
from pydantic import BaseModel, Field, field_validator


class DataType(str, Enum):
    """Types of ERP data that can be analyzed."""
    FINANCIAL = "financial"
    MANUFACTURING = "manufacturing"
    INVENTORY = "inventory"
    SALES = "sales"
    PURCHASE = "purchase"
    UNKNOWN = "unknown"


class Severity(str, Enum):
    """Severity levels for insights and risks."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class Priority(str, Enum):
    """Priority levels for recommendations."""
    IMMEDIATE = "immediate"  # 0-30 days
    SHORT_TERM = "short_term"  # 1-3 months
    MEDIUM_TERM = "medium_term"  # 3-6 months


class TimeHorizon(str, Enum):
    """Time horizon for recommendations."""
    IMMEDIATE = "0-30 days"
    SHORT_TERM = "1-3 months"
    MEDIUM_TERM = "3-6 months"


class InsightCategory(str, Enum):
    """Categories for insights."""
    FINANCIAL = "Financial Insights"
    MANUFACTURING = "Manufacturing & Operations Insights"
    INVENTORY = "Inventory & Stock Insights"
    SALES = "Sales Insights"
    PURCHASE = "Purchase & Supply Chain Insights"
    RISK = "Critical Risks"


class DataQualityIssue(BaseModel):
    """
    Single data quality issue - problems are NOT hidden.
    """
    column: str
    issue_type: str  # missing, invalid, outlier, inconsistent, duplicate
    affected_rows: int
    severity: Severity
    description: str
    recommendation: str


class DataQualityReport(BaseModel):
    """
    Complete data quality report - brutally honest about data issues.
    """
    total_rows: int
    total_columns: int
    columns: List[str]
    issues: List[DataQualityIssue] = Field(default_factory=list)
    missing_percentage: Dict[str, float] = Field(default_factory=dict)
    duplicate_rows: int = 0
    is_usable: bool = True
    blocking_issues: List[str] = Field(default_factory=list)

    @property
    def issue_count(self) -> int:
        return len(self.issues)

    @property
    def has_critical_issues(self) -> bool:
        return any(i.severity == Severity.CRITICAL for i in self.issues)

    @property
    def has_high_issues(self) -> bool:
        return any(i.severity == Severity.HIGH for i in self.issues)


class ColumnMapping(BaseModel):
    """
    Maps user column names to expected field names for auto-detection.
    """
    column_name: str
    expected_field: str
    confidence: float = Field(ge=0, le=1)


class SchemaMatch(BaseModel):
    """
    Result of schema matching for data type detection.
    """
    data_type: DataType
    confidence: float = Field(ge=0, le=1)
    matched_columns: List[str]
    missing_columns: List[str]
    column_mappings: List[ColumnMapping]
    suggested_fields: Dict[str, str]
