#!/usr/bin/env python
"""Test runner for the hotel reservation system"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from tests.test_models import (
    test_customer_creation,
    test_reservation_creation,
    test_calculate_nights
)
from tests.test_agents import (
    test_receptionist_agent,
    test_availability_agent,
    test_payment_agent,
    test_confirmation_agent
)
from tests.test_system import (
    test_system_initialization,
    test_check_availability,
    test_get_room_info,
    test_complete_booking_workflow
)


def main():
    """Run all tests"""
    print("=" * 70)
    print("Hotel Reservation System - Test Suite")
    print("=" * 70)
    print()
    
    test_count = 0
    passed = 0
    failed = 0
    
    # Model tests
    print("Running Model Tests...")
    print("-" * 70)
    tests = [
        ("Customer Creation", test_customer_creation),
        ("Reservation Creation", test_reservation_creation),
        ("Calculate Nights", test_calculate_nights)
    ]
    
    for test_name, test_func in tests:
        test_count += 1
        try:
            test_func()
            passed += 1
        except Exception as e:
            print(f"✗ {test_name} failed: {e}")
            failed += 1
    print()
    
    # Agent tests
    print("Running Agent Tests...")
    print("-" * 70)
    tests = [
        ("Receptionist Agent", test_receptionist_agent),
        ("Availability Agent", test_availability_agent),
        ("Payment Agent", test_payment_agent),
        ("Confirmation Agent", test_confirmation_agent)
    ]
    
    for test_name, test_func in tests:
        test_count += 1
        try:
            test_func()
            passed += 1
        except Exception as e:
            print(f"✗ {test_name} failed: {e}")
            failed += 1
    print()
    
    # System tests
    print("Running System Tests...")
    print("-" * 70)
    tests = [
        ("System Initialization", test_system_initialization),
        ("Check Availability", test_check_availability),
        ("Get Room Info", test_get_room_info),
        ("Complete Booking Workflow", test_complete_booking_workflow)
    ]
    
    for test_name, test_func in tests:
        test_count += 1
        try:
            test_func()
            passed += 1
        except Exception as e:
            print(f"✗ {test_name} failed: {e}")
            failed += 1
    print()
    
    # Summary
    print("=" * 70)
    print("Test Summary")
    print("=" * 70)
    print(f"Total tests: {test_count}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print()
    
    if failed == 0:
        print("✓ All tests passed!")
        return 0
    else:
        print(f"✗ {failed} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
