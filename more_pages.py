import streamlit as st

# قائمة الصفحات الإضافية التي تظهر في شاشة 'المزيد' (More)
# نستخدم رموز الأيموجي/FontAwesome لسهولة الدمج
MORE_PAGES = [
    {'id': 'doctors', 'label': 'إدارة الأطباء', 'icon': '👨‍⚕️'},
    {'id': 'treatments', 'label': 'العلاجات والخدمات', 'icon': '💊'},
    {'id': 'suppliers', 'label': 'إدارة الموردين', 'icon': '🚚'},
    {'id': 'expenses', 'label': 'المصروفات', 'icon': '🧾'},
    {'id': 'reports', 'label': 'التقارير والإحصاء', 'icon': '📊'},
    {'id': 'activity_log', 'label': 'سجل الأنشطة', 'icon': '⏱️'},
    {'id': 'settings', 'label': 'إعدادات النظام', 'icon': '⚙️'},
]


def handle_more_page_click(page_id):
    """دالة Python لمعالجة تغيير الصفحة"""
    st.session_state.current_page = page_id
    st.rerun()

def render():
    """الدالة الرئيسية لعرض صفحة المزيد"""
    st.header("☰ المزيد من وحدات النظام")
    st.markdown("<p style='font-size: 16px; color: #7f8c8d;'>اختر الوحدة التي تريد إدارتها أو الاطلاع عليها.</p>", unsafe_allow_html=True)
    
    st.markdown("<div class='more-pages-grid'>", unsafe_allow_html=True)

    cols_per_row = 2 
    num_pages = len(MORE_PAGES)
    
    for i in range(0, num_pages, cols_per_row):
        cols = st.columns(cols_per_row)
        for j in range(cols_per_row):
            idx = i + j
            if idx < num_pages:
                page = MORE_PAGES[idx]
                
                with cols[j]:
                    # بناء الـ label كـ نص متعدد الأسطر: أيقونة + سطر جديد + نص
                    button_label = f"{page['icon']}\n{page['label']}"

                    # استخدام st.button بشكل مباشر داخل Grid
                    clicked = st.button(
                        label=button_label,
                        key=f"more_btn_{page['id']}",
                        use_container_width=True
                    )
                    
                    if clicked:
                        handle_more_page_click(page['id'])

    st.markdown("</div>", unsafe_allow_html=True)

