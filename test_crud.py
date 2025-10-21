#!/usr/bin/env python3
"""
Test script for CRUD operations with validation
"""

import sys
import os
sys.path.append('database')

from database.crud import crud
from database.validation import validator

def test_validation_functions():
    """Test validation functions"""
    print('Testing validation functions...')
    try:
        report = validator.get_validation_report()
        print(f'Found {report["summary"]["total_issues"]} issues in database')
        return True
    except Exception as e:
        print(f'Error testing validation: {e}')
        return False

def test_crud_operations():
    """Test CRUD operations with validation"""
    print('Testing CRUD operations with validation...')
    try:
        # Test creating a doctor with validation
        doctor_id = crud.create_doctor('Test Doctor', 'General', '0123456789', 'test@clinic.com', 'Test Address', '2024-01-01', 10000.0, 10.0)
        print(f'Created doctor with ID: {doctor_id}')

        # Test creating a patient
        patient_id = crud.create_patient('Test Patient', '0123456789', 'test@patient.com', 'Test Address', '1990-01-01', 'Male')
        print(f'Created patient with ID: {patient_id}')

        # Test creating an appointment
        appointment_id = crud.create_appointment(patient_id, doctor_id, None, '2024-12-01', '10:00', 'Test appointment', 200.0)
        print(f'Created appointment with ID: {appointment_id}')

        print('CRUD operations with validation working correctly')
        return True

    except Exception as e:
        print(f'Error in CRUD operations: {e}')
        return False

def test_cascade_delete():
    """Test cascade delete logic"""
    print('Testing cascade delete logic...')
    try:
        # Create test data
        doctor_id = crud.create_doctor('Cascade Test Doctor', 'Test', '0123456789', 'cascade@test.com', 'Test', '2024-01-01', 10000.0, 10.0)
        patient_id = crud.create_patient('Cascade Test Patient', '0123456789', 'cascade@patient.com', 'Test', '1990-01-01', 'Male')
        appointment_id = crud.create_appointment(patient_id, doctor_id, None, '2024-12-01', '10:00', 'Test', 200.0)
        payment_id = crud.create_payment(appointment_id, patient_id, 200.0, 'Cash', '2024-12-01', 'Test payment')

        print(f'Created test data: Doctor {doctor_id}, Patient {patient_id}, Appointment {appointment_id}, Payment {payment_id}')

        # Check dependent records before deletion
        appointments_before = len(crud.get_all_appointments())
        payments_before = len(crud.get_all_payments())

        print(f'Before deletion: {appointments_before} appointments, {payments_before} payments')

        # Delete patient (should cascade to appointments and payments)
        crud.delete_patient(patient_id)
        print('Deleted patient - cascade logic should have handled related records')

        # Check records after deletion
        appointments_after = len(crud.get_all_appointments())
        payments_after = len(crud.get_all_payments())

        print(f'After deletion: {appointments_after} appointments, {payments_after} payments')

        if appointments_after < appointments_before and payments_after < payments_before:
            print('✅ Cascade delete logic working correctly')
            return True
        else:
            print('❌ Cascade delete logic may not be working properly')
            return False

    except Exception as e:
        print(f'Error testing cascade logic: {e}')
        return False

def main():
    """Run all tests"""
    print("🧪 Starting CRUD and Validation Tests...\n")

    results = []

    # Test validation functions
    results.append(test_validation_functions())
    print()

    # Test CRUD operations
    results.append(test_crud_operations())
    print()

    # Test cascade delete
    results.append(test_cascade_delete())
    print()

    # Summary
    passed = sum(results)
    total = len(results)

    print(f"📊 Test Results: {passed}/{total} tests passed")

    if passed == total:
        print("✅ All tests passed successfully!")
        return 0
    else:
        print("❌ Some tests failed")
        return 1

if __name__ == "__main__":
    exit(main())
