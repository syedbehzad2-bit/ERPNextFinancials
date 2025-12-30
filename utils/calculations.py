"""Calculation utilities."""
from typing import Union
from decimal import Decimal
import numpy as np


def calculate_growth(current: float, prior: float) -> float:
    """Calculate percentage growth."""
    if prior == 0:
        return 0.0
    return ((current - prior) / prior) * 100


def calculate_margin(revenue: float, cost: float) -> float:
    """Calculate gross margin percentage."""
    if revenue == 0:
        return 0.0
    return ((revenue - cost) / revenue) * 100


def calculate_margin_pct(gross_profit: float, revenue: float) -> float:
    """Calculate margin percentage."""
    if revenue == 0:
        return 0.0
    return (gross_profit / revenue) * 100


def calculate_turnover(cogs: float, avg_inventory: float) -> float:
    """Calculate inventory turnover ratio."""
    if avg_inventory == 0:
        return 0.0
    return cogs / avg_inventory


def calculate_days_inventory(turnover: float) -> float:
    """Calculate days inventory outstanding."""
    if turnover == 0:
        return 0.0
    return 365 / turnover


def calculate_variance(actual: float, planned: float) -> tuple:
    """Calculate variance in amount and percentage."""
    variance = actual - planned
    variance_pct = (variance / planned * 100) if planned != 0 else 0
    return variance, variance_pct


def calculate_efficiency(actual: float, planned: float) -> float:
    """Calculate production efficiency percentage."""
    if planned == 0:
        return 0.0
    return (actual / planned) * 100


def calculate_yield(good_units: float, total_units: float) -> float:
    """Calculate yield percentage."""
    if total_units == 0:
        return 0.0
    return (good_units / total_units) * 100


def calculate_wastage_rate(waste: float, total: float) -> float:
    """Calculate wastage percentage."""
    if total == 0:
        return 0.0
    return (waste / total) * 100


def calculate_reorder_point(
    daily_demand: float,
    lead_time: float,
    safety_stock: float = 0
) -> float:
    """Calculate reorder point."""
    return (daily_demand * lead_time) + safety_stock


def calculate_eoq(
    annual_demand: float,
    ordering_cost: float,
    holding_cost: float
) -> float:
    """Calculate Economic Order Quantity."""
    if holding_cost == 0:
        return 0.0
    return np.sqrt((2 * annual_demand * ordering_cost) / holding_cost)


def calculate_safety_stock(
    max_daily_demand: float,
    avg_daily_demand: float,
    max_lead_time: float,
    avg_lead_time: float
) -> float:
    """Calculate safety stock."""
    return (max_daily_demand * max_lead_time) - (avg_daily_demand * avg_lead_time)


def calculate_customer_concentration(
    customer_revenue: dict,
    total_revenue: float
) -> dict:
    """Calculate customer concentration metrics."""
    sorted_revenue = sorted(customer_revenue.items(), key=lambda x: x[1], reverse=True)

    top_customer = sorted_revenue[0] if sorted_revenue else (None, 0)
    top_3 = sorted_revenue[:3]
    top_5 = sorted_revenue[:5]

    return {
        'top_customer': {
            'id': top_customer[0],
            'revenue': top_customer[1],
            'percentage': (top_customer[1] / total_revenue * 100) if total_revenue > 0 else 0
        },
        'top_3': {
            'total_revenue': sum(r[1] for r in top_3),
            'percentage': (sum(r[1] for r in top_3) / total_revenue * 100) if total_revenue > 0 else 0
        },
        'top_5': {
            'total_revenue': sum(r[1] for r in top_5),
            'percentage': (sum(r[1] for r in top_5) / total_revenue * 100) if total_revenue > 0 else 0
        }
    }


def calculate_pareto_metrics(data: dict) -> dict:
    """Calculate Pareto analysis metrics."""
    sorted_items = sorted(data.items(), key=lambda x: x[1], reverse=True)
    total = sum(data.values())

    if total == 0:
        return {'items_for_80': 0, 'concentration': 'LOW', 'top_contributors': []}

    cumulative = 0
    items_for_80 = 0
    for i, (item, value) in enumerate(sorted_items):
        cumulative += value
        if cumulative / total <= 0.8:
            items_for_80 = i + 1

    top_20_value = sum(v for k, v in sorted_items[:max(1, len(sorted_items) // 5)])
    top_20_pct = (top_20_value / total * 100) if total > 0 else 0

    concentration = 'HIGH' if top_20_pct > 80 else 'MEDIUM' if top_20_pct > 60 else 'LOW'

    return {
        'items_for_80': items_for_80,
        'items_for_80_pct': items_for_80 / len(sorted_items) * 100 if sorted_items else 0,
        'top_20_contribution_pct': top_20_pct,
        'concentration': concentration,
        'total_value': total
    }
