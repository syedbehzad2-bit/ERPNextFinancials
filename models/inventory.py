"""
Inventory data models for Stock, Aging, and Movements.
"""
from typing import Optional
from datetime import date, datetime
from decimal import Decimal
from pydantic import BaseModel, Field


class StockItem(BaseModel):
    """
    Inventory stock item snapshot.
    """
    sku: str
    product_name: str
    category: Optional[str] = None
    subcategory: Optional[str] = None
    quantity_on_hand: int
    unit_cost: Decimal
    unit_price: Optional[Decimal] = None
    warehouse_location: Optional[str] = None
    receipt_date: datetime
    last_movement_date: Optional[datetime] = None

    @property
    def stock_value(self) -> Decimal:
        return self.quantity_on_hand * self.unit_cost

    @property
    def retail_value(self) -> Optional[Decimal]:
        if self.unit_price:
            return self.quantity_on_hand * self.unit_price
        return None

    @property
    def age_days(self) -> int:
        if isinstance(self.receipt_date, datetime):
            return (datetime.now() - self.receipt_date).days
        elif isinstance(self.receipt_date, date):
            return (datetime.now().date() - self.receipt_date).days
        return 0

    @property
    def days_since_movement(self) -> Optional[int]:
        if self.last_movement_date:
            if isinstance(self.last_movement_date, datetime):
                return (datetime.now() - self.last_movement_date).days
            elif isinstance(self.last_movement_date, date):
                return (datetime.now().date() - self.last_movement_date).days
        return None

    @property
    def is_dead_stock(self) -> bool:
        """Dead stock: no movement for 180+ days."""
        days = self.days_since_movement
        return days is not None and days >= 180

    @property
    def is_stagnant(self) -> bool:
        """Stagnant: no movement for 90+ days."""
        days = self.days_since_movement
        return days is not None and days >= 90


class InventoryMovement(BaseModel):
    """
    Stock movement record (IN, OUT, ADJUSTMENT).
    """
    date: datetime
    sku: str
    movement_type: str  # IN, OUT, ADJUSTMENT, TRANSFER
    quantity: int
    reference: Optional[str] = None  # PO number, SO number, etc.
    warehouse: Optional[str] = None
    notes: Optional[str] = None

    @property
    def is_inbound(self) -> bool:
        return self.movement_type.upper() in ["IN", "RECEIPT", "RETURN"]

    @property
    def is_outbound(self) -> bool:
        return self.movement_type.upper() in ["OUT", "SHIPMENT", "SALE"]


class StockCoverage(BaseModel):
    """
    Stock coverage analysis.
    """
    sku: str
    product_name: Optional[str] = None
    quantity_on_hand: int
    average_daily_usage: Decimal
    days_of_stock: Decimal
    reorder_point: int
    reorder_quantity: Optional[int] = None
    safety_stock: Optional[int] = None

    @property
    def is_overstock(self) -> bool:
        """Overstock: more than 90 days of coverage."""
        return self.days_of_stock > 90

    @property
    def is_understock(self) -> bool:
        """Understock: below reorder point."""
        return self.quantity_on_hand <= self.reorder_point

    @property
    def stock_out_risk(self) -> str:
        """Risk of stock out."""
        days_to_stockout = self.days_of_stock
        if days_to_stockout <= 7:
            return "CRITICAL"
        elif days_to_stockout <= 14:
            return "HIGH"
        elif days_to_stockout <= 30:
            return "MEDIUM"
        return "LOW"


class AgingBucket(BaseModel):
    """
    Stock aging bucket for analysis.
    """
    bucket_name: str  # 0-30, 31-60, 61-90, 90+ days
    min_days: int
    max_days: int
    sku_count: int
    total_quantity: int
    total_value: Decimal
    percentage_of_total: Decimal
