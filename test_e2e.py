"""
End-to-end testing script for ERP Intelligence Agent.
Tests the complete flow with ONLY sales data uploaded.
"""
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import requests
import json
from pathlib import Path

API_URL = "http://localhost:8000"

print("=" * 80)
print("END-TO-END TEST: Sales Data Only")
print("=" * 80)

# Test 1: Health Check
print("\n1. Testing API Health...")
response = requests.get(f"{API_URL}/api/health")
print(f"   Status: {response.status_code}")
print(f"   Response: {response.json()}")
assert response.status_code == 200, "Health check failed"
print("   ✅ PASS")

# Test 2: Upload Sales File
print("\n2. Testing Sales File Upload...")
sales_file = Path("sample_data/sample_sales.csv")
if not sales_file.exists():
    print(f"   ❌ FAIL: File not found: {sales_file}")
    exit(1)

with open(sales_file, 'rb') as f:
    files = {'file': ('sample_sales.csv', f, 'text/csv')}
    response = requests.post(f"{API_URL}/api/upload", files=files)

print(f"   Status: {response.status_code}")
upload_result = response.json()
print(f"   File ID: {upload_result['file_id']}")
print(f"   Data Type: {upload_result['data_type']}")
print(f"   Confidence: {upload_result['schema_confidence']}")
print(f"   Required Columns Present: {upload_result['required_columns_present']}")

assert upload_result['success'] == True, "Upload failed"
assert upload_result['data_type'] == 'sales', f"Wrong type detected: {upload_result['data_type']}"
assert upload_result['schema_confidence'] >= 0.5, "Low confidence"
assert upload_result['required_columns_present'] == True, "Missing required columns"
print("   ✅ PASS")

file_id = upload_result['file_id']

# Test 3: Run Analysis
print("\n3. Testing Analysis with Sales Data ONLY...")
analysis_request = {
    "files": [
        {
            "id": file_id,
            "name": "sample_sales.csv",
            "type": "sales"
        }
    ],
    "config": {
        "analysis_types": {
            "financial": False,
            "manufacturing": False,
            "inventory": False,
            "sales": True,
            "purchase": False
        },
        "analysis_depth": "detailed",
        "enable_cross_file_analysis": False
    }
}

response = requests.post(
    f"{API_URL}/api/analyze",
    json=analysis_request,
    headers={'Content-Type': 'application/json'}
)

print(f"   Status: {response.status_code}")
analysis_result = response.json()

if not analysis_result.get('success'):
    print(f"   ❌ FAIL: {analysis_result.get('error')}")
    exit(1)

data = analysis_result['data']
print(f"\n   === ANALYSIS RESULTS ===")
print(f"   Enabled Domains: {data['enabled_domains']}")
print(f"   Files Analyzed: {data['files_analyzed']}")
print(f"   Total Insights: {data['total_insights']}")
print(f"   Critical Risks: {data['critical_count']}")

# CRITICAL ASSERTIONS
print(f"\n   === VALIDATION ===")

# Check enabled_domains
assert data['enabled_domains'] == ['sales'], f"ERROR: enabled_domains = {data['enabled_domains']}, expected ['sales']"
print(f"   ✅ enabled_domains = ['sales'] only")

# Check that ONLY sales domain has data
domains_with_kpis = list(data['kpis'].keys())
print(f"   Domains with KPIs: {domains_with_kpis}")
assert domains_with_kpis == ['sales'], f"ERROR: {domains_with_kpis}"
print(f"   ✅ ONLY sales has KPIs")

# Check insights
domains_with_insights = list(data['insights_by_category'].keys())
print(f"   Domains with Insights: {domains_with_insights}")
assert domains_with_insights == ['sales'], f"ERROR: {domains_with_insights}"
print(f"   ✅ ONLY sales has insights")

# Check that other domains are NOT present
unwanted_domains = ['financial', 'manufacturing', 'inventory', 'purchase']
for domain in unwanted_domains:
    assert domain not in data['enabled_domains'], f"ERROR: {domain} should NOT be in enabled_domains"
    assert domain not in domains_with_kpis, f"ERROR: {domain} should NOT have KPIs"
    assert domain not in domains_with_insights, f"ERROR: {domain} should NOT have insights"
print(f"   ✅ No unwanted domains present")

# Check cross-domain insights
cross_domain_count = len(data.get('cross_domain_insights', []))
print(f"   Cross-domain insights: {cross_domain_count}")
assert cross_domain_count == 0, "Should be 0 with only 1 domain"
print(f"   ✅ No cross-domain insights (correct for single domain)")

print("\n   ✅ ALL VALIDATION PASSED")

# Test 4: Template Download
print("\n4. Testing Template Download...")
response = requests.get(f"{API_URL}/api/templates/sales")
print(f"   Status: {response.status_code}")
assert response.status_code == 200, "Template download failed"
assert len(response.content) > 0, "Empty template file"
print(f"   File size: {len(response.content)} bytes")
print("   ✅ PASS")

# Test 5: Sample Download
print("\n5. Testing Sample Download...")
response = requests.get(f"{API_URL}/api/samples/sales")
print(f"   Status: {response.status_code}")
assert response.status_code == 200, "Sample download failed"
assert len(response.content) > 0, "Empty sample file"
print(f"   File size: {len(response.content)} bytes")
print("   ✅ PASS")

print("\n" + "=" * 80)
print("ALL TESTS PASSED ✅")
print("=" * 80)
print("\nSUMMARY:")
print("  ✅ Backend only analyzes uploaded domains (sales)")
print("  ✅ No fake data for financial/manufacturing/inventory/purchase")
print("  ✅ enabled_domains correctly returned")
print("  ✅ Template downloads working")
print("  ✅ Sample downloads working")
print("\nThe system is now working correctly!")
print("=" * 80)
