import streamlit as st
from datetime import date
# تأكد من أن هذه الاستيرادات صحيحة بناءً على هيكل ملفاتك
from database.crud import crud 
from database.models import db 
from styles import load_custom_css # استيراد دالة CSS فقط
from components.notifications import NotificationCenter

# استيراد الصفحات الأساسية
import dashboard
import appointments
import patients
import treatments
import payments
import inventory
# استيراد ملف صفحة 'المزيد' الذي يحتوي على باقي الوحدات
import more_pages 

# استيراد الصفحات الأخرى (لاستخدامها في التوجيه داخل more_pages.py)
import doctors
import suppliers
import expenses
import reports
import settings
import activity_log


# =========================
# تهيئة التطبيق
# =========================
# استخدام collapsed لإخفاء الشريط الجانبي الافتراضي
st.set_page_config(
    page_title="Cura Clinic - نظام إدارة العيادة",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed" 
)

@st.cache_resource
def init_db():
    # تهيئة قاعدة البيانات مرة واحدة
    db.initialize()
    return True

init_db()

# تطبيق الـ CSS المخصص لتفعيل الشريط السفلي
load_custom_css()

# ==================================================================================
# الشريط السفلي - التنقل (Mobile Navigation Bar)
# ==================================================================================

# قائمة الصفحات الأساسية للتنقل السفلي (أيقونات Lucide Icons)
BOTTOM_NAV_PAGES = [
    {'id': 'dashboard', 'label': 'الرئيسية', 'icon_data': '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-home"><path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>'},
    {'id': 'appointments', 'label': 'المواعيد', 'icon_data': '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-calendar-check"><path d="M8 2v4"/><path d="M16 2v4"/><rect width="18" height="18" x="3" y="4" rx="2"/><path d="M3 10h18"/><path d="m9 16 2 2 4-4"/></svg>'},
    {'id': 'patients', 'label': 'المرضى', 'icon_data': '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-users"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>'},
    {'id': 'payments', 'label': 'المالية', 'icon_data': '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-dollar-sign"><line x1="12" x2="12" y1="2" y2="22"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>'},
    {'id': 'inventory', 'label': 'المخزون', 'icon_data': '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-package"><path d="m7.5 4.27 9 5.15"/><path d="m21 12-9-5.15-9 5.15"/><path d="m3 12 9 5.15 9-5.15"/><line x1="12" x2="12" y1="22" y2="17.73"/><path d="M12 17.73 3 12"/><path d="M12 17.73 21 12"/></svg>'},
    {'id': 'more_pages', 'label': 'المزيد', 'icon_data': '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-menu"><line x1="4" x2="20" y1="12" y2="12"/><line x1="4" x2="20" y1="6" y2="6"/><line x1="4" x2="20" y1="18" y2="18"/></svg>'}
]

