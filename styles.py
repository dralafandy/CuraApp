import streamlit as st

def load_custom_css():
    """تطبيق الـ CSS اللازم لتثبيت الشريط السفلي وتنسيقات أزرار Streamlit."""
    
    css_code = """
        <style>
        /* ======================================= */
        /* 1. إخفاء الشريط الجانبي وبعض عناصر Streamlit */
        /* ======================================= */
        section[data-testid="stSidebar"] {
            display: none !important;
        }
        button[data-testid="baseButton-header"] {
            display: none !important;
        }
        
        /* ======================================= */
        /* 2. تنسيق حاوية شريط التنقل السفلي */
        /* ======================================= */
        .mobile-nav-container {
            position: fixed; 
            bottom: 0;      
            left: 0;
            right: 0;
            z-index: 1000;  
            background-color: #ffffff;
            padding: 5px 0 0 0;
            border-top: 1px solid #e0e0e0;
            box-shadow: 0 -4px 10px rgba(0, 0, 0, 0.05);
            margin: 0 !important;
            width: 100%;
            max-width: 100%;
        }
        
        /* ضمان وجود مساحة أسفل المحتوى */
        .stApp {
            padding-bottom: 70px; 
        }
        
        /* إزالة الهوامش الداخلية للأعمدة في الشريط السفلي */
        .mobile-nav-container [data-testid="stVerticalBlock"] > div:nth-child(2) > div {
             gap: 0px !important; /* لتقليل المسافة بين الأزرار */
        }

        /* ======================================= */
        /* 3. تنسيق أزرار التنقل (st.button) */
        /* ======================================= */
        
        /* استهداف زر Streamlit الأصلي */
        .mobile-nav-container button {
            /* إزالة كل تنسيق Streamlit الافتراضي */
            background-color: transparent !important;
            border: none !important;
            box-shadow: none !important;
            padding: 5px 0px !important;
            margin: 0 !important;
            height: 100% !important;
            width: 100% !important;
            
            /* تنسيق المحتوى ليكون عمودياً */
            display: flex !important;
            flex-direction: column !important;
            align-items: center !important;
            justify-content: center !important;
            text-align: center !important;
            
            /* لون غير نشط (رمادي) */
            color: #7f8c8d !important; 
            transition: color 0.2s ease, transform 0.1s;
        }

        /* تنسيق المحتوى داخل الزر (يحتوي على الأيقونة والنص) */
        .mobile-nav-container button p {
            font-size: 10px !important;
            margin: 0 !important;
            padding: 0 !important;
            line-height: 1.1 !important;
            white-space: nowrap;
        }
        
        /* تنسيق الأيقونات (باستخدام FontAwesome/Emojis) */
        .mobile-nav-container button span {
            font-size: 20px !important; 
            margin-bottom: 2px !important;
            line-height: 1 !important;
        }
        
        /* تأثير النقر للهواتف (Touch/Active) */
        .mobile-nav-container button:active {
            transform: scale(0.95);
        }

        /* ======================================= */
        /* 4. تنسيق الزر النشط (Active Button) */
        /* ======================================= */
        /* Streamlit يضيف كلاس .st-emotion-xyz.st-emotion-abc:focus (تعتمد على الإصدار) */
        /* بما أننا لا نستطيع الاعتماد على كلاس ثابت، سنستخدم حيلة بسيطة في app.py */
        
        
        /* ======================================= */
        /* 5. تنسيق شريط الإحصائيات العلوي */
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
        /* 6. تنسيق شاشة 'المزيد' (More Pages) */
        /* ======================================= */
        .more-pages-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }
        
        /* تنسيق زر الـ Grid لجعله يشبه البطاقة */
        .more-pages-grid button {
            background-color: #f7f7f7 !important;
            border: 1px solid #e0e0e0 !important;
            border-radius: 12px !important;
            padding: 20px 10px !important;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05) !important;
            transition: all 0.2s ease !important;
            
            /* إعادة تعيين تنسيقات النص والأيقونات داخل بطاقة الـ Grid */
            color: #333 !important; /* اللون الافتراضي للـ Grid */
        }
        .more-pages-grid button:hover {
            background-color: #ffffff !important;
            border-color: #3498db !important;
            transform: translateY(-2px);
            box-shadow: 0 6px 10px rgba(0, 0, 0, 0.1) !important;
        }
        .more-pages-grid button:active {
            transform: scale(0.98);
        }
        
        /* تنسيق الأيقونة داخل زر الـ Grid */
        .more-pages-grid button span {
            font-size: 30px !important; /* حجم أكبر */
            color: #3498db !important; /* لون أزرق */
            margin-bottom: 10px !important;
            line-height: 1 !important;
        }
        
        /* تنسيق النص داخل زر الـ Grid */
        .more-pages-grid button p {
            font-size: 14px !important;
            font-weight: 600 !important;
        }
        
        </style>
    """
    st.markdown(css_code, unsafe_allow_html=True)

