def get_custom_css():
    """Return custom CSS for styling the Streamlit app"""
    return """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@600;700&family=Roboto:wght@400;500&display=swap');
    
    /* Tailwind-inspired utility classes */
    .flex { display: flex; }
    .flex-col { flex-direction: column; }
    .flex-row { flex-direction: row; }
    .items-center { align-items: center; }
    .justify-center { justify-content: center; }
    .justify-between { justify-content: space-between; }
    .gap-4 { gap: 1rem; }
    .p-4 { padding: 1rem; }
    .px-6 { padding-left: 1.5rem; padding-right: 1.5rem; }
    .py-3 { padding-top: 0.75rem; padding-bottom: 0.75rem; }
    .rounded-lg { border-radius: 0.5rem; }
    .shadow-lg { box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1); }
    
    /* Global Styles */
    [data-testid="stAppViewContainer"] {
        background-color: #ffffff;
        font-family: 'Roboto', sans-serif;
    }

    [data-testid="stHeader"] {
        background-color: rgba(255,0,0,0);
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #A7F3D0 0%, #6EE7B7 100%);
        font-family: 'Roboto', sans-serif;
    }

    [data-testid="stSidebarContent"] {
        background: transparent;
    }

    /* Typography */
    h1, h2, h3 {
        font-family: 'Poppins', sans-serif;
        color: #374151;
    }

    h1 {
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 1rem;
    }

    h2 {
        font-size: 26px;
        font-weight: 600;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }

    h3 {
        color: #374151;
        font-size: 20px;
        margin-top: 1.5rem;
    }

    p, div, label, span {
        font-family: 'Roboto', sans-serif;
        font-size: 16px;
        color: #000000;
    }

    /* Button Styles */
    button, .stButton > button {
        font-family: 'Roboto', sans-serif;
        font-size: 14px;
        font-weight: 500;
        transition: all 0.3s ease;
    }

    /* Navigation Buttons */
    div[data-testid="column"] button[kind="secondary"] {
        background-color: #ffffff !important;
        color: #6B7280 !important;
        border: 2px solid #D1D5DB !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
    }

    div[data-testid="column"] button[kind="secondary"]:hover {
        background-color: #F3F4F6 !important;
        border-color: #A7F3D0 !important;
        transform: translateY(-2px);
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }

    div[data-testid="column"] button[kind="primary"],
    div[data-testid="column"] button[kind="primary"]:hover,
    div[data-testid="column"] button[kind="primary"]:focus,
    div[data-testid="column"] button[kind="primary"]:active,
    button[data-testid*="baseButton-primary"],
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #A7F3D0 0%, #6EE7B7 100%) !important;
        background-color: #A7F3D0 !important;
        color: #374151 !important;
        border: 2px solid #A7F3D0 !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 8px rgba(167, 243, 208, 0.4) !important;
    }

    div[data-testid="column"] button:active {
        transform: translateY(0) !important;
    }

    /* Cards */
    .metric-card {
        background: linear-gradient(135deg, #F0FDF4 0%, #DCFCE7 100%);
        border: 2px solid #A7F3D0;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease;
    }

    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 15px rgba(0, 0, 0, 0.15);
    }

    /* Tables */
    [data-testid="stDataFrame"] {
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }

    /* Info/Warning boxes */
    .stAlert {
        border-radius: 8px;
        border-left: 4px solid #A7F3D0;
    }

    /* File uploader */
    [data-testid="stFileUploadDropzone"] {
        border: 2px dashed #A7F3D0;
        border-radius: 12px;
        background: #F0FDF4;
        transition: all 0.3s ease;
    }

    [data-testid="stFileUploadDropzone"]:hover {
        border-color: #6EE7B7;
        background: #DCFCE7;
    }

    /* Selectbox */
    .stSelectbox > div > div {
        border-radius: 8px;
        border-color: #D1D5DB;
    }

    .stSelectbox > div > div:focus-within {
        border-color: #A7F3D0;
        box-shadow: 0 0 0 1px #A7F3D0;
    }

    /* Slider */
    .stSlider > div > div > div {
        background: linear-gradient(90deg, #A7F3D0 0%, #6EE7B7 100%);
    }

    /* Divider */
    hr {
        margin: 2rem 0;
        border: none;
        border-top: 2px solid #E5E7EB;
    }

    /* Custom classes for metrics display */
    .metric-row {
        display: flex;
        gap: 1rem;
        flex-wrap: wrap;
        margin: 1.5rem 0;
    }

    .metric-item {
        flex: 1;
        min-width: 200px;
        background: white;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #E5E7EB;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }

    .metric-label {
        font-size: 14px;
        color: #6B7280;
        font-weight: 500;
        margin-bottom: 0.5rem;
    }

    .metric-value {
        font-size: 24px;
        color: #374151;
        font-weight: 700;
        font-family: 'Poppins', sans-serif;
    }

    /* Animation */
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    .fade-in {
        animation: fadeIn 0.5s ease-out;
    }
    </style>
    """