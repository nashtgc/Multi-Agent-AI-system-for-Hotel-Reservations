"""Test agent functionality"""

import sys
import os
from datetime import datetime, timedelta

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from hotel_reservation_system.agents import (
    ReceptionistAgent, AvailabilityAgent, PaymentAgent, 
    ConfirmationAgent, AgentMessage, MessageType
)


def test_receptionist_agent():
    """Test receptionist agent"""
    agent = ReceptionistAgent()
    
    check_in = (datetime.now() + timedelta(days=7)).isoformat()
    check_out = (datetime.now() + timedelta(days=10)).isoformat()
    
    message = AgentMessage(
        message_id="test-001",
        sender="test",
        receiver=agent.agent_id,
        message_type=MessageType.REQUEST,
        content={
            "action": "create_booking",
            "customer": {
                "name": "Test User",
                "email": "test@example.com",
                "phone": "+1-555-0000"
            },
            "booking": {
                "room_type": "double",
                "check_in_date": check_in,
                "check_out_date": check_out,
                "number_of_guests": 2
            }
        }
    )
    
    response = agent.process_message(message)
    assert response is not None
    assert response.content.get("status") == "success"
    print("✓ Receptionist agent test passed")


def test_availability_agent():
    """Test availability agent"""
    agent = AvailabilityAgent()
    
    check_in = (datetime.now() + timedelta(days=7)).isoformat()
    check_out = (datetime.now() + timedelta(days=10)).isoformat()
    
    message = AgentMessage(
        message_id="test-002",
        sender="test",
        receiver=agent.agent_id,
        message_type=MessageType.REQUEST,
        content={
            "action": "check_availability",
            "reservation": {
                "room_type": "double",
                "check_in_date": check_in,
                "check_out_date": check_out,
                "number_of_guests": 2
            }
        }
    )
    
    response = agent.process_message(message)
    assert response is not None
    assert response.content.get("status") == "success"
    assert response.content.get("available") == True
    # Verify price calculation: 3 nights * price per night
    expected_price = 3 * 150.0
    assert response.content.get("total_price") == expected_price
    assert response.content.get("nights") == 3
    print("✓ Availability agent test passed")


def test_payment_agent():
    """Test payment agent"""
    agent = PaymentAgent()
    
    message = AgentMessage(
        message_id="test-003",
        sender="test",
        receiver=agent.agent_id,
        message_type=MessageType.REQUEST,
        content={
            "action": "process_payment",
            "reservation_id": "RES12345",
            "amount": 450.0,
            "payment_method": "credit_card"
        }
    )
    
    response = agent.process_message(message)
    assert response is not None
    # Payment might fail randomly (10% chance), so check for status field
    assert "payment_status" in response.content
    print("✓ Payment agent test passed")


def test_confirmation_agent():
    """Test confirmation agent"""
    agent = ConfirmationAgent()
    
    message = AgentMessage(
        message_id="test-004",
        sender="test",
        receiver=agent.agent_id,
        message_type=MessageType.REQUEST,
        content={
            "action": "send_confirmation",
            "reservation": {
                "reservation_id": "RES12345",
                "customer": {
                    "name": "Test User",
                    "email": "test@example.com"
                },
                "room_type": "double",
                "check_in_date": "2025-12-15",
                "check_out_date": "2025-12-18",
                "number_of_guests": 2,
                "total_price": 450.0
            },
            "payment": {
                "transaction_id": "TXN12345",
                "amount": 450.0
            }
        }
    )
    
    response = agent.process_message(message)
    assert response is not None
    assert response.content.get("status") == "success"
    assert response.content.get("confirmation_sent") == True
    print("✓ Confirmation agent test passed")


if __name__ == "__main__":
    test_receptionist_agent()
    test_availability_agent()
    test_payment_agent()
    test_confirmation_agent()
    print("\nAll agent tests passed! ✓")