def render_top_stats_bar():
    # منطق شريط الإحصائيات (لم يتغير)
    try:
        stats = crud.get_dashboard_stats()
    except Exception:
        # fallback
        stats = {'today_appointments': 0, 'low_stock_items': 0}
    
    st.markdown("<div class='top-stats-bar'>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    
    # 1. مواعيد اليوم
    with col1:
        st.markdown(f"<div class='stat-card stat-success'>📅 مواعيد: {stats['today_appointments']}</div>", unsafe_allow_html=True)

    # 2. المخزون المنخفض
    with col2:
        if stats['low_stock_items'] > 0:
            st.markdown(f"<div class='stat-card stat-warning'>⚠️ مخزون: {stats['low_stock_items']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='stat-card stat-info'>✅ المخزون جيد</div>", unsafe_allow_html=True)

    # 3. المصروفات الشهرية
    try:
        financial_summary = crud.get_financial_summary()
        monthly_expenses = financial_summary.get('current_month_expenses', financial_summary.get('total_expenses', 0))
    except:
        monthly_expenses = 0 
        
    with col3:
        # يتم تقريب الرقم لأقرب عدد صحيح للعرض في المساحة الصغيرة
        st.markdown(f"<div class='stat-card stat-error'>💰 المصروفات: {monthly_expenses:.0f}</div>", unsafe_allow_html=True)
        
    st.markdown("</div>", unsafe_allow_html=True)


def handle_nav_click(page_id):
    """دالة Python لمعالجة تغيير الصفحة"""
    st.session_state.current_page = page_id
    st.rerun()

def render_bottom_nav():
    """
    يرسم شريط التنقل السفلي الثابت باستخدام حيلة st.button الشفاف
    لضمان استجابة النقر.
    """
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'dashboard'
        
    current_page = st.session_state.current_page
    
    st.markdown("<div class='mobile-nav-container'>", unsafe_allow_html=True)
    
    # استخدام st.columns لتقسيم المساحة
    cols = st.columns(len(BOTTOM_NAV_PAGES))
    
    for idx, page in enumerate(BOTTOM_NAV_PAGES):
        with cols[idx]:
            is_active = current_page == page['id']
            page_id = page['id']

            # 1. عرض الـ HTML المنسق (الأيقونة والنص)
            content_html = f"""
            <div class='nav-button-content {"active" if is_active else ""}' id='nav-content-{page_id}'>
                <div class='nav-icon'>{page['icon_data']}</div>
                <div class='nav-label'>{page['label']}</div>
            </div>
            """
            st.markdown(content_html, unsafe_allow_html=True)

            # 2. وضع زر Streamlit حقيقي وشفاف فوق الـ HTML المنسق لضمان الاستجابة
            # نستخدم st.form لضمان أن النقر على زر Streamlit سيعمل بسلاسة
            with st.form(key=f"nav_form_{page_id}", clear_on_submit=False):
                # زر Streamlit شفاف وحقيقي، يغطي منطقة الـ HTML المنسق
                submitted = st.form_submit_button(
                    label=" ", # مسافة فارغة لجعل الزر شفافاً قدر الإمكان
                    use_container_width=True,
                    # نستخدم key فريد في كل مرة لضمان عدم وجود تكرار
                    key=f"nav_btn_{page_id}_submit"
                )
                
                if submitted:
                    handle_nav_click(page_id)
            
            # حقن CSS إضافي لجعل الزر الشفاف يغطي الـ HTML بشكل مثالي ويصبح غير مرئي
            st.markdown(f"""
                <style>
                    /* استهداف الحاوية الرئيسية للزر (النموذج) */
                    div[data-testid="stForm"] > div:has(button[key="nav_btn_{page_id}_submit"]) {{
                        position: absolute; /* وضعه بشكل مطلق لتغطية المحتوى المنسق */
                        top: 0;
                        left: 0;
                        right: 0;
                        bottom: 0;
                        height: 100%;
                        width: 100%;
                        margin: 0 !important;
                        padding: 0 !important;
                    }}
                    /* جعل الزر نفسه شفافاً */
                    button[key="nav_btn_{page_id}_submit"] {{
                        background: transparent !important;
                        color: transparent !important;
                        border: none !important;
                        box-shadow: none !important;
                        height: 100%;
                        width: 100%;
                        margin: 0;
                        padding: 0;
                        z-index: 1001; /* فوق المحتوى المنسق */
                        cursor: pointer;
                    }}
                    /* إخفاء تسمية النموذج */
                    div[data-testid="stForm"] > div > div > label {{
                        display: none !important;
                    }}
                    
                    /* إعادة ترتيب الأعمدة لتكون حاوية للـ DIVs والأزرار */
                    .stApp .stColumn {{
                        position: relative; /* لتمكين وضع الزر بشكل مطلق داخل العمود */
                        display: flex;
                        flex-direction: column;
                        align-items: center;
                        justify-content: center;
                    }}
                    
                    /* لضمان أن الـ HTML المنسق يأخذ وضع نسبي ليتمكن الزر المطلق من تغطيته */
                    #nav-content-{page_id} {{
                         position: relative;
                         z-index: 1000;
                    }}

                </style>
                """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
    
    NotificationCenter.show_urgent_toast_notifications()


# =========================
# التوجيه إلى الصفحات
# =========================
def main():
    
    # عرض شريط الإحصائيات العلوي
    render_top_stats_bar()
    
    # عرض شريط التنقل السفلي
    render_bottom_nav() 
    
    # خريطة التوجيه بين الـ ID والدالة المسؤولة عن عرض الصفحة
    page_mapping = {
        'dashboard': dashboard.render,
        'appointments': appointments.render,
        'patients': patients.render,
        'payments': payments.render,
        'inventory': inventory.render,
        'more_pages': more_pages.render, # استخدام الملف الجديد لعرض المزيد من الخيارات
        
        # وحدات النظام التي يمكن الوصول إليها من صفحة 'المزيد'
        'doctors': doctors.render,
        'treatments': treatments.render,
        'suppliers': suppliers.render,
        'expenses': expenses.render,
        'reports': reports.render,
        'settings': settings.render,
        'activity_log': activity_log.render
    }
    
    page = st.session_state.get('current_page', 'dashboard')
    
    if page in page_mapping:
        # عرض محتوى الصفحة المختارة
        page_mapping[page]()
    else:
        # عرض لوحة القيادة كافتراض
        dashboard.render()

if __name__ == '__main__':
    main()

