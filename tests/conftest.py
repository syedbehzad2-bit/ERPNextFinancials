"""Test configuration for ERP Intelligence Agent."""
import pytest
import pandas as pd
from pathlib import Path


@pytest.fixture
def sample_financial_data():
    """Sample financial data for testing."""
    return pd.DataFrame({
        'period': pd.date_range(start='2024-01-01', periods=12, freq='ME'),
        'revenue': [100000, 110000, 105000, 120000, 115000, 130000,
                    125000, 140000, 135000, 150000, 145000, 160000],
        'cost_of_goods_sold': [60000, 66000, 63000, 72000, 69000, 78000,
                              75000, 84000, 81000, 90000, 87000, 96000],
        'operating_expenses': [25000, 26000, 25500, 27000, 26500, 28000,
                              27500, 29000, 28500, 30000, 29500, 31000],
        'net_income': [15000, 18000, 16500, 21000, 19500, 24000,
                      22500, 27000, 25500, 30000, 28500, 33000]
    })


@pytest.fixture
def sample_inventory_data():
    """Sample inventory data for testing."""
    import numpy as np
    return pd.DataFrame({
        'sku': [f'SKU-{i:04d}' for i in range(1, 51)],
        'product_name': [f'Product {i}' for i in range(1, 51)],
        'category': np.random.choice(['Electronics', 'Clothing', 'Food', 'Hardware'], 50),
        'quantity': np.random.randint(10, 500, 50),
        'unit_cost': np.random.uniform(10, 100, 50).round(2),
        'receipt_date': pd.date_range(start='2024-01-01', periods=50, freq='7D'),
        'last_movement': pd.date_range(start='2024-06-01', periods=50, freq='-5D')
    })


@pytest.fixture
def sample_sales_data():
    """Sample sales data for testing."""
    import numpy as np
    np.random.seed(42)
    return pd.DataFrame({
        'date': pd.date_range(start='2024-01-01', periods=100, freq='D'),
        'order_id': [f'ORD-{i:05d}' for i in range(1, 101)],
        'customer_id': np.random.choice([f'CUST-{i:03d}' for i in range(1, 21)], 100),
        'customer_name': [f'Customer {i}' for i in np.random.randint(1, 21, 100)],
        'product_id': np.random.choice([f'PROD-{i:03d}' for i in range(1, 16)], 100),
        'product_name': [f'Product {i}' for i in np.random.randint(1, 16, 100)],
        'quantity': np.random.randint(1, 20, 100),
        'unit_price': np.random.uniform(20, 200, 100).round(2),
        'total_amount': np.random.uniform(100, 3000, 100).round(2)
    })


@pytest.fixture
def sample_manufacturing_data():
    """Sample manufacturing data for testing."""
    import numpy as np
    np.random.seed(42)
    return pd.DataFrame({
        'date': pd.date_range(start='2024-01-01', periods=30, freq='D'),
        'product_id': np.random.choice([f'PROD-{i:03d}' for i in range(1, 11)], 30),
        'product_name': [f'Product {i}' for i in np.random.randint(1, 11, 30)],
        'production_line': np.random.choice(['Line A', 'Line B', 'Line C'], 30),
        'planned_quantity': np.random.randint(500, 1000, 30),
        'actual_quantity': np.random.randint(400, 1100, 30),
        'good_quantity': np.random.randint(380, 1050, 30),
        'rejected_quantity': np.random.randint(0, 50, 30),
        'wastage_quantity': np.random.randint(0, 30, 30),
        'material_cost': np.random.uniform(5000, 10000, 30).round(2),
        'labor_cost': np.random.uniform(2000, 5000, 30).round(2),
        'overhead_cost': np.random.uniform(1000, 3000, 30).round(2)
    })


@pytest.fixture
def sample_purchase_data():
    """Sample purchase data for testing."""
    import numpy as np
    np.random.seed(42)
    return pd.DataFrame({
        'po_number': [f'PO-{i:05d}' for i in range(1, 51)],
        'order_date': pd.date_range(start='2024-01-01', periods=50, freq='3D'),
        'expected_delivery_date': pd.date_range(start='2024-01-10', periods=50, freq='3D'),
        'supplier_id': np.random.choice([f'SUP-{i:03d}' for i in range(1, 8)], 50),
        'supplier_name': np.random.choice(['Acme Corp', 'Global Supplies', 'FastParts Inc',
                                           'Quality Goods', 'Prime Materials', 'BestSource',
                                           'TopDistributors'], 50),
        'item_id': np.random.choice([f'ITEM-{i:03d}' for i in range(1, 21)], 50),
        'quantity_ordered': np.random.randint(100, 1000, 50),
        'quantity_received': np.random.randint(80, 1050, 50),
        'unit_price': np.random.uniform(5, 50, 50).round(2),
        'total_amount': np.random.uniform(1000, 30000, 50).round(2),
        'is_on_time': np.random.choice([True, False], 50, p=[0.8, 0.2])
    })


@pytest.fixture
def loader():
    """DataLoader instance for testing."""
    from data_loader.loader import DataLoader
    return DataLoader()
