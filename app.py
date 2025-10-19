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
page_title=“Cura Clinic | نظام إدارة العيادة”,
page_icon=“🏥”,
layout=“wide”,
initial_sidebar_state=“auto”  # تلقائي للتكيف مع حجم الشاشة
)

@st.cache_resource
def init_db():
db.initialize()
return True

init_db()

# ========================

# القائمة العلوية للموبايل

# ========================

def render_mobile_header():
“”“عرض هيدر مخصص للموبايل”””
col1, col2, col3 = st.columns([1, 3, 1])

```
with col1:
    if st.button("☰", key="mobile_menu", help="القائمة"):
        st.session_state.show_mobile_menu = not st.session_state.get('show_mobile_menu', False)

with col2:
    st.markdown("""
        <div style='text-align: center;'>
            <h2 style='margin: 0; color: var(--primary-color);'>🏥 Cura Clinic</h2>
        </div>
    """, unsafe_allow_html=True)

with col3:
    # إشعارات سريعة
    stats = crud.get_dashboard_stats()
    notification_count = stats.get('low_stock_items', 0) + stats.get('expiring_items', 0)
    if notification_count > 0:
        st.button(f"🔔 {notification_count}", key="notifications_btn")
```

# ========================

# الشريط الجانبي المحسّن

# ========================

def render_sidebar():
with st.sidebar:
# رأس العيادة
st.markdown(”””
<div style='text-align: center; padding: 1.5rem 0.5rem; background: linear-gradient(135deg, var(--primary-color)20, var(--primary-color)10); border-radius: 12px; margin-bottom: 1rem;'>
<div style='font-size: 3rem; margin-bottom: 0.5rem;'>🏥</div>
<h2 style='color: var(--primary-color); margin: 0; font-size: 1.5rem;'>Cura Clinic</h2>
<p style='color: #6b7280; margin: 0.3rem 0 0 0; font-size: 0.9rem;'>نظام إدارة العيادة</p>
</div>
“””, unsafe_allow_html=True)

