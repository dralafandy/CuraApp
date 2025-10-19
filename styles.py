import streamlit as st

def load_custom_css():
    """تطبيق الـ CSS اللازم لتثبيت الشريط السفلي وتنسيقات الأيقونات."""
    
    # CSS العام
    css_code = """
        <style>
        /* ======================================= */
        /* 1. إخفاء الشريط الجانبي الافتراضي */
        /* ======================================= */
        section[data-testid="stSidebar"] {
            display: none !important;
        }
        
        button[data-testid="baseButton-header"] {
            display: none !important;
        }

        /* ======================================= */
        /* 2. تنسيق شريط التنقل السفلي (الهواتف) */
        /* ======================================= */
        
        .mobile-nav-container {
            position: fixed; 
            bottom: 0;      
            left: 0;
            right: 0;
            z-index: 1000;  
            background-color: #ffffff;
            padding: 5px 0;
            border-top: 1px solid #e0e0e0;
            box-shadow: 0 -4px 10px rgba(0, 0, 0, 0.05);
            /* إزالة الفراغات المضافة من Streamlit حول الأعمدة */
            margin: 0 !important;
            width: 100%;
            max-width: 100%;
        }
        
        /* ضمان وجود مساحة أسفل المحتوى لمنع الشريط السفلي من حجب النص */
        .stApp {
            padding-bottom: 70px; 
        }

        /* تنسيق الأزرار المحقونة بـ JS في الشريط السفلي */
        .mobile-nav-container button.custom-nav-button {
            /* إزالة التنسيقات الافتراضية للزر */
            background: none !important;
            border: none !important;
            padding: 0 !important;
            margin: 0 !important;
            height: auto !important;
            box-shadow: none !important;
            cursor: pointer;
            width: 100%;
        }
        
        /* محتوى الزر (الأيقونة + النص) - هذا هو الكلاس الذي تم حقنه في app.py */
        .mobile-nav-container .nav-button-content {
            color: #7f8c8d; /* اللون الافتراضي (رمادي) */
            transition: color 0.3s ease;
            width: 100%;
            /* تنسيق مرن للمحتوى */
            display: flex;
            flex-direction: column;
            align-items: center;
            line-height: 1.1;
            padding: 5px 0; 
        }

        /* الأيقونة داخل الزر */
        .mobile-nav-container .nav-icon svg {
            width: 20px;
            height: 20px;
            margin-bottom: 2px;
            stroke-width: 2.2; 
            transition: stroke 0.3s ease;
            /* اللون يتغير عبر currentColor */
            stroke: currentColor; 
        }

        /* النص تحت الأيقونة */
        .mobile-nav-container .nav-label {
            font-size: 10px;
            white-space: nowrap;
        }
        
        /* تنسيق الزر النشط */
        .mobile-nav-container .nav-button-content.active {
            color: #3498db; /* لون نشط (أزرق طبي) */
            font-weight: bold;
        }

        /* ======================================= */
        /* 3. تنسيق شريط الإحصائيات العلوي */
        /* ======================================= */
        .top-stats-bar {
            padding: 5px 0 15px 0;
            border-bottom: 1px solid #f0f0f0;
            margin-bottom: 20px;
        }
        
        .stat-card {
            border-radius: 8px;
            padding: 10px 5px;
            text-align: center;
            font-size: 12px;
            font-weight: 600;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            margin: 5px;
            min-height: 45px;
            display: flex;
            align-items: center;
            justify-content: center;
            line-height: 1.2;
        }
        
        .stat-success { background-color: #e6f7ff; color: #1890ff; border: 1px solid #91d5ff; } 
        .stat-warning { background-color: #fffbe6; color: #faad14; border: 1px solid #ffe58f; } 
        .stat-error { background-color: #fff1f0; color: #f5222d; border: 1px solid #ffa39e; } 
        .stat-info { background-color: #f9f9f9; color: #595959; border: 1px solid #d9d9d9; } 
        
        /* ======================================= */
        /* 4. تنسيق شاشة 'المزيد' (More Pages) */
        /* ======================================= */
        .more-pages-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }
        
        /* تنسيق زر Streamlit في صفحة المزيد (يتم تطبيق هذا الكلاس عبر JS) */
        button.more-page-button {
            /* إعادة تعيين تنسيقات Streamlit */
            background-color: #f7f7f7 !important;
            border: 1px solid #e0e0e0 !important;
            border-radius: 12px !important;
            padding: 20px 10px !important;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05) !important;
            transition: all 0.2s ease;
            cursor: pointer;
            height: 100% !important;
        }
        
        button.more-page-button:hover {
            background-color: #ffffff !important;
            border-color: #3498db !important;
            transform: translateY(-2px);
            box-shadow: 0 6px 10px rgba(0, 0, 0, 0.1) !important;
        }

        /* تنسيق المحتوى المحقون داخل زر More Pages */
        .more-page-button-content {
            text-align: center;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100%;
        }

        .more-page-button-content .icon-svg svg {
            width: 30px;
            height: 30px;
            color: #3498db;
            margin-bottom: 10px;
            stroke-width: 2;
        }
        
        .more-page-button-content .label {
            font-size: 14px;
            font-weight: 600;
            color: #333;
        }

        </style>
    """
    st.markdown(css_code, unsafe_allow_html=True)

