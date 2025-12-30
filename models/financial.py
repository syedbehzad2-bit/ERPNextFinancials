"""
Financial data models for P&L, Revenue, and Expenses.
"""
from typing import Optional
from datetime import date, datetime
from decimal import Decimal
from pydantic import BaseModel, Field


class PLStatement(BaseModel):
    """
    Profit & Loss statement line item.
    """
    period: datetime
    revenue: Decimal = Field(..., description="Total revenue for period")
    cost_of_goods_sold: Optional[Decimal] = None
    gross_profit: Optional[Decimal] = None
    operating_expenses: Optional[Decimal] = None
    operating_income: Optional[Decimal] = None
    net_income: Optional[Decimal] = None
    other_income: Optional[Decimal] = None
    interest_expense: Optional[Decimal] = None
    taxes: Optional[Decimal] = None

    @property
    def gross_margin_pct(self) -> Optional[Decimal]:
        if self.revenue and self.revenue > 0 and self.gross_profit:
            return (self.gross_profit / self.revenue) * 100
        elif self.revenue and self.revenue > 0 and self.cost_of_goods_sold:
            return ((self.revenue - self.cost_of_goods_sold) / self.revenue) * 100
        return None

    @property
    def net_margin_pct(self) -> Optional[Decimal]:
        if self.revenue and self.revenue > 0 and self.net_income:
            return (self.net_income / self.revenue) * 100
        return None

    @property
    def operating_margin_pct(self) -> Optional[Decimal]:
        if self.revenue and self.revenue > 0 and self.operating_income:
            return (self.operating_income / self.revenue) * 100
        return None


class ExpenseItem(BaseModel):
    """
    Expense line item with categorization.
    """
    period: datetime
    category: str  # Material, Labor, Overhead, Other
    subcategory: Optional[str] = None
    amount: Decimal
    budgeted_amount: Optional[Decimal] = None
    department: Optional[str] = None
    cost_center: Optional[str] = None

    @property
    def variance(self) -> Optional[Decimal]:
        if self.budgeted_amount:
            return self.amount - self.budgeted_amount
        return None

    @property
    def variance_pct(self) -> Optional[Decimal]:
        if self.budgeted_amount and self.budgeted_amount != 0:
            return ((self.amount - self.budgeted_amount) / self.budgeted_amount) * 100
        return None

    @property
    def is_over_budget(self) -> bool:
        if self.budgeted_amount:
            return self.amount > self.budgeted_amount
        return False


class RevenueItem(BaseModel):
    """
    Revenue line item with source tracking.
    """
    period: datetime
    source: str  # Product line, Customer segment, Region, Channel
    amount: Decimal
    quantity: Optional[int] = None
    unit_price: Optional[Decimal] = None

    @property
    def avg_price_per_unit(self) -> Optional[Decimal]:
        if self.quantity and self.quantity > 0:
            return self.amount / self.quantity
        return None


class CostBreakdown(BaseModel):
    """
    Cost breakdown by component.
    """
    period: datetime
    product_id: Optional[str] = None
    product_name: Optional[str] = None
    material_cost: Decimal = Decimal(0)
    labor_cost: Decimal = Decimal(0)
    overhead_cost: Decimal = Decimal(0)
    other_cost: Decimal = Decimal(0)
    total_cost: Decimal

    @property
    def material_pct(self) -> Decimal:
        if self.total_cost and self.total_cost > 0:
            return (self.material_cost / self.total_cost) * 100
        return Decimal(0)

    @property
    def labor_pct(self) -> Decimal:
        if self.total_cost and self.total_cost > 0:
            return (self.labor_cost / self.total_cost) * 100
        return Decimal(0)

    @property
    def overhead_pct(self) -> Decimal:
        if self.total_cost and self.total_cost > 0:
            return (self.overhead_cost / self.total_cost) * 100
        return Decimal(0)

    @property
    def cost_per_unit(self) -> Optional[Decimal]:
        return None  # Override in subclass with quantity
