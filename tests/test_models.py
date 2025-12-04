"""Test data models"""

import sys
import os
from datetime import datetime, timedelta

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from hotel_reservation_system.models import (
    Reservation, Customer, RoomType, BookingStatus, PaymentStatus
)


def test_customer_creation():
    """Test customer model creation"""
    customer = Customer(
        name="John Doe",
        email="john@example.com",
        phone="+1-555-0123"
    )
    assert customer.name == "John Doe"
    assert customer.email == "john@example.com"
    print("✓ Customer creation test passed")


def test_reservation_creation():
    """Test reservation model creation"""
    customer = Customer(
        name="Jane Smith",
        email="jane@example.com",
        phone="+1-555-0456"
    )
    
    check_in = datetime.now() + timedelta(days=7)
    check_out = datetime.now() + timedelta(days=10)
    
    reservation = Reservation(
        customer=customer,
        room_type=RoomType.DOUBLE,
        check_in_date=check_in,
        check_out_date=check_out,
        number_of_guests=2
    )
    
    assert reservation.customer.name == "Jane Smith"
    assert reservation.room_type == RoomType.DOUBLE
    assert reservation.number_of_guests == 2
    assert reservation.booking_status == BookingStatus.PENDING
    assert reservation.payment_status == PaymentStatus.PENDING
    print("✓ Reservation creation test passed")


def test_calculate_nights():
    """Test night calculation"""
    customer = Customer(
        name="Test User",
        email="test@example.com",
        phone="+1-555-0000"
    )
    
    check_in = datetime(2025, 12, 10)
    check_out = datetime(2025, 12, 15)
    
    reservation = Reservation(
        customer=customer,
        room_type=RoomType.SUITE,
        check_in_date=check_in,
        check_out_date=check_out,
        number_of_guests=4
    )
    
    assert reservation.calculate_nights() == 5
    print("✓ Calculate nights test passed")


if __name__ == "__main__":
    test_customer_creation()
    test_reservation_creation()
    test_calculate_nights()
    print("\nAll model tests passed! ✓")
