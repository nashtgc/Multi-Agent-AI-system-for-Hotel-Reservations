"""Example: Demonstrating inter-agent communication"""

import sys
import os
from datetime import datetime, timedelta

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from hotel_reservation_system.agents import (
    ReceptionistAgent, AvailabilityAgent, AgentMessage, MessageType
)


def main():
    """Demonstrate agent-to-agent communication"""
    print("=" * 70)
    print("Multi-Agent Communication Demo")
    print("=" * 70)
    print()
    
    # Create agents
    receptionist = ReceptionistAgent()
    availability = AvailabilityAgent()
    
    print("Agents created:")
    print(f"  - {receptionist}")
    print(f"  - {availability}")
    print()
    
    # Scenario 1: Customer inquiry
    print("-" * 70)
    print("Scenario 1: Customer Inquiry")
    print("-" * 70)
    
    inquiry_msg = AgentMessage(
        message_id="INQ-001",
        sender="customer",
        receiver=receptionist.agent_id,
        message_type=MessageType.REQUEST,
        content={
            "action": "inquiry",
            "inquiry_type": "room_types"
        }
    )
    
    print(f"Customer → {receptionist.name}")
    print(f"  Question: What room types are available?")
    print()
    
    response = receptionist.process_message(inquiry_msg)
    print(f"{receptionist.name} → Customer")
    print(f"  Response: {response.content['response']}")
    print()
    
    # Scenario 2: Check availability
    print("-" * 70)
    print("Scenario 2: Direct Availability Check")
    print("-" * 70)
    
    check_in = (datetime.now() + timedelta(days=5)).isoformat()
    check_out = (datetime.now() + timedelta(days=8)).isoformat()
    
    avail_msg = AgentMessage(
        message_id="AVAIL-001",
        sender="system",
        receiver=availability.agent_id,
        message_type=MessageType.REQUEST,
        content={
            "action": "check_availability",
            "reservation": {
                "room_type": "suite",
                "check_in_date": check_in,
                "check_out_date": check_out,
                "number_of_guests": 3
            }
        }
    )
    
    print(f"System → {availability.name}")
    print(f"  Request: Check availability for Suite")
    print(f"  Check-in: {check_in[:10]}")
    print(f"  Check-out: {check_out[:10]}")
    print()
    
    avail_response = availability.process_message(avail_msg)
    
    print(f"{availability.name} → System")
    if avail_response.content.get("available"):
        print(f"  ✓ Room available!")
        print(f"  Price: ${avail_response.content['total_price']:.2f}")
        print(f"  Nights: {avail_response.content['nights']}")
    else:
        print(f"  ✗ Room not available")
    print()
    
    # Scenario 3: Create booking request with Receptionist
    print("-" * 70)
    print("Scenario 3: Booking Request Processing")
    print("-" * 70)
    
    booking_msg = AgentMessage(
        message_id="BOOK-001",
        sender="customer",
        receiver=receptionist.agent_id,
        message_type=MessageType.REQUEST,
        content={
            "action": "create_booking",
            "customer": {
                "name": "Alice Johnson",
                "email": "alice@example.com",
                "phone": "+1-555-1234"
            },
            "booking": {
                "room_type": "deluxe",
                "check_in_date": check_in,
                "check_out_date": check_out,
                "number_of_guests": 2,
                "special_requests": "Late check-in requested"
            }
        }
    )
    
    print(f"Customer → {receptionist.name}")
    print(f"  Request: Create booking for Deluxe room")
    print(f"  Customer: Alice Johnson")
    print(f"  Special Request: Late check-in requested")
    print()
    
    booking_response = receptionist.process_message(booking_msg)
    
    print(f"{receptionist.name} → Customer")
    print(f"  Status: {booking_response.content['status']}")
    print(f"  Message: {booking_response.content['message']}")
    if booking_response.content.get('reservation'):
        reservation = booking_response.content['reservation']
        print(f"  Reservation ID: {reservation['reservation_id']}")
    print()
    
    print("=" * 70)
    print("Multi-Agent Communication Demo Complete!")
    print("=" * 70)
    print()
    print("Key Observations:")
    print("  • Each agent has a specific responsibility")
    print("  • Agents communicate through structured messages")
    print("  • Messages include sender, receiver, type, and content")
    print("  • Agents can process requests independently")
    print("  • The coordinator orchestrates complex workflows")
    print()


if __name__ == "__main__":
    main()
