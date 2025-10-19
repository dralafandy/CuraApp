import streamlit as st

def load_custom_css(theme=“blue”):
“”“تحميل الأنماط المخصصة المتجاوبة حسب الثيم”””

```
themes = {
    "blue": {
        "primary": "#3b82f6",
        "secondary": "#60a5fa",
        "light": "#dbeafe",
        "dark": "#1e40af"
    },
    "green": {
        "primary": "#10b981",
        "secondary": "#34d399",
        "light": "#d1fae5",
        "dark": "#047857"
    },
    "orange": {
        "primary": "#f97316",
        "secondary": "#fb923c",
        "light": "#fed7aa",
        "dark": "#c2410c"
    },
    "pink": {
        "primary": "#ec4899",
        "secondary": "#f472b6",
        "light": "#fce7f3",
        "dark": "#be185d"
    },
    "purple": {
        "primary": "#8b5cf6",
        "secondary": "#a78bfa",
        "light": "#ede9fe",
        "dark": "#6d28d9"
    },
    "dark": {
        "primary": "#1f2937",
        "secondary": "#374151",
        "light": "#d1d5db",
        "dark": "#111827"
    },
}

colors = themes.get(theme, themes["blue"])

css = f"""
<style>
/* ==================== متغيرات الألوان ==================== */
:root {{
    --primary-color: {colors['primary']};
    --secondary-color: {colors['secondary']};
    --light-color: {colors['light']};
    --dark-color: {colors['dark']};
    --success: #10b981;
    --warning: #f59e0b;
    --error: #ef4444;
    --info: #3b82f6;
}}

/* ==================== الخطوط والأساسيات ==================== */
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700&display=swap');

* {{
    font-family: 'Cairo', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}}

html, body, [data-testid="stAppViewContainer"] {{
    scroll-behavior: smooth;
}}

/* ==================== الشريط الجانبي ==================== */
[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, {colors['primary']}08 0%, {colors['primary']}03 100%);
    border-right: 1px solid {colors['primary']}15;
}}

[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {{
    padding: 0.5rem;
}}

/* تحسين أزرار الشريط الجانبي */
[data-testid="stSidebar"] .stButton > button {{
    width: 100%;
    text-align: right;
    padding: 0.75rem 1rem;
    margin-bottom: 0.4rem;
    border-radius: 10px;
    border: 1px solid transparent;
    background: transparent;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    font-size: 0.95rem;
    font-weight: 500;
}}

[data-testid="stSidebar"] .stButton > button:hover {{
    background: {colors['primary']}15;
    border-color: {colors['primary']}30;
    transform: translateX(-3px);
    box-shadow: 0 2px 8px {colors['primary']}20;
}}

/* الزر النشط */
[data-testid="stSidebar"] .stButton > button[kind="primary"] {{
    background: linear-gradient(135deg, {colors['primary']}20, {colors['primary']}10);
    border-color: {colors['primary']};
    font-weight: 600;
    box-shadow: 0 2px 8px {colors['primary']}25;
}}

/* ==================== العناوين ==================== */
h1, h2, h3, h4, h5, h6 {{
    color: {colors['dark']};
    font-weight: 700;
    line-height: 1.3;
}}

h1 {{
    font-size: clamp(1.8rem, 4vw, 2.5rem);
    margin-bottom: 1rem;
    background: linear-gradient(135deg, {colors['primary']}, {colors['secondary']});
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}}

h2 {{
    font-size: clamp(1.5rem, 3vw, 2rem);
    color: {colors['primary']};
}}

h3 {{
    font-size: clamp(1.2rem, 2.5vw, 1.5rem);
    color: {colors['dark']};
}}

/* ==================== الأزرار العامة ==================== */
.stButton > button {{
    border-radius: 10px;
    padding: 0.65rem 1.5rem;
    font-weight: 600;
    border: 2px solid transparent;
    transition: all 0.3s ease;
    box-shadow: 0 2px 4px rgba(0,0,0,0.08);
    font-size: 0.95rem;
}}

.stButton > button:hover {{
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    border-color: {colors['primary']};
}}

.stButton > button:active {{
    transform: translateY(0);
}}

.stButton > button[kind="primary"] {{
    background: linear-gradient(135deg, {colors['primary']}, {colors['secondary']});
    color: white;
    border: none;
}}

.stButton > button[kind="secondary"] {{
    background: white;
    color: {colors['primary']};
    border-color: {colors['primary']}30;
}}

/* ==================== البطاقات والحاويات ==================== */
.main-header {{
    background: linear-gradient(135deg, {colors['light']}80 0%, {colors['light']}40 100%);
    padding: clamp(1.5rem, 3vw, 2.5rem);
    border-radius: 16px;
    margin-bottom: 2rem;
    box-shadow: 0 4px 6px rgba(0,0,0,0.07);
    border: 1px solid {colors['primary']}20;
}}

[data-testid="stExpander"] {{
    background: white;
    border-radius: 12px;
    border: 1px solid #e5e7eb;
    margin-bottom: 1rem;
    overflow: hidden;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}}

[data-testid="stExpander"]:hover {{
    box-shadow: 0 4px 6px rgba(0,0,0,0.08);
    border-color: {colors['primary']}30;
}}

/* ==================== الجداول ==================== */
[data-testid="stDataFrame"] {{
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    border: 1px solid #e5e7eb;
}}

[data-testid="stDataFrame"] table {{
    font-size: 0.9rem;
}}

[data-testid="stDataFrame"] thead tr {{
    background: linear-gradient(135deg, {colors['primary']}15, {colors['primary']}08);
}}

[data-testid="stDataFrame"] thead th {{
    color: {colors['dark']};
    font-weight: 700;
    padding: 1rem 0.75rem;
}}

[data-testid="stDataFrame"] tbody tr:hover {{
    background: {colors['light']}40;
}}

/* ==================== حقول الإدخال ==================== */
.stTextInput > div > div > input,
.stSelectbox > div > div > select,
.stTextArea > div > div > textarea,
.stNumberInput > div > div > input,
.stDateInput > div > div > input {{
    border-radius: 10px;
    border: 2px solid #e5e7eb;
    padding: 0.75rem 1rem;
    font-size: 0.95rem;
    transition: all 0.3s ease;
}}

.stTextInput > div > div > input:focus,
.stSelectbox > div > div > select:focus,
.stTextArea > div > div > textarea:focus,
.stNumberInput > div > div > input:focus,
.stDateInput > div > div > input:focus {{
    border-color: {colors['primary']};
    box-shadow: 0 0 0 3px {colors['primary']}15;
    outline: none;
}}

/* ==================== المقاييس (Metrics) ==================== */
[data-testid="stMetric"] {{
    background: linear-gradient(135deg, {colors['light']}40, white);
    padding: 1.5rem;
    border-radius: 12px;
    border: 1px solid {colors['primary']}20;
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    transition: all 0.3s ease;
}}

[data-testid="stMetric"]:hover {{
    transform: translateY(-3px);
    box-shadow: 0 6px 16px rgba(0,0,0,0.1);
}}

[data-testid="stMetricValue"] {{
    color: {colors['primary']};
    font-size: clamp(1.5rem, 3vw, 2.2rem);
    font-weight: 800;
}}

[data-testid="stMetricLabel"] {{
    color: #6b7280;
    font-weight: 600;
    font-size: 0.9rem;
}}

/* ==================== التنبيهات ==================== */
.stAlert {{
    border-radius: 12px;
    padding: 1rem 1.25rem;
    border-left: 4px solid;
    box-shadow: 0 2px 4px rgba(0,0,0,0.08);
}}

[data-baseweb="notification"] {{
    border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}}

/* ==================== التبويبات (Tabs) ==================== */
.stTabs [data-baseweb="tab-list"] {{
    gap: 0.5rem;
    background: {colors['light']}30;
    padding: 0.5rem;
    border-radius: 12px;
}}

.stTabs [data-baseweb="tab"] {{
    border-radius: 8px;
    padding: 0.75rem 1.5rem;
    font-weight: 600;
    transition: all 0.3s ease;
    border: 2px solid transparent;
}}

.stTabs [data-baseweb="tab"]:hover {{
    background: white;
    border-color: {colors['primary']}30;
}}

.stTabs [aria-selected="true"] {{
    background: linear-gradient(135deg, {colors['primary']}, {colors['secondary']});
    color: white !important;
    box-shadow: 0 2px 8px {colors['primary']}40;
}}

/* ==================== التمرير المخصص ==================== */
::-webkit-scrollbar {{
    width: 8px;
    height: 8px;
}}

::-webkit-scrollbar-track {{
    background: #f1f5f9;
    border-radius: 10px;
}}

::-webkit-scrollbar-thumb {{
    background: {colors['primary']}60;
    border-radius: 10px;
}}

::-webkit-scrollbar-thumb:hover {{
    background: {colors['primary']};
}}

/* ==================== الرسوم البيانية ==================== */
[data-testid="stPlotlyChart"] {{
    border-radius: 12px;
    overflow: hidden;
    box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}}

/* ==================== الاستجابة للموبايل ==================== */
@media (max-width: 768px) {{
    /* تصغير الحشو */
    .main-header {{
        padding: 1.5rem 1rem;
        margin-bottom: 1rem;
    }}
    
    /* تحسين الأزرار للموبايل */
    .stButton > button {{
        padding: 0.7rem 1rem;
        font-size: 0.9rem;
        width: 100%;
    }}
    
    /* تحسين الجداول */
    [data-testid="stDataFrame"] {{
        font-size: 0.85rem;
    }}
    
    /* تحسين المقاييس */
    [data-testid="stMetric"] {{
        padding: 1rem;
    }}
    
    [data-testid="stMetricValue"] {{
        font-size: 1.5rem;
    }}
    
    /* تحسين الأعمدة */
    [data-testid="column"] {{
        padding: 0.5rem 0.25rem;
    }}
    
    /* إخفاء الشريط الجانبي تلقائياً */
    [data-testid="stSidebar"][aria-expanded="true"] {{
        width: 280px;
    }}
    
    /* تحسين حقول الإدخال */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > select {{
        font-size: 16px; /* منع التكبير التلقائي في iOS */
    }}
}}

@media (max-width: 480px) {{
    h1 {{
        font-size: 1.5rem;
    }}
    
    h2 {{
        font-size: 1.3rem;
    }}
    
    h3 {{
        font-size: 1.1rem;
    }}
    
    [data-testid="stMetric"] {{
        padding: 0.75rem;
    }}
    
    .stTabs [data-baseweb="tab"] {{
        padding: 0.6rem 1rem;
        font-size: 0.85rem;
    }}
}}

/* ==================== تحسينات إضافية ==================== */
/* إخفاء علامة streamlit */
#MainMenu {{visibility: hidden;}}
footer {{visibility: hidden;}}

/* تحسين الرسوم المتحركة */
* {{
    -webkit-tap-highlight-color: transparent;
}}

/* تحسين التباعد */
.block-container {{
    padding-top: 2rem;
    padding-bottom: 2rem;
    padding-left: clamp(1rem, 3vw, 3rem);
    padding-right: clamp(1rem, 3vw, 3rem);
}}

/* تحسين الظلال */
.element-container {{
    transition: all 0.3s ease;
}}

/* Badge للأرقام */
.badge {{
    display: inline-block;
    padding: 0.25rem 0.6rem;
    font-size: 0.75rem;
    font-weight: 700;
    border-radius: 12px;
    background: {colors['primary']};
    color: white;
}}
</style>
"""

st.markdown(css, unsafe_allow_html=True)
```
