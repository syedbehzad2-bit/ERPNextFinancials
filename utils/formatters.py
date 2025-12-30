"""Formatting utilities."""
from typing import Union
from decimal import Decimal


def format_currency(value: Union[float, int, Decimal], precision: int = 0) -> str:
    """Format number as currency."""
    if value is None:
        return "N/A"
    value = float(value)
    if abs(value) >= 1_000_000:
        return f"${value / 1_000_000:.1f}M"
    elif abs(value) >= 1_000:
        return f"${value / 1_000:.1f}K"
    else:
        return f"${value:,.{precision}f}"


def format_pct(value: Union[float, int, Decimal], precision: int = 1) -> str:
    """Format number as percentage."""
    if value is None:
        return "N/A"
    return f"{float(value):.{precision}f}%"


def format_number(value: Union[float, int, Decimal], precision: int = 1) -> str:
    """Format number with thousand separators."""
    if value is None:
        return "N/A"
    return f"{float(value):,.{precision}f}"


def format_change(value: Union[float, int, Decimal]) -> str:
    """Format change with arrow and color."""
    if value is None:
        return "N/A"
    value = float(value)
    arrow = "↑" if value > 0 else "↓" if value < 0 else "→"
    color = "green" if value > 0 else "red" if value < 0 else "gray"
    return f"{arrow} {abs(value):.1f}%"


def format_compact(value: Union[float, int, Decimal]) -> str:
    """Format number in compact form (1.2K, 3.4M, etc.)."""
    if value is None:
        return "N/A"
    value = float(value)
    if abs(value) >= 1_000_000_000:
        return f"{value / 1_000_000_000:.1f}B"
    elif abs(value) >= 1_000_000:
        return f"{value / 1_000_000:.1f}M"
    elif abs(value) >= 1_000:
        return f"{value / 1_000:.1f}K"
    else:
        return f"{value:.0f}"
