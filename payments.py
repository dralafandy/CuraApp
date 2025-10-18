# payments.py

import streamlit as st
import pandas as pd
from datetime import date
from database.crud import crud
from database.models import db # لافتراض الاتصال بقاعدة البيانات

def render():
    """صفحة إدارة المدفوعات"""
    st.markdown("## 💰 إدارة المدفوعات")
    
    tab1, tab2, tab3 = st.tabs(["📋 جميع المدفوعات", "➕ تسجيل دفعة", "📊 تقارير مالية قصيرة"])
    
    with tab1:
        render_all_payments()
    
    with tab2:
        render_add_payment()
    
    with tab3:
        render_payment_summary()

# =======================================================
# ========== عرض جميع المدفوعات ==========
# =======================================================
def render_all_payments():
    """عرض المدفوعات"""
    st.markdown("### 📋 جميع المدفوعات والتقسيم")
    payments = crud.get_all_payments()
    if not payments.empty:
        st.dataframe(
            payments[['id', 'patient_name', 'doctor_name', 'amount', 'doctor_share', 'clinic_share', 
                      'payment_method', 'payment_date', 'status']],
            use_container_width=True,
            hide_index=True,
            column_rename={
                'doctor_share': 'حصة الطبيب', 'clinic_share': 'حصة العيادة', 'amount': 'قيمة الدفع', 
                'patient_name': 'المريض', 'doctor_name': 'الطبيب', 'payment_method': 'طريقة الدفع', 
                'payment_date': 'التاريخ', 'status': 'الحالة'
            }
        )
        with st.expander("🔄 تحديث حالة دفعة"):
            payment_id = st.number_input("رقم الدفعة", min_value=1, step=1, key='update_payment_id')
            new_status = st.selectbox("الحالة الجديدة", ["مكتمل", "ملغي", "معلق"], key='update_payment_status')
            if st.button("تحديث الحالة"):
                try:
                    crud.update_payment_status(payment_id, new_status)
                    st.success("✅ تم التحديث")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ خطأ: {e}")
    else:
        st.info("لا توجد مدفوعات مسجلة.")

