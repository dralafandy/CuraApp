# app.py
import streamlit as st
from datetime import date
from database.crud import crud
from database.models import db
from styles import load_custom_css
from components.notifications import NotificationCenter

# استيراد الصفحات
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

# ========================
# تهيئة التطبيق
# ========================
st.set_page_config(
    page_title="نظام إدارة العيادة - Cura Clinic",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="collapsed"  # إخفاء الشريط الجانبي
)

@st.cache_resource
def init_db():
    db.initialize()
    return True

init_db()

# ========================
# شريط التنقل العلوي
# ========================
def render_navbar():
    st.markdown("""
        <style>
        .navbar {
            background: linear-gradient(90deg, #2c3e50 0%, #3498db 100%);
            padding: 1rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-radius: 0 0 12px 12px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }
        .navbar-brand {
            color: white;
            font-size: 1.8rem;
            font-weight: bold;
            margin: 0;
        }
        .navbar-menu {
            display: flex;
            gap: 1rem;
        }
        .navbar-item {
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 8px;
            text-decoration: none;
            transition: background 0.3s ease;
        }
        .navbar-item:hover {
            background: rgba(255,255,255,0.2);
        }
        .navbar-item.active {
            background: rgba(255,255,255,0.3);
        }
        </style>
    """, unsafe_allow_html=True)

    with st.container():
        st.markdown("""
            <div class="navbar">
                <div class="navbar-brand">🏥 Cura Clinic</div>
                <div class="navbar-menu">
                    <div class="navbar-item">🏠 الرئيسية</div>
                    <div class="navbar-item">📅 المواعيد</div>
                    <div class="navbar-item">👥 المرضى</div>
                    <div class="navbar-item">👨‍⚕️ الأطباء</div>
                    <div class="navbar-item">💉 العلاجات</div>
                    <div class="navbar-item">💰 المدفوعات</div>
                    <div class="navbar-item">📦 المخزون</div>
                    <div class="navbar-item">🏪 الموردين</div>
                    <div class="navbar-item">💸 المصروفات</div>
                    <div class="navbar-item">📊 التقارير</div>
                    <div class="navbar-item">⚙️ الإعدادات</div>
                    <div class="navbar-item">📝 سجل الأنشطة</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    # التحكم بالتنقل
    menu_items = {
        "🏠 الرئيسية": "dashboard",
        "📅 المواعيد": "appointments",
        "👥 المرضى": "patients",
        "👨‍⚕️ الأطباء": "doctors",
        "💉 العلاجات": "treatments",
        "💰 المدفوعات": "payments",
        "📦 المخزون": "inventory",
        "🏪 الموردين": "suppliers",
        "💸 المصروفات": "expenses",
        "📊 التقارير": "reports",
        "⚙️ الإعدادات": "settings",
        "📝 سجل الأنشطة": "activity_log"
    }
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'dashboard'

    cols = st.columns(len(menu_items))
    for idx, (label, page_id) in enumerate(menu_items.items()):
        with cols[idx]:
            if st.button(label, key=f"nav_{page_id}", use_container_width=True):
                st.session_state.current_page = page_id
                st.rerun()

    # اختيار الثيم
    theme_map = {
        "فاتح": "light",
        "داكن": "dark",
        "أزرق": "blue",
        "أخضر": "green",
        "أحمر": "red"
    }
    theme_choice = st.selectbox("🎨 اختر الثيم", list(theme_map.keys()), key="theme_select")
    load_custom_css(theme=theme_map[theme_choice])

    # إحصائيات سريعة
    stats = crud.get_dashboard_stats()
    with st.container():
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📅 التاريخ", date.today().strftime('%Y-%m-%d'))
        with col2:
            st.metric("📌 مواعيد اليوم", stats['today_appointments'])
        with col3:
            if stats['low_stock_items'] > 0:
                st.metric("⚠️ مخزون منخفض", f"{stats['low_stock_items']} عنصر")
            if stats['expiring_items'] > 0:
                st.metric("🚨 أصناف تنتهي قريباً", f"{stats['expiring_items']}")

    # إشعارات
    NotificationCenter.render()

# ========================
# التوجيه إلى الصفحات
# ========================
def main():
    render_navbar()
    NotificationCenter.show_urgent_toast_notifications()

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
        'activity_log': activity_log.render
    }
    page = st.session_state.get('current_page', 'dashboard')
    render_func = page_mapping.get(page, dashboard.render)
    render_func()

if __name__ == "__main__":
    main()