```
    # اختيار الثيم في expander
    with st.expander("🎨 تخصيص المظهر", expanded=False):
        theme_map = {
            "💜 بنفسجي": "purple",
            "💙 أزرق": "blue",
            "💚 أخضر": "green",
            "🧡 برتقالي": "orange",
            "🖤 داكن": "dark",
            "💗 وردي": "pink"
        }
        theme_choice = st.selectbox("اختر الثيم", list(theme_map.keys()), key="theme_select", label_visibility="collapsed")
        load_custom_css(theme=theme_map[theme_choice])

    st.markdown("<br>", unsafe_allow_html=True)

    # القائمة الرئيسية مع أيقونات محسّنة
    menu_sections = {
        "رئيسية": [
            ("🏠", "الرئيسية", "dashboard"),
            ("📅", "المواعيد", "appointments"),
        ],
        "إدارة": [
            ("👥", "المرضى", "patients"),
            ("👨‍⚕️", "الأطباء", "doctors"),
            ("💉", "العلاجات", "treatments"),
        ],
        "مالية": [
            ("💰", "المدفوعات", "payments"),
            ("💸", "المصروفات", "expenses"),
        ],
        "مخزون": [
            ("📦", "المخزون", "inventory"),
            ("🏪", "الموردين", "suppliers"),
        ],
        "أخرى": [
            ("📊", "التقارير", "reports"),
            ("⚙️", "الإعدادات", "settings"),
            ("📝", "سجل الأنشطة", "activity_log"),
        ]
    }

    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'dashboard'

    for section, items in menu_sections.items():
        st.markdown(f"**{section}**")
        for icon, label, page_id in items:
            is_active = st.session_state.current_page == page_id
            button_style = "primary" if is_active else "secondary"
            
            if st.button(
                f"{icon} {label}",
                key=f"nav_{page_id}",
                use_container_width=True,
                type=button_style
            ):
                st.session_state.current_page = page_id
                st.rerun()
        st.markdown("<div style='margin: 0.5rem 0;'></div>", unsafe_allow_html=True)

    # معلومات سريعة
    st.markdown("---")
    with st.container():
        stats = crud.get_dashboard_stats()
        
        st.markdown(f"""
            <div style='background: linear-gradient(135deg, #f0f9ff, #e0f2fe); padding: 1rem; border-radius: 8px; margin-bottom: 0.5rem;'>
                <div style='font-size: 0.85rem; color: #0369a1;'>📅 التاريخ</div>
                <div style='font-size: 1rem; font-weight: bold; color: #075985;'>{date.today().strftime('%Y-%m-%d')}</div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
            <div style='background: linear-gradient(135deg, #f0fdf4, #dcfce7); padding: 1rem; border-radius: 8px; margin-bottom: 0.5rem;'>
                <div style='font-size: 0.85rem; color: #15803d;'>📌 مواعيد اليوم</div>
                <div style='font-size: 1.5rem; font-weight: bold; color: #166534;'>{stats['today_appointments']}</div>
            </div>
        """, unsafe_allow_html=True)
        
        if stats['low_stock_items'] > 0:
            st.markdown(f"""
                <div style='background: linear-gradient(135deg, #fffbeb, #fef3c7); padding: 1rem; border-radius: 8px; margin-bottom: 0.5rem;'>
                    <div style='font-size: 0.85rem; color: #a16207;'>⚠️ مخزون منخفض</div>
                    <div style='font-size: 1.3rem; font-weight: bold; color: #ca8a04;'>{stats['low_stock_items']} عنصر</div>
                </div>
            """, unsafe_allow_html=True)
        
        if stats['expiring_items'] > 0:
            st.markdown(f"""
                <div style='background: linear-gradient(135deg, #fef2f2, #fee2e2); padding: 1rem; border-radius: 8px;'>
                    <div style='font-size: 0.85rem; color: #991b1b;'>🚨 تنتهي قريباً</div>
                    <div style='font-size: 1.3rem; font-weight: bold; color: #dc2626;'>{stats['expiring_items']} صنف</div>
                </div>
            """, unsafe_allow_html=True)

    # إشعارات
    st.markdown("---")
    with st.expander("🔔 الإشعارات", expanded=False):
        NotificationCenter.render()
```

# ========================

# عرض القائمة للموبايل

# ========================

def render_mobile_menu():
“”“عرض قائمة منبثقة للموبايل”””
if st.session_state.get(‘show_mobile_menu’, False):
with st.container():
st.markdown(”””
<div style='background: white; padding: 1rem; border-radius: 12px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 1rem;'>
“””, unsafe_allow_html=True)

```
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
        
        cols = st.columns(3)
        for idx, (label, page_id) in enumerate(menu_items.items()):
            with cols[idx % 3]:
                if st.button(label, key=f"mobile_nav_{page_id}", use_container_width=True):
                    st.session_state.current_page = page_id
                    st.session_state.show_mobile_menu = False
                    st.rerun()
        
        st.markdown("</div>", unsafe_allow_html=True)
```

# ========================

# التوجيه إلى الصفحات

# ========================

def main():
# تحميل الأنماط أولاً
theme_map = {
“💜 بنفسجي”: “purple”,
“💙 أزرق”: “blue”,
“💚 أخضر”: “green”,
“🧡 برتقالي”: “orange”,
“🖤 داكن”: “dark”,
“💗 وردي”: “pink”
}
current_theme = st.session_state.get(‘theme_select’, “💙 أزرق”)
load_custom_css(theme=theme_map.get(current_theme, “blue”))

```
# عرض الشريط الجانبي
render_sidebar()

# عرض القائمة للموبايل إذا كانت مفتوحة
if st.session_state.get('show_mobile_menu', False):
    render_mobile_menu()

# عرض الإشعارات العاجلة
NotificationCenter.show_urgent_toast_notifications()

# توجيه الصفحات
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

# عرض الصفحة مع padding مناسب
with st.container():
    render_func()
```

if **name** == “**main**”:
main()
