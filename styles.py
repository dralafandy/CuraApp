# styles.py
import streamlit as st

def load_custom_css(theme="blue"):
    """تحميل الأنماط المخصصة حسب الثيم"""
    
    themes = {
        "light": "#ffffff",
        "dark": "#1a202c",
        "blue": "#1e40af",
        "green": "#059669",
        "red": "#dc2626"
    }
    
    primary_color = themes.get(theme, "#1e40af")
    secondary_color = "#f3f4f6" if theme == "light" else "#374151"
    
    css = f"""
    <style>
    /* خلفية الصفحة */
    .main {{
        background: {secondary_color};
        padding: 1rem;
        border-radius: 12px;
    }}
    
    /* العناوين */
    h1, h2, h3 {{
        color: {primary_color};
        font-family: 'Cairo', sans-serif;
        font-weight: 700;
        margin-bottom: 1rem;
    }}
    
    /* الأزرار */
    .stButton>button {{
        background: {primary_color};
        color: white;
        border-radius: 12px;
        border: none;
        padding: 0.8rem 1.5rem;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }}
    
    .stButton>button:hover {{
        background: {primary_color}cc;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.3);
    }}
    
    /* البطاقات */
    .main-header {{
        background: {primary_color}10;
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        transition: transform 0.3s ease;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }}
    
    .main-header:hover {{
        transform: translateY(-4px);
    }}
    
    .main-header h1 {{
        font-size: 2rem;
        margin: 0;
    }}
    
    .main-header p {{
        color: #4b5563;
        font-size: 1rem;
        margin: 0.5rem 0 0 0;
    }}
    
    /* الجداول */
    [data-testid="stDataFrame"] {{
        border: none;
        border-radius: 12px;
        background: {secondary_color};
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }}
    
    /* المدخلات */
    .stTextInput>div>div>input,
    .stSelectbox>div>div>select,
    .stTextArea>div>div>textarea {{
        border-radius: 10px;
        border: 1px solid {primary_color}40;
        background: {secondary_color};
        padding: 0.8rem;
        transition: border-color 0.3s ease;
    }}
    
    .stTextInput>div>div>input:focus,
    .stSelectbox>div>div>select:focus,
    .stTextArea>div>div>textarea:focus {{
        border-color: {primary_color};
        box-shadow: 0 0 8px {primary_color}40;
    }}
    
    /* المقاييس */
    [data-testid="stMetricValue"] {{
        color: {primary_color};
        font-size: 1.6rem;
        font-weight: 600;
    }}
    
    /* التنبيهات */
    .stAlert {{
        border-radius: 10px;
        background: {primary_color}10;
        border: 1px solid {primary_color}30;
        padding: 1rem;
    }}
    
    /* التبويبات */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 12px;
        background: {secondary_color};
        padding: 0.5rem;
        border-radius: 12px;
    }}
    
    .stTabs [data-baseweb="tab"] {{
        border-radius: 10px;
        padding: 0.8rem 1.5rem;
        transition: all 0.3s ease;
    }}
    
    .stTabs [aria-selected="true"] {{
        background: {primary_color};
        color: white;
    }}
    
    /* الخطوط العربية */
    * {{
        font-family: 'Cairo', sans-serif;
    }}
    
    /* تأثيرات عامة */
    .stMarkdown, .stContainer {{
        transition: all 0.3s ease;
    }}
    </style>
    """
    
    st.markdown(css, unsafe_allow_html=True)
