import streamlit as st

# قائمة الصفحات الإضافية التي تظهر في شاشة 'المزيد' (More)
MORE_PAGES = [
    {'id': 'doctors', 'label': 'إدارة الأطباء', 'icon_data': '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-stethoscope"><path d="M11.3 4a2 2 0 0 0-1.26.68L8 7.37"/><path d="M7 11.35 5.37 9.72A2 2 0 0 0 4 8.74V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v4.74a2 2 0 0 0-.64 1.35z"/><path d="M12 18V9.74a2 2 0 0 0-2-2H6a2 2 0 0 0-2 2v1.5"/><path d="M12 18a2 2 0 0 0 2 2h2v-6"/><path d="M12 18a2 2 0 0 1-2 2h-2v-6"/><path d="M14 18h-4"/></svg>'},
    {'id': 'treatments', 'label': 'العلاجات والخدمات', 'icon_data': '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-pill"><path d="m10.5 20.5-9-9a2.83 2.83 0 1 1 4-4l9 9"/><path d="M8.27 16.27 19.5 5.04"/><path d="M18.83 7.76a3 3 0 0 1 3 3v.17a2.83 2.83 0 0 1-4 4L11.5 22.5"/><path d="m14 8-6 6"/></svg>'},
    {'id': 'suppliers', 'label': 'إدارة الموردين', 'icon_data': '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-truck"><path d="M14 18V6a2 2 0 0 0-2-2H4a2 2 0 0 0-2 2v11a1 1 0 0 0 1 1h2"/><path d="M15 18H5"/><path d="M19 18h2a1 1 0 0 0 1-1v-3.5a1 1 0 0 0-1-1h-1.5"/><path d="M19 18v-5.5"/><circle cx="7.5" cy="18.5" r="1.5"/><circle cx="17.5" cy="18.5" r="1.5"/></svg>'},
    {'id': 'expenses', 'label': 'المصروفات', 'icon_data': '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-receipt-text"><path d="M4 2v20l2-1 2 1 2-1 2 1 2-1 2 1 2-1 2 1V2l-2 1-2-1-2 1-2-1-2 1-2-1-2 1Z"/><path d="M15 11H9"/><path d="M15 15H9"/></svg>'},
    {'id': 'reports', 'label': 'التقارير والإحصاء', 'icon_data': '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-bar-chart-3"><path d="M3 3v18h18"/><path d="M18 17V9"/><path d="M13 17V5"/><path d="M8 17v-3"/></svg>'},
    {'id': 'activity_log', 'label': 'سجل الأنشطة', 'icon_data': '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-history"><path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-1.39 1.67"/><path d="M12 7v5l4 2"/><path d="M12 2v4"/><path d="M12 18v4"/><path d="M4.2 8.6c.7 1.3 1.7 2.4 2.9 3.2"/><path d="M17 14.8c1.2-.8 2.2-1.9 2.9-3.2"/></svg>'},
    {'id': 'settings', 'label': 'إعدادات النظام', 'icon_data': '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="lucide lucide-settings-2"><path d="M20 7h-9"/><path d="M14 17h-5"/><circle cx="17" cy="17" r="3"/><circle cx="7" cy="7" r="3"/></svg>'},
]


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
                    
                    # 1. بناء المحتوى البصري (الأيقونة والنص) باستخدام HTML
                    button_label_html = f"""
                    <div class='more-page-button-content'>
                        <div class='icon-svg'>{page['icon_data']}</div>
                        <div class='label'>{page['label']}</div>
                    </div>
                    """
                    
                    button_key = f"more_nav_{page['id']}"
                    
                    # 2. عرض زر Streamlit باستخدام HTML المحقون كـ label
                    if st.button(
                        label=button_label_html, 
                        key=button_key, 
                        use_container_width=True
                    ):
                        st.session_state.current_page = page['id']
                        st.rerun()

                    # حقن الـ CSS للسماح بـ HTML داخل الـ label
                    st.markdown(
                        f"<style>button[key='{button_key}'] {{ padding: 20px 10px !important; }}</style>", 
                        unsafe_allow_html=True
                    )


    st.markdown("</div>", unsafe_allow_html=True)

