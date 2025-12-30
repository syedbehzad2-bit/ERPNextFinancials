"""
Upload page - Multiple file upload and data validation.
"""
import streamlit as st
import pandas as pd
import os

from data_loader.loader import DataLoader


def render_upload_page() -> None:
    """Render the data upload page with multiple file support."""
    st.header("Upload ERP Data")

    st.markdown("""
    Upload your ERP data files for comprehensive multi-domain analysis.
    Upload multiple files (Financial, Manufacturing, Inventory, Sales, Purchase) for AI-powered
    cross-domain insights and recommendations.

    **Supported Formats:** CSV, Excel (.xlsx, .xls)
    """)

    # Initialize session state for uploaded files if not exists
    if 'uploaded_files' not in st.session_state:
        st.session_state.uploaded_files = []

    # Templates section
    with st.expander("📥 Download Templates", expanded=False):
        st.markdown("""
        **Don't have data ready?** Download template files, fill them with your data, and upload for analysis.
        Each template contains the required columns for accurate AI analysis.
        """)

        templates = {
            "Financial Template": ("templates/template_financial.xlsx", "📊 P&L, Revenue, Budget vs Actual"),
            "Manufacturing Template": ("templates/template_manufacturing.xlsx", "🏭 Production, Wastage, Efficiency"),
            "Inventory Template": ("templates/template_inventory.xlsx", "📦 Stock Levels, Aging, Costs"),
            "Sales Template": ("templates/template_sales.xlsx", "💰 Orders, Customers, Discounts"),
            "Purchase Template": ("templates/template_purchase.xlsx", "🛒 POs, Suppliers, Deliveries"),
        }

        template_cols = st.columns(3)
        for idx, (name, (file_path, desc)) in enumerate(templates.items()):
            col = template_cols[idx % 3]
            with col:
                st.markdown(f"**{name}**")
                st.caption(desc)
                full_path = os.path.join(os.path.dirname(__file__), "..", "..", file_path)
                try:
                    with open(full_path, "rb") as f:
                        st.download_button(
                            label="Download",
                            data=f,
                            file_name=os.path.basename(file_path),
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            key=f"template_{idx}"
                        )
                except FileNotFoundError:
                    st.error("Template not found")

    st.markdown("---")

    # Sample data section
    with st.expander("🧪 Sample Data (for Testing)", expanded=False):
        st.markdown("**Test the application** with pre-generated sample ERP data files.")

        sample_files = [
            ("sample_data/sample_financial.csv", "Financial Sample (CSV)"),
            ("sample_data/sample_financial.xlsx", "Financial Sample (Excel)"),
            ("sample_data/sample_manufacturing.csv", "Manufacturing Sample (CSV)"),
            ("sample_data/sample_inventory.xlsx", "Inventory Sample (Excel)"),
            ("sample_data/sample_sales.csv", "Sales Sample (CSV)"),
            ("sample_data/sample_purchase.xlsx", "Purchase Sample (Excel)"),
        ]

        sample_cols = st.columns(2)
        for idx, (file_path, name) in enumerate(sample_files):
            col = sample_cols[idx % 2]
            with col:
                mime = "text/csv" if file_path.endswith('.csv') else "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                full_path = os.path.join(os.path.dirname(__file__), "..", "..", file_path)
                try:
                    with open(full_path, "rb") as f:
                        st.download_button(
                            label=name,
                            data=f,
                            file_name=os.path.basename(file_path),
                            mime=mime,
                            key=f"sample_{idx}"
                        )
                except FileNotFoundError:
                    st.warning(f"File not found")

    st.markdown("---")

    # File upload section with 3D effect
    st.subheader("📁 Upload Data Files")

    uploaded_files = st.file_uploader(
        "Drag and drop your ERP data files here",
        type=['csv', 'xlsx', 'xls'],
        accept_multiple_files=True,
        help="Upload multiple files for comprehensive cross-domain analysis"
    )

    if uploaded_files:
        # Process new files
        for uploaded_file in uploaded_files:
            # Check if file is already uploaded
            existing_names = [f.get('file_name') for f in st.session_state.uploaded_files]
            if uploaded_file.name not in existing_names:
                with st.spinner(f"Loading {uploaded_file.name}..."):
                    loader = DataLoader()
                    try:
                        df = loader.load_file(file_obj=uploaded_file, file_name=uploaded_file.name)
                        st.session_state.uploaded_files.append({
                            'df': df,
                            'data_type': loader.data_type,
                            'quality_report': loader.quality_report,
                            'file_name': uploaded_file.name,
                            'loader': loader
                        })
                        st.success(f"✓ {uploaded_file.name} loaded successfully")
                    except Exception as e:
                        st.error(f"Error loading {uploaded_file.name}: {str(e)}")

    # Display uploaded files
    if st.session_state.uploaded_files:
        st.markdown("### 📋 Uploaded Files")

        # Summary cards
        summary_cols = st.columns(5)
        file_counts = {
            'Financial': 0,
            'Manufacturing': 0,
            'Inventory': 0,
            'Sales': 0,
            'Purchase': 0
        }

        for f in st.session_state.uploaded_files:
            dt = f['data_type'].value.title() if f['data_type'] else 'Unknown'
            file_counts[dt] = file_counts.get(dt, 0) + 1

        type_icons = {
            'Financial': '📊',
            'Manufacturing': '🏭',
            'Inventory': '📦',
            'Sales': '💰',
            'Purchase': '🛒'
        }

        for idx, (dtype, count) in enumerate(file_counts.items()):
            if idx < 5:
                with summary_cols[idx]:
                    st.markdown(f"""
                    <div class="kpi-card">
                        <div class="kpi-value">{count}</div>
                        <div class="kpi-label">{type_icons.get(dtype, '📄')} {dtype}</div>
                    </div>
                    """, unsafe_allow_html=True)

        st.markdown("")

        # File list with remove option
        for idx, file_info in enumerate(st.session_state.uploaded_files):
            col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 0.5])

            with col1:
                file_name = file_info['file_name']
                st.markdown(f"**{file_name}**")

            with col2:
                dtype = file_info['data_type'].value.title() if file_info['data_type'] else 'Unknown'
                st.caption(f"Type: {dtype}")

            with col3:
                rows = len(file_info['df'])
                st.caption(f"Rows: {rows:,}")

            with col4:
                cols = len(file_info['df'].columns)
                st.caption(f"Cols: {cols}")

            with col5:
                if st.button("✕", key=f"remove_{idx}", help="Remove file"):
                    st.session_state.uploaded_files.pop(idx)
                    st.rerun()

        st.markdown("---")

        # Analysis options
        st.subheader("⚙️ Analysis Configuration")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Cross-File Analysis**")
            enable_cross_analysis = st.checkbox(
                "Enable cross-domain insights",
                value=True,
                help="When enabled, AI will analyze relationships between different data types (e.g., how inventory affects sales)"
            )

        with col2:
            st.markdown("**Analysis Depth**")
            analysis_level = st.select_slider(
                "Detail Level",
                options=["Summary", "Detailed", "Comprehensive"],
                value="Detailed",
                help="Summary = Quick overview, Detailed = Full analysis, Comprehensive = AI with recommendations"
            )

        # Proceed button with 3D effect
        st.markdown("")
        if st.button("🚀 Run Multi-File Analysis", type="primary", use_container_width=True):
            # Store analysis config
            st.session_state.analysis_config = {
                'enable_cross_analysis': enable_cross_analysis,
                'analysis_level': analysis_level,
                'multiple_files': len(st.session_state.uploaded_files) > 1
            }
            st.session_state.current_page = 'analysis'
            st.rerun()

        # Clear all button
        if st.button("🗑️ Clear All Files", use_container_width=True):
            st.session_state.uploaded_files = []
            st.rerun()

    else:
        # Empty state - use light theme with dark text for readability
        st.markdown("""
        <div class="card-3d" style="text-align: center; padding: 3rem;">
            <div style="font-size: 4rem; margin-bottom: 1rem;">📁</div>
            <h3 style="color: #1e293b !important;">No Files Uploaded</h3>
            <p style="color: #64748b !important;">Upload your ERP data files above to get started with AI-powered analysis.</p>
            <p style="color: #6366f1 !important; margin-top: 1rem;">💡 Tip: Upload multiple files (Financial + Sales + Inventory) for comprehensive cross-domain insights!</p>
        </div>
        """, unsafe_allow_html=True)
