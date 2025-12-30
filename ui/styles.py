"""
Custom CSS styling for the ERP Intelligence Agent UI - Clean Professional Theme.
"""

STYLES = """
<style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    /* Base font and colors */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
    }

    /* Main app background */
    .stApp {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 50%, #f1f5f9 100%);
    }

    /* Main container */
    .main-container {
        padding: 1rem;
        min-height: 100vh;
    }

    /* Headers with proper contrast */
    h1 {
        color: #1e293b !important;
        font-weight: 700 !important;
        font-size: 2rem !important;
        margin-bottom: 1rem !important;
    }

    h2 {
        color: #334155 !important;
        font-weight: 600 !important;
        font-size: 1.5rem !important;
        margin-bottom: 0.75rem !important;
    }

    h3 {
        color: #475569 !important;
        font-weight: 600 !important;
        font-size: 1.25rem !important;
        margin-bottom: 0.5rem !important;
    }

    h4 {
        color: #64748b !important;
        font-weight: 500 !important;
    }

    /* Paragraph and body text - dark for readability */
    p, div, span {
        color: #334155 !important;
    }

    /* Caption text */
    .stCaption, .caption, p.caption {
        color: #64748b !important;
        font-size: 0.875rem !important;
    }

    /* Label text */
    label, .stLabel {
        color: #475569 !important;
        font-weight: 500 !important;
    }

    /* 3D Button Styles with proper contrast */
    .stButton > button {
        background: linear-gradient(180deg, #6366f1 0%, #4f46e5 50%, #4338ca 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        box-shadow:
            0 4px 6px -1px rgba(99, 102, 241, 0.3),
            0 2px 4px -2px rgba(99, 102, 241, 0.2),
            inset 0 1px 0 rgba(255, 255, 255, 0.1) !important;
        transition: all 0.2s ease !important;
    }

    .stButton > button:hover {
        background: linear-gradient(180deg, #818cf8 0%, #6366f1 50%, #4f46e5 100%) !important;
        box-shadow:
            0 8px 16px -4px rgba(99, 102, 241, 0.4),
            0 4px 8px -4px rgba(99, 102, 241, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
        transform: translateY(-2px) !important;
    }

    .stButton > button:active {
        background: linear-gradient(180deg, #4f46e5 0%, #4338ca 50%, #3730a3 100%) !important;
        box-shadow:
            0 2px 4px -1px rgba(99, 102, 241, 0.3),
            inset 0 2px 4px rgba(0, 0, 0, 0.2) !important;
        transform: translateY(1px) !important;
    }

    /* Primary 3D Green Button */
    .primary-3d > button {
        background: linear-gradient(180deg, #10b981 0%, #059669 50%, #047857 100%) !important;
        color: #ffffff !important;
        box-shadow:
            0 6px 0 #065f46,
            0 8px 12px -4px rgba(16, 185, 129, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.15) !important;
        border-radius: 16px !important;
    }

    .primary-3d > button:hover {
        background: linear-gradient(180deg, #34d399 0%, #10b981 50%, #059669 100%) !important;
        transform: translateY(-2px);
        box-shadow:
            0 8px 0 #065f46,
            0 12px 16px -4px rgba(16, 185, 129, 0.5),
            inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
    }

    .primary-3d > button:active {
        transform: translateY(4px);
        box-shadow:
            0 2px 0 #065f46,
            0 4px 8px -4px rgba(16, 185, 129, 0.3),
            inset 0 2px 4px rgba(0, 0, 0, 0.2) !important;
    }

    /* Secondary 3D Purple Button */
    .secondary-3d > button {
        background: linear-gradient(180deg, #8b5cf6 0%, #7c3aed 50%, #6d28d9 100%) !important;
        color: #ffffff !important;
        box-shadow:
            0 6px 0 #5b21b6,
            0 8px 12px -4px rgba(139, 92, 246, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.15) !important;
        border-radius: 16px !important;
    }

    .secondary-3d > button:hover {
        background: linear-gradient(180deg, #a78bfa 0%, #8b5cf6 50%, #7c3aed 100%) !important;
        transform: translateY(-2px);
        box-shadow:
            0 8px 0 #5b21b6,
            0 12px 16px -4px rgba(139, 92, 246, 0.5),
            inset 0 1px 0 rgba(255, 255, 255, 0.2) !important;
    }

    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
        border-right: 1px solid #334155;
    }

    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #f1f5f9 !important;
    }

    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] div,
    [data-testid="stSidebar"] span {
        color: #e2e8f0 !important;
    }

    [data-testid="stSidebar"] .stRadio label {
        color: #e2e8f0 !important;
    }

    /* Sidebar radio buttons */
    [data-testid="stSidebar"] [data-testid="stRadio"] label {
        color: #e2e8f0 !important;
    }

    /* Sidebar success/warning/info boxes */
    [data-testid="stSidebar"] .stSuccess,
    [data-testid="stSidebar"] .stWarning,
    [data-testid="stSidebar"] .stInfo {
        color: #1e293b !important;
    }

    /* Card styling with proper contrast */
    .card-3d {
        background: linear-gradient(145deg, #ffffff 0%, #f8fafc 100%);
        border-radius: 20px;
        padding: 1.5rem;
        box-shadow:
            0 10px 40px -10px rgba(0, 0, 0, 0.15),
            0 2px 10px -2px rgba(0, 0, 0, 0.1),
            inset 0 1px 0 rgba(255, 255, 255, 1);
        border: 1px solid #e2e8f0;
    }

    .card-3d h1,
    .card-3d h2,
    .card-3d h3 {
        color: #1e293b !important;
    }

    .card-3d p,
    .card-3d div {
        color: #334155 !important;
    }

    /* Executive Summary - dark card for contrast */
    .executive-summary {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        padding: 2rem;
        border-radius: 20px;
        margin-bottom: 1.5rem;
        border-left: 6px solid #e94560;
        box-shadow:
            0 10px 30px -10px rgba(233, 69, 96, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.05);
    }

    .executive-summary h3 {
        color: #f1f5f9 !important;
        margin-bottom: 1rem;
    }

    .executive-summary li {
        color: #e2e8f0 !important;
        padding: 0.75rem 0;
        border-bottom: 1px solid rgba(255,255,255,0.1);
    }

    /* Insight cards */
    .insight-card {
        padding: 1.25rem;
        border-radius: 16px;
        margin-bottom: 1rem;
        border-left: 6px solid;
        background: #ffffff;
        box-shadow: 0 4px 15px -5px rgba(0, 0, 0, 0.1);
    }

    .insight-card p,
    .insight-card div {
        color: #334155 !important;
    }

    .insight-finding {
        color: #1e293b !important;
        font-weight: 600 !important;
    }

    .insight-impact {
        color: #64748b !important;
    }

    .insight-action {
        background: rgba(99, 102, 241, 0.1);
        padding: 0.75rem;
        border-radius: 12px;
        font-size: 0.85rem;
        color: #4f46e5 !important;
    }

    /* KPI Cards */
    .kpi-card {
        background: linear-gradient(145deg, #ffffff 0%, #f8fafc 100%);
        padding: 1.5rem;
        border-radius: 20px;
        text-align: center;
        border: 1px solid #e2e8f0;
        box-shadow:
            0 8px 32px -8px rgba(0, 0, 0, 0.1),
            inset 0 1px 0 rgba(255, 255, 255, 1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }

    .kpi-card:hover {
        transform: translateY(-4px);
        box-shadow:
            0 12px 40px -8px rgba(99, 102, 241, 0.15),
            inset 0 1px 0 rgba(255, 255, 255, 1);
    }

    .kpi-value {
        font-size: 2rem;
        font-weight: 700;
        color: #1e293b;
        text-shadow: none;
    }

    .kpi-label {
        color: #64748b !important;
        font-size: 0.9rem;
        margin-top: 0.5rem;
    }

    .kpi-change {
        font-size: 0.85rem;
        margin-top: 0.75rem;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        display: inline-block;
    }

    .kpi-positive {
        background: rgba(16, 185, 129, 0.15);
        color: #059669;
    }

    .kpi-negative {
        background: rgba(239, 68, 68, 0.15);
        color: #dc2626;
    }

    /* Risk Section */
    .risk-section {
        background: linear-gradient(145deg, #fef2f2 0%, #fee2e2 100%);
        border: 1px solid #fecaca;
        border-radius: 20px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow:
            0 8px 32px -8px rgba(239, 68, 68, 0.15),
            inset 0 1px 0 rgba(255, 255, 255, 1);
    }

    .risk-section p,
    .risk-section div {
        color: #334155 !important;
    }

    /* Action Plan */
    .action-plan {
        background: linear-gradient(145deg, #f0fdf4 0%, #dcfce7 100%);
        border: 1px solid #bbf7d0;
        border-radius: 20px;
        padding: 1.5rem;
        box-shadow:
            0 8px 32px -8px rgba(16, 185, 129, 0.15),
            inset 0 1px 0 rgba(255, 255, 255, 1);
    }

    .action-plan p,
    .action-plan div {
        color: #334155 !important;
    }

    .action-immediate {
        border-left: 6px solid #ef4444;
    }

    .action-short-term {
        border-left: 6px solid #f59e0b;
    }

    .action-medium-term {
        border-left: 6px solid #10b981;
    }

    /* Data Quality Warning */
    .data-quality-warning {
        background: linear-gradient(145deg, #fffbeb 0%, #fef3c7 100%);
        border: 1px solid #fcd34d;
        border-radius: 16px;
        padding: 1.25rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 15px -5px rgba(245, 158, 11, 0.2);
    }

    .data-quality-warning p,
    .data-quality-warning div {
        color: #334155 !important;
    }

    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        background: #f1f5f9;
        padding: 0.5rem;
        border-radius: 16px;
    }

    .stTabs [data-baseweb="tab"] {
        padding: 1rem 1.5rem;
        border-radius: 12px;
        background: transparent;
        border: none;
        color: #64748b !important;
        transition: all 0.2s ease;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(180deg, #6366f1 0%, #4f46e5 100%);
        color: #ffffff !important;
        box-shadow:
            0 4px 12px -4px rgba(99, 102, 241, 0.4),
            inset 0 1px 0 rgba(255, 255, 255, 0.1);
    }

    /* Metrics */
    [data-testid="stMetricValue"] {
        color: #1e293b !important;
        font-weight: 700 !important;
    }

    [data-testid="stMetricLabel"] {
        color: #64748b !important;
    }

    /* Charts container */
    .chart-container {
        background: linear-gradient(145deg, #ffffff 0%, #f8fafc 100%);
        border-radius: 20px;
        padding: 1.25rem;
        margin-bottom: 1rem;
        border: 1px solid #e2e8f0;
        box-shadow:
            0 8px 32px -8px rgba(0, 0, 0, 0.1),
            inset 0 1px 0 rgba(255, 255, 255, 1);
    }

    /* Priority badges */
    .priority-badge {
        display: inline-block;
        padding: 0.35rem 0.85rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
    }

    .priority-immediate {
        background: linear-gradient(180deg, #ef4444 0%, #dc2626 100%);
        color: #ffffff;
    }

    .priority-short-term {
        background: linear-gradient(180deg, #f59e0b 0%, #d97706 100%);
        color: #ffffff;
    }

    .priority-medium-term {
        background: linear-gradient(180deg, #10b981 0%, #059669 100%);
        color: #ffffff;
    }

    /* Info boxes */
    .info-box {
        padding: 1rem;
        border-radius: 16px;
        margin-bottom: 1rem;
        border: 1px solid;
    }

    .info-box-warning {
        background: linear-gradient(145deg, #fffbeb 0%, #fef3c7 100%);
        border-left: 6px solid #f59e0b;
    }

    .info-box-error {
        background: linear-gradient(145deg, #fef2f2 0%, #fee2e2 100%);
        border-left: 6px solid #ef4444;
    }

    .info-box-success {
        background: linear-gradient(145deg, #f0fdf4 0%, #dcfce7 100%);
        border-left: 6px solid #10b981;
    }

    /* Expander styling */
    .streamlit-expander {
        background: linear-gradient(145deg, #ffffff 0%, #f8fafc 100%);
        border-radius: 16px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 15px -5px rgba(0, 0, 0, 0.1);
    }

    /* Progress bar */
    .stProgress > div > div {
        background: linear-gradient(90deg, #6366f1 0%, #8b5cf6 100%);
        border-radius: 10px;
        box-shadow: 0 2px 8px -4px rgba(99, 102, 241, 0.4);
    }

    /* Selectbox dropdown */
    [data-testid="stSelectbox"] > div {
        background: #ffffff !important;
        border-radius: 12px !important;
        border: 1px solid #e2e8f0 !important;
    }

    /* Checkbox styling */
    .stCheckbox > label {
        color: #475569 !important;
    }

    /* Slider styling */
    .stSlider [data-baseweb="slider"] {
        background: #e2e8f0 !important;
    }

    /* DataFrame/Table styling */
    [data-testid="stDataFrame"] {
        background: #ffffff;
        border-radius: 16px;
        border: 1px solid #e2e8f0;
        overflow: hidden;
    }

    /* Spinner */
    .stSpinner {
        color: #6366f1;
    }

    /* Toast notifications */
    [data-testid="stToast"] {
        background: #ffffff;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        color: #334155 !important;
    }

    /* Divider */
    hr {
        border-color: #e2e8f0 !important;
    }

    /* File uploader */
    [data-testid="stFileUploader"] {
        background: linear-gradient(145deg, #f8fafc 0%, #f1f5f9 100%) !important;
        border: 3px dashed #cbd5e1 !important;
        border-radius: 20px !important;
        padding: 2rem !important;
        transition: all 0.3s ease !important;
    }

    [data-testid="stFileUploader"]:hover {
        border-color: #6366f1 !important;
        box-shadow:
            inset 0 2px 4px rgba(0, 0, 0, 0.05),
            0 0 20px rgba(99, 102, 241, 0.1) !important;
    }

    /* Success/Warning/Info messages */
    .stSuccess {
        background: linear-gradient(145deg, #f0fdf4 0%, #dcfce7 100%) !important;
        color: #166534 !important;
        border-radius: 12px !important;
        border: 1px solid #bbf7d0 !important;
    }

    .stWarning {
        background: linear-gradient(145deg, #fffbeb 0%, #fef3c7 100%) !important;
        color: #92400e !important;
        border-radius: 12px !important;
        border: 1px solid #fcd34d !important;
    }

    .stError {
        background: linear-gradient(145deg, #fef2f2 0%, #fee2e2 100%) !important;
        color: #991b1b !important;
        border-radius: 12px !important;
        border: 1px solid #fecaca !important;
    }

    .stInfo {
        background: linear-gradient(145deg, #eff6ff 0%, #dbeafe 100%) !important;
        color: #1e40af !important;
        border-radius: 12px !important;
        border: 1px solid #bfdbfe !important;
    }

    /* Number input */
    .stNumberInput input {
        background: #ffffff !important;
        color: #1e293b !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 12px !important;
    }

    /* Text input */
    .stTextInput input {
        background: #ffffff !important;
        color: #1e293b !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 12px !important;
    }

    /* Text area */
    .stTextArea textarea {
        background: #ffffff !important;
        color: #1e293b !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 12px !important;
    }

    /* Date input */
    .stDateInput input {
        background: #ffffff !important;
        color: #1e293b !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 12px !important;
    }

    /* Multiselect */
    .stMultiSelect [data-baseweb="select"] {
        background: #ffffff !important;
        border-radius: 12px !important;
        border: 1px solid #e2e8f0 !important;
    }
</style>
"""
