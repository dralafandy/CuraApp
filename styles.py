import streamlit as st
from datetime import date
from database.crud import crud
from database.models import db
from styles import load_custom_css # استيراد دالة CSS
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

# =======================
# تهيئة التطبيق
# =======================
st.set_page_config(
    page_title="نظام إدارة العيادة - Cura Clinic",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded" # Keep expanded for desktop, becomes menu on mobile
)

@st.cache_resource
def init_db():
    # تهيئة قاعدة البيانات مرة واحدة
    db.initialize()
    return True

init_db()

# تطبيق الـ CSS المخصص
load_custom_css()

# ==================================================================================
# هيكل الشريط الجانبي - التنقل المنظم
# ==================================================================================

SIDEBAR_GROUPS = [
    {
        'title': 'العمليات الأساسية',
        'pages': [
            {'id': 'dashboard', 'label': 'لوحة القيادة', 'icon': '🏠'},
            {'id': 'appointments', 'label': 'إدارة المواعيد', 'icon': '📅'},
            {'id': 'patients', 'label': 'ملفات المرضى', 'icon': '🧑‍🤝‍🧑'},
            {'id': 'treatments', 'label': 'العلاجات والخدمات', 'icon': '⚕️'},
        ]
    },
    {
        'title': 'الإدارة والمالية',
        'pages': [
            {'id': 'payments', 'label': 'المعاملات المالية', 'icon': '💵'},
            {'id': 'expenses', 'label': 'المصروفات', 'icon': '🧾'},
            {'id': 'inventory', 'label': 'إدارة المخزون', 'icon': '📦'},
            {'id': 'suppliers', 'label': 'إدارة الموردين', 'icon': '🚚'},
            {'id': 'doctors', 'label': 'إدارة الأطباء', 'icon': '👨‍⚕️'},
        ]
    },
    {
        'title': 'النظام والتقارير',
        'pages': [
            {'id': 'reports', 'label': 'التقارير والإحصاء', 'icon': '📊'},
            {'id': 'activity_log', 'label': 'سجل الأنشطة', 'icon': '⏱️'},
            {'id': 'settings', 'label': 'إعدادات النظام', 'icon': '⚙️'},
        ]
    },
]

def render_sidebar():
    """يرسم شريط التنقل الجانبي المنظم."""
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'dashboard'
        
    current_page = st.session_state.current_page

    with st.sidebar:
        # رأس الشريط الجانبي
        st.markdown("""
            <div style='text-align: center; padding: 10px 0;'>
                <h1 style='color: #3498db; margin: 0; font-size: 28px;'>🏥 Cura Clinic</h1>
                <p style='color: #95a5a6; margin: 5px 0;'>نظام إدارة العيادة</p>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("---")
        
        # التنقل (Navigation)
        for group in SIDEBAR_GROUPS:
            st.subheader(group['title'])
            for page in group['pages']:
                
                # بناء اسم الزر (أيقونة + نص)
                button_label = f"{page['icon']}  {page['label']}"
                
                # استخدام st.button للتحكم في التنقل
                # Streamlit يقوم تلقائياً بتمييز الزر الذي تم النقر عليه
                if st.button(
                    button_label, 
                    key=f"nav_{page['id']}", 
                    use_container_width=True
                ):
                    st.session_state.current_page = page['id']
                    st.rerun()

                # حقن CSS بسيط لتمييز الزر النشط باللون
                if page['id'] == current_page:
                    st.markdown(f"""
                        <style>
                            /* استهداف الزر النشط في الشريط الجانبي فقط */
                            [data-testid="stSidebar"] button[key="nav_{page['id']}"] {{
                                background-color: #3498db !important; 
                                color: white !important;
                                border-color: #3498db !important;
                                font-weight: bold;
                            }}
                        </style>
                    """, unsafe_allow_html=True)
            st.markdown("---")
        
        # معلومات سريعة في الشريط الجانبي
        st.markdown("<h4 style='color: #34495e;'>معلومات سريعة</h4>", unsafe_allow_html=True)
        try:
            stats = crud.get_dashboard_stats()
        except:
            stats = {'today_appointments': 0, 'low_stock_items': 0}
            
        st.info(f"📅 اليوم: {date.today().strftime('%Y-%m-%d')}")
        st.success(f"📌 مواعيد اليوم: {stats['today_appointments']}")
        
        if stats['low_stock_items'] > 0:
            st.warning(f"⚠️ مخزون منخفض: {stats['low_stock_items']} عنصر")
        else:
            st.success("✅ المخزون جيد")
            
        # إشعارات
        NotificationCenter.render()

# =======================
# التوجيه إلى الصفحات
# =======================
def main():
    
    # 1. عرض الشريط الجانبي
    render_sidebar()
    
    # 2. عرض إشعارات Toast (لأنها لا تحتاج إلى إعادة تحميل)
    NotificationCenter.show_urgent_toast_notifications()

    # 3. خريطة التوجيه وعرض الصفحة المطلوبة
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
    
    st.title(f"{page_mapping[page].__module__.split('.')[-1].capitalize()}") # عنوان الصفحة ديناميكياً
    
    if page in page_mapping:
        # عرض محتوى الصفحة المختارة
        page_mapping[page]()
    else:
        # عرض لوحة القيادة كافتراض
        dashboard.render()

if __name__ == '__main__':
    main()

