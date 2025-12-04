"""Receptionist Agent - Handles customer inquiries and booking requests"""

from typing import Optional
from .base_agent import BaseAgent, AgentMessage, MessageType
from ..models import Reservation, Customer, RoomType
from datetime import datetime


class ReceptionistAgent(BaseAgent):
    """Agent responsible for customer interaction and initial booking requests"""
    
    def __init__(self):
        super().__init__(agent_id="receptionist", name="Receptionist Agent")
        
    def process_message(self, message: AgentMessage) -> Optional[AgentMessage]:
        """Process customer booking requests"""
        if message.message_type == MessageType.REQUEST:
            action = message.content.get("action")
            
            if action == "create_booking":
                return self._handle_booking_request(message)
            elif action == "inquiry":
                return self._handle_inquiry(message)
                
        return None
    
    def _handle_booking_request(self, message: AgentMessage) -> AgentMessage:
        """Handle new booking request"""
        try:
            # Extract customer and booking details
            customer_data = message.content.get("customer")
            booking_data = message.content.get("booking")
            
            customer = Customer(**customer_data)
            
            # Create reservation object
            reservation = Reservation(
                customer=customer,
                room_type=RoomType(booking_data["room_type"]),
                check_in_date=datetime.fromisoformat(booking_data["check_in_date"]),
                check_out_date=datetime.fromisoformat(booking_data["check_out_date"]),
                number_of_guests=booking_data["number_of_guests"],
                special_requests=booking_data.get("special_requests")
            )
            
            return self.send_message(
                receiver="coordinator",
                message_type=MessageType.RESPONSE,
                content={
                    "status": "success",
                    "reservation": reservation.model_dump(mode="json"),
                    "message": "Booking request received and processed"
                },
                reply_to=message.message_id
            )
            
        except Exception as e:
            return self.send_message(
                receiver=message.sender,
                message_type=MessageType.ERROR,
                content={
                    "status": "error",
                    "message": f"Failed to process booking request: {str(e)}"
                },
                reply_to=message.message_id
            )
    
    def _handle_inquiry(self, message: AgentMessage) -> AgentMessage:
        """Handle customer inquiry"""
        inquiry_type = message.content.get("inquiry_type")
        
        response_messages = {
            "room_types": "We offer Single, Double, Suite, and Deluxe rooms.",
            "amenities": "All rooms include WiFi, TV, air conditioning, and complimentary breakfast.",
            "policies": "Check-in: 3 PM, Check-out: 11 AM. Cancellation allowed up to 24 hours before check-in."
        }
        
        return self.send_message(
            receiver=message.sender,
            message_type=MessageType.RESPONSE,
            content={
                "status": "success",
                "inquiry_type": inquiry_type,
                "response": response_messages.get(inquiry_type, "Please contact our support for more information.")
            },
            reply_to=message.message_id
        )
