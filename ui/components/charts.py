"""
Chart components using Plotly for dashboard visualizations.
"""
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from typing import Dict, Any, List, Optional


def render_kpi_cards(kpis: Dict[str, Any]) -> None:
    """Render KPI metric cards in a row."""
    col1, col2, col3, col4 = st.columns(4)

    # Revenue
    with col1:
        value = kpis.get('total_revenue', kpis.get('total_spend', 0))
        render_metric_card(
            label="Total Revenue",
            value=f"${value:,.0f}" if value else "$0",
            change=kpis.get('revenue_growth_pct', kpis.get('revenue_growth', 0))
        )

    # Net Margin
    with col2:
        margin = kpis.get('net_margin_pct', kpis.get('average_margin_pct', 0))
        render_metric_card(
            label="Net Margin",
            value=f"{margin:.1f}%" if margin else "N/A",
            change=None,
            is_percentage=True
        )

    # Inventory/Ops depending on data type
    with col3:
        if 'total_stock_value' in kpis:
            render_metric_card(
                label="Inventory Value",
                value=f"${kpis['total_stock_value']:,.0f}"
            )
        elif 'production_efficiency_pct' in kpis:
            render_metric_card(
                label="Production Efficiency",
                value=f"{kpis['production_efficiency_pct']:.1f}%"
            )
        else:
            render_metric_card(
                label="Orders",
                value=f"{kpis.get('order_count', kpis.get('total_orders', 0)):,}"
            )

    # Fourth metric
    with col4:
        if 'days_inventory_outstanding' in kpis:
            render_metric_card(
                label="Days Inventory",
                value=f"{kpis['days_inventory_outstanding']:.0f}"
            )
        elif 'average_lead_time_days' in kpis:
            render_metric_card(
                label="Avg Lead Time",
                value=f"{kpis['average_lead_time_days']:.1f} days"
            )
        else:
            render_metric_card(
                label="Unique Customers",
                value=f"{kpis.get('unique_customers', 0):,}"
            )


