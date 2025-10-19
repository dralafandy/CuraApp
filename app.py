import streamlit as st
from datetime import date
# تأكد من أن هذه الاستيرادات صحيحة بناءً على هيكل ملفاتك
from database.crud import crud 
from database.models import db 
from styles import load_custom_css # استيراد الدالة التي تطبق الـ CSS المخصص
from components.notifications import NotificationCenter

# استيراد الصفحات - يجب أن تكون هذه الملفات موجودة في مجلد التطبيق
import dashboard
import appointments
import patients
import doctors
import treatments
import payments
import inventory
import suppliers
import expenses
import reports
import settings
import activity_log

# =========================
# تهيئة التطبيق
# =========================
st.set_page_config(
    page_title="نظام إدارة العيادة - Cura Clinic",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed" # تغيير الحالة الافتراضية إلى مطوية
)

@st.cache_resource
def init_db():
    # تأكد من تهيئة قاعدة البيانات مرة واحدة
    db.initialize()
    return True

init_db()

# تطبيق الـ CSS المخصص لتفعيل الشريط السفلي وإخفاء الجانبي
load_custom_css()

# ==================================================================================
# الشريط السفلي - التنقل (بديل الشريط الجانبي)
# ==================================================================================

# قائمة الصفحات الأساسية للتنقل السفلي
BOTTOM_NAV_PAGES = [
    {'id': 'dashboard', 'label': 'الرئيسية', 'icon': '🏠'},
    {'id': 'appointments', 'label': 'المواعيد', 'icon': '📅'},
    {'id': 'patients', 'label': 'المرضى', 'icon': '🧑'},
    {'id': 'payments', 'label': 'المالية', 'icon': '💰'},
    {'id': 'inventory', 'label': 'المخزون', 'icon': '📦'},
    {'id': 'settings', 'label': 'المزيد', 'icon': '☰'}
]

def render_bottom_nav():
    # استخدام session_state لتتبع الصفحة الحالية
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'dashboard'
        
    current_page = st.session_state.current_page
    
    # 1. عرض الإحصائيات والمعلومات في الشريط العلوي (بدلاً من الشريط الجانبي)
    stats = crud.get_dashboard_stats()
    
    # عرض الإحصائيات في عمودين علويين ليناسبوا الهاتف
    st.markdown("<div class='top-stats-bar'>", unsafe_allow_html=True)
    col1, col2 = st.columns([1, 1])
    with col1:
        st.info(f"📅 {date.today().strftime('%Y-%m-%d')}", icon="📅")
    with col2:
        st.success(f"📌 مواعيد اليوم: {stats['today_appointments']}", icon="📌")

    st.markdown("</div>", unsafe_allow_html=True)
    
    # 2. إنشاء شريط التنقل السفلي الفعلي
    
    # استخدام st.markdown مع كود HTML/CSS لإنشاء شريط تنقل ثابت في الأسفل
    st.markdown("""
        <div class='mobile-nav-container'>
            <div class='mobile-nav-content'>
    """, unsafe_allow_html=True)
    
    # عرض الأزرار في أعمدة متساوية داخل الشريط السفلي
    cols = st.columns(len(BOTTOM_NAV_PAGES))
    
    for idx, page in enumerate(BOTTOM_NAV_PAGES):
        with cols[idx]:
            # استخدام زر Streamlit العادي مع key فريد
            is_active = current_page == page['id']
            
            # محتوى الزر (أيقونة + نص)
            button_html = f"""
            <div style='font-size: 20px; margin-bottom: 2px;'>{page['icon']}</div>
            <div style='font-size: 10px;'>{page['label']}</div>
            """
            
            # تطبيق لون مختلف على الزر النشط باستخدام CSS Class
            button_style = "mobile-nav-button active" if is_active else "mobile-nav-button"
            
            # استخدام st.button مع زر Streamlit عادي لضمان عمل Rerun
            if st.button(
                label=page['icon'],
                key=f"nav_bottom_{page['id']}",
                use_container_width=True
            ):
                 st.session_state.current_page = page['id']
                 st.rerun()

    # إغلاق الـ container
    st.markdown("""
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # رسائل التنبيهات المنخفضة أو المنتهية الصلاحية
    if stats['low_stock_items'] > 0:
        st.toast(f"⚠️ مخزون منخفض: {stats['low_stock_items']} عنصر", icon="⚠️")
    if stats['expiring_items'] > 0:
        st.toast(f"🚨 أصناف تنتهي قريباً: {stats['expiring_items']}", icon="🚨")
    
    # عرض الإشعارات العاجلة الأخرى
    NotificationCenter.show_urgent_toast_notifications()
    

# =========================
# التوجيه إلى الصفحات
# =========================
def main():
    # لا يوجد استدعاء لـ render_sidebar() بعد الآن
    
    # عرض شريط التنقل السفلي
    render_bottom_nav() 
    
    page_mapping = {
        'dashboard': dashboard.render,
        'appointments': appointments.render,
        'patients': patients.render,
        'doctors': doctors.render,
        'treatments': treatments.render,
        'payments': payments.render,
        'inventory': inventory.render,
        'suppliers': suppliers.render,
        'expenses': expenses.render,
        'reports': reports.render,
        'settings': settings.render,
        'activity_log': activity_log.render,
        # يمكن إضافة المزيد من الصفحات هنا عند الحاجة
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
