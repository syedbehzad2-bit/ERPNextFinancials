"""
Manufacturing data models for Production, Wastage, and Costs.
"""
from typing import Optional
from datetime import date, datetime
from decimal import Decimal
from pydantic import BaseModel, Field


class ProductionRecord(BaseModel):
    """
    Production batch/run record.
    """
    date: datetime
    production_line: Optional[str] = None
    product_id: str
    product_name: str
    planned_quantity: int
    actual_quantity: int
    good_quantity: int
    rejected_quantity: int = 0
    wastage_quantity: int = 0

    @property
    def efficiency_pct(self) -> Decimal:
        if self.planned_quantity and self.planned_quantity > 0:
            return Decimal(self.actual_quantity / self.planned_quantity * 100)
        return Decimal(0)

    @property
    def yield_pct(self) -> Decimal:
        if self.actual_quantity and self.actual_quantity > 0:
            return Decimal(self.good_quantity / self.actual_quantity * 100)
        return Decimal(0)

    @property
    def rejection_pct(self) -> Decimal:
        if self.actual_quantity and self.actual_quantity > 0:
            return Decimal(self.rejected_quantity / self.actual_quantity * 100)
        return Decimal(0)

    @property
    def wastage_pct(self) -> Decimal:
        if self.actual_quantity and self.actual_quantity > 0:
            return Decimal(self.wastage_quantity / self.actual_quantity * 100)
        return Decimal(0)

    @property
    def shortfall_units(self) -> int:
        return max(0, self.planned_quantity - self.actual_quantity)


class ProductionCost(BaseModel):
    """
    Cost breakdown per production run.
    """
    date: datetime
    production_run_id: Optional[str] = None
    product_id: str
    product_name: Optional[str] = None
    quantity_produced: int
    material_cost: Decimal
    labor_cost: Decimal
    overhead_cost: Decimal
    other_cost: Decimal = Decimal(0)

    @property
    def total_cost(self) -> Decimal:
        return self.material_cost + self.labor_cost + self.overhead_cost + self.other_cost

    @property
    def cost_per_unit(self) -> Decimal:
        if self.quantity_produced and self.quantity_produced > 0:
            return self.total_cost / self.quantity_produced
        return Decimal(0)

    @property
    def material_pct(self) -> Decimal:
        total = self.total_cost
        if total and total > 0:
            return (self.material_cost / total) * 100
        return Decimal(0)

    @property
    def labor_pct(self) -> Decimal:
        total = self.total_cost
        if total and total > 0:
            return (self.labor_cost / total) * 100
        return Decimal(0)

    @property
    def overhead_pct(self) -> Decimal:
        total = self.total_cost
        if total and total > 0:
            return (self.overhead_cost / total) * 100
        return Decimal(0)


class WastageRecord(BaseModel):
    """
    Wastage tracking record.
    """
    date: datetime
    product_id: str
    product_name: Optional[str] = None
    production_line: Optional[str] = None
    wastage_type: str  # Scrap, Rework, Damage, Expiration, Other
    quantity: int
    unit_cost: Decimal
    total_cost: Decimal

    @property
    def total_wastage_value(self) -> Decimal:
        return self.quantity * self.unit_cost


class EquipmentEfficiency(BaseModel):
    """
    Equipment/OEE (Overall Equipment Effectiveness) data.
    """
    date: datetime
    equipment_id: str
    equipment_name: Optional[str] = None
    planned_production_time: int  # minutes
    actual_run_time: int  # minutes
    downtime_time: int  # minutes
    good_units_produced: int
    theoretical_cycle_time: int  # seconds per unit

    @property
    def availability_pct(self) -> Decimal:
        if self.planned_production_time and self.planned_production_time > 0:
            return Decimal(self.actual_run_time / self.planned_production_time * 100)
        return Decimal(0)

    @property
    def performance_pct(self) -> Decimal:
        if self.actual_run_time and self.actual_run_time > 0:
            theoretical_output = (self.actual_run_time * 60) / self.theoretical_cycle_time
            if theoretical_output > 0:
                return Decimal(self.good_units_produced / theoretical_output * 100)
        return Decimal(0)

    @property
    def quality_pct(self) -> Decimal:
        # Quality is already accounted in good_units_produced
        return Decimal(100)  # Simplified

    @property
    def oee(self) -> Decimal:
        avail = self.availability_pct / 100
        perf = self.performance_pct / 100
        qual = self.quality_pct / 100
        return Decimal(avail * perf * qual * 100)