# =======================================================
# ========== تسجيل دفعة جديدة (مع ربط بالموعد) ==========
# =======================================================
def get_pending_appointments():
    """وظيفة مساعدة لجلب المواعيد غير المكتملة الدفع."""
    conn = db.get_connection()
    query = """
        SELECT 
            a.id, 
            a.total_cost, 
            a.patient_id, 
            p.name AS patient_name,
            d.name AS doctor_name,
            t.name AS treatment_name
        FROM appointments a
        JOIN patients p ON a.patient_id = p.id
        JOIN doctors d ON a.doctor_id = d.id
        JOIN treatments t ON a.treatment_id = t.id
        WHERE a.status IN ('مجدول', 'مؤكد', 'قيد التنفيذ') 
        ORDER BY a.appointment_date, a.start_time
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def render_add_payment():
    """نموذج تسجيل دفعة جديدة (محدث ليختار الموعد أولاً)"""
    st.markdown("### ➕ تسجيل دفعة جديدة")
    
    pending_appointments = get_pending_appointments() 
    
    if pending_appointments.empty:
        st.info("👍 لا توجد مواعيد معلقة تتطلب دفعات حالياً.")
        return

    # إنشاء خيار عرض لسهولة الاختيار
    pending_appointments['display'] = pending_appointments.apply(
        lambda row: f"#{row['id']} | المريض: {row['patient_name']} | العلاج: {row['treatment_name']} | التكلفة: {row['total_cost']:,.0f}", axis=1)

    # 1. اختيار الموعد
    appointment_option = st.selectbox(
        "اختر الموعد المطلوب سداد دفعته *",
        options=[''] + pending_appointments['display'].tolist(),
        index=0,
        key='payment_appointment_select'
    )

    appointment_id = None
    patient_id = None
    if appointment_option:
        # استخراج رقم الموعد وتفاصيله
        appointment_id = int(appointment_option.split(' | ')[0].replace('#', ''))
        selected_details = pending_appointments[pending_appointments['id'] == appointment_id].iloc[0]
        patient_id = selected_details['patient_id']
        
        st.info(f"""
            **💰 تكلفة الموعد الإجمالية:** {selected_details['total_cost']:,.0f} ج.م | 
            **الطبيب:** {selected_details['doctor_name']}
        """)
        
        # 2. إدخال تفاصيل الدفعة
        col1, col2 = st.columns(2)
        with col1:
            amount = st.number_input("قيمة الدفعة المسددة *", min_value=0.0, step=10.0, 
                                     value=float(selected_details['total_cost']), key='payment_amount')
            payment_method = st.selectbox("طريقة الدفع *", ["نقدي", "بطاقة ائتمان", "تحويل بنكي", "شيك"], key='payment_method')
        
        with col2:
            payment_date = st.date_input("تاريخ الدفع", value=date.today(), key='payment_date')
            st.markdown(f"**رقم المريض (للتأكيد):** `{patient_id}`")
            
        notes = st.text_area("ملاحظات الدفعة")
        
        if st.button("💾 حفظ الدفعة وتسجيل الإيراد", type="primary"):
            try:
                if amount > 0 and appointment_id and patient_id:
                    crud.create_payment(
                        appointment_id,
                        patient_id,
                        amount,
                        payment_method,
                        payment_date.isoformat(),
                        notes
                    )
                    st.success(f"✅ تم حفظ الدفعة بنجاح! تم توزيع الإيراد تلقائياً.")
                    st.balloons()
                    st.rerun()
                else:
                    st.warning("⚠️ تأكد من قيمة الدفعة الصحيحة.")
            except Exception as e:
                st.error(f"❌ خطأ في تسجيل الدفعة: {e}")
    else:
         st.info("يرجى اختيار موعد لإدخال بيانات الدفعة.")

# =======================================================
# ========== ملخص الإيرادات والمصروفات ==========
# =======================================================
def render_payment_summary():
    """عرض ملخص مالي سريع (محدث)"""
    st.markdown("### 📊 ملخص إيرادات ومصروفات سريعة")
    
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("من تاريخ", value=date.today().replace(day=1), key='summary_start_date')
    with col2:
        end_date = st.date_input("حتى تاريخ", value=date.today(), key='summary_end_date')
    
    if start_date > end_date:
        st.warning("⚠️ التاريخ غير منطقي")
        return
    
    if st.button("استعراض الملخص", key='btn_financial_summary', type='secondary'):
        summary = crud.get_financial_summary(start_date.isoformat(), end_date.isoformat())
        
        st.markdown("---")
        
        col1, col2, col3, col4 = st.columns(4)
        
        # 1. الإيرادات الإجمالية
        with col1:
            st.metric(
                label="إجمالي الإيرادات المحصلة", 
                value=f"{summary['total_revenue']:,.2f} ج.م",
                help="إجمالي المبالغ التي دفعها المرضى."
            )
        # 2. حصة العيادة الصافية
        with col2:
            st.metric(
                label="صافي إيراد العيادة", 
                value=f"{summary['net_clinic_revenue']:,.2f} ج.م",
                help="الإيرادات الإجمالية بعد خصم حصص الأطباء."
            )
        # 3. المصروفات التشغيلية
        with col3:
            st.metric(
                label="إجمالي المصروفات التشغيلية", 
                value=f"{summary['total_expenses']:,.2f} ج.م",
                delta_color="inverse"
            )
        # 4. صافي الربح الكلي
        with col4:
            net_profit_value = summary['net_profit']
            st.metric(
                label="صافي الربح الكلي", 
                value=f"{net_profit_value:,.2f} ج.م",
                delta=f"{'▲' if net_profit_value >= 0 else '▼'} ",
                delta_color="normal" if net_profit_value >= 0 else "inverse"
            )
        
        st.markdown(f"**تكلفة عمولات الأطباء المدفوعة:** `{summary['doctor_commission_cost']:,.2f} ج.م` (تعتبر تكلفة تشغيلية على العيادة)")
