"""
Purchase data models for POs and Supplier Performance.
"""
from typing import Optional
from datetime import date, datetime
from decimal import Decimal
from pydantic import BaseModel, Field


class PurchaseOrder(BaseModel):
    """
    Purchase order record.
    """
    po_number: str
    order_date: datetime
    expected_delivery_date: datetime
    actual_delivery_date: Optional[datetime] = None
    supplier_id: str
    supplier_name: str
    item_id: str
    item_name: str
    quantity_ordered: int
    quantity_received: Optional[int] = None
    unit_price: Decimal
    total_amount: Decimal
    status: str = "pending"  # pending, partial, received, cancelled

    @property
    def is_on_time(self) -> Optional[bool]:
        if self.actual_delivery_date:
            return self.actual_delivery_date <= self.expected_delivery_date
        return None

    @property
    def days_late(self) -> Optional[int]:
        if self.actual_delivery_date and self.actual_delivery_date > self.expected_delivery_date:
            return (self.actual_delivery_date - self.expected_delivery_date).days
        return None

    @property
    def days_early(self) -> Optional[int]:
        if self.actual_delivery_date and self.actual_delivery_date < self.expected_delivery_date:
            return (self.expected_delivery_date - self.actual_delivery_date).days
        return None

    @property
    def is_complete(self) -> bool:
        if self.quantity_received is None:
            return False
        return self.quantity_received >= self.quantity_ordered

    @property
    def fill_rate_pct(self) -> Optional[Decimal]:
        if self.quantity_received and self.quantity_received > 0:
            return Decimal(self.quantity_received / self.quantity_ordered * 100)
        return None


class SupplierMetrics(BaseModel):
    """
    Supplier performance metrics.
    """
    supplier_id: str
    supplier_name: str
    total_orders: int
    total_spend: Decimal
    on_time_delivery_rate: Decimal  # Percentage
    late_delivery_count: int = 0
    quality_rejection_rate: Decimal = Decimal(0)  # Percentage
    quality_rejection_count: int = 0
    average_lead_time_days: Decimal
    lead_time_variance: Decimal = Decimal(0)
    price_variance_pct: Decimal = Decimal(0)  # vs standard cost

    @property
    def spend_share_pct(self) -> Decimal:
        """Share of total purchase spend - used for concentration analysis."""
        return Decimal(0)  # Set externally

    @property
    def delivery_score(self) -> str:
        """Overall delivery performance score."""
        rate = self.on_time_delivery_rate
        if rate >= 95:
            return "EXCELLENT"
        elif rate >= 90:
            return "GOOD"
        elif rate >= 80:
            return "ACCEPTABLE"
        elif rate >= 70:
            return "POOR"
        return "CRITICAL"

    @property
    def quality_score(self) -> str:
        """Overall quality performance score."""
        rejection = self.quality_rejection_rate
        if rejection <= 1:
            return "EXCELLENT"
        elif rejection <= 3:
            return "GOOD"
        elif rejection <= 5:
            return "ACCEPTABLE"
        elif rejection <= 10:
            return "POOR"
        return "CRITICAL"

    @property
    def overall_score(self) -> Decimal:
        """Combined supplier score."""
        delivery_weight = Decimal("0.4")
        quality_weight = Decimal("0.4")
        lead_time_weight = Decimal("0.2")
        # Simplified scoring
        delivery_score = min(self.on_time_delivery_rate, Decimal("100"))
        quality_score = max(Decimal("100") - self.quality_rejection_rate * 10, Decimal("0"))
        lead_time_score = max(Decimal("100") - self.lead_time_variance, Decimal("0"))
        return delivery_score * delivery_weight + quality_score * quality_weight + lead_time_score * lead_time_weight


class PurchaseSummary(BaseModel):
    """
    Summary metrics for purchase analysis.
    """
    total_spend: Decimal
    total_orders: int
    total_suppliers: int
    total_items: int
    average_order_value: Decimal
    average_lead_time_days: Decimal
    on_time_delivery_rate: Decimal
    period_start: datetime
    period_end: datetime

    @property
    def spend_per_supplier(self) -> Decimal:
        if self.total_suppliers > 0:
            return self.total_spend / self.total_suppliers
        return Decimal(0)

    @property
    def late_delivery_rate(self) -> Decimal:
        return Decimal("100") - self.on_time_delivery_rate
