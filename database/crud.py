# database/crud.py

import sqlite3
import pandas as pd
from datetime import datetime, date, timedelta
from .models import db

class CRUDOperations:
    def __init__(self):
        self.db = db

    # =========================
    # الأطباء
    # =========================
    def create_doctor(self, name, specialization, phone, email, address, hire_date, salary, commission_rate=0.0):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO doctors (name, specialization, phone, email, address, hire_date, salary, commission_rate)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (name, specialization, phone, email, address, hire_date, salary, commission_rate))
            doctor_id = cursor.lastrowid
            # حساب مالي
            self.create_or_update_account('doctor', doctor_id, name)
            self.log_activity(conn, "إضافة طبيب", "doctors", doctor_id, f"تم إضافة طبيب: {name}")
            conn.commit()
            return doctor_id
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def get_all_doctors(self, active_only=True):
        conn = self.db.get_connection()
        query = "SELECT * FROM doctors"
        if active_only:
            query += " WHERE is_active = 1"
        query += " ORDER BY name"
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df

    def get_doctor_by_id(self, doctor_id):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM doctors WHERE id = ?", (doctor_id,))
        res = cursor.fetchone()
        conn.close()
        return res

    def update_doctor(self, doctor_id, name, specialization, phone, email, address, salary, commission_rate):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE doctors
            SET name=?, specialization=?, phone=?, email=?, address=?, salary=?, commission_rate=?
            WHERE id=?
        ''', (name, specialization, phone, email, address, salary, commission_rate, doctor_id))
        self.log_activity(conn, "تحديث طبيب", "doctors", doctor_id, f"تم تحديث: {name}")
        conn.commit()
        conn.close()

    def delete_doctor(self, doctor_id):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE doctors SET is_active = 0 WHERE id = ?", (doctor_id,))
        self.log_activity(conn, "حذف طبيب", "doctors", doctor_id, f"تم إلغاء التفعيل")
        conn.commit()
        conn.close()

    # =========================
    # المرضى
    # =========================
    def create_patient(self, name, phone, email, address, date_of_birth, gender, medical_history="",
                       emergency_contact="", blood_type="", allergies="", notes=""):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO patients (name, phone, email, address, date_of_birth, gender, medical_history,
                                      emergency_contact, blood_type, allergies, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (name, phone, email, address, date_of_birth, gender, medical_history,
                  emergency_contact, blood_type, allergies, notes))
            patient_id = cursor.lastrowid
            self.create_or_update_account('patient', patient_id, name)
            self.log_activity(conn, "إضافة مريض", "patients", patient_id, f"تم إضافة: {name}")
            conn.commit()
            return patient_id
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def get_all_patients(self, active_only=True):
        conn = self.db.get_connection()
        query = "SELECT * FROM patients"
        if active_only:
            query += " WHERE is_active = 1"
        query += " ORDER BY name"
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df

    def get_patient_by_id(self, patient_id):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM patients WHERE id = ?", (patient_id,))
        res = cursor.fetchone()
        conn.close()
        return res

    def update_patient(self, patient_id, name, phone, email, address, date_of_birth, gender,
                       medical_history, emergency_contact, blood_type="", allergies="", notes=""):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE patients
            SET name=?, phone=?, email=?, address=?, date_of_birth=?, gender=?,
                medical_history=?, emergency_contact=?, blood_type=?, allergies=?, notes=?
            WHERE id=?
        ''', (name, phone, email, address, date_of_birth, gender,
              medical_history, emergency_contact, blood_type, allergies, notes, patient_id))
        self.log_activity(conn, "تحديث مريض", "patients", patient_id, f"تم تحديث: {name}")
        conn.commit()
        conn.close()

    def delete_patient(self, patient_id):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE patients SET is_active = 0 WHERE id = ?", (patient_id,))
        self.log_activity(conn, "حذف مريض", "patients", patient_id, f"إلغاء تفعيل")
        conn.commit()
        conn.close()

    def search_patients(self, search_term):
        conn = self.db.get_connection()
        query = '''
            SELECT * FROM patients
            WHERE is_active = 1 AND (name LIKE ? OR phone LIKE ? OR email LIKE ?)
            ORDER BY name
        '''
        like = f"%{search_term}%"
        df = pd.read_sql_query(query, conn, params=(like, like, like))
        conn.close()
        return df

    # =========================
    # العلاجات
    # =========================
    def create_treatment(self, name, description, base_price, duration_minutes, category,
                         doctor_percentage=50.0, clinic_percentage=50.0):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO treatments (name, description, base_price, duration_minutes, category,
                                    doctor_percentage, clinic_percentage)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (name, description, base_price, duration_minutes, category, doctor_percentage, clinic_percentage))
        tid = cursor.lastrowid
        self.log_activity(conn, "إضافة علاج", "treatments", tid, f"إضافة: {name}")
        conn.commit()
        conn.close()
        return tid

    def get_all_treatments(self, active_only=True):
        conn = self.db.get_connection()
        query = "SELECT * FROM treatments"
        if active_only:
            query += " WHERE is_active = 1"
        query += " ORDER BY name"
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df

    def get_treatment_by_id(self, treatment_id):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM treatments WHERE id = ?", (treatment_id,))
        res = cursor.fetchone()
        conn.close()
        return res

    def update_treatment(self, treatment_id, name, description, base_price, duration_minutes,
                         category, doctor_percentage=50.0, clinic_percentage=50.0):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE treatments
            SET name=?, description=?, base_price=?, duration_minutes=?, category=?,
                doctor_percentage=?, clinic_percentage=?
            WHERE id=?
        ''', (name, description, base_price, duration_minutes, category, doctor_percentage, clinic_percentage, treatment_id))
        self.log_activity(conn, "تحديث علاج", "treatments", treatment_id, f"تحديث: {name}")
        conn.commit()
        conn.close()

    def delete_treatment(self, treatment_id):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE treatments SET is_active = 0 WHERE id = ?", (treatment_id,))
        self.log_activity(conn, "حذف علاج", "treatments", treatment_id, f"إلغاء تفعيل")
        conn.commit()
        conn.close()

    # =========================
    # المواعيد
    # =========================
    def create_appointment(self, patient_id, doctor_id, treatment_id, appointment_date,
                           appointment_time, notes="", total_cost=0.0):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO appointments (patient_id, doctor_id, treatment_id, appointment_date,
                                          appointment_time, notes, total_cost)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (patient_id, doctor_id, treatment_id, appointment_date, appointment_time, notes, total_cost))
            appointment_id = cursor.lastrowid
            conn.commit()
            # تسجيل دين على المريض (debit)
            if total_cost and total_cost > 0:
                patient_name = pd.read_sql_query("SELECT name FROM patients WHERE id = ?", conn, params=(patient_id,)).iloc[0]['name']
                acc_id = self.create_or_update_account('patient', patient_id, patient_name)
                if acc_id:
                    self.add_financial_transaction(
                        acc_id, 'debit', total_cost,
                        f"تكلفة علاج (موعد رقم {appointment_id})",
                        'appointment', appointment_id
                    )
            self.log_activity(conn, "إضافة موعد", "appointments", appointment_id, f"موعد بتكلفة {total_cost}")
            return appointment_id
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def get_all_appointments(self):
        conn = self.db.get_connection()
        query = '''
            SELECT a.id, a.patient_id, a.doctor_id, a.treatment_id,
                   p.name as patient_name, d.name as doctor_name, t.name as treatment_name,
                   a.appointment_date, a.appointment_time, a.status, a.total_cost, a.notes
            FROM appointments a
            LEFT JOIN patients p ON a.patient_id = p.id
            LEFT JOIN doctors d ON a.doctor_id = d.id
            LEFT JOIN treatments t ON a.treatment_id = t.id
            ORDER BY a.appointment_date DESC, a.appointment_time DESC
        '''
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df

    def get_appointments_by_date(self, target_date):
        conn = self.db.get_connection()
        query = '''
            SELECT a.id, p.name as patient_name, p.phone as patient_phone,
                   d.name as doctor_name, t.name as treatment_name,
                   a.appointment_time, a.status, a.total_cost, a.notes
            FROM appointments a
            LEFT JOIN patients p ON a.patient_id = p.id
            LEFT JOIN doctors d ON a.doctor_id = d.id
            LEFT JOIN treatments t ON a.treatment_id = t.id
            WHERE a.appointment_date = ?
            ORDER BY a.appointment_time
        '''
        df = pd.read_sql_query(query, conn, params=(target_date,))
        conn.close()
        return df

    def get_doctor_schedule(self, doctor_id, target_date):
        conn = self.db.get_connection()
        query = '''
            SELECT a.id, a.appointment_time, p.name as patient_name, p.phone as patient_phone,
                   t.name as treatment_name, a.status, a.notes
            FROM appointments a
            LEFT JOIN patients p ON a.patient_id = p.id
            LEFT JOIN treatments t ON a.treatment_id = t.id
            WHERE a.doctor_id = ? AND a.appointment_date = ?
            ORDER BY a.appointment_time
        '''
        df = pd.read_sql_query(query, conn, params=(doctor_id, target_date))
        conn.close()
        return df

    def update_appointment_status(self, appointment_id, status):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE appointments SET status = ? WHERE id = ?", (status, appointment_id))
        self.log_activity(conn, "تحديث موعد", "appointments", appointment_id, f"تحديث الحالة: {status}")
        conn.commit()
        conn.close()

    def delete_appointment(self, appointment_id):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM appointments WHERE id = ?", (appointment_id,))
        self.log_activity(conn, "حذف موعد", "appointments", appointment_id, f"حذف")
        conn.commit()
        conn.close()

    def get_upcoming_appointments(self, days=7):
        conn = self.db.get_connection()
        today = date.today().isoformat()
        future = (date.today() + timedelta(days=days)).isoformat()
        query = '''
            SELECT a.id, a.appointment_date, a.appointment_time,
                   p.name as patient_name, p.phone as patient_phone,
                   d.name as doctor_name, t.name as treatment_name, a.status
            FROM appointments a
            LEFT JOIN patients p ON a.patient_id = p.id
            LEFT JOIN doctors d ON a.doctor_id = d.id
            LEFT JOIN treatments t ON a.treatment_id = t.id
            WHERE a.appointment_date BETWEEN ? AND ?
            AND a.status IN ('مجدول', 'مؤكد')
            ORDER BY a.appointment_date, a.appointment_time
        '''
        df = pd.read_sql_query(query, conn, params=(today, future))
        conn.close()
        return df

    # =========================
    # المدفوعات
    # =========================
    def create_payment(self, appointment_id, patient_id, amount, payment_method, payment_date, notes=""):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            doctor_share = clinic_share = doctor_percentage = clinic_percentage = 0.0
            doctor_id = None
            if appointment_id:
                cursor.execute('''
                    SELECT t.doctor_percentage, t.clinic_percentage, a.doctor_id
                    FROM appointments a
                    LEFT JOIN treatments t ON a.treatment_id = t.id
                    WHERE a.id = ?
                ''', (appointment_id,))
                res = cursor.fetchone()
                if res and res[0] is not None:
                    doctor_percentage, clinic_percentage, doctor_id = res
                    doctor_share = (amount * doctor_percentage) / 100.0
                    clinic_share = amount - doctor_share
                else:
                    cursor.execute("SELECT doctor_id FROM appointments WHERE id = ?", (appointment_id,))
                    dr = cursor.fetchone()
                    if dr:
                        doctor_id = dr[0]
                    doctor_share = amount * 0.5
                    clinic_share = amount * 0.5
            else:
                clinic_share = amount

            cursor.execute('''
                INSERT INTO payments (appointment_id, patient_id, amount, payment_method, payment_date, notes,
                                      doctor_share, clinic_share, doctor_percentage, clinic_percentage)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (appointment_id, patient_id, amount, payment_method, payment_date, notes,
                  doctor_share, clinic_share, doctor_percentage, clinic_percentage))
            payment_id = cursor.lastrowid
            conn.commit()

            # حركات الحسابات
            patient_name = pd.read_sql_query("SELECT name FROM patients WHERE id = ?", conn, params=(patient_id,)).iloc[0]['name']
            pat_acc = self.create_or_update_account('patient', patient_id, patient_name)
            if pat_acc:
                self.add_financial_transaction(
                    pat_acc, 'payment', amount,
                    f"دفعة (رقم {payment_id}) ل{'موعد ' + str(appointment_id) if appointment_id else 'دفعة عامة'}",
                    'payment', payment_id, payment_method, notes
                )

            if doctor_id and doctor_share > 0:
                doctor_name = pd.read_sql_query("SELECT name FROM doctors WHERE id = ?", conn, params=(doctor_id,)).iloc[0]['name']
                doc_acc = self.create_or_update_account('doctor', doctor_id, doctor_name)
                if doc_acc:
                    self.add_financial_transaction(
                        doc_acc, 'credit', doctor_share,
                        f"عمولة من دفعة {payment_id}", 'payment', payment_id, None, f"حصة من {amount}"
                    )

            clinic_acc = self.create_or_update_account('clinic', 1, 'حساب العيادة العام')
            if clinic_acc and clinic_share > 0:
                self.add_financial_transaction(
                    clinic_acc, 'credit', clinic_share,
                    f"إيراد من دفعة {payment_id}", 'payment', payment_id, None, f"حصة من {amount}"
                )

            self.log_activity(conn, "إضافة دفعة", "payments", payment_id, f"دفعة {amount} للمريض {patient_name}")
            return payment_id
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def get_all_payments(self):
        conn = self.db.get_connection()
        query = '''
            SELECT pay.id, pay.appointment_id, p.name as patient_name, pay.amount, pay.doctor_share, pay.clinic_share,
                   pay.doctor_percentage, pay.clinic_percentage, pay.payment_method, pay.payment_date, pay.status, pay.notes
            FROM payments pay
            LEFT JOIN patients p ON pay.patient_id = p.id
            ORDER BY pay.payment_date DESC
        '''
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df

    def update_payment_status(self, payment_id, status):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE payments SET status = ? WHERE id = ?", (status, payment_id))
        self.log_activity(conn, "تحديث دفعة", "payments", payment_id, f"تحديث الحالة: {status}")
        conn.commit()
        conn.close()

    def delete_payment(self, payment_id):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM payments WHERE id = ?", (payment_id,))
        self.log_activity(conn, "حذف دفعة", "payments", payment_id, "حذف")
        conn.commit()
        conn.close()

    # =========================
    # المخزون
    # =========================
    def create_inventory_item(self, item_name, category, quantity, unit_price, min_stock_level,
                              supplier_id=None, expiry_date=None, location="", barcode=""):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO inventory (item_name, category, quantity, unit_price, min_stock_level,
                                   supplier_id, expiry_date, location, barcode)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (item_name, category, quantity, unit_price, min_stock_level,
              supplier_id, expiry_date, location, barcode))
        iid = cursor.lastrowid
        self.log_activity(conn, "إضافة صنف", "inventory", iid, f"إضافة {item_name} كمية {quantity}")
        conn.commit()
        conn.close()
        return iid

    def get_all_inventory(self, active_only=True):
        conn = self.db.get_connection()
        query = '''
            SELECT i.*, s.name as supplier_name
            FROM inventory i
            LEFT JOIN suppliers s ON i.supplier_id = s.id
        '''
        if active_only:
            query += " WHERE i.is_active = 1"
        query += " ORDER BY i.item_name"
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df

    def get_low_stock_items(self):
        conn = self.db.get_connection()
        query = '''
            SELECT * FROM inventory
            WHERE quantity <= min_stock_level AND is_active = 1
            ORDER BY quantity
        '''
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df

    def get_expiring_inventory(self, days=30):
        conn = self.db.get_connection()
        query = '''
            SELECT i.item_name, i.category, i.quantity, i.expiry_date, s.name as supplier_name,
                   CAST((julianday(i.expiry_date) - julianday('now')) AS INTEGER) as days_to_expire
            FROM inventory i
            LEFT JOIN suppliers s ON i.supplier_id = s.id
            WHERE i.expiry_date IS NOT NULL AND i.is_active = 1
              AND (julianday(i.expiry_date) - julianday('now')) <= ?
            ORDER BY days_to_expire
        '''
        df = pd.read_sql_query(query, conn, params=(days,))
        conn.close()
        return df

    def update_inventory_quantity(self, item_id, quantity, operation="set"):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        if operation == "set":
            cursor.execute("UPDATE inventory SET quantity = ? WHERE id = ?", (quantity, item_id))
        elif operation == "add":
            cursor.execute("UPDATE inventory SET quantity = quantity + ? WHERE id = ?", (quantity, item_id))
        elif operation == "subtract":
            cursor.execute("UPDATE inventory SET quantity = quantity - ? WHERE id = ?", (quantity, item_id))
        self.log_activity(conn, "تحديث مخزون", "inventory", item_id, f"عملية {operation} بقيمة {quantity}")
        conn.commit()
        conn.close()

    def update_inventory_item(self, item_id, item_name, category, quantity, unit_price,
                              min_stock_level, supplier_id, expiry_date, location, barcode):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE inventory
            SET item_name=?, category=?, quantity=?, unit_price=?, min_stock_level=?,
                supplier_id=?, expiry_date=?, location=?, barcode=?
            WHERE id=?
        ''', (item_name, category, quantity, unit_price, min_stock_level,
              supplier_id, expiry_date, location, barcode, item_id))
        self.log_activity(conn, "تحديث صنف", "inventory", item_id, f"تحديث {item_name}")
        conn.commit()
        conn.close()

    def delete_inventory_item(self, item_id):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE inventory SET is_active = 0 WHERE id = ?", (item_id,))
        self.log_activity(conn, "حذف صنف", "inventory", item_id, f"إلغاء تفعيل")
        conn.commit()
        conn.close()

    # =========================
    # الموردون
    # =========================
    def create_supplier(self, name, contact_person, phone, email, address, payment_terms):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO suppliers (name, contact_person, phone, email, address, payment_terms)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (name, contact_person, phone, email, address, payment_terms))
        sid = cursor.lastrowid
        self.create_or_update_account('supplier', sid, name)
        self.log_activity(conn, "إضافة مورد", "suppliers", sid, f"إضافة {name}")
        conn.commit()
        conn.close()
        return sid

    def get_all_suppliers(self, active_only=True):
        conn = self.db.get_connection()
        query = "SELECT * FROM suppliers"
        if active_only:
            query += " WHERE is_active = 1"
        query += " ORDER BY name"
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df

    def get_supplier_by_id(self, supplier_id):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM suppliers WHERE id = ?", (supplier_id,))
        res = cursor.fetchone()
        conn.close()
        return res

    def update_supplier(self, supplier_id, name, contact_person, phone, email, address, payment_terms):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE suppliers
            SET name=?, contact_person=?, phone=?, email=?, address=?, payment_terms=?
            WHERE id=?
        ''', (name, contact_person, phone, email, address, payment_terms, supplier_id))
        self.log_activity(conn, "تحديث مورد", "suppliers", supplier_id, f"تحديث {name}")
        conn.commit()
        conn.close()

    def delete_supplier(self, supplier_id):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE suppliers SET is_active = 0 WHERE id = ?", (supplier_id,))
        self.log_activity(conn, "حذف مورد", "suppliers", supplier_id, f"إلغاء تفعيل")
        conn.commit()
        conn.close()

    def get_supplier_detailed_report(self, supplier_id):
        conn = self.db.get_connection()
        # بيانات المورد
        supq = "SELECT * FROM suppliers WHERE id = ?"
        cur = conn.cursor()
        cur.execute(supq, (supplier_id,))
        cols = [d[0] for d in cur.description]
        row = cur.fetchone()
        supplier = dict(zip(cols, row)) if row else {}

        # أصناف المورد
        itemsq = '''
            SELECT item_name, category, quantity, unit_price, (quantity*unit_price) as total_value,
                   expiry_date, location
            FROM inventory WHERE supplier_id = ? ORDER BY item_name
        '''
        items = pd.read_sql_query(itemsq, conn, params=(supplier_id,))
        total_items = len(items)
        total_value = items['total_value'].sum() if not items.empty else 0

        low_stock_q = '''
            SELECT COUNT(*) as cnt FROM inventory WHERE supplier_id=? AND quantity <= min_stock_level AND is_active=1
        '''
        low_stock = pd.read_sql_query(low_stock_q, conn, params=(supplier_id,)).iloc[0]['cnt']

        catq = '''
            SELECT category, COUNT(*) as item_count, SUM(quantity) as total_quantity, SUM(quantity*unit_price) as total_value
            FROM inventory WHERE supplier_id = ?
            GROUP BY category ORDER BY total_value DESC
        '''
        cats = pd.read_sql_query(catq, conn, params=(supplier_id,))
        conn.close()
        return {
            'supplier': supplier,
            'items': items,
            'total_items': total_items,
            'total_value': total_value,
            'low_stock_items': low_stock,
            'categories': cats
        }

    # =========================
    # المصروفات
    # =========================
    def create_expense(self, category, description, amount, expense_date, payment_method,
                       receipt_number="", notes="", approved_by="", is_recurring=False):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO expenses (category, description, amount, expense_date, payment_method,
                                  receipt_number, notes, approved_by, is_recurring)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (category, description, amount, expense_date, payment_method, receipt_number, notes, approved_by, is_recurring))
        eid = cursor.lastrowid
        self.log_activity(conn, "إضافة مصروف", "expenses", eid, f"مصروف {category} بمبلغ {amount}")
        conn.commit()
        conn.close()
        return eid

    def get_all_expenses(self):
        conn = self.db.get_connection()
        df = pd.read_sql_query("SELECT * FROM expenses ORDER BY expense_date DESC", conn)
        conn.close()
        return df

    def get_expense_by_id(self, expense_id):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM expenses WHERE id = ?", (expense_id,))
        res = cursor.fetchone()
        conn.close()
        return res

    def update_expense(self, expense_id, category, description, amount, expense_date,
                       payment_method, receipt_number, notes, approved_by, is_recurring):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE expenses
            SET category=?, description=?, amount=?, expense_date=?, payment_method=?,
                receipt_number=?, notes=?, approved_by=?, is_recurring=?
            WHERE id=?
        ''', (category, description, amount, expense_date, payment_method,
              receipt_number, notes, approved_by, is_recurring, expense_id))
        self.log_activity(conn, "تحديث مصروف", "expenses", expense_id, f"تحديث {description}")
        conn.commit()
        conn.close()

    def delete_expense(self, expense_id):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
        self.log_activity(conn, "حذف مصروف", "expenses", expense_id, "حذف")
        conn.commit()
        conn.close()

    def get_expenses_by_category(self, start_date, end_date):
        conn = self.db.get_connection()
        query = '''
            SELECT category, SUM(amount) as total, COUNT(*) as count
            FROM expenses
            WHERE expense_date BETWEEN ? AND ?
            GROUP BY category
            ORDER BY total DESC
        '''
        df = pd.read_sql_query(query, conn, params=(start_date, end_date))
        conn.close()
        return df

    # =========================
    # ملخص مالي وتقارير
    # =========================
    def get_financial_summary(self, start_date=None, end_date=None):
        conn = self.db.get_connection()
        pay_q = "SELECT COALESCE(SUM(amount), 0) as total_payments FROM payments"
        exp_q = "SELECT COALESCE(SUM(amount), 0) as total_expenses FROM expenses"
        if start_date and end_date:
            pay_q += " WHERE payment_date BETWEEN ? AND ?"
            exp_q += " WHERE expense_date BETWEEN ? AND ?"
            total_payments = pd.read_sql_query(pay_q, conn, params=(start_date, end_date)).iloc[0]['total_payments']
            total_expenses = pd.read_sql_query(exp_q, conn, params=(start_date, end_date)).iloc[0]['total_expenses']
        else:
            total_payments = pd.read_sql_query(pay_q, conn).iloc[0]['total_payments']
            total_expenses = pd.read_sql_query(exp_q, conn).iloc[0]['total_expenses']
        conn.close()
        return {
            'total_revenue': total_payments,
            'total_expenses': total_expenses,
            'net_profit': total_payments - total_expenses
        }

    def get_daily_revenue_comparison(self, days=30):
        conn = self.db.get_connection()
        query = '''
            SELECT payment_date, SUM(amount) as daily_revenue, COUNT(*) as payment_count
            FROM payments
            WHERE payment_date >= date('now', ?)
            GROUP BY payment_date
            ORDER BY payment_date
        '''
        df = pd.read_sql_query(query, conn, params=(f'-{days} days',))
        conn.close()
        return df

    def get_monthly_comparison(self, months=None):
        conn = self.db.get_connection()
        try:
            if months is None or months == 1:
                # مقارنة شهرية سريعة (قاموس)
                today = date.today()
                current_start = today.replace(day=1).isoformat()
                current_end = today.isoformat()
                last_end = (today.replace(day=1) - timedelta(days=1))
                last_start = last_end.replace(day=1).isoformat()
                last_end_iso = last_end.isoformat()
                current_revenue = pd.read_sql_query(
                    "SELECT COALESCE(SUM(amount),0) as total FROM payments WHERE payment_date BETWEEN ? AND ?",
                    conn, params=(current_start, current_end)
                ).iloc[0]['total']
                last_revenue = pd.read_sql_query(
                    "SELECT COALESCE(SUM(amount),0) as total FROM payments WHERE payment_date BETWEEN ? AND ?",
                    conn, params=(last_start, last_end_iso)
                ).iloc[0]['total']
                current_expenses = pd.read_sql_query(
                    "SELECT COALESCE(SUM(amount),0) as total FROM expenses WHERE expense_date BETWEEN ? AND ?",
                    conn, params=(current_start, current_end)
                ).iloc[0]['total']
                last_expenses = pd.read_sql_query(
                    "SELECT COALESCE(SUM(amount),0) as total FROM expenses WHERE expense_date BETWEEN ? AND ?",
                    conn, params=(last_start, last_end_iso)
                ).iloc[0]['total']
                current_appointments = pd.read_sql_query(
                    "SELECT COUNT(*) as total FROM appointments WHERE appointment_date BETWEEN ? AND ?",
                    conn, params=(current_start, current_end)
                ).iloc[0]['total']
                last_appointments = pd.read_sql_query(
                    "SELECT COUNT(*) as total FROM appointments WHERE appointment_date BETWEEN ? AND ?",
                    conn, params=(last_start, last_end_iso)
                ).iloc[0]['total']
                revenue_change = ((current_revenue - last_revenue)/last_revenue*100) if last_revenue > 0 else 0
                expenses_change = ((current_expenses - last_expenses)/last_expenses*100) if last_expenses > 0 else 0
                appointments_change = ((current_appointments - last_appointments)/last_appointments*100) if last_appointments > 0 else 0
                return {
                    'current_revenue': current_revenue,
                    'last_revenue': last_revenue,
                    'revenue_change': revenue_change,
                    'current_expenses': current_expenses,
                    'last_expenses': last_expenses,
                    'expenses_change': expenses_change,
                    'current_appointments': current_appointments,
                    'last_appointments': last_appointments,
                    'appointments_change': appointments_change,
                    'current_profit': current_revenue - current_expenses,
                    'last_profit': last_revenue - last_expenses
                }
            else:
                rev_q = '''
                    SELECT strftime('%Y-%m', payment_date) as month, SUM(amount) as revenue
                    FROM payments
                    WHERE payment_date >= date('now', ?)
                    GROUP BY month ORDER BY month
                '''
                exp_q = '''
                    SELECT strftime('%Y-%m', expense_date) as month, SUM(amount) as expenses
                    FROM expenses
                    WHERE expense_date >= date('now', ?)
                    GROUP BY month ORDER BY month
                '''
                rev_df = pd.read_sql_query(rev_q, conn, params=(f'-{months} months',))
                exp_df = pd.read_sql_query(exp_q, conn, params=(f'-{months} months',))
                result = pd.merge(rev_df, exp_df, on='month', how='outer').fillna(0)
                result['profit'] = result['revenue'] - result['expenses']
                return result
        finally:
            conn.close()

    def get_revenue_by_period(self, start_date, end_date, group_by='day'):
        conn = self.db.get_connection()
        if group_by == 'day':
            fmt = '%Y-%m-%d'
        elif group_by == 'month':
            fmt = '%Y-%m'
        elif group_by == 'year':
            fmt = '%Y'
        else:
            fmt = '%Y-%m-%d'
        query = f'''
            SELECT strftime('{fmt}', payment_date) as period, SUM(amount) as total_revenue, COUNT(*) as payment_count
            FROM payments WHERE payment_date BETWEEN ? AND ?
            GROUP BY period ORDER BY period
        '''
        df = pd.read_sql_query(query, conn, params=(start_date, end_date))
        conn.close()
        return df

    def get_doctor_performance(self, start_date, end_date):
        conn = self.db.get_connection()
        query = '''
            SELECT d.name as doctor_name, d.specialization,
                   COUNT(a.id) as total_appointments,
                   SUM(CASE WHEN a.status='مكتمل' THEN 1 ELSE 0 END) as completed_appointments,
                   COALESCE(SUM(a.total_cost), 0) as total_revenue,
                   COALESCE(AVG(a.total_cost), 0) as avg_revenue_per_appointment,
                   d.commission_rate,
                   COALESCE((SUM(a.total_cost) * d.commission_rate / 100), 0) as total_commission
            FROM doctors d
            LEFT JOIN appointments a ON d.id = a.doctor_id
                AND a.appointment_date BETWEEN ? AND ?
            WHERE d.is_active=1
            GROUP BY d.id, d.name, d.specialization, d.commission_rate
            ORDER BY total_revenue DESC
        '''
        df = pd.read_sql_query(query, conn, params=(start_date, end_date))
        conn.close()
        return df

    def get_treatment_popularity(self, start_date, end_date):
        conn = self.db.get_connection()
        query = '''
            SELECT t.name as treatment_name, t.category,
                   COUNT(a.id) as booking_count,
                   COALESCE(SUM(a.total_cost), 0) as total_revenue,
                   COALESCE(AVG(a.total_cost), 0) as avg_price
            FROM treatments t
            LEFT JOIN appointments a ON t.id = a.treatment_id
            WHERE a.appointment_date BETWEEN ? AND ?
            GROUP BY t.id, t.name, t.category
            HAVING booking_count > 0
            ORDER BY booking_count DESC
        '''
        df = pd.read_sql_query(query, conn, params=(start_date, end_date))
        conn.close()
        return df

    def get_appointment_status_stats(self, start_date, end_date):
        conn = self.db.get_connection()
        query = '''
            SELECT status, COUNT(*) as count, COALESCE(SUM(total_cost),0) as total_revenue
            FROM appointments
            WHERE appointment_date BETWEEN ? AND ?
            GROUP BY status ORDER BY count DESC
        '''
        df = pd.read_sql_query(query, conn, params=(start_date, end_date))
        conn.close()
        return df

    def get_payment_methods_stats(self, start_date, end_date):
        conn = self.db.get_connection()
        query = '''
            SELECT payment_method, COUNT(*) as count, SUM(amount) as total
            FROM payments WHERE payment_date BETWEEN ? AND ?
            GROUP BY payment_method ORDER BY total DESC
        '''
        df = pd.read_sql_query(query, conn, params=(start_date, end_date))
        conn.close()
        return df

    # =========================
    # نظام الحسابات المالي
    # =========================
    def create_or_update_account(self, account_type, holder_id, holder_name):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT id FROM accounts WHERE account_type=? AND account_holder_id=?", (account_type, holder_id))
            ex = cursor.fetchone()
            if ex:
                return ex[0]
            cursor.execute("INSERT INTO accounts (account_type, account_holder_id, account_holder_name) VALUES (?, ?, ?)",
                           (account_type, holder_id, holder_name))
            acc_id = cursor.lastrowid
            conn.commit()
            return acc_id
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def add_financial_transaction(self, account_id, transaction_type, amount,
                                  description, reference_type=None, reference_id=None,
                                  payment_method=None, notes=None):
        if not account_id:
            raise ValueError("account_id مطلوب")
        if amount <= 0:
            raise ValueError("المبلغ يجب أن يكون أكبر من صفر")

        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO financial_transactions
                (account_id, transaction_type, amount, description, reference_type, reference_id, transaction_date, payment_method, notes)
                VALUES (?, ?, ?, ?, ?, ?, date('now'), ?, ?)
            ''', (account_id, transaction_type, amount, description, reference_type, reference_id, payment_method, notes))

            cursor.execute("SELECT account_type, balance, total_dues, total_paid FROM accounts WHERE id = ?", (account_id,))
            row = cursor.fetchone()
            if not row:
                raise ValueError(f"الحساب {account_id} غير موجود")
            account_type, balance, total_dues, total_paid = row

            # حسابات حسب النوع
            if account_type == 'patient':
                if transaction_type == 'payment':
                    balance = balance + amount
                    total_paid = (total_paid or 0) + amount
                    cursor.execute("UPDATE accounts SET total_paid=?, balance=?, last_transaction_date=date('now'), updated_at=CURRENT_TIMESTAMP WHERE id=?",
                                   (total_paid, balance, account_id))
                elif transaction_type == 'debit':
                    balance = balance - amount
                    total_dues = (total_dues or 0) + amount
                    cursor.execute("UPDATE accounts SET total_dues=?, balance=?, last_transaction_date=date('now'), updated_at=CURRENT_TIMESTAMP WHERE id=?",
                                   (total_dues, balance, account_id))
            elif account_type == 'doctor':
                if transaction_type == 'credit':
                    balance = balance + amount
                    cursor.execute("UPDATE accounts SET balance=?, last_transaction_date=date('now'), updated_at=CURRENT_TIMESTAMP WHERE id=?",
                                   (balance, account_id))
                elif transaction_type == 'withdrawal':
                    balance = balance - amount
                    cursor.execute("UPDATE accounts SET balance=?, last_transaction_date=date('now'), updated_at=CURRENT_TIMESTAMP WHERE id=?",
                                   (balance, account_id))
            elif account_type == 'supplier':
                if transaction_type == 'credit':  # فاتورة لصالح المورد
                    balance = balance + amount
                elif transaction_type == 'payment':  # دفعة للمورد
                    balance = balance - amount
                cursor.execute("UPDATE accounts SET balance=?, last_transaction_date=date('now'), updated_at=CURRENT_TIMESTAMP WHERE id=?",
                               (balance, account_id))
            elif account_type == 'clinic':
                if transaction_type == 'credit':
                    balance = balance + amount
                elif transaction_type == 'debit':
                    balance = balance - amount
                cursor.execute("UPDATE accounts SET balance=?, last_transaction_date=date('now'), updated_at=CURRENT_TIMESTAMP WHERE id=?",
                               (balance, account_id))

            conn.commit()
            return True
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def get_account_statement(self, account_type, holder_id):
        conn = self.db.get_connection()
        try:
            acc_id_df = pd.read_sql_query(
                "SELECT id FROM accounts WHERE account_type=? AND account_holder_id=?",
                conn, params=(account_type, holder_id))
            if acc_id_df.empty:
                return None
            account_id = acc_id_df.iloc[0]['id']
            tx = pd.read_sql_query(
                "SELECT * FROM financial_transactions WHERE account_id=? ORDER BY transaction_date DESC, created_at DESC",
                conn, params=(account_id,))
            acc = pd.read_sql_query("SELECT * FROM accounts WHERE id=?", conn, params=(account_id,)).iloc[0].to_dict()
            return {'account': acc, 'transactions': tx}
        finally:
            conn.close()

    def get_patient_financial_summary(self, patient_id):
        conn = self.db.get_connection()
        try:
            # إجمالي تكلفة المواعيد المكتملة/المؤكدة
            total_cost = pd.read_sql_query('''
                SELECT COALESCE(SUM(total_cost),0) as total_cost
                FROM appointments WHERE patient_id=? AND status IN ('مكتمل','مؤكد')
            ''', conn, params=(patient_id,)).iloc[0]['total_cost']
            # إجمالي المدفوعات
            total_paid = pd.read_sql_query('''
                SELECT COALESCE(SUM(amount),0) as total_paid
                FROM payments WHERE patient_id=? AND status='مكتمل'
            ''', conn, params=(patient_id,)).iloc[0]['total_paid']
            outstanding = total_cost - total_paid
            return {
                'total_treatments_cost': total_cost,
                'total_paid': total_paid,
                'outstanding_balance': outstanding,
                'payment_status': 'مدفوع بالكامل' if outstanding <= 0 else f'متبقي {outstanding:.2f} ج.م'
            }
        finally:
            conn.close()

    def get_doctor_financial_summary(self, doctor_id):
        conn = self.db.get_connection()
        try:
            total_earnings = pd.read_sql_query('''
                SELECT COALESCE(SUM(p.doctor_share),0) as total_earnings
                FROM payments p JOIN appointments a ON p.appointment_id=a.id
                WHERE a.doctor_id=? AND p.status='مكتمل'
            ''', conn, params=(doctor_id,)).iloc[0]['total_earnings']
            total_withdrawn = pd.read_sql_query('''
                SELECT COALESCE(SUM(amount),0) as total_withdrawn
                FROM financial_transactions ft JOIN accounts a ON ft.account_id=a.id
                WHERE a.account_type='doctor' AND a.account_holder_id=? AND ft.transaction_type='withdrawal'
            ''', conn, params=(doctor_id,)).iloc[0]['total_withdrawn']
            current_balance = total_earnings - total_withdrawn
            monthly_earnings = pd.read_sql_query('''
                SELECT strftime('%Y-%m', p.payment_date) as month, SUM(p.doctor_share) as earnings
                FROM payments p JOIN appointments a ON p.appointment_id=a.id
                WHERE a.doctor_id=? AND p.status='مكتمل'
                GROUP BY month ORDER BY month DESC LIMIT 6
            ''', conn, params=(doctor_id,))
            return {
                'total_earnings': total_earnings,
                'total_withdrawn': total_withdrawn,
                'current_balance': current_balance,
                'monthly_earnings': monthly_earnings
            }
        finally:
            conn.close()

    def get_supplier_financial_summary(self, supplier_id):
        conn = self.db.get_connection()
        try:
            total_purchases = pd.read_sql_query('''
                SELECT COALESCE(SUM(quantity*unit_price),0) as total_purchases
                FROM inventory WHERE supplier_id=?
            ''', conn, params=(supplier_id,)).iloc[0]['total_purchases']
            # مدفوعات للمورد (من الحركات)
            total_paid = pd.read_sql_query('''
                SELECT COALESCE(SUM(ft.amount),0) as total_paid
                FROM financial_transactions ft JOIN accounts a ON ft.account_id=a.id
                WHERE a.account_type='supplier' AND a.account_holder_id=? AND ft.transaction_type='payment'
            ''', conn, params=(supplier_id,)).iloc[0]['total_paid']
            outstanding = total_purchases - total_paid
            return {
                'total_purchases': total_purchases,
                'total_paid': total_paid,
                'outstanding_balance': outstanding,
                'payment_status': 'مسدد' if outstanding <= 0 else f'متبقي {outstanding:.2f} ج.م'
            }
        finally:
            conn.close()

    def get_clinic_financial_summary(self):
        conn = self.db.get_connection()
        try:
            total_revenue = pd.read_sql_query("SELECT COALESCE(SUM(clinic_share),0) as total FROM payments WHERE status='مكتمل'", conn).iloc[0]['total']
            total_expenses = pd.read_sql_query("SELECT COALESCE(SUM(amount),0) as total FROM expenses", conn).iloc[0]['total']
            net_profit = total_revenue - total_expenses
            monthly_revenue = pd.read_sql_query('''
                SELECT strftime('%Y-%m', payment_date) as month, SUM(clinic_share) as revenue
                FROM payments WHERE status='مكتمل'
                GROUP BY month ORDER BY month DESC LIMIT 6
            ''', conn)
            return {
                'total_revenue': total_revenue,
                'total_expenses': total_expenses,
                'net_profit': net_profit,
                'monthly_revenue': monthly_revenue
            }
        finally:
            conn.close()

    def get_all_accounts_summary(self):
        conn = self.db.get_connection()
        try:
            summary = pd.read_sql_query('''
                SELECT account_type,
                       COUNT(*) as accounts_count,
                       COALESCE(SUM(total_dues),0) as total_dues,
                       COALESCE(SUM(total_paid),0) as total_paid,
                       COALESCE(SUM(balance),0) as total_balance
                FROM accounts
                GROUP BY account_type
            ''', conn)
            return summary
        finally:
            conn.close()

    # =========================
    # تقارير متقدمة
    # =========================
    def get_patient_detailed_report(self, patient_id):
        conn = self.db.get_connection()
        # معلومات المريض
        cq = conn.cursor()
        cq.execute("SELECT * FROM patients WHERE id = ?", (patient_id,))
        cols = [d[0] for d in cq.description]
        row = cq.fetchone()
        patient_data = dict(zip(cols, row)) if row else {}
        # زيارات
        visits = pd.read_sql_query('''
            SELECT COUNT(*) as total_visits,
                   COUNT(CASE WHEN status='مكتمل' THEN 1 END) as completed_visits,
                   COUNT(CASE WHEN status='ملغي' THEN 1 END) as cancelled_visits,
                   MIN(appointment_date) as first_visit,
                   MAX(appointment_date) as last_visit
            FROM appointments WHERE patient_id=?
        ''', conn, params=(patient_id,)).iloc[0].to_dict()
        appts = pd.read_sql_query('''
            SELECT a.appointment_date, a.appointment_time, d.name as doctor_name, t.name as treatment_name,
                   a.status, a.total_cost, a.notes
            FROM appointments a
            LEFT JOIN doctors d ON a.doctor_id=d.id
            LEFT JOIN treatments t ON a.treatment_id=t.id
            WHERE a.patient_id=? ORDER BY a.appointment_date DESC, a.appointment_time DESC
        ''', conn, params=(patient_id,))
        pays = pd.read_sql_query('''
            SELECT payment_date, amount, payment_method, status, notes
            FROM payments WHERE patient_id=? ORDER BY payment_date DESC
        ''', conn, params=(patient_id,))
        fin = self.get_patient_financial_summary(patient_id)
        treatments_df = pd.read_sql_query('''
            SELECT t.name as treatment_name, t.category, COUNT(*) as usage_count, SUM(a.total_cost) as total_cost,
                   MAX(a.appointment_date) as last_used
            FROM appointments a LEFT JOIN treatments t ON a.treatment_id=t.id
            WHERE a.patient_id=? GROUP BY t.id, t.name, t.category ORDER BY usage_count DESC
        ''', conn, params=(patient_id,))
        doctors_df = pd.read_sql_query('''
            SELECT d.name as doctor_name, d.specialization, COUNT(*) as visit_count, MAX(a.appointment_date) as last_visit
            FROM appointments a LEFT JOIN doctors d ON a.doctor_id=d.id
            WHERE a.patient_id=? GROUP BY d.id, d.name, d.specialization ORDER BY visit_count DESC
        ''', conn, params=(patient_id,))
        try:
            files_df = pd.read_sql_query('''
                SELECT file_name, file_type, category, upload_date, notes
                FROM patient_files WHERE patient_id=? ORDER BY upload_date DESC
            ''', conn, params=(patient_id,))
        except Exception:
            files_df = pd.DataFrame()
        conn.close()
        return {
            'patient': patient_data,
            'visits_stats': visits,
            'appointments': appts,
            'payments': pays,
            'financial_stats': fin,
            'treatments': treatments_df,
            'doctors': doctors_df,
            'files': files_df,
            'total_cost': fin['total_treatments_cost'],
            'total_paid': fin['total_paid'],
            'outstanding': fin['outstanding_balance']
        }

    def get_doctor_detailed_report(self, doctor_id, start_date=None, end_date=None):
        conn = self.db.get_connection()
        try:
            cur = conn.cursor()
            cur.execute("SELECT * FROM doctors WHERE id = ?", (doctor_id,))
            cols = [d[0] for d in cur.description]
            row = cur.fetchone()
            doc_data = dict(zip(cols, row)) if row else {}
            date_cond = ""
            params = [doctor_id]
            if start_date and end_date:
                date_cond = "AND a.appointment_date BETWEEN ? AND ?"
                params.extend([start_date, end_date])
            stats = pd.read_sql_query(f'''
                SELECT COUNT(*) as total_appointments,
                       COUNT(CASE WHEN status='مكتمل' THEN 1 END) as completed,
                       COUNT(CASE WHEN status='ملغي' THEN 1 END) as cancelled,
                       COUNT(CASE WHEN status='مجدول' THEN 1 END) as scheduled,
                       COALESCE(SUM(total_cost),0) as total_revenue,
                       COALESCE(AVG(total_cost),0) as average_revenue
                FROM appointments a WHERE doctor_id=? {date_cond}
            ''', conn, params=params).iloc[0].to_dict()
            monthly = pd.read_sql_query(f'''
                SELECT strftime('%Y-%m', appointment_date) as month, COUNT(*) as appointment_count, SUM(total_cost) as revenue
                FROM appointments WHERE doctor_id=? {date_cond}
                GROUP BY month ORDER BY month
            ''', conn, params=params)
            treatments = pd.read_sql_query(f'''
                SELECT t.name as treatment_name, t.category, COUNT(*) as count, SUM(a.total_cost) as total_revenue, AVG(a.total_cost) as avg_price
                FROM appointments a LEFT JOIN treatments t ON a.treatment_id=t.id
                WHERE a.doctor_id=? {date_cond}
                GROUP BY t.id, t.name, t.category ORDER BY count DESC
            ''', conn, params=params)
            commission_rate = doc_data.get('commission_rate', 0) if doc_data else 0
            total_commission = (stats['total_revenue'] * (commission_rate or 0)) / 100.0
            cancellation_rate = (stats['cancelled'] / stats['total_appointments'] * 100.0) if stats['total_appointments'] > 0 else 0
            completion_rate = (stats['completed'] / stats['total_appointments'] * 100.0) if stats['total_appointments'] > 0 else 0
            return {
                'doctor': doc_data,
                'appointments_stats': stats,
                'monthly_performance': monthly,
                'treatments': treatments,
                'total_commission': total_commission,
                'cancellation_rate': cancellation_rate,
                'completion_rate': completion_rate
            }
        finally:
            conn.close()

    def get_treatment_detailed_report(self, treatment_id, start_date=None, end_date=None):
        conn = self.db.get_connection()
        try:
            cur = conn.cursor()
            cur.execute("SELECT * FROM treatments WHERE id=?", (treatment_id,))
            cols = [d[0] for d in cur.description]
            row = cur.fetchone()
            tr_data = dict(zip(cols, row)) if row else {}
            date_cond = ""
            params = [treatment_id]
            if start_date and end_date:
                date_cond = "AND a.appointment_date BETWEEN ? AND ?"
                params.extend([start_date, end_date])
            usage_stats = pd.read_sql_query(f'''
                SELECT COUNT(*) as total_bookings,
                       COUNT(CASE WHEN status='مكتمل' THEN 1 END) as completed,
                       SUM(total_cost) as total_revenue,
                       AVG(total_cost) as average_price,
                       MIN(appointment_date) as first_booking,
                       MAX(appointment_date) as last_booking
                FROM appointments WHERE treatment_id=? {date_cond}
            ''', conn, params=params).iloc[0].to_dict()
            return {
                'treatment': tr_data,
                'usage_stats': usage_stats
            }
        finally:
            conn.close()

    def get_comprehensive_financial_report(self, start_date, end_date):
        conn = self.db.get_connection()
        try:
            clinic_earnings = pd.read_sql_query('''
                SELECT SUM(clinic_share) as total_clinic_earnings, SUM(doctor_share) as total_doctor_earnings, SUM(amount) as total_revenue
                FROM payments WHERE payment_date BETWEEN ? AND ?
            ''', conn, params=(start_date, end_date)).iloc[0].to_dict()
            cash_flow = pd.read_sql_query('''
                SELECT date,
                       SUM(CASE WHEN type='revenue' THEN amount ELSE 0 END) as revenue,
                       SUM(CASE WHEN type='expense' THEN amount ELSE 0 END) as expense
                FROM (
                    SELECT payment_date as date, amount, 'revenue' as type FROM payments WHERE payment_date BETWEEN ? AND ?
                    UNION ALL
                    SELECT expense_date as date, amount, 'expense' as type FROM expenses WHERE expense_date BETWEEN ? AND ?
                )
                GROUP BY date ORDER BY date
            ''', conn, params=(start_date, end_date, start_date, end_date))
            if not cash_flow.empty:
                cash_flow['net_flow'] = cash_flow['revenue'] - cash_flow['expense']
                cash_flow['cumulative'] = cash_flow['net_flow'].cumsum()
            return {
                'clinic_earnings': clinic_earnings,
                'cash_flow': cash_flow
            }
        finally:
            conn.close()

    # =========================
    # الإعدادات والأنشطة
    # =========================
    def get_setting(self, key):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT value FROM settings WHERE key = ?", (key,))
        res = cursor.fetchone()
        conn.close()
        return res[0] if res else None

    def update_setting(self, key, value):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT OR REPLACE INTO settings (key, value, updated_at) VALUES (?, ?, CURRENT_TIMESTAMP)", (key, value))
        conn.commit()
        conn.close()

    def get_all_settings(self):
        conn = self.db.get_connection()
        df = pd.read_sql_query("SELECT * FROM settings ORDER BY key", conn)
        conn.close()
        return df

    def log_activity(self, conn, action, table_name, record_id, details, user_name="النظام"):
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO activity_log (action, table_name, record_id, details, user_name)
            VALUES (?, ?, ?, ?, ?)
        ''', (action, table_name, record_id, details, user_name))

    def get_activity_log(self, limit=100):
        conn = self.db.get_connection()
        df = pd.read_sql_query(f"SELECT * FROM activity_log ORDER BY created_at DESC LIMIT {limit}", conn)
        conn.close()
        return df

    def get_dashboard_stats(self):
        conn = self.db.get_connection()
        stats = {}
        try:
            stats['total_patients'] = pd.read_sql_query("SELECT COUNT(*) as c FROM patients WHERE is_active=1", conn).iloc[0]['c']
            stats['total_doctors'] = pd.read_sql_query("SELECT COUNT(*) as c FROM doctors WHERE is_active=1", conn).iloc[0]['c']
            today = date.today().isoformat()
            stats['today_appointments'] = pd.read_sql_query("SELECT COUNT(*) as c FROM appointments WHERE appointment_date=?", conn, params=(today,)).iloc[0]['c']
            future = (date.today() + timedelta(days=7)).isoformat()
            stats['upcoming_appointments'] = pd.read_sql_query(
                "SELECT COUNT(*) as c FROM appointments WHERE appointment_date BETWEEN ? AND ? AND status IN ('مجدول','مؤكد')",
                conn, params=(today, future)).iloc[0]['c']
            stats['low_stock_items'] = pd.read_sql_query(
                "SELECT COUNT(*) as c FROM inventory WHERE quantity <= min_stock_level AND is_active=1", conn).iloc[0]['c']
            stats['expiring_items'] = pd.read_sql_query(
                "SELECT COUNT(*) as c FROM inventory WHERE expiry_date IS NOT NULL AND julianday(expiry_date)-julianday('now') <= 30 AND is_active=1",
                conn).iloc[0]['c']
        finally:
            conn.close()
        return stats

    # =========================
    # الإشعارات
    # =========================
    def create_notification(self, notification_type, title, message, priority='normal', target_date=None, related_id=None, action_link=None):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO notifications (type, title, message, priority, target_date, related_id, action_link)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (notification_type, title, message, priority, target_date, related_id, action_link))
        nid = cursor.lastrowid
        conn.commit()
        conn.close()
        return nid

    def get_unread_notifications(self, limit=10):
        conn = self.db.get_connection()
        df = pd.read_sql_query('''
            SELECT * FROM notifications WHERE is_read = 0
            ORDER BY
                CASE priority
                    WHEN 'urgent' THEN 1
                    WHEN 'high' THEN 2
                    WHEN 'normal' THEN 3
                    WHEN 'low' THEN 4
                END, created_at DESC
            LIMIT ?
        ''', conn, params=(limit,))
        conn.close()
        return df

    def get_all_notifications(self, limit=50):
        conn = self.db.get_connection()
        df = pd.read_sql_query(f"SELECT * FROM notifications ORDER BY created_at DESC LIMIT {limit}", conn)
        conn.close()
        return df

    def mark_notification_as_read(self, notification_id):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE notifications SET is_read=1 WHERE id=?", (notification_id,))
        conn.commit()
        conn.close()

    def mark_all_notifications_as_read(self):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE notifications SET is_read=1 WHERE is_read=0")
        conn.commit()
        conn.close()

    def delete_notification(self, notification_id):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM notifications WHERE id=?", (notification_id,))
        conn.commit()
        conn.close()

    def generate_daily_notifications(self):
        today = date.today().isoformat()
        # مواعيد اليوم
        appts = self.get_appointments_by_date(today)
        if not appts.empty:
            self.create_notification('appointment', 'مواعيد اليوم', f"لديك {len(appts)} موعد اليوم", 'high', today, None, 'appointments')
        # مخزون منخفض
        low = self.get_low_stock_items()
        if not low.empty:
            for _, it in low.iterrows():
                self.create_notification('inventory', 'تنبيه مخزون منخفض',
                                         f"الصنف '{it['item_name']}' وصل للحد الأدنى (الكمية: {it['quantity']})",
                                         'urgent', today, it['id'], 'inventory')
        # أصناف قريبة الانتهاء
        exp = self.get_expiring_inventory(days=30)
        if not exp.empty:
            for _, it in exp.head(5).iterrows():
                self.create_notification('inventory', 'تنبيه انتهاء صلاحية',
                                         f"الصنف '{it['item_name']}' ينتهي خلال {it['days_to_expire']} يوم",
                                         'high', today, None, 'inventory')

# إنشاء مثيل
crud = CRUDOperations()