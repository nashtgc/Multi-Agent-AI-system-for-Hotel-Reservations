"""Coordinator Agent - Orchestrates workflow between agents"""

from typing import Optional, Dict, List
from .base_agent import BaseAgent, AgentMessage, MessageType
from ..models import BookingStatus, PaymentStatus, Reservation


class CoordinatorAgent(BaseAgent):
    """Agent responsible for coordinating the booking workflow"""
    
    def __init__(self, receptionist, availability, payment, confirmation):
        super().__init__(agent_id="coordinator", name="Coordinator Agent")
        self.receptionist = receptionist
        self.availability = availability
        self.payment = payment
        self.confirmation = confirmation
        self.active_workflows = {}
        
    def process_message(self, message: AgentMessage) -> Optional[AgentMessage]:
        """Process coordination requests"""
        if message.message_type == MessageType.RESPONSE:
            # Handle responses from other agents
            return self._handle_agent_response(message)
        elif message.message_type == MessageType.REQUEST:
            action = message.content.get("action")
            if action == "start_booking":
                return self._start_booking_workflow(message)
        return None
    
    def _start_booking_workflow(self, message: AgentMessage) -> Optional[AgentMessage]:
        """Start the complete booking workflow"""
        try:
            # Step 1: Process booking request with receptionist
            receptionist_msg = AgentMessage(
                message_id=f"coord-recept-{message.message_id}",
                sender=self.agent_id,
                receiver=self.receptionist.agent_id,
                message_type=MessageType.REQUEST,
                content={
                    "action": "create_booking",
                    "customer": message.content.get("customer"),
                    "booking": message.content.get("booking")
                }
            )
            receptionist_response = self.receptionist.process_message(receptionist_msg)
            
            if not receptionist_response or receptionist_response.content.get("status") != "success":
                return receptionist_response
            
            reservation_data = receptionist_response.content.get("reservation")
            
            # Step 2: Check availability and get price
            availability_msg = AgentMessage(
                message_id=f"coord-avail-{message.message_id}",
                sender=self.agent_id,
                receiver=self.availability.agent_id,
                message_type=MessageType.REQUEST,
                content={
                    "action": "check_availability",
                    "reservation": reservation_data
                }
            )
            availability_response = self.availability.process_message(availability_msg)
            
            if not availability_response.content.get("available", False):
                return self.send_message(
                    receiver=message.sender,
                    message_type=MessageType.RESPONSE,
                    content={
                        "status": "unavailable",
                        "message": "Room not available for selected dates"
                    },
                    reply_to=message.message_id
                )
            
            # Update reservation with price
            total_price = availability_response.content.get("total_price")
            reservation_data["total_price"] = total_price
            
            # Step 3: Process payment
            payment_msg = AgentMessage(
                message_id=f"coord-pay-{message.message_id}",
                sender=self.agent_id,
                receiver=self.payment.agent_id,
                message_type=MessageType.REQUEST,
                content={
                    "action": "process_payment",
                    "reservation_id": reservation_data["reservation_id"],
                    "amount": total_price,
                    "payment_method": message.content.get("payment_method", "credit_card")
                }
            )
            payment_response = self.payment.process_message(payment_msg)
            
            if payment_response.content.get("payment_status") != PaymentStatus.COMPLETED.value:
                return self.send_message(
                    receiver=message.sender,
                    message_type=MessageType.RESPONSE,
                    content={
                        "status": "payment_failed",
                        "message": "Payment processing failed. Please try again."
                    },
                    reply_to=message.message_id
                )
            
            # Update reservation status
            reservation_data["booking_status"] = BookingStatus.CONFIRMED.value
            reservation_data["payment_status"] = PaymentStatus.COMPLETED.value
            
            # Step 4: Send confirmation
            confirmation_msg = AgentMessage(
                message_id=f"coord-conf-{message.message_id}",
                sender=self.agent_id,
                receiver=self.confirmation.agent_id,
                message_type=MessageType.REQUEST,
                content={
                    "action": "send_confirmation",
                    "reservation": reservation_data,
                    "payment": payment_response.content
                }
            )
            confirmation_response = self.confirmation.process_message(confirmation_msg)
            
            # Store workflow result
            self.active_workflows[reservation_data["reservation_id"]] = {
                "reservation": reservation_data,
                "status": "completed"
            }
            
            return self.send_message(
                receiver=message.sender,
                message_type=MessageType.RESPONSE,
                content={
                    "status": "success",
                    "booking_status": BookingStatus.CONFIRMED.value,
                    "reservation": reservation_data,
                    "payment": payment_response.content,
                    "confirmation": confirmation_response.content,
                    "message": "Booking completed successfully!"
                },
                reply_to=message.message_id
            )
            
        except Exception as e:
            return self.send_message(
                receiver=message.sender,
                message_type=MessageType.ERROR,
                content={
                    "status": "error",
                    "message": f"Booking workflow failed: {str(e)}"
                },
                reply_to=message.message_id
            )
    
    def _handle_agent_response(self, message: AgentMessage) -> Optional[AgentMessage]:
        """Handle responses from other agents"""
        # This can be extended to handle async workflows
        return None
    
    def get_booking_status(self, reservation_id: str) -> Optional[Dict]:
        """Get status of a booking"""
        return self.active_workflows.get(reservation_id)
