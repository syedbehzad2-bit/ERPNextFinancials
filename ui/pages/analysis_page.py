"""
Analysis configuration page - supports single and multi-file analysis.
"""
import streamlit as st

from agent_modules.orchestrator import ERPAgentOrchestrator


def render_analysis_page() -> None:
    """Render the analysis configuration page."""
    st.header("Configure Analysis")

    # Check for uploaded files
    if 'uploaded_files' not in st.session_state or not st.session_state.uploaded_files:
        st.warning("Please upload data files first")
        if st.button("Go to Upload"):
            st.session_state.current_page = 'upload'
            st.rerun()
        return

    uploaded_files = st.session_state.uploaded_files
    is_multi_file = len(uploaded_files) > 1

    # File summary
    st.info(f"📊 **{len(uploaded_files)} file(s) loaded for analysis**")

    # Show file types
    file_types = {}
    for f in uploaded_files:
        dtype = f['data_type'].value.title() if f['data_type'] else 'Unknown'
        file_types[dtype] = file_types.get(dtype, 0) + 1

    type_icons = {
        'Financial': '📊',
        'Manufacturing': '🏭',
        'Inventory': '📦',
        'Sales': '💰',
        'Purchase': '🛒'
    }

    type_col1, type_col2, type_col3, type_col4, type_col5 = st.columns(5)
    type_cols = [type_col1, type_col2, type_col3, type_col4, type_col5]

    for idx, (dtype, count) in enumerate(file_types.items()):
        with type_cols[idx]:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-value">{count}</div>
                <div class="kpi-label">{type_icons.get(dtype, '📄')} {dtype}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    if is_multi_file:
        # Multi-file analysis options
        st.subheader("📋 Cross-File Analysis Configuration")

        col_select1, col_select2 = st.columns(2)

        with col_select1:
            st.markdown("**Select Files to Analyze**")
            selected_files = []
            for idx, f in enumerate(uploaded_files):
                dtype = f['data_type'].value.title() if f['data_type'] else 'Unknown'
                icon = type_icons.get(dtype, '📄')
                if st.checkbox(f"{icon} {f['file_name']} ({dtype})", value=True, key=f"select_file_{idx}"):
                    selected_files.append(f)

        with col_select2:
            st.markdown("**Cross-Domain Insights**")
            enable_cross_domain = st.checkbox(
                "Enable cross-domain analysis",
                value=True,
                help="Analyze relationships between different data types (e.g., how inventory affects sales)"
            )

            if enable_cross_domain:
                st.caption("The AI will analyze:")
                st.caption("• Financial ↔ Sales correlations")
                st.caption("• Inventory ↔ Sales patterns")
                st.caption("• Manufacturing ↔ Inventory supply")
                st.caption("• Purchase ↔ Inventory replenishment")

    else:
        # Single file analysis - use original UI
        selected_files = uploaded_files
        enable_cross_domain = False

        data_info = uploaded_files[0]
        st.markdown(f"**Analyzing: {data_info['file_name']}** ({data_info['data_type'].value.title()})")

        st.subheader("Select Analysis Types")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Financial Analysis**")
            fin_pl = st.checkbox("P&L Analysis", value=True)
            fin_revenue = st.checkbox("Revenue Analysis", value=True)
            fin_expense = st.checkbox("Expense Analysis", value=True)
            fin_margin = st.checkbox("Margin Analysis", value=True)

            st.markdown("**Manufacturing Analysis**")
            mfg_production = st.checkbox("Production Analysis", value=True)
            mfg_wastage = st.checkbox("Wastage Analysis", value=True)
            mfg_cost = st.checkbox("Cost per Unit Analysis", value=True)

        with col2:
            st.markdown("**Inventory Analysis**")
            inv_aging = st.checkbox("Stock Aging", value=True)
            inv_dead = st.checkbox("Dead Stock", value=True)
            inv_over = st.checkbox("Overstock", value=True)
            inv_turn = st.checkbox("Inventory Turnover", value=True)

            st.markdown("**Sales Analysis**")
            sales_trend = st.checkbox("Sales Trends (MoM/QoQ)", value=True)
            sales_product = st.checkbox("Product Performance", value=True)
            sales_customer = st.checkbox("Customer Concentration", value=True)

        st.markdown("---")

        # Analysis methods
        st.subheader("Analysis Methods")

        c1, c2, c3 = st.columns(3)
        with c1:
            method_trend = st.checkbox("Trend Analysis (MoM/QoQ)", value=True)
            method_ratio = st.checkbox("Ratio Analysis", value=True)
        with c2:
            method_variance = st.checkbox("Variance Analysis", value=True)
            method_cost = st.checkbox("Cost Breakdown", value=True)
        with c3:
            method_pareto = st.checkbox("Pareto Analysis (80/20)", value=True)

    st.markdown("---")

    # Analysis level
    st.subheader("🎯 Analysis Depth")
    analysis_level = st.select_slider(
        "Select detail level",
        options=["Summary", "Detailed", "Comprehensive"],
        value="Comprehensive",
        help="Summary = KPIs only, Detailed = Full analysis, Comprehensive = AI insights + recommendations"
    )

    st.markdown("")

    # Run button
    col_run1, col_run2, col_run3 = st.columns([1, 2, 1])
    with col_run2:
        if st.button("🚀 Run Multi-File Analysis", type="primary", use_container_width=True):
            if not selected_files:
                st.error("Please select at least one file")
            else:
                with st.spinner("Running comprehensive analysis... This may take a moment."):
                    try:
                        orchestrator = ERPAgentOrchestrator()

                        # Prepare data for multi-file analysis
                        if is_multi_file and enable_cross_domain:
                            # Multi-file analysis
                            dfs = {f['data_type'].value: f['df'] for f in selected_files}
                            results = orchestrator.analyze_multi_file(
                                data_frames=dfs,
                                analysis_level=analysis_level
                            )
                        else:
                            # Single file analysis
                            f = selected_files[0]
                            results = orchestrator.analyze(
                                data_frame=f['df'],
                                data_type=f['data_type']
                            )

                        st.session_state.analysis_results = results
                        st.session_state.analysis_config = {
                            'files': [{'file_name': f['file_name'], 'data_type': f['data_type'].value}
                                     for f in selected_files],
                            'is_multi_file': is_multi_file,
                            'enable_cross_domain': enable_cross_domain,
                            'analysis_level': analysis_level
                        }

                        st.success("Analysis complete!")
                        st.session_state.current_page = 'results'
                        st.rerun()

                    except Exception as e:
                        import traceback
                        st.error(f"Analysis failed: {str(e)}")
                        if st.expander("Show error details"):
                            st.code(traceback.format_exc())
