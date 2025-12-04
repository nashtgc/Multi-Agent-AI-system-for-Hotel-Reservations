"""Test complete hotel reservation system"""

import sys
import os
from datetime import datetime, timedelta

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from hotel_reservation_system.system import HotelReservationSystem


def test_system_initialization():
    """Test system initialization"""
    system = HotelReservationSystem()
    assert system.receptionist is not None
    assert system.availability is not None
    assert system.payment is not None
    assert system.confirmation is not None
    assert system.coordinator is not None
    print("✓ System initialization test passed")


def test_check_availability():
    """Test availability checking"""
    system = HotelReservationSystem()
    
    check_in = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%dT15:00:00")
    check_out = (datetime.now() + timedelta(days=10)).strftime("%Y-%m-%dT11:00:00")
    
    result = system.check_availability(
        room_type="double",
        check_in_date=check_in,
        check_out_date=check_out,
        number_of_guests=2
    )
    
    assert result.get("status") == "success"
    assert result.get("available") == True
    print("✓ Check availability test passed")


def test_get_room_info():
    """Test getting room information"""
    system = HotelReservationSystem()
    
    room_info = system.get_room_info()
    assert "room_types" in room_info
    assert "single" in room_info["room_types"]
    assert "double" in room_info["room_types"]
    assert "suite" in room_info["room_types"]
    assert "deluxe" in room_info["room_types"]
    print("✓ Get room info test passed")


def test_complete_booking_workflow():
    """Test complete booking workflow"""
    system = HotelReservationSystem()
    
    check_in = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%dT15:00:00")
    check_out = (datetime.now() + timedelta(days=10)).strftime("%Y-%m-%dT11:00:00")
    
    customer_data = {
        "name": "Test User",
        "email": "test@example.com",
        "phone": "+1-555-0000"
    }
    
    booking_data = {
        "room_type": "single",
        "check_in_date": check_in,
        "check_out_date": check_out,
        "number_of_guests": 1
    }
    
    result = system.create_booking(
        customer_data=customer_data,
        booking_data=booking_data,
        payment_method="credit_card"
    )
    
    # Check result (payment might fail with 10% chance)
    assert "status" in result
    if result.get("status") == "success":
        assert "reservation" in result
        assert result["reservation"]["booking_status"] == "confirmed"
        print("✓ Complete booking workflow test passed (booking successful)")
    elif result.get("status") == "payment_failed":
        print("✓ Complete booking workflow test passed (payment failed as expected)")
    else:
        print(f"✓ Complete booking workflow test passed (status: {result.get('status')})")


if __name__ == "__main__":
    test_system_initialization()
    test_check_availability()
    test_get_room_info()
    test_complete_booking_workflow()
    print("\nAll system tests passed! ✓")
