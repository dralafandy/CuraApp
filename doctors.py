# doctors.py

import streamlit as st
import pandas as pd
from datetime import date
from database.crud import crud
# تتطلب هذه المكتبة: pip install python-dateutil
from dateutil.relativedelta import relativedelta 

def render():
    """صفحة إدارة الأطباء"""
    st.markdown("## 👨‍⚕️ إدارة الأطباء")
    
    # إضافة علامة تبويب تقرير الدفعات
    tab1, tab2, tab3 = st.tabs(["📋 قائمة الأطباء", "➕ إضافة طبيب جديد", "💸 تقرير مستحقات طبيب"])

    with tab1:
        render_doctor_list()

    with tab2:
        render_add_doctor()
    
    with tab3:
        render_doctor_payout_report()

# =======================================================
# ========== عرض قائمة الأطباء وتعديلهم ==========
# =======================================================
def render_doctor_list():
    """عرض جميع الأطباء"""
    st.markdown("### 📋 قائمة الأطباء")
    doctors = crud.get_all_doctors()
    if not doctors.empty:
        st.dataframe(
            doctors[['id', 'name', 'specialization', 'phone', 'email', 'salary', 'commission_rate']],
            use_container_width=True,
            hide_index=True,
            column_rename={
                'name': 'الاسم', 'specialization': 'التخصص', 'phone': 'الهاتف', 
                'email': 'البريد الإلكتروني', 'salary': 'الراتب', 'commission_rate': 'عمولة %'
            }
        )
        with st.expander("🛠 تحديث بيانات طبيب"):
            selected_id = st.number_input("رقم الطبيب", min_value=1, step=1, key='update_doc_id')
            doctor = crud.get_doctor_by_id(selected_id)
            if doctor:
                # ترتيب الأعمدة: 1: name, 2: specialization, 3: phone, 4: email, 5: address, 7: salary, 8: commission_rate
                name = st.text_input("الاسم", doctor[1], key='up_name')
                spec = st.text_input("التخصص", doctor[2], key='up_spec')
                phone = st.text_input("الهاتف", doctor[3], key='up_phone')
                email = st.text_input("البريد الإلكتروني", doctor[4], key='up_email')
                address = st.text_input("العنوان", doctor[5], key='up_address')
                salary = st.number_input("الراتب", float(doctor[7]), key='up_salary', min_value=0.0)
                commission = st.number_input("نسبة العمولة %", float(doctor[8]), key='up_commission', min_value=0.0, max_value=100.0, step=1.0)
                
                if st.button("حفظ التحديث"):
                    try:
                        crud.update_doctor(selected_id, name, spec, phone, email, address, salary, commission)
                        st.success("✅ تم تحديث بيانات الطبيب بنجاح.")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ خطأ: {e}")
                
                if st.button("🗑 إلغاء تفعيل الطبيب"):
                    crud.delete_doctor(selected_id)
                    st.success("🚫 تم إلغاء تفعيل الطبيب")
                    st.rerun()
            else:
                st.warning("لم يتم العثور على الطبيب")
    else:
        st.info("لا يوجد أطباء في النظام حالياً.")

# =======================================================
# ========== إضافة طبيب جديد ==========
# =======================================================
def render_add_doctor():
    """إضافة طبيب جديد"""
    st.markdown("### ➕ إضافة طبيب جديد")
    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input("اسم الطبيب *", key='add_name')
        specialization = st.text_input("التخصص *", key='add_spec')
        phone = st.text_input("رقم الهاتف", key='add_phone')
        salary = st.number_input("الراتب الأساسي", min_value=0.0, step=100.0, key='add_salary')
    
    with col2:
        email = st.text_input("البريد الإلكتروني", key='add_email')
        address = st.text_input("العنوان", key='add_address')
        hire_date = st.date_input("تاريخ التعيين", value=date.today(), key='add_hire_date')
        commission_rate = st.number_input("نسبة العمولة %", min_value=0.0, max_value=100.0, step=1.0, key='add_commission')

    if st.button("💾 حفظ الطبيب", type="primary", use_container_width=True):
        if name and specialization:
            crud.create_doctor(
                name, specialization, phone, email, address, hire_date.isoformat(), salary, commission_rate
            )
            st.success(f"✅ تم حفظ الطبيب: {name}")
            st.rerun()
        else:
            st.error("الرجاء إدخال الاسم والتخصص على الأقل.")

# =======================================================
# ========== تقرير مستحقات الطبيب (عمولات + راتب) ==========
# =======================================================
def render_doctor_payout_report():
    """عرض تقرير الدفعات (العمولات + الراتب) لطبيب معين"""
    st.markdown("### 💸 تقرير مستحقات الطبيب")

    doctors = crud.get_all_doctors(active_only=True)
    if doctors.empty:
        st.info("لا يوجد أطباء نشطون لإصدار التقرير.")
        return

    # إنشاء خريطة للاختيار
    doctor_map = {f"{row['name']} ({row['specialization']})": row['id'] for index, row in doctors.iterrows()}
    
    selected_doctor_name = st.selectbox("اختر الطبيب", options=list(doctor_map.keys()), key='payout_doctor_select')
    
    if selected_doctor_name:
        selected_doctor_id = doctor_map[selected_doctor_name]

        # اختيار فترة التقرير
        col1, col2 = st.columns(2)
        today = date.today()
        
        with col1:
            # افتراضيًا: بداية الشهر الحالي
            start_date = st.date_input("من تاريخ", value=today.replace(day=1), key='payout_start_date') 
        with col2:
            end_date = st.date_input("حتى تاريخ", value=today, key='payout_end_date')

        if start_date > end_date:
            st.error("⚠️ تاريخ البداية لا يمكن أن يكون بعد تاريخ النهاية.")
            return

        if st.button("📊 استعراض التقرير", type="primary"):
            try:
                summary = crud.get_doctor_payout_summary(start_date=start_date.isoformat(), end_date=end_date.isoformat(), doctor_id=selected_doctor_id)

                st.markdown("#### ملخص مستحقات الطبيب")
                
                # عرض المقاييس المالية
                col_metrics = st.columns(3)
                with col_metrics[0]:
                    st.metric(
                        label="إجمالي العمولات المستحقة", 
                        value=f"{summary['total_commission']:,.2f} ج.م", 
                        help="مجموع حصة الطبيب من المدفوعات المكتملة في الفترة المحددة."
                    )
                with col_metrics[1]:
                    st.metric(
                        label="الراتب الأساسي الشهري", 
                        value=f"{summary['monthly_salary']:,.2f} ج.م", 
                        help="الراتب الشهري الثابت للطبيب."
                    )
                with col_metrics[2]:
                    # إجمالي المبلغ المستحق (الراتب + العمولات)
                    st.metric(
                        label="إجمالي المستحقات (الدفعية)", 
                        value=f"{summary['total_payout']:,.2f} ج.م", 
                        delta="مجموع العمولة والراتب الأساسي لفترة التقرير.",
                        delta_color="normal"
                    )
                
                st.success("⚠️ ملاحظة: العمولات محسوبة بناءً على نسبة العلاج المخصص للطبيب من قيمة الدفعة المحصلة، بالإضافة إلى الراتب الثابت.")
            except Exception as e:
                st.error(f"❌ حدث خطأ أثناء إعداد التقرير: {e}")
