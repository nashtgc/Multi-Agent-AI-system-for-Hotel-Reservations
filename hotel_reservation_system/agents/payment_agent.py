"""Payment Agent - Processes payment transactions"""

from typing import Optional
from .base_agent import BaseAgent, AgentMessage, MessageType
from ..models import PaymentStatus
import random


class PaymentAgent(BaseAgent):
    """Agent responsible for processing payments"""
    
    def __init__(self):
        super().__init__(agent_id="payment", name="Payment Agent")
        self.processed_payments = {}
        
    def process_message(self, message: AgentMessage) -> Optional[AgentMessage]:
        """Process payment requests"""
        if message.message_type == MessageType.REQUEST:
            action = message.content.get("action")
            
            if action == "process_payment":
                return self._process_payment(message)
            elif action == "refund_payment":
                return self._refund_payment(message)
                
        return None
    
    def _process_payment(self, message: AgentMessage) -> AgentMessage:
        """Process payment for a reservation"""
        try:
            reservation_id = message.content.get("reservation_id")
            amount = message.content.get("amount")
            payment_method = message.content.get("payment_method", "credit_card")
            
            # Simulate payment processing
            # In a real system, this would integrate with payment gateway
            payment_success = self._simulate_payment_processing(amount)
            
            if payment_success:
                transaction_id = f"TXN{reservation_id}{random.randint(1000, 9999)}"
                self.processed_payments[reservation_id] = {
                    "transaction_id": transaction_id,
                    "amount": amount,
                    "status": PaymentStatus.COMPLETED.value,
                    "payment_method": payment_method
                }
                
                return self.send_message(
                    receiver=message.sender,
                    message_type=MessageType.RESPONSE,
                    content={
                        "status": "success",
                        "payment_status": PaymentStatus.COMPLETED.value,
                        "transaction_id": transaction_id,
                        "amount": amount,
                        "message": f"Payment of ${amount:.2f} processed successfully"
                    },
                    reply_to=message.message_id
                )
            else:
                return self.send_message(
                    receiver=message.sender,
                    message_type=MessageType.RESPONSE,
                    content={
                        "status": "failed",
                        "payment_status": PaymentStatus.FAILED.value,
                        "message": "Payment processing failed. Please try again."
                    },
                    reply_to=message.message_id
                )
                
        except Exception as e:
            return self.send_message(
                receiver=message.sender,
                message_type=MessageType.ERROR,
                content={
                    "status": "error",
                    "payment_status": PaymentStatus.FAILED.value,
                    "message": f"Payment processing error: {str(e)}"
                },
                reply_to=message.message_id
            )
    
    def _refund_payment(self, message: AgentMessage) -> AgentMessage:
        """Process refund for a reservation"""
        try:
            reservation_id = message.content.get("reservation_id")
            
            if reservation_id in self.processed_payments:
                payment_info = self.processed_payments[reservation_id]
                amount = payment_info["amount"]
                
                # Simulate refund processing
                self.processed_payments[reservation_id]["status"] = PaymentStatus.REFUNDED.value
                
                return self.send_message(
                    receiver=message.sender,
                    message_type=MessageType.RESPONSE,
                    content={
                        "status": "success",
                        "payment_status": PaymentStatus.REFUNDED.value,
                        "amount": amount,
                        "message": f"Refund of ${amount:.2f} processed successfully"
                    },
                    reply_to=message.message_id
                )
            else:
                return self.send_message(
                    receiver=message.sender,
                    message_type=MessageType.ERROR,
                    content={
                        "status": "error",
                        "message": "No payment found for this reservation"
                    },
                    reply_to=message.message_id
                )
                
        except Exception as e:
            return self.send_message(
                receiver=message.sender,
                message_type=MessageType.ERROR,
                content={
                    "status": "error",
                    "message": f"Refund processing error: {str(e)}"
                },
                reply_to=message.message_id
            )
    
    def _simulate_payment_processing(self, amount: float) -> bool:
        """Simulate payment processing (90% success rate)"""
        # In a real system, this would call actual payment gateway
        return random.random() < 0.9  # 90% success rate
