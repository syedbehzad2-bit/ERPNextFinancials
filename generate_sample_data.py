"""
Generate sample data files for ERP Agent testing and templates.
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

np.random.seed(42)
random.seed(42)

# Sample data directory
output_dir = "D:/ERP Agent/sample_data"
template_dir = "D:/ERP Agent/templates"

# Create directories if they don't exist
os.makedirs(output_dir, exist_ok=True)
os.makedirs(template_dir, exist_ok=True)

# ============== FINANCIAL DATA ==============
financial_data = []
periods = pd.date_range(start='2024-01-01', end='2024-12-31', freq='ME')
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

for i, (period, month) in enumerate(zip(periods, months)):
    base_revenue = 800000 + (i * 40000) + random.randint(-50000, 50000)
    cogs = base_revenue * random.uniform(0.55, 0.62)
    gross_profit = base_revenue - cogs
    opex = 180000 + (i * 5000) + random.randint(-10000, 10000)
    operating_income = gross_profit - opex
    interest = random.uniform(5000, 15000)
    tax = operating_income * random.uniform(0.20, 0.28)
    net_income = operating_income - interest - tax
    budget = 850000 + (i * 35000)

    financial_data.append({
        'period': period.strftime('%Y-%m'),
        'month': month,
        'revenue': round(base_revenue, 2),
        'cost_of_goods_sold': round(cogs, 2),
        'gross_profit': round(gross_profit, 2),
        'operating_expenses': round(opex, 2),
        'operating_income': round(operating_income, 2),
        'interest_expense': round(interest, 2),
        'income_tax': round(tax, 2),
        'net_income': round(net_income, 2),
        'budget': round(budget, 2),
        'variance': round(base_revenue - budget, 2)
    })

df_financial = pd.DataFrame(financial_data)
df_financial.to_csv(f"{output_dir}/sample_financial.csv", index=False)
df_financial.to_excel(f"{output_dir}/sample_financial.xlsx", index=False)
print("Created sample_financial.csv and sample_financial.xlsx")

# ============== MANUFACTURING DATA ==============
products = [f'PRD-{i:03d}' for i in range(1, 11)]
product_names = [f'Product {i}' for i in range(1, 11)]
lines = ['Line A', 'Line B', 'Line C', 'Line D']

manufacturing_data = []
for _ in range(200):
    product = random.choice(products)
    idx = products.index(product)
    planned = random.randint(500, 2000)
    actual = int(planned * random.uniform(0.85, 1.05))
    good = int(actual * random.uniform(0.90, 0.99))
    rejected = actual - good
    wastage = int(good * random.uniform(0.01, 0.08))

    manufacturing_data.append({
        'product_id': product,
        'product_name': product_names[idx],
        'production_line': random.choice(lines),
        'planned_quantity': planned,
        'actual_quantity': actual,
        'good_quantity': good,
        'rejected_quantity': rejected,
        'wastage_quantity': wastage,
        'production_date': (datetime.now() - timedelta(days=random.randint(0, 60))).strftime('%Y-%m-%d'),
        'efficiency': round(good / planned * 100, 2),
        'yield_rate': round(good / actual * 100, 2)
    })

df_manufacturing = pd.DataFrame(manufacturing_data)
df_manufacturing.to_csv(f"{output_dir}/sample_manufacturing.csv", index=False)
df_manufacturing.to_excel(f"{output_dir}/sample_manufacturing.xlsx", index=False)
print("Created sample_manufacturing.csv and sample_manufacturing.xlsx")

# ============== INVENTORY DATA ==============
skus = [f'SKU-{i:04d}' for i in range(1, 51)]
warehouses = ['WH-01', 'WH-02', 'WH-03']

inventory_data = []
for sku in skus:
    for _ in range(random.randint(1, 3)):
        qty = random.randint(10, 500)
        age = random.randint(1, 365)
        last_move = datetime.now() - timedelta(days=age)
        inventory_data.append({
            'sku': sku,
            'product_name': f'Item {sku.split("-")[1]}',
            'quantity': qty,
            'unit_cost': round(random.uniform(10, 500), 2),
            'unit_price': round(random.uniform(15, 800), 2),
            'warehouse': random.choice(warehouses),
            'receipt_date': last_move.strftime('%Y-%m-%d'),
            'last_movement_date': last_move.strftime('%Y-%m-%d'),
            'days_in_stock': age,
            'stock_value': round(qty * random.uniform(10, 500), 2),
            'category': random.choice(['Raw Material', 'WIP', 'Finished Goods'])
        })

df_inventory = pd.DataFrame(inventory_data)
df_inventory.to_csv(f"{output_dir}/sample_inventory.csv", index=False)
df_inventory.to_excel(f"{output_dir}/sample_inventory.xlsx", index=False)
print("Created sample_inventory.csv and sample_inventory.xlsx")

# ============== SALES DATA ==============
customers = [f'CUST-{i:04d}' for i in range(1, 31)]
customer_names = [f'Customer {i}' for i in range(1, 31)]
products_sold = [f'PRD-{i:03d}' for i in range(1, 11)]
regions = ['North', 'South', 'East', 'West']
channels = ['Online', 'Retail', 'Wholesale', 'Direct']

sales_data = []
for _ in range(500):
    qty = random.randint(1, 100)
    unit_price = random.uniform(20, 200)
    discount = random.uniform(0, 0.15)
    total_amount = qty * unit_price * (1 - discount)

    sales_data.append({
        'order_id': f'ORD-{random.randint(10000, 99999)}',
        'customer_id': random.choice(customers),
        'customer_name': customer_names[customers.index(random.choice(customers))],
        'product_id': random.choice(products_sold),
        'quantity': qty,
        'unit_price': round(unit_price, 2),
        'discount': round(discount * 100, 2),
        'total_amount': round(total_amount, 2),
        'order_date': (datetime.now() - timedelta(days=random.randint(0, 180))).strftime('%Y-%m-%d'),
        'region': random.choice(regions),
        'channel': random.choice(channels),
        'sales_rep': random.choice(['Rep A', 'Rep B', 'Rep C', 'Rep D'])
    })

df_sales = pd.DataFrame(sales_data)
df_sales.to_csv(f"{output_dir}/sample_sales.csv", index=False)
df_sales.to_excel(f"{output_dir}/sample_sales.xlsx", index=False)
print("Created sample_sales.csv and sample_sales.xlsx")

# ============== PURCHASE DATA ==============
suppliers = [f'SUP-{i:04d}' for i in range(1, 21)]
supplier_names = [f'Supplier {i}' for i in range(1, 21)]
po_products = [f'MAT-{i:04d}' for i in range(1, 31)]

purchase_data = []
for _ in range(300):
    qty = random.randint(50, 2000)
    unit_price = random.uniform(5, 150)
    total = qty * unit_price

    order_date = datetime.now() - timedelta(days=random.randint(10, 90))
    lead_time = random.randint(5, 30)
    delivery_date = order_date + timedelta(days=lead_time)

    purchase_data.append({
        'po_number': f'PO-{random.randint(10000, 99999)}',
        'supplier_id': random.choice(suppliers),
        'supplier_name': supplier_names[suppliers.index(random.choice(suppliers))],
        'product_id': random.choice(po_products),
        'quantity_ordered': qty,
        'quantity_received': int(qty * random.uniform(0.95, 1.02)),
        'unit_price': round(unit_price, 2),
        'total_amount': round(total, 2),
        'order_date': order_date.strftime('%Y-%m-%d'),
        'expected_delivery_date': delivery_date.strftime('%Y-%m-%d'),
        'actual_delivery_date': (delivery_date + timedelta(days=random.randint(-3, 5))).strftime('%Y-%m-%d'),
        'lead_time_days': lead_time,
        'quality_score': round(random.uniform(85, 100), 2)
    })

df_purchase = pd.DataFrame(purchase_data)
df_purchase.to_csv(f"{output_dir}/sample_purchase.csv", index=False)
df_purchase.to_excel(f"{output_dir}/sample_purchase.xlsx", index=False)
print("Created sample_purchase.csv and sample_purchase.xlsx")

# ============== CREATE TEMPLATES ==============
# Template Financial
template_financial = pd.DataFrame({
    'period': ['2024-01', '2024-02'],
    'month': ['Jan', 'Feb'],
    'revenue': [0, 0],
    'cost_of_goods_sold': [0, 0],
    'gross_profit': [0, 0],
    'operating_expenses': [0, 0],
    'operating_income': [0, 0],
    'interest_expense': [0, 0],
    'income_tax': [0, 0],
    'net_income': [0, 0],
    'budget': [0, 0],
    'variance': [0, 0]
})
template_financial.to_excel(f"{template_dir}/template_financial.xlsx", index=False)
print("Created template_financial.xlsx")

# Template Manufacturing
template_manufacturing = pd.DataFrame({
    'product_id': ['PRD-001', 'PRD-002'],
    'product_name': ['Product 1', 'Product 2'],
    'production_line': ['Line A', 'Line A'],
    'planned_quantity': [1000, 1000],
    'actual_quantity': [0, 0],
    'good_quantity': [0, 0],
    'rejected_quantity': [0, 0],
    'wastage_quantity': [0, 0],
    'production_date': ['2024-01-01', '2024-01-02'],
    'efficiency': [0, 0],
    'yield_rate': [0, 0]
})
template_manufacturing.to_excel(f"{template_dir}/template_manufacturing.xlsx", index=False)
print("Created template_manufacturing.xlsx")

# Template Inventory
template_inventory = pd.DataFrame({
    'sku': ['SKU-0001', 'SKU-0002'],
    'product_name': ['Item 1', 'Item 2'],
    'quantity': [0, 0],
    'unit_cost': [0, 0],
    'unit_price': [0, 0],
    'warehouse': ['WH-01', 'WH-01'],
    'receipt_date': ['2024-01-01', '2024-01-01'],
    'last_movement_date': ['2024-01-01', '2024-01-01'],
    'days_in_stock': [0, 0],
    'stock_value': [0, 0],
    'category': ['Finished Goods', 'Finished Goods']
})
template_inventory.to_excel(f"{template_dir}/template_inventory.xlsx", index=False)
print("Created template_inventory.xlsx")

# Template Sales
template_sales = pd.DataFrame({
    'order_id': ['ORD-10001', 'ORD-10002'],
    'customer_id': ['CUST-0001', 'CUST-0002'],
    'customer_name': ['Customer 1', 'Customer 2'],
    'product_id': ['PRD-001', 'PRD-002'],
    'quantity': [0, 0],
    'unit_price': [0, 0],
    'discount': [0, 0],
    'total_amount': [0, 0],
    'order_date': ['2024-01-01', '2024-01-01'],
    'region': ['North', 'North'],
    'channel': ['Online', 'Online'],
    'sales_rep': ['Rep A', 'Rep A']
})
template_sales.to_excel(f"{template_dir}/template_sales.xlsx", index=False)
print("Created template_sales.xlsx")

# Template Purchase
template_purchase = pd.DataFrame({
    'po_number': ['PO-10001', 'PO-10002'],
    'supplier_id': ['SUP-0001', 'SUP-0002'],
    'supplier_name': ['Supplier 1', 'Supplier 2'],
    'product_id': ['MAT-0001', 'MAT-0002'],
    'quantity_ordered': [0, 0],
    'quantity_received': [0, 0],
    'unit_price': [0, 0],
    'total_amount': [0, 0],
    'order_date': ['2024-01-01', '2024-01-01'],
    'expected_delivery_date': ['2024-01-15', '2024-01-15'],
    'actual_delivery_date': ['2024-01-15', '2024-01-15'],
    'lead_time_days': [0, 0],
    'quality_score': [0, 0]
})
template_purchase.to_excel(f"{template_dir}/template_purchase.xlsx", index=False)
print("Created template_purchase.xlsx")

print("\nAll sample data and template files created successfully!")
