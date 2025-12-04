"""Example: Basic hotel booking workflow"""

import sys
import os
from datetime import datetime, timedelta

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from hotel_reservation_system.system import HotelReservationSystem


def main():
    """Demonstrate basic booking workflow"""
    print("=" * 70)
    print("Multi-Agent Hotel Reservation System - Demo")
    print("=" * 70)
    print()
    
    # Initialize the system
    system = HotelReservationSystem()
    print()
    
    # Show available room types
    print("-" * 70)
    print("Available Room Types and Pricing:")
    print("-" * 70)
    room_info = system.get_room_info()
    for room_type, details in room_info["room_types"].items():
        print(f"\n{details['name']}:")
        print(f"  Price per night: ${details['price_per_night']:.2f}")
        print(f"  Capacity: {details['capacity']} guest(s)")
        print(f"  Amenities: {', '.join(details['amenities'])}")
    print()
    
    # Check availability
    print("-" * 70)
    print("Checking Availability:")
    print("-" * 70)
    check_in = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
    check_out = (datetime.now() + timedelta(days=10)).strftime("%Y-%m-%d")
    
    availability = system.check_availability(
        room_type="double",
        check_in_date=f"{check_in}T15:00:00",
        check_out_date=f"{check_out}T11:00:00",
        number_of_guests=2
    )
    
    if availability.get("available"):
        print(f"✓ Room available!")
        print(f"  Room Type: {availability['room_type']}")
        print(f"  Price per night: ${availability['price_per_night']:.2f}")
        print(f"  Number of nights: {availability['nights']}")
        print(f"  Total price: ${availability['total_price']:.2f}")
    else:
        print("✗ Room not available")
    print()
    
    # Create a booking
    print("-" * 70)
    print("Creating Booking:")
    print("-" * 70)
    
    customer_data = {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "phone": "+1-555-0123",
        "id_number": "ID12345"
    }
    
    booking_data = {
        "room_type": "double",
        "check_in_date": f"{check_in}T15:00:00",
        "check_out_date": f"{check_out}T11:00:00",
        "number_of_guests": 2,
        "special_requests": "Non-smoking room with city view"
    }
    
    print(f"Customer: {customer_data['name']}")
    print(f"Email: {customer_data['email']}")
    print(f"Room Type: {booking_data['room_type']}")
    print(f"Check-in: {check_in}")
    print(f"Check-out: {check_out}")
    print(f"Guests: {booking_data['number_of_guests']}")
    print()
    
    result = system.create_booking(
        customer_data=customer_data,
        booking_data=booking_data,
        payment_method="credit_card"
    )
    
    print("-" * 70)
    print("Booking Result:")
    print("-" * 70)
    
    if result.get("status") == "success":
        print("✓ Booking completed successfully!")
        print()
        reservation = result.get("reservation")
        payment = result.get("payment")
        
        print(f"Reservation ID: {reservation['reservation_id']}")
        print(f"Booking Status: {reservation['booking_status']}")
        print(f"Total Amount: ${reservation['total_price']:.2f}")
        print(f"Payment Status: {payment.get('payment_status')}")
        print(f"Transaction ID: {payment.get('transaction_id')}")
        print()
        print("Confirmation email sent to:", customer_data['email'])
    else:
        print(f"✗ Booking failed: {result.get('message')}")
    
    print()
    print("=" * 70)
    print("Demo completed!")
    print("=" * 70)


if __name__ == "__main__":
    main()
