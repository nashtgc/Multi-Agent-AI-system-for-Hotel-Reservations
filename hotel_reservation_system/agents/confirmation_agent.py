"""Confirmation Agent - Sends booking confirmations"""

from typing import Optional
from .base_agent import BaseAgent, AgentMessage, MessageType
from datetime import datetime


class ConfirmationAgent(BaseAgent):
    """Agent responsible for sending booking confirmations"""
    
    def __init__(self):
        super().__init__(agent_id="confirmation", name="Confirmation Agent")
        self.sent_confirmations = {}
        
    def process_message(self, message: AgentMessage) -> Optional[AgentMessage]:
        """Process confirmation requests"""
        if message.message_type == MessageType.REQUEST:
            action = message.content.get("action")
            
            if action == "send_confirmation":
                return self._send_confirmation(message)
            elif action == "send_cancellation":
                return self._send_cancellation(message)
                
        return None
    
    def _send_confirmation(self, message: AgentMessage) -> AgentMessage:
        """Send booking confirmation to customer"""
        try:
            reservation_data = message.content.get("reservation")
            payment_data = message.content.get("payment")
            
            # Generate confirmation message
            confirmation_message = self._generate_confirmation_message(
                reservation_data, payment_data
            )
            
            # Store confirmation
            reservation_id = reservation_data["reservation_id"]
            self.sent_confirmations[reservation_id] = {
                "sent_at": datetime.now().isoformat(),
                "confirmation_message": confirmation_message,
                "customer_email": reservation_data["customer"]["email"]
            }
            
            return self.send_message(
                receiver=message.sender,
                message_type=MessageType.RESPONSE,
                content={
                    "status": "success",
                    "confirmation_sent": True,
                    "confirmation_message": confirmation_message,
                    "message": "Confirmation email sent successfully"
                },
                reply_to=message.message_id
            )
            
        except Exception as e:
            return self.send_message(
                receiver=message.sender,
                message_type=MessageType.ERROR,
                content={
                    "status": "error",
                    "confirmation_sent": False,
                    "message": f"Failed to send confirmation: {str(e)}"
                },
                reply_to=message.message_id
            )
    
    def _send_cancellation(self, message: AgentMessage) -> AgentMessage:
        """Send cancellation notice to customer"""
        try:
            reservation_id = message.content.get("reservation_id")
            customer_email = message.content.get("customer_email")
            
            cancellation_message = f"""
            Dear Customer,
            
            Your reservation {reservation_id} has been cancelled successfully.
            If a refund is applicable, it will be processed within 5-7 business days.
            
            Thank you for considering our hotel.
            
            Best regards,
            Hotel Management
            """
            
            return self.send_message(
                receiver=message.sender,
                message_type=MessageType.RESPONSE,
                content={
                    "status": "success",
                    "cancellation_sent": True,
                    "message": "Cancellation notice sent successfully"
                },
                reply_to=message.message_id
            )
            
        except Exception as e:
            return self.send_message(
                receiver=message.sender,
                message_type=MessageType.ERROR,
                content={
                    "status": "error",
                    "message": f"Failed to send cancellation notice: {str(e)}"
                },
                reply_to=message.message_id
            )
    
    def _generate_confirmation_message(self, reservation_data: dict, payment_data: dict) -> str:
        """Generate confirmation email message"""
        return f"""
        Dear {reservation_data['customer']['name']},
        
        Your booking has been confirmed!
        
        Reservation Details:
        - Reservation ID: {reservation_data['reservation_id']}
        - Room Type: {reservation_data['room_type']}
        - Check-in: {reservation_data['check_in_date']}
        - Check-out: {reservation_data['check_out_date']}
        - Number of Guests: {reservation_data['number_of_guests']}
        - Total Amount: ${reservation_data.get('total_price', 0):.2f}
        - Transaction ID: {payment_data.get('transaction_id', 'N/A')}
        
        We look forward to welcoming you!
        
        Best regards,
        Hotel Management
        """
