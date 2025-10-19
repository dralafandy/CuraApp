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
# استيراد ملف صفحة 'المزيد'
import more_pages 

# استيراد الصفحات الأخرى (لاستخدامها في التوجيه)
import doctors
import suppliers
import expenses
import reports
import settings
import activity_log


# =========================
# تهيئة التطبيق
# =========================
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

# تطبيق الـ CSS المخصص لتفعيل الشريط السفلي وتنسيق الأزرار
load_custom_css()

# ==================================================================================
# الشريط السفلي - التنقل (Mobile Navigation Bar)
# ==================================================================================

# قائمة الصفحات الأساسية للتنقل السفلي (باستخدام رموز الأيموجي/FontAwesome لسهولة الدمج)
# التنسيق: أيقونة HTML (مثل FontAwesome) متبوعة بالنص
BOTTOM_NAV_PAGES = [
    {'id': 'dashboard', 'label': 'الرئيسية', 'icon': '🏠'},
    {'id': 'appointments', 'label': 'المواعيد', 'icon': '📅'},
    {'id': 'patients', 'label': 'المرضى', 'icon': '🧑'}, # نستخدم رمز شخص واحد
    {'id': 'payments', 'label': 'المالية', 'icon': '💵'},
    {'id': 'inventory', 'label': 'المخزون', 'icon': '📦'},
    {'id': 'more_pages', 'label': 'المزيد', 'icon': '☰'}
]

def render_top_stats_bar():
    """يعرض شريط إحصائيات علوي مرن يناسب الهاتف."""
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
    يرسم شريط التنقل السفلي الثابت باستخدام st.button بشكل مباشر
    مما يضمن استجابة النقر.
    """
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'dashboard'
        
    current_page = st.session_state.current_page
    
    st.markdown("<div class='mobile-nav-container'>", unsafe_allow_html=True)
    
    # استخدام st.columns لتقسيم المساحة
    cols = st.columns(len(BOTTOM_NAV_PAGES))
    
    for idx, page in enumerate(BOTTOM_NAV_PAGES):
        # بناء الـ label كـ HTML (أيقونة + سطر جديد + نص)
        # Streamlit سيحول هذا النص إلى HTML (نظرياً) لكنه سيظهر النص فقط.
        # لذا سنستخدم تنسيق Markdown بسيط:
        button_label = f"<div class='nav-label-content'><span class='nav-icon'>{page['icon']}</span><p>{page['label']}</p></div>"
        
        with cols[idx]:
            
            # 1. استخدام st.button بشكل مباشر
            # لا يمكننا تمرير HTML كـ label، لذا نستخدم HTML لتنسيقه لاحقاً
            clicked = st.button(
                label=f"{page['icon']}\n{page['label']}",
                key=f"nav_btn_{page['id']}",
                use_container_width=True
            )
            
            if clicked:
                handle_nav_click(page['id'])

            # 2. حقن CSS مخصص لتلوين الزر النشط في هذا الإطار فقط
            if page['id'] == current_page:
                st.markdown(f"""
                    <style>
                        /* استهداف الزر النشط بواسطة مفتاحه الفريد */
                        button[key="nav_btn_{page['id']}"] {{
                            color: #3498db !important; /* لون نشط (أزرق طبي) */
                            font-weight: bold !important;
                        }}
                        button[key="nav_btn_{page['id']}"] p {{
                            font-weight: bold !important;
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

