"""
Database Validation Module for Cura Clinic App
Provides comprehensive data validation and integrity checks
"""

import sqlite3
import pandas as pd
from datetime import datetime, date
from .models import db

class DataValidator:
    """Data validation and integrity checking class"""

    def __init__(self):
        self.db = db

    def validate_foreign_keys(self):
        """Validate all foreign key relationships in the database"""
        issues = []

        try:
            conn = self.db.get_connection()

            # Check appointments foreign keys
            issues.extend(self._check_appointments_references(conn))

            # Check payments foreign keys
            issues.extend(self._check_payments_references(conn))

            # Check inventory foreign keys
            issues.extend(self._check_inventory_references(conn))

            # Check inventory_usage foreign keys
            issues.extend(self._check_inventory_usage_references(conn))

            conn.close()

        except Exception as e:
            issues.append(f"Error during foreign key validation: {str(e)}")

        return issues

    def _check_appointments_references(self, conn):
        """Check appointments table foreign key references"""
        issues = []

        # Check patient_id references
        query = """
            SELECT a.id, a.patient_id, p.name
            FROM appointments a
            LEFT JOIN patients p ON a.patient_id = p.id
            WHERE p.id IS NULL OR p.is_active = 0
        """
        orphaned = pd.read_sql_query(query, conn)
        if not orphaned.empty:
            for _, row in orphaned.iterrows():
                issues.append({
                    'table': 'appointments',
                    'record_id': row['id'],
                    'issue': f"Invalid patient_id {row['patient_id']} - patient not found or inactive",
                    'severity': 'high'
                })

        # Check doctor_id references
        query = """
            SELECT a.id, a.doctor_id, d.name
            FROM appointments a
            LEFT JOIN doctors d ON a.doctor_id = d.id
            WHERE d.id IS NULL OR d.is_active = 0
        """
        orphaned = pd.read_sql_query(query, conn)
        if not orphaned.empty:
            for _, row in orphaned.iterrows():
                issues.append({
                    'table': 'appointments',
                    'record_id': row['id'],
                    'issue': f"Invalid doctor_id {row['doctor_id']} - doctor not found or inactive",
                    'severity': 'high'
                })

        # Check treatment_id references (nullable)
        query = """
            SELECT a.id, a.treatment_id, t.name
            FROM appointments a
            LEFT JOIN treatments t ON a.treatment_id = t.id
            WHERE a.treatment_id IS NOT NULL AND (t.id IS NULL OR t.is_active = 0)
        """
        orphaned = pd.read_sql_query(query, conn)
        if not orphaned.empty:
            for _, row in orphaned.iterrows():
                issues.append({
                    'table': 'appointments',
                    'record_id': row['id'],
                    'issue': f"Invalid treatment_id {row['treatment_id']} - treatment not found or inactive",
                    'severity': 'medium'
                })

        return issues

    def _check_payments_references(self, conn):
        """Check payments table foreign key references"""
        issues = []

        # Check appointment_id references (nullable)
        query = """
            SELECT p.id, p.appointment_id
            FROM payments p
            LEFT JOIN appointments a ON p.appointment_id = a.id
            WHERE p.appointment_id IS NOT NULL AND a.id IS NULL
        """
        orphaned = pd.read_sql_query(query, conn)
        if not orphaned.empty:
            for _, row in orphaned.iterrows():
                issues.append({
                    'table': 'payments',
                    'record_id': row['id'],
                    'issue': f"Invalid appointment_id {row['appointment_id']} - appointment not found",
                    'severity': 'medium'
                })

        # Check patient_id references
        query = """
            SELECT p.id, p.patient_id, pat.name
            FROM payments p
            LEFT JOIN patients pat ON p.patient_id = pat.id
            WHERE pat.id IS NULL OR pat.is_active = 0
        """
        orphaned = pd.read_sql_query(query, conn)
        if not orphaned.empty:
            for _, row in orphaned.iterrows():
                issues.append({
                    'table': 'payments',
                    'record_id': row['id'],
                    'issue': f"Invalid patient_id {row['patient_id']} - patient not found or inactive",
                    'severity': 'high'
                })

        return issues

    def _check_inventory_references(self, conn):
        """Check inventory table foreign key references"""
        issues = []

        # Check supplier_id references (nullable)
        query = """
            SELECT i.id, i.supplier_id, s.name
            FROM inventory i
            LEFT JOIN suppliers s ON i.supplier_id = s.id
            WHERE i.supplier_id IS NOT NULL AND (s.id IS NULL OR s.is_active = 0)
        """
        orphaned = pd.read_sql_query(query, conn)
        if not orphaned.empty:
            for _, row in orphaned.iterrows():
                issues.append({
                    'table': 'inventory',
                    'record_id': row['id'],
                    'issue': f"Invalid supplier_id {row['supplier_id']} - supplier not found or inactive",
                    'severity': 'medium'
                })

        return issues

    def _check_inventory_usage_references(self, conn):
        """Check inventory_usage table foreign key references"""
        issues = []

        # Check inventory_id references
        query = """
            SELECT iu.id, iu.inventory_id, i.item_name
            FROM inventory_usage iu
            LEFT JOIN inventory i ON iu.inventory_id = i.id
            WHERE i.id IS NULL OR i.is_active = 0
        """
        orphaned = pd.read_sql_query(query, conn)
        if not orphaned.empty:
            for _, row in orphaned.iterrows():
                issues.append({
                    'table': 'inventory_usage',
                    'record_id': row['id'],
                    'issue': f"Invalid inventory_id {row['inventory_id']} - inventory item not found or inactive",
                    'severity': 'high'
                })

        # Check appointment_id references (nullable)
        query = """
            SELECT iu.id, iu.appointment_id
            FROM inventory_usage iu
            LEFT JOIN appointments a ON iu.appointment_id = a.id
            WHERE iu.appointment_id IS NOT NULL AND a.id IS NULL
        """
        orphaned = pd.read_sql_query(query, conn)
        if not orphaned.empty:
            for _, row in orphaned.iterrows():
                issues.append({
                    'table': 'inventory_usage',
                    'record_id': row['id'],
                    'issue': f"Invalid appointment_id {row['appointment_id']} - appointment not found",
                    'severity': 'medium'
                })

        return issues

    def validate_data_consistency(self):
        """Validate data consistency across tables"""
        issues = []

        try:
            conn = self.db.get_connection()

            # Check payment amounts match appointment costs
            issues.extend(self._check_payment_appointment_consistency(conn))

            # Check inventory quantities are not negative
            issues.extend(self._check_inventory_quantities(conn))

            # Check appointment dates are not in the past (for future appointments)
            issues.extend(self._check_appointment_dates(conn))

            # Check doctor commission rates are reasonable
            issues.extend(self._check_doctor_commissions(conn))

            conn.close()

        except Exception as e:
            issues.append(f"Error during data consistency validation: {str(e)}")

        return issues

    def _check_payment_appointment_consistency(self, conn):
        """Check that payments match appointment costs"""
        issues = []

        query = """
            SELECT
                p.id as payment_id,
                p.amount,
                p.appointment_id,
                a.total_cost,
                a.patient_id
            FROM payments p
            LEFT JOIN appointments a ON p.appointment_id = a.id
            WHERE p.appointment_id IS NOT NULL
        """
        data = pd.read_sql_query(query, conn)

        for _, row in data.iterrows():
            if abs(row['amount'] - row['total_cost']) > 0.01:  # Allow small rounding differences
                issues.append({
                    'table': 'payments',
                    'record_id': row['payment_id'],
                    'issue': f"Payment amount {row['amount']} doesn't match appointment cost {row['total_cost']}",
                    'severity': 'low'
                })

        return issues

    def _check_inventory_quantities(self, conn):
        """Check inventory quantities are valid"""
        issues = []

        query = "SELECT id, item_name, quantity FROM inventory WHERE quantity < 0"
        negative_qty = pd.read_sql_query(query, conn)

        if not negative_qty.empty:
            for _, row in negative_qty.iterrows():
                issues.append({
                    'table': 'inventory',
                    'record_id': row['id'],
                    'issue': f"Negative quantity {row['quantity']} for item '{row['item_name']}'",
                    'severity': 'high'
                })

        return issues

    def _check_appointment_dates(self, conn):
        """Check appointment dates are reasonable"""
        issues = []

        today = date.today().isoformat()

        # Find appointments with past dates that are still scheduled
        query = f"""
            SELECT id, appointment_date, status
            FROM appointments
            WHERE appointment_date < '{today}'
            AND status IN ('مجدول', 'مؤكد')
        """
        past_scheduled = pd.read_sql_query(query, conn)

        if not past_scheduled.empty:
            for _, row in past_scheduled.iterrows():
                issues.append({
                    'table': 'appointments',
                    'record_id': row['id'],
                    'issue': f"Past appointment date {row['appointment_date']} still has status '{row['status']}'",
                    'severity': 'medium'
                })

        return issues

    def _check_doctor_commissions(self, conn):
        """Check doctor commission rates are reasonable"""
        issues = []

        query = "SELECT id, name, commission_rate FROM doctors WHERE commission_rate < 0 OR commission_rate > 100"
        invalid_rates = pd.read_sql_query(query, conn)

        if not invalid_rates.empty:
            for _, row in invalid_rates.iterrows():
                issues.append({
                    'table': 'doctors',
                    'record_id': row['id'],
                    'issue': f"Invalid commission rate {row['commission_rate']}% for doctor '{row['name']}'",
                    'severity': 'medium'
                })

        return issues

    def validate_before_operation(self, operation_type, table_name, data):
        """Validate data before database operations"""
        issues = []

        if operation_type == 'create':
            issues.extend(self._validate_create_data(table_name, data))
        elif operation_type == 'update':
            issues.extend(self._validate_update_data(table_name, data))
        elif operation_type == 'delete':
            issues.extend(self._validate_delete_data(table_name, data))

        return issues

    def _validate_create_data(self, table_name, data):
        """Validate data before create operations"""
        issues = []

        if table_name == 'appointments':
            issues.extend(self._validate_appointment_data(data))
        elif table_name == 'payments':
            issues.extend(self._validate_payment_data(data))
        elif table_name == 'inventory':
            issues.extend(self._validate_inventory_data(data))

        return issues

    def _validate_update_data(self, table_name, data):
        """Validate data before update operations"""
        issues = []

        # For updates, we need to check if the record exists and validate the new data
        if 'id' not in data:
            issues.append(f"Missing 'id' field for {table_name} update")
            return issues

        # Check if record exists
        if not self._record_exists(table_name, data['id']):
            issues.append(f"Record with id {data['id']} does not exist in {table_name}")
            return issues

        # Validate the data
        issues.extend(self._validate_create_data(table_name, data))

        return issues

    def _validate_delete_data(self, table_name, data):
        """Validate data before delete operations"""
        issues = []

        if 'id' not in data:
            issues.append(f"Missing 'id' field for {table_name} delete")
            return issues

        # Check if record exists
        if not self._record_exists(table_name, data['id']):
            issues.append(f"Record with id {data['id']} does not exist in {table_name}")
            return issues

        # Check for dependent records
        dependent_issues = self._check_dependent_records(table_name, data['id'])
        issues.extend(dependent_issues)

        return issues

    def _validate_appointment_data(self, data):
        """Validate appointment data"""
        issues = []

        required_fields = ['patient_id', 'doctor_id', 'appointment_date', 'appointment_time']
        for field in required_fields:
            if field not in data or not data[field]:
                issues.append(f"Missing required field: {field}")

        # Validate foreign keys
        if 'patient_id' in data and not self._record_exists('patients', data['patient_id'], active_only=True):
            issues.append(f"Invalid patient_id: {data['patient_id']}")

        if 'doctor_id' in data and not self._record_exists('doctors', data['doctor_id'], active_only=True):
            issues.append(f"Invalid doctor_id: {data['doctor_id']}")

        if 'treatment_id' in data and data['treatment_id'] and not self._record_exists('treatments', data['treatment_id'], active_only=True):
            issues.append(f"Invalid treatment_id: {data['treatment_id']}")

        # Validate date format
        if 'appointment_date' in data:
            try:
                date.fromisoformat(data['appointment_date'])
            except ValueError:
                issues.append(f"Invalid date format for appointment_date: {data['appointment_date']}")

        return issues

    def _validate_payment_data(self, data):
        """Validate payment data"""
        issues = []

        required_fields = ['patient_id', 'amount', 'payment_method', 'payment_date']
        for field in required_fields:
            if field not in data or not data[field]:
                issues.append(f"Missing required field: {field}")

        # Validate amount is positive
        if 'amount' in data and data['amount'] <= 0:
            issues.append(f"Payment amount must be positive: {data['amount']}")

        # Validate foreign keys
        if 'patient_id' in data and not self._record_exists('patients', data['patient_id'], active_only=True):
            issues.append(f"Invalid patient_id: {data['patient_id']}")

        if 'appointment_id' in data and data['appointment_id'] and not self._record_exists('appointments', data['appointment_id']):
            issues.append(f"Invalid appointment_id: {data['appointment_id']}")

        return issues

    def _validate_inventory_data(self, data):
        """Validate inventory data"""
        issues = []

        required_fields = ['item_name', 'quantity', 'unit_price']
        for field in required_fields:
            if field not in data or data[field] is None:
                issues.append(f"Missing required field: {field}")

        # Validate quantity and price are non-negative
        if 'quantity' in data and data['quantity'] < 0:
            issues.append(f"Quantity cannot be negative: {data['quantity']}")

        if 'unit_price' in data and data['unit_price'] < 0:
            issues.append(f"Unit price cannot be negative: {data['unit_price']}")

        # Validate supplier if provided
        if 'supplier_id' in data and data['supplier_id'] and not self._record_exists('suppliers', data['supplier_id'], active_only=True):
            issues.append(f"Invalid supplier_id: {data['supplier_id']}")

        return issues

    def _record_exists(self, table_name, record_id, active_only=False):
        """Check if a record exists in the database"""
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()

            query = f"SELECT id FROM {table_name} WHERE id = ?"
            if active_only and table_name in ['patients', 'doctors', 'inventory', 'suppliers', 'treatments']:
                query += " AND is_active = 1"

            cursor.execute(query, (record_id,))
            result = cursor.fetchone()
            conn.close()

            return result is not None
        except Exception:
            return False

    def _check_dependent_records(self, table_name, record_id):
        """Check for records that depend on the one being deleted"""
        issues = []

        try:
            conn = self.db.get_connection()

            if table_name == 'patients':
                # Check appointments
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM appointments WHERE patient_id = ?", (record_id,))
                count = cursor.fetchone()[0]
                if count > 0:
                    issues.append(f"Patient has {count} appointments that will be affected")

                # Check payments
                cursor.execute("SELECT COUNT(*) FROM payments WHERE patient_id = ?", (record_id,))
                count = cursor.fetchone()[0]
                if count > 0:
                    issues.append(f"Patient has {count} payments that will be affected")

            elif table_name == 'doctors':
                # Check appointments
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM appointments WHERE doctor_id = ?", (record_id,))
                count = cursor.fetchone()[0]
                if count > 0:
                    issues.append(f"Doctor has {count} appointments that will be affected")

            elif table_name == 'treatments':
                # Check appointments
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM appointments WHERE treatment_id = ?", (record_id,))
                count = cursor.fetchone()[0]
                if count > 0:
                    issues.append(f"Treatment has {count} appointments that will be affected")

            elif table_name == 'appointments':
                # Check payments
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM payments WHERE appointment_id = ?", (record_id,))
                count = cursor.fetchone()[0]
                if count > 0:
                    issues.append(f"Appointment has {count} payments that will be affected")

                # Check inventory usage
                cursor.execute("SELECT COUNT(*) FROM inventory_usage WHERE appointment_id = ?", (record_id,))
                count = cursor.fetchone()[0]
                if count > 0:
                    issues.append(f"Appointment has {count} inventory usage records that will be affected")

            elif table_name == 'inventory':
                # Check inventory usage
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM inventory_usage WHERE inventory_id = ?", (record_id,))
                count = cursor.fetchone()[0]
                if count > 0:
                    issues.append(f"Inventory item has {count} usage records that will be affected")

            conn.close()

        except Exception as e:
            issues.append(f"Error checking dependent records: {str(e)}")

        return issues

    def get_validation_report(self):
        """Generate a comprehensive validation report"""
        report = {
            'foreign_key_issues': self.validate_foreign_keys(),
            'data_consistency_issues': self.validate_data_consistency(),
            'summary': {}
        }

        # Generate summary
        all_issues = report['foreign_key_issues'] + report['data_consistency_issues']
        report['summary'] = {
            'total_issues': len(all_issues),
            'high_severity': len([i for i in all_issues if i.get('severity') == 'high']),
            'medium_severity': len([i for i in all_issues if i.get('severity') == 'medium']),
            'low_severity': len([i for i in all_issues if i.get('severity') == 'low']),
            'issues_by_table': {}
        }

        # Count issues by table
        for issue in all_issues:
            table = issue.get('table', 'unknown')
            if table not in report['summary']['issues_by_table']:
                report['summary']['issues_by_table'][table] = 0
            report['summary']['issues_by_table'][table] += 1

        return report

# Create validator instance
validator = DataValidator()