def render_metric_card(label: str, value: str, change: Optional[float] = None,
                       is_percentage: bool = False) -> None:
    """Render a single metric card."""
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-value">{value}</div>
        <div class="kpi-label">{label}</div>
        {f'<div class="kpi-change {"kpi-positive" if change and change > 0 else "kpi-negative" if change and change < 0 else ""}">{"↑" if change and change > 0 else "↓" if change and change < 0 else ""} {abs(change):.1f}%</div>' if change is not None else ''}
    </div>
    """, unsafe_allow_html=True)


def render_revenue_trend_chart(data: List[Dict]) -> None:
    """Render revenue trend line chart."""
    if not data:
        return

    fig = go.Figure()

    periods = [d.get('period', d.get('date', '')) for d in data]
    values = [d.get('revenue', d.get('value', 0)) for d in data]

    fig.add_trace(go.Scatter(
        x=periods,
        y=values,
        mode='lines+markers',
        name='Revenue',
        line=dict(color='#e94560', width=3),
        fill='tozeroy',
        fillcolor='rgba(233, 69, 96, 0.1)'
    ))

    fig.update_layout(
        title=dict(text='Revenue Trend', font=dict(color='#1e293b', size=16)),
        paper_bgcolor='transparent',
        plot_bgcolor='#ffffff',
        font=dict(color='#475569'),
        xaxis=dict(showgrid=False, color='#64748b'),
        yaxis=dict(showgrid=True, gridcolor='#e2e8f0', color='#64748b'),
        margin=dict(l=20, r=20, t=40, b=20),
        height=300
    )

    st.plotly_chart(fig, use_container_width=True)


def render_margin_chart(data: List[Dict]) -> None:
    """Render margin trend chart."""
    if not data:
        return

    fig = go.Figure()

    periods = [d.get('period', '') for d in data]
    margins = [d.get('margin', d.get('gross_margin_pct', 0)) for d in data]

    fig.add_trace(go.Scatter(
        x=periods,
        y=margins,
        mode='lines+markers',
        name='Margin %',
        line=dict(color='#00c896', width=3),
        fill='tozeroy',
        fillcolor='rgba(0, 200, 150, 0.1)'
    ))

    # Add threshold line
    fig.add_hline(y=20, line_dash="dash", line_color="#ffa500",
                  annotation_text="Target: 20%")

    fig.update_layout(
        title=dict(text='Margin Trend (%)', font=dict(color='#1e293b', size=16)),
        paper_bgcolor='transparent',
        plot_bgcolor='#ffffff',
        font=dict(color='#475569'),
        xaxis=dict(showgrid=False, color='#64748b'),
        yaxis=dict(showgrid=True, gridcolor='#e2e8f0', color='#64748b', range=[0, max(max(margins) * 1.2, 30)]),
        margin=dict(l=20, r=20, t=40, b=20),
        height=300
    )

    st.plotly_chart(fig, use_container_width=True)


def render_aging_chart(data: List[Dict]) -> None:
    """Render stock aging distribution pie/donut chart."""
    if not data:
        return

    labels = [d.get('bucket', d.get('category', '')) for d in data]
    values = [d.get('value', 0) for d in data]

    colors = ['#00c896', '#4ecdc4', '#45b7d1', '#e94560']

    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.4,
        marker=dict(colors=colors[:len(data)])
    )])

    fig.update_layout(
        title=dict(text='Stock Aging Distribution', font=dict(color='#1e293b', size=16)),
        paper_bgcolor='transparent',
        font=dict(color='#475569'),
        margin=dict(l=20, r=20, t=40, b=20),
        height=300,
        showlegend=True
    )

    st.plotly_chart(fig, use_container_width=True)


def render_pareto_chart(data: List[Dict]) -> None:
    """Render Pareto chart for product/customer analysis."""
    if not data:
        return

    categories = [d.get('category', d.get('product', d.get('sku', ''))) for d in data]
    values = [d.get('value', 0) for d in data]
    cumulative = []
    total = sum(values)
    cumsum = 0
    for v in values:
        cumsum += v
        cumulative.append(cumsum / total * 100 if total > 0 else 0)

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
        go.Bar(x=categories, y=values, name='Value', marker_color='#e94560'),
        secondary_y=False
    )

    fig.add_trace(
        go.Scatter(x=categories, y=cumulative, name='Cumulative %',
                   line=dict(color='#00c896', width=3)),
        secondary_y=True
    )

    fig.add_hline(y=80, line_dash="dash", line_color="#ffa500",
                  annotation_text="80%", secondary_y=True)

    fig.update_layout(
        title=dict(text='Pareto Analysis (80/20)', font=dict(color='#1e293b', size=16)),
        paper_bgcolor='transparent',
        plot_bgcolor='#ffffff',
        font=dict(color='#475569'),
        xaxis=dict(showgrid=False, color='#64748b'),
        yaxis=dict(showgrid=True, gridcolor='#e2e8f0', color='#64748b'),
        yaxis2=dict(showgrid=False, color='#64748b'),
        margin=dict(l=20, r=20, t=40, b=20),
        height=350,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    st.plotly_chart(fig, use_container_width=True)


def render_efficiency_chart(data: List[Dict]) -> None:
    """Render production efficiency bar chart."""
    if not data:
        return

    products = [d.get('product', '') for d in data]
    efficiencies = [d.get('efficiency', 0) for d in data]

    colors = ['#ff4b4b' if e < 70 else '#ffa500' if e < 85 else '#00c896' for e in efficiencies]

    fig = go.Figure(go.Bar(
        x=products,
        y=efficiencies,
        marker_color=colors
    ))

    fig.add_hline(y=95, line_dash="dash", line_color="#00c896",
                  annotation_text="Target: 95%")

    fig.update_layout(
        title=dict(text='Production Efficiency by Product', font=dict(color='#1e293b', size=16)),
        paper_bgcolor='transparent',
        plot_bgcolor='#ffffff',
        font=dict(color='#475569'),
        xaxis=dict(showgrid=False, color='#64748b'),
        yaxis=dict(showgrid=True, gridcolor='#e2e8f0', color='#64748b', range=[0, 110]),
        margin=dict(l=20, r=20, t=40, b=20),
        height=300
    )

    st.plotly_chart(fig, use_container_width=True)


def render_wastage_chart(data: List[Dict]) -> None:
    """Render wastage by product horizontal bar chart."""
    if not data:
        return

    fig = go.Figure(go.Bar(
        x=[d.get('wastage', 0) for d in data],
        y=[d.get('product', '') for d in data],
        orientation='h',
        marker_color='#e94560'
    ))

    fig.update_layout(
        title=dict(text='Wastage by Product', font=dict(color='#1e293b', size=16)),
        paper_bgcolor='transparent',
        plot_bgcolor='#ffffff',
        font=dict(color='#475569'),
        xaxis=dict(showgrid=True, gridcolor='#e2e8f0', color='#64748b'),
        yaxis=dict(showgrid=False, color='#64748b'),
        margin=dict(l=100, r=20, t=40, b=20),
        height=300
    )

    st.plotly_chart(fig, use_container_width=True)


def render_delivery_performance_chart(data: List[Dict]) -> None:
    """Render delivery performance pie chart."""
    if not data:
        return

    labels = [d.get('status', '') for d in data]
    values = [d.get('count', 0) for d in data]
    colors = ['#00c896', '#e94560']

    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.4,
        marker=dict(colors=colors[:len(data)])
    )])

    fig.update_layout(
        title=dict(text='Delivery Performance', font=dict(color='#1e293b', size=16)),
        paper_bgcolor='transparent',
        font=dict(color='#475569'),
        margin=dict(l=20, r=20, t=40, b=20),
        height=250
    )

    st.plotly_chart(fig, use_container_width=True)


def render_spend_by_supplier_chart(data: List[Dict]) -> None:
    """Render spend by supplier horizontal bar chart."""
    if not data:
        return

    fig = go.Figure(go.Bar(
        x=[d.get('spend', 0) for d in data],
        y=[d.get('supplier', '') for d in data],
        orientation='h',
        marker_color='#45b7d1'
    ))

    fig.update_layout(
        title=dict(text='Spend by Supplier', font=dict(color='#1e293b', size=16)),
        paper_bgcolor='transparent',
        plot_bgcolor='#ffffff',
        font=dict(color='#475569'),
        xaxis=dict(showgrid=True, gridcolor='#e2e8f0', color='#64748b'),
        yaxis=dict(showgrid=False, color='#64748b'),
        margin=dict(l=100, r=20, t=40, b=20),
        height=300
    )

    st.plotly_chart(fig, use_container_width=True)


def render_lead_time_trend_chart(data: List[Dict]) -> None:
    """Render lead time trend line chart."""
    if not data:
        return

    fig = go.Figure()

    periods = [d.get('period', '') for d in data]
    lead_times = [d.get('lead_time', 0) for d in data]

    fig.add_trace(go.Scatter(
        x=periods,
        y=lead_times,
        mode='lines+markers',
        name='Lead Time (days)',
        line=dict(color='#ffa500', width=3)
    ))

    fig.update_layout(
        title=dict(text='Lead Time Trend', font=dict(color='#1e293b', size=16)),
        paper_bgcolor='transparent',
        plot_bgcolor='#ffffff',
        font=dict(color='#475569'),
        xaxis=dict(showgrid=False, color='#64748b'),
        yaxis=dict(showgrid=True, gridcolor='#e2e8f0', color='#64748b'),
        margin=dict(l=20, r=20, t=40, b=20),
        height=250
    )

    st.plotly_chart(fig, use_container_width=True)
