import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { files, config } = body;

    // In production, this would call the Python backend
    // For now, return mock results

    const mockResults = {
      generated_at: new Date().toISOString(),
      data_source: files.map((f: any) => f.name).join(', '),
      data_types: [...new Set(files.map((f: any) => f.type))],
      data_quality: {
        total_rows: files.reduce((sum: number, f: any) => sum + f.rows, 0),
        total_columns: files[0]?.columns?.length || 0,
        missing_values: {},
        duplicate_rows: 0,
        issues: [],
        is_usable: true,
        usable_message: 'Data is ready for analysis',
      },
      executive_summary: [
        'Revenue shows a positive trend with 12% growth over the analysis period',
        'Inventory turnover needs attention - 23% of stock is aged over 90 days',
        'Customer concentration risk identified - top 3 customers represent 45% of revenue',
        'Production efficiency improved by 8% compared to previous period',
        'Supplier delivery performance is stable at 94% on-time rate',
      ],
      financial: {
        kpis: [
          { label: 'Total Revenue', value: '$2.4M', change: 12.5 },
          { label: 'Net Margin', value: '18.2%', isPercentage: true },
          { label: 'Gross Profit', value: '$890K', change: 8.3 },
          { label: 'Operating Expenses', value: '$456K', change: -2.1 },
        ],
        charts_data: {},
        insights: [
          {
            category: 'financial',
            severity: 'high',
            finding: 'Operating expenses increased by 15% in Q4',
            impact: 'Higher costs are reducing net margin by 2 percentage points',
            action: 'Review Q4 expense reports and identify non-essential spending',
            metrics: { amount: 456000, percentage: 15 },
          },
        ],
      },
      manufacturing: {
        kpis: [
          { label: 'Production Efficiency', value: '87%', change: 5.2 },
          { label: 'Wastage Rate', value: '3.2%', isPercentage: true },
          { label: 'Units Produced', value: 45600 },
          { label: 'Cost per Unit', value: '$24.50', change: -1.5 },
        ],
        charts_data: {},
        insights: [
          {
            category: 'manufacturing',
            severity: 'medium',
            finding: 'Wastage on Product Line A exceeded target',
            impact: 'Additional $12,000 in material costs this quarter',
            action: 'Investigate machine calibration and operator training for Line A',
            metrics: { wastage: 3.2, target: 2.0 },
          },
        ],
      },
      inventory: {
        kpis: [
          { label: 'Stock Value', value: '$1.2M' },
          { label: 'Turnover Ratio', value: '4.2x' },
          { label: 'Days Inventory', value: '87 days' },
          { label: 'Dead Stock', value: '$45K', isPercentage: true },
        ],
        charts_data: {},
        insights: [
          {
            category: 'inventory',
            severity: 'critical',
            finding: '23% of inventory aged over 90 days',
            impact: 'Tied up capital of $276,000 in slow-moving stock',
            action: 'Implement discount strategy for aged items or consider liquidation',
            metrics: { aged_percentage: 23, amount: 276000 },
          },
        ],
      },
      sales: {
        kpis: [
          { label: 'Total Orders', value: 1250 },
          { label: 'Revenue', value: '$2.4M', change: 12.5 },
          { label: 'Avg Order Value', value: '$1,920' },
          { label: 'Unique Customers', value: 89 },
        ],
        charts_data: {},
        insights: [
          {
            category: 'sales',
            severity: 'high',
            finding: 'Top 3 customers represent 45% of total revenue',
            impact: 'High customer concentration creates significant revenue risk',
            action: 'Develop customer diversification strategy and increase marketing to new segments',
            metrics: { concentration: 45, risk_level: 'high' },
          },
        ],
      },
      purchase: {
        kpis: [
          { label: 'Total Spend', value: '$890K' },
          { label: 'Suppliers', value: 23 },
          { label: 'Avg Lead Time', value: '8.5 days' },
          { label: 'On-Time Delivery', value: '94%', isPercentage: true },
        ],
        charts_data: {},
        insights: [],
      },
      critical_risks: [
        {
          id: '1',
          title: 'Customer Concentration Risk',
          category: 'sales',
          description: 'Top 3 customers account for 45% of revenue',
          probability: 'high',
          financial_impact: '$1.08M',
          time_to_impact: '3-6 months',
          severity: 'critical',
          mitigation: 'Diversify customer base through targeted marketing',
          early_warning_signals: ['Customer satisfaction decline', 'Large contract renewals pending'],
        },
        {
          id: '2',
          title: 'Slow Moving Inventory',
          category: 'inventory',
          description: '$276,000 tied up in aged stock',
          probability: 'high',
          financial_impact: '$276K',
          time_to_impact: '1-3 months',
          severity: 'high',
          mitigation: 'Clearance sales and inventory review',
          early_warning_signals: ['No movement for 90+ days', 'Storage costs accumulating'],
        },
      ],
      action_plan: [
        {
          id: '1',
          title: 'Clear Aged Inventory',
          what: 'Implement 15% discount on items aged 90+ days',
          why: 'Capital is tied up in slow-moving stock',
          how: '1. Identify items 2. Calculate discount 3. Update pricing 4. Monitor movement',
          impact: 'Release $150K in working capital',
          priority: 'immediate',
          timeline: '0-30 days',
          estimated_savings: 150000,
        },
        {
          id: '2',
          title: 'Reduce Customer Concentration',
          what: 'Launch customer acquisition campaign',
          why: '45% revenue from top 3 customers is risky',
          how: '1. Budget allocation 2. Channel selection 3. Campaign execution 4. Track new signups',
          impact: 'Reduce top-3 concentration to 30%',
          priority: 'short_term',
          timeline: '1-3 months',
          estimated_revenue_impact: 250000,
        },
        {
          id: '3',
          title: 'Improve Production Efficiency',
          what: 'Operator training program for Line A',
          why: 'Line A wastage exceeds 2% target',
          how: '1. Assess training needs 2. Develop curriculum 3. Schedule sessions 4. Measure results',
          impact: 'Reduce wastage by 50%',
          priority: 'short_term',
          timeline: '1-3 months',
          estimated_savings: 6000,
        },
      ],
      analysis_results: {},
    };

    return NextResponse.json({ success: true, data: mockResults });
  } catch (error) {
    return NextResponse.json(
      { success: false, error: 'Analysis failed' },
      { status: 500 }
    );
  }
}
