import sqlite3
import pandas as pd
from datetime import datetime, date, timedelta
from .models import db # يفترض وجود ملف database/models.py يحتوي على كلاس db

class CRUDOperations:
    def __init__(self):
        self.db = db
    
    # =======================================================
    # ========== عمليات الأطباء (Doctors Operations) ==========
    # =======================================================
    def create_doctor(self, name, specialization, phone, email, address, hire_date, salary, commission_rate=0.0):
        """إضافة طبيب جديد"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO doctors (name, specialization, phone, email, address, hire_date, salary, commission_rate, is_active)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, 1)
        ''', (name, specialization, phone, email, address, hire_date, salary, commission_rate))
        
        doctor_id = cursor.lastrowid
        self.log_activity(conn, "إضافة طبيب", "doctors", doctor_id, f"تم إضافة طبيب: {name}")
        
        conn.commit()
        conn.close()
        return doctor_id
    
    def get_all_doctors(self, active_only=True):
        """الحصول على جميع الأطباء"""
        conn = self.db.get_connection()
        query = "SELECT * FROM doctors"
        if active_only:
            query += " WHERE is_active = 1"
        query += " ORDER BY name"
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    
    def get_doctor_by_id(self, doctor_id):
        """الحصول على بيانات طبيب محدد"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM doctors WHERE id = ?", (doctor_id,))
        doctor = cursor.fetchone()
        conn.close()
        return doctor

    def update_doctor(self, doctor_id, name, specialization, phone, email, address, salary, commission_rate):
        """تحديث بيانات طبيب"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE doctors SET name = ?, specialization = ?, phone = ?, email = ?, address = ?, salary = ?, commission_rate = ?
            WHERE id = ?
        ''', (name, specialization, phone, email, address, salary, commission_rate, doctor_id))
        
        self.log_activity(conn, "تحديث طبيب", "doctors", doctor_id, f"تم تحديث بيانات الطبيب: {name}")
        
        conn.commit()
        conn.close()

    def delete_doctor(self, doctor_id):
        """إلغاء تفعيل الطبيب (soft delete)"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("UPDATE doctors SET is_active = 0 WHERE id = ?", (doctor_id,))
        self.log_activity(conn, "إلغاء تفعيل طبيب", "doctors", doctor_id, f"تم إلغاء تفعيل الطبيب رقم: {doctor_id}")
        
        conn.commit()
        conn.close()

    # =======================================================
    # ========== عمليات المرضى (Patients Operations) ==========
    # =======================================================

    def create_patient(self, name, phone, email, date_of_birth, gender, blood_type, address):
        """إضافة مريض جديد"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO patients (name, phone, email, date_of_birth, gender, blood_type, address)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (name, phone, email, date_of_birth, gender, blood_type, address))
        
        patient_id = cursor.lastrowid
        self.log_activity(conn, "إضافة مريض", "patients", patient_id, f"تم إضافة مريض: {name}")
        
        conn.commit()
        conn.close()
        return patient_id

    def get_all_patients(self):
        """الحصول على جميع المرضى"""
        conn = self.db.get_connection()
        df = pd.read_sql_query("SELECT * FROM patients ORDER BY name", conn)
        conn.close()
        return df
    
    def search_patients(self, search_term):
        """البحث عن مريض"""
        conn = self.db.get_connection()
        search_term = f'%{search_term}%'
        query = """
            SELECT * FROM patients 
            WHERE name LIKE ? OR phone LIKE ? OR email LIKE ?
            ORDER BY name
        """
        df = pd.read_sql_query(query, conn, params=(search_term, search_term, search_term))
        conn.close()
        return df

    def get_patient_history(self, patient_id):
        """الحصول على سجل مواعيد ومدفوعات مريض"""
        conn = self.db.get_connection()
        
        appointments_query = """
            SELECT a.*, d.name as doctor_name, t.name as treatment_name
            FROM appointments a
            JOIN doctors d ON a.doctor_id = d.id
            JOIN treatments t ON a.treatment_id = t.id
            WHERE a.patient_id = ?
            ORDER BY a.appointment_date DESC
        """
        appointments_df = pd.read_sql_query(appointments_query, conn, params=(patient_id,))
        
        payments_query = """
            SELECT * FROM payments WHERE patient_id = ? ORDER BY payment_date DESC
        """
        payments_df = pd.read_sql_query(payments_query, conn, params=(patient_id,))
        
        conn.close()
        return {'appointments': appointments_df, 'payments': payments_df}

    # =======================================================
    # ========== عمليات العلاجات (Treatment Operations) ==========
    # =======================================================

    def create_treatment(self, name, description, cost, duration_minutes, doctor_percentage, clinic_percentage):
        """إضافة علاج جديد"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO treatments (name, description, cost, duration_minutes, doctor_percentage, clinic_percentage)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (name, description, cost, duration_minutes, doctor_percentage, clinic_percentage))
        
        treatment_id = cursor.lastrowid
        self.log_activity(conn, "إضافة علاج", "treatments", treatment_id, f"تم إضافة علاج: {name}")
        
        conn.commit()
        conn.close()
        return treatment_id

    def get_all_treatments(self):
        """الحصول على جميع العلاجات"""
        conn = self.db.get_connection()
        df = pd.read_sql_query("SELECT * FROM treatments ORDER BY name", conn)
        conn.close()
        return df

    # =======================================================
    # ========== عمليات المواعيد (Appointment Operations) ==========
    # =======================================================

    def create_appointment(self, doctor_id, patient_id, treatment_id, appointment_date, start_time, total_cost, status='مؤكد'):
        """إضافة موعد جديد"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO appointments (doctor_id, patient_id, treatment_id, appointment_date, start_time, total_cost, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (doctor_id, patient_id, treatment_id, appointment_date, start_time, total_cost, status))
        
        appointment_id = cursor.lastrowid
        self.log_activity(conn, "إضافة موعد", "appointments", appointment_id, f"موعد جديد للمريض {patient_id} مع الطبيب {doctor_id}")
        
        conn.commit()
        conn.close()
        return appointment_id

    def get_all_appointments(self, status_filter=None):
        """الحصول على جميع المواعيد مع تفاصيل الطبيب والمريض والعلاج"""
        conn = self.db.get_connection()
        query = """
            SELECT a.*, d.name AS doctor_name, p.name AS patient_name, t.name AS treatment_name
            FROM appointments a
            JOIN doctors d ON a.doctor_id = d.id
            JOIN patients p ON a.patient_id = p.id
            JOIN treatments t ON a.treatment_id = t.id
        """
        params = []
        if status_filter:
            placeholders = ','.join('?' for _ in status_filter)
            query += f" WHERE a.status IN ({placeholders})"
            params.extend(status_filter)
        
        query += " ORDER BY a.appointment_date DESC, a.start_time DESC"
        
        df = pd.read_sql_query(query, conn, params=params)
        conn.close()
        return df
    
    # =======================================================
    # ========== عمليات المدفوعات والتقسيم (Payment & Share Logic) ==========
    # =======================================================
    
    def create_payment(self, appointment_id, patient_id, amount, payment_method, payment_date, notes=""):
        """
        إضافة دفعة جديدة مع حساب تقسيم حصة الطبيب والعيادة تلقائياً.
        """
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        doctor_share = 0.0
        clinic_share = 0.0
        doctor_percentage = 0.0
        clinic_percentage = 0.0
        doctor_id = None 

        # 1. جلب تفاصيل الموعد (Doctor ID, Treatment Percentages)
        if appointment_id:
            cursor.execute('''
                SELECT 
                    a.doctor_id, 
                    a.treatment_id,
                    t.doctor_percentage, 
                    t.clinic_percentage
                FROM appointments a
                LEFT JOIN treatments t ON a.treatment_id = t.id
                WHERE a.id = ?
            ''', (appointment_id,))
            
            result = cursor.fetchone()
            
            if result and result[0] is not None:
                doctor_id = result[0]
                # استخدام النسبة من العلاج، مع قيمة افتراضية 50% إذا كانت فارغة
                doctor_percentage = result[2] if result[2] is not None else 50.0
                clinic_percentage = result[3] if result[3] is not None else 50.0
                
                # حساب حصة الطبيب والعيادة
                doctor_share = (amount * doctor_percentage) / 100
                clinic_share = amount - doctor_share 

                # 2. تحديث حالة الموعد إلى 'مكتمل'
                cursor.execute("UPDATE appointments SET status = ? WHERE id = ?", ('مكتمل', appointment_id))

            else:
                # موعد موجود لكن تفاصيل الطبيب/العلاج مفقودة
                doctor_percentage = 50.0
                clinic_percentage = 50.0
                doctor_share = amount * 0.5
                clinic_share = amount * 0.5
        else:
            # دفعة بدون موعد، تذهب للعيادة بالكامل
            doctor_percentage = 0.0
            clinic_percentage = 100.0
            doctor_share = 0.0
            clinic_share = amount
            # doctor_id يبقى None

        # 3. إدراج الدفعة
        cursor.execute('''
            INSERT INTO payments (
                appointment_id, patient_id, doctor_id, amount, payment_method, payment_date, notes,
                doctor_share, clinic_share, doctor_percentage, clinic_percentage, status
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (appointment_id, patient_id, doctor_id, amount, payment_method, payment_date, notes,
              doctor_share, clinic_share, doctor_percentage, clinic_percentage, 'مكتمل'))
        
        payment_id = cursor.lastrowid
        
        self.log_activity(conn, "إضافة دفعة", "payments", payment_id, 
                         f"تم إضافة دفعة بمبلغ {amount} - الطبيب: {doctor_share}, العيادة: {clinic_share}")
        
        conn.commit()
        conn.close()
        return payment_id
    
    def get_all_payments(self):
        """الحصول على جميع المدفوعات مع تفاصيل التقسيم والطبيب"""
        conn = self.db.get_connection()
        query = '''
            SELECT 
                pay.id,
                pay.appointment_id,
                p.name as patient_name,
                d.name as doctor_name, 
                pay.amount,
                pay.doctor_share,
                pay.clinic_share,
                pay.payment_method,
                pay.payment_date,
                pay.status,
                pay.notes
            FROM payments pay
            LEFT JOIN patients p ON pay.patient_id = p.id
            LEFT JOIN doctors d ON pay.doctor_id = d.id
            ORDER BY pay.payment_date DESC
        '''
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df

    def update_payment_status(self, payment_id, new_status):
        """تحديث حالة الدفعة."""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("UPDATE payments SET status = ? WHERE id = ?", (new_status, payment_id))
        self.log_activity(conn, "تحديث حالة دفعة", "payments", payment_id, f"تحديث حالة الدفعة {payment_id} إلى {new_status}")
        
        conn.commit()
        conn.close()
    
    # =======================================================
    # ========== عمليات المصروفات (Expenses Operations) ==========
    # =======================================================
    
    def create_expense(self, amount, category, expense_date, notes=""):
        """إضافة مصروف جديد"""
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO expenses (amount, category, expense_date, notes)
            VALUES (?, ?, ?, ?)
        ''', (amount, category, expense_date, notes))
        
        expense_id = cursor.lastrowid
        self.log_activity(conn, "إضافة مصروف", "expenses", expense_id, f"مصروف جديد بقيمة: {amount} في فئة: {category}")
        
        conn.commit()
        conn.close()
        return expense_id
    
    def get_all_expenses(self):
        """الحصول على جميع المصروفات"""
        conn = self.db.get_connection()
        df = pd.read_sql_query("SELECT * FROM expenses ORDER BY expense_date DESC", conn)
        conn.close()
        return df
    
    # =======================================================
    # ========== تقارير وإحصائيات (Reporting & Analytics) ==========
    # =======================================================

    def get_financial_summary(self, start_date=None, end_date=None):
        """الحصول على ملخص مالي مع حساب حصة العيادة وصافي الربح"""
        conn = self.db.get_connection()
        
        # إجمالي الإيرادات المحصلة وحصة العيادة والطبيب
        payments_query = "SELECT COALESCE(SUM(amount), 0) as total_payments, COALESCE(SUM(clinic_share), 0) as net_clinic_revenue, COALESCE(SUM(doctor_share), 0) as doctor_commission_cost FROM payments"
        if start_date and end_date:
            payments_query += f" WHERE payment_date BETWEEN '{start_date}' AND '{end_date}' AND status = 'مكتمل'"

        payments_summary = pd.read_sql_query(payments_query, conn).iloc[0]
        total_payments = payments_summary['total_payments']
        net_clinic_revenue = payments_summary['net_clinic_revenue']
        doctor_commission_cost = payments_summary['doctor_commission_cost']

        # إجمالي المصروفات التشغيلية
        expenses_query = "SELECT COALESCE(SUM(amount), 0) as total_expenses FROM expenses"
        if start_date and end_date:
            expenses_query += f" WHERE expense_date BETWEEN '{start_date}' AND '{end_date}'"
            
        total_expenses = pd.read_sql_query(expenses_query, conn).iloc[0]['total_expenses']

        conn.close()
        
        # صافي الربح = (إيراد حصة العيادة) - (إجمالي المصروفات)
        net_profit = net_clinic_revenue - total_expenses

        return {
            'total_revenue': total_payments,
            'net_clinic_revenue': net_clinic_revenue,
            'total_expenses': total_expenses,
            'doctor_commission_cost': doctor_commission_cost,
            'net_profit': net_profit
        }

    def get_doctor_payout_summary(self, doctor_id, start_date, end_date):
        """
        حساب إجمالي المستحقات للطبيب في فترة محددة: (العمولات + الراتب الثابت).
        """
        conn = self.db.get_connection()
        
        # 1. إجمالي العمولات
        query = """
            SELECT 
                COALESCE(SUM(doctor_share), 0) AS total_commission
            FROM payments 
            WHERE doctor_id = ? 
            AND payment_date BETWEEN ? AND ? 
            AND status = 'مكتمل'
        """
        total_commission = pd.read_sql_query(query, conn, params=(doctor_id, start_date, end_date)).iloc[0]['total_commission']
        
        # 2. الراتب الثابت
        doctor_info = self.get_doctor_by_id(doctor_id)
        # الراتب (يفترض العمود 7 في صف Doctor)
        salary = float(doctor_info[7]) if doctor_info and len(doctor_info) > 7 and doctor_info[7] is not None else 0.0

        conn.close()

        total_commission = float(total_commission) if total_commission is not None else 0.0

        return {
            'total_commission': total_commission,
            'monthly_salary': salary,
            'total_payout': total_commission + salary
        }

    def get_dashboard_stats(self):
        """الحصول على إحصائيات لوحة التحكم."""
        conn = self.db.get_connection()
        
        # مواعيد اليوم
        today = date.today().isoformat()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM appointments WHERE appointment_date = ?", (today,))
        today_appointments = cursor.fetchone()[0]

        # المصروفات لهذا الشهر
        current_month_start = date.today().replace(day=1).isoformat()
        current_month_end = date.today().isoformat()
        cursor.execute("SELECT COALESCE(SUM(amount), 0) FROM expenses WHERE expense_date BETWEEN ? AND ?", (current_month_start, current_month_end))
        current_month_expenses = cursor.fetchone()[0]
        
        # إجمالي الإيرادات هذا الشهر (حصة العيادة فقط)
        payments_query = "SELECT COALESCE(SUM(clinic_share), 0) FROM payments WHERE payment_date BETWEEN ? AND ? AND status = 'مكتمل'"
        cursor.execute(payments_query, (current_month_start, current_month_end))
        current_month_revenue = cursor.fetchone()[0]
        
        conn.close()

        return {
            'today_appointments': today_appointments,
            'current_month_revenue': current_month_revenue,
            'current_month_expenses': current_month_expenses,
            'low_stock_items': 0, 
            'expiring_items': 0
        }

    # =======================================================
    # ========== تسجيل الأنشطة (Activity Logging) ==========
    # =======================================================
    
    def log_activity(self, conn, action, table_name, record_id, details):
        """تسجيل الأنشطة (للتدقيق)."""
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO activity_log (timestamp, action, table_name, record_id, details)
            VALUES (?, ?, ?, ?, ?)
        ''', (datetime.now().isoformat(), action, table_name, record_id, details))
        
# إنشاء مثيل من عمليات CRUD
crud = CRUDOperations()
