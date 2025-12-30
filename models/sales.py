"""
Sales data models for Transactions, Products, and Customers.
"""
from typing import Optional
from datetime import date, datetime
from decimal import Decimal
from pydantic import BaseModel, Field


class SalesTransaction(BaseModel):
    """
    Sales transaction record.
    """
    date: datetime
    order_id: str
    customer_id: str
    customer_name: str
    product_id: str
    product_name: str
    quantity: int
    unit_price: Decimal
    total_amount: Decimal
    cost_of_goods: Optional[Decimal] = None
    discount_amount: Decimal = Decimal(0)
    tax_amount: Decimal = Decimal(0)
    sales_rep: Optional[str] = None
    channel: Optional[str] = None

    @property
    def gross_margin(self) -> Optional[Decimal]:
        if self.cost_of_goods:
            return self.total_amount - self.cost_of_goods
        return None

    @property
    def gross_margin_pct(self) -> Optional[Decimal]:
        if self.cost_of_goods and self.total_amount > 0:
            return ((self.total_amount - self.cost_of_goods) / self.total_amount) * 100
        return None

    @property
    def net_amount(self) -> Decimal:
        """Amount after discount."""
        return self.total_amount - self.discount_amount


class CustomerMetrics(BaseModel):
    """
    Customer-level aggregated metrics.
    """
    customer_id: str
    customer_name: str
    total_revenue: Decimal
    order_count: int
    average_order_value: Decimal
    first_order_date: datetime
    last_order_date: datetime
    gross_margin: Optional[Decimal] = None
    margin_pct: Optional[Decimal] = None
    product_categories: Optional[list] = None

    @property
    def revenue_share_pct(self) -> Decimal:
        """Share of total revenue - used for concentration analysis."""
        return Decimal(0)  # Set externally after total is known

    @property
    def customer_since_years(self) -> float:
        """Years as a customer."""
        delta = self.last_order_date - self.first_order_date
        return delta.days / 365.25

    @property
    def is_active(self) -> bool:
        """Active if ordered in last 90 days."""
        if isinstance(self.last_order_date, datetime):
            return (datetime.now() - self.last_order_date).days <= 90
        return False


class ProductPerformance(BaseModel):
    """
    Product performance metrics.
    """
    product_id: str
    product_name: str
    category: Optional[str] = None
    total_quantity_sold: int
    total_revenue: Decimal
    total_cost: Decimal = Decimal(0)
    gross_margin: Optional[Decimal] = None
    margin_pct: Optional[Decimal] = None
    order_count: int = 0
    average_order_quantity: Decimal = Decimal(0)

    @property
    def revenue_share_pct(self) -> Decimal:
        return Decimal(0)  # Set externally after total is known

    @property
    def is_profitable(self) -> bool:
        return self.margin_pct is not None and self.margin_pct > 0


class SalesSummary(BaseModel):
    """
    Summary metrics for sales analysis.
    """
    total_revenue: Decimal
    total_orders: int
    total_customers: int
    total_products: int
    average_order_value: Decimal
    average_margin_pct: Decimal
    period_start: datetime
    period_end: datetime

    @property
    def revenue_per_customer(self) -> Decimal:
        if self.total_customers > 0:
            return self.total_revenue / self.total_customers
        return Decimal(0)

    @property
    def revenue_per_product(self) -> Decimal:
        if self.total_products > 0:
            return self.total_revenue / self.total_products
        return Decimal(0)

    @property
    def orders_per_customer(self) -> Decimal:
        if self.total_customers > 0:
            return Decimal(self.total_orders / self.total_customers)
        return Decimal(0)
