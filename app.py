"""
ERP Intelligence Agent - Main Streamlit Application

A Senior ERP Financial & Operations Intelligence Agent that analyzes
business reports and produces brutally honest, actionable recommendations.
"""
import streamlit as st

# Page configuration
st.set_page_config(
    page_title="ERP Intelligence Agent",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom styles
from ui.styles import STYLES
st.markdown(STYLES, unsafe_allow_html=True)

# Session state initialization
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'upload'
if 'uploaded_data' not in st.session_state:
    st.session_state.uploaded_data = None
if 'analysis_results' not in st.session_state:
    st.session_state.analysis_results = None
if 'analysis_config' not in st.session_state:
    st.session_state.analysis_config = None


def main() -> None:
    """Main application entry point."""

    # Sidebar navigation
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 1rem 0;">
            <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">📊</div>
            <h1 style="font-size: 1.3rem; margin: 0; color: #f1f5f9 !important;">ERP Intelligence Agent</h1>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("---")

        # Navigation with styled radio
        page = st.radio(
            "Go to",
            ["📁 Upload Data", "⚙️ Configure Analysis", "📈 View Results"],
            index=["upload", "analysis", "results"].index(st.session_state.current_page),
            label_visibility="collapsed"
        )

        page_map = {
            "📁 Upload Data": "upload",
            "⚙️ Configure Analysis": "analysis",
            "📈 View Results": "results"
        }
        st.session_state.current_page = page_map[page]

        st.markdown("---")
        st.markdown("### Data Status")
        col1, col2 = st.columns(2)
        with col1:
            if st.session_state.uploaded_data:
                st.success("Data loaded")
            else:
                st.warning("No data")
        with col2:
            if st.session_state.analysis_results:
                st.success("Analyzed")
            else:
                st.info("Pending")

        st.markdown("---")
        st.markdown("""
        **About**

        Analyzes ERP data across 5 domains:
        - **Financial** (P&L, Revenue)
        - **Manufacturing** (Production)
        - **Inventory** (Stock)
        - **Sales** (Orders)
        - **Purchase** (Suppliers)

        Every insight includes specific numbers and exact actions.
        """)

    # Main content area
    if st.session_state.current_page == 'upload':
        from ui.pages.upload_page import render_upload_page
        render_upload_page()

    elif st.session_state.current_page == 'analysis':
        from ui.pages.analysis_page import render_analysis_page
        render_analysis_page()

    elif st.session_state.current_page == 'results':
        from ui.pages.results_page import render_results_page
        render_results_page()


if __name__ == "__main__":
    main()
