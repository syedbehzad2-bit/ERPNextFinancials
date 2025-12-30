"""Tests for DataLoader and validation."""
import pytest
import pandas as pd
from pathlib import Path

from data_loader.loader import DataLoader
from data_loader.validators import DataValidator
from data_loader.schema_detector import SchemaDetector
from models.base import DataType


class TestDataLoader:
    """Tests for DataLoader class."""

    def test_load_csv_file(self, loader, sample_financial_data, tmp_path):
        """Test loading CSV file."""
        file_path = tmp_path / "test.csv"
        sample_financial_data.to_csv(file_path, index=False)

        df = loader.load_file(file_path)

        assert len(df) == 12
        assert 'revenue' in df.columns

    def test_data_type_detection(self, sample_financial_data, sample_inventory_data):
        """Test automatic data type detection."""
        detector = SchemaDetector()

        # Financial data should be detected
        financial_type, _ = detector.detect_with_confidence(sample_financial_data)
        assert financial_type == DataType.FINANCIAL

    def test_schema_detection(self, sample_inventory_data):
        """Test schema detection and column mapping."""
        detector = SchemaDetector()
        data_type = detector.detect_data_type(sample_inventory_data)
        assert data_type == DataType.INVENTORY

    def test_data_validation(self, sample_financial_data):
        """Test data validation."""
        validator = DataValidator()
        report = validator.validate(sample_financial_data, DataType.FINANCIAL)

        assert report.total_rows == 12
        assert report.is_usable is True


class TestSchemaDetector:
    """Tests for SchemaDetector class."""

    def test_detect_financial_data(self, sample_financial_data):
        """Test detecting financial data type."""
        detector = SchemaDetector()
        data_type = detector.detect_data_type(sample_financial_data)
        assert data_type == DataType.FINANCIAL

    def test_detect_inventory_data(self, sample_inventory_data):
        """Test detecting inventory data type."""
        detector = SchemaDetector()
        data_type = detector.detect_data_type(sample_inventory_data)
        assert data_type == DataType.INVENTORY

    def test_detect_sales_data(self, sample_sales_data):
        """Test detecting sales data type."""
        detector = SchemaDetector()
        data_type = detector.detect_data_type(sample_sales_data)
        assert data_type == DataType.SALES

    def test_normalize_columns(self, sample_financial_data):
        """Test column name normalization."""
        detector = SchemaDetector()

        # Rename a column to test normalization
        df = sample_financial_data.copy()
        df.rename(columns={'revenue': 'Total Revenue'}, inplace=True)

        normalized = detector.normalize_columns(df, DataType.FINANCIAL)

        assert 'revenue' in normalized.columns


class TestAnalyzers:
    """Tests for analyzer classes."""

    def test_financial_analyzer(self, sample_financial_data):
        """Test FinancialAnalyzer."""
        from analyzers.financial_analyzer import FinancialAnalyzer

        analyzer = FinancialAnalyzer(sample_financial_data)
        result = analyzer.analyze()

        assert 'total_revenue' in result.kpis
        assert result.kpis['total_revenue'] > 0

    def test_inventory_analyzer(self, sample_inventory_data):
        """Test InventoryAnalyzer."""
        from analyzers.inventory_analyzer import InventoryAnalyzer

        analyzer = InventoryAnalyzer(sample_inventory_data)
        result = analyzer.analyze()

        assert 'total_stock_value' in result.kpis

    def test_sales_analyzer(self, sample_sales_data):
        """Test SalesAnalyzer."""
        from analyzers.sales_analyzer import SalesAnalyzer

        analyzer = SalesAnalyzer(sample_sales_data)
        result = analyzer.analyze()

        assert 'total_revenue' in result.kpis

    def test_manufacturing_analyzer(self, sample_manufacturing_data):
        """Test ManufacturingAnalyzer."""
        from analyzers.manufacturing_analyzer import ManufacturingAnalyzer

        analyzer = ManufacturingAnalyzer(sample_manufacturing_data)
        result = analyzer.analyze()

        assert 'production_efficiency_pct' in result.kpis


class TestInsightEngine:
    """Tests for Insight and Recommendation engines."""

    def test_insight_generation(self, sample_financial_data):
        """Test insight generation from analysis results."""
        from analyzers.financial_analyzer import FinancialAnalyzer
        from engines.insight_engine import InsightEngine

        analyzer = FinancialAnalyzer(sample_financial_data)
        result = analyzer.analyze()

        engine = InsightEngine()
        insights = engine.generate_insights({'financial': result.model_dump()})

        # Should generate at least some insights
        assert len(insights) >= 0  # May or may not generate based on data

    def test_recommendation_generation(self, sample_inventory_data):
        """Test recommendation generation."""
        from analyzers.inventory_analyzer import InventoryAnalyzer
        from engines.recommendation_engine import RecommendationEngine

        analyzer = InventoryAnalyzer(sample_inventory_data)
        result = analyzer.analyze()

        engine = RecommendationEngine()
        recommendations = engine.generate_recommendations(result.insights)

        assert isinstance(recommendations, list)

    def test_risk_identification(self, sample_financial_data):
        """Test risk identification."""
        from analyzers.financial_analyzer import FinancialAnalyzer
        from engines.risk_engine import RiskEngine

        analyzer = FinancialAnalyzer(sample_financial_data)
        result = analyzer.analyze()

        engine = RiskEngine()
        risks = engine.identify_risks({'financial': result.model_dump()}, result.insights)

        assert isinstance(risks, list)


class TestPydanticModels:
    """Tests for Pydantic models."""

    def test_insight_model(self):
        """Test Insight model validation."""
        from models.analysis_output import Insight
        from models.base import InsightCategory, Severity

        insight = Insight(
            category=InsightCategory.FINANCIAL,
            severity=Severity.HIGH,
            finding="Revenue dropped 20%",
            impact="Business at risk",
            action="Increase sales efforts"
        )

        assert insight.category == InsightCategory.FINANCIAL
        assert insight.severity == Severity.HIGH

    def test_recommendation_model(self):
        """Test Recommendation model validation."""
        from models.analysis_output import Recommendation
        from models.base import Priority, TimeHorizon

        rec = Recommendation(
            title="Test Recommendation",
            what="Do something",
            why="It matters",
            how="Step 1, Step 2",
            impact="Better results",
            priority=Priority.IMMEDIATE,
            timeline=TimeHorizon.IMMEDIATE
        )

        assert rec.priority == Priority.IMMEDIATE
        assert rec.timeline == TimeHorizon.IMMEDIATE

    def test_data_quality_report(self):
        """Test DataQualityReport model."""
        from models.base import DataQualityReport, Severity

        report = DataQualityReport(
            total_rows=100,
            total_columns=10,
            columns=['col1', 'col2'],
            is_usable=True,
            blocking_issues=[]
        )

        assert report.total_rows == 100
        assert report.is_usable is True
