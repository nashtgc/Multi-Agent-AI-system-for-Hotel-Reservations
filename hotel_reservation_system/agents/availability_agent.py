"""Availability Agent - Checks room availability and pricing"""

from typing import Optional, Dict
from .base_agent import BaseAgent, AgentMessage, MessageType
from ..models import RoomType, Reservation
from datetime import datetime


class AvailabilityAgent(BaseAgent):
    """Agent responsible for checking room availability and calculating pricing"""
    
    # Room pricing per night
    ROOM_PRICES = {
        RoomType.SINGLE: 100.0,
        RoomType.DOUBLE: 150.0,
        RoomType.SUITE: 250.0,
        RoomType.DELUXE: 350.0
    }
    
    # Simulated room inventory
    ROOM_INVENTORY = {
        RoomType.SINGLE: 10,
        RoomType.DOUBLE: 15,
        RoomType.SUITE: 5,
        RoomType.DELUXE: 3
    }
    
    def __init__(self):
        super().__init__(agent_id="availability", name="Availability Agent")
        self.booked_rooms = {}  # Track bookings by date and room type
        
    def process_message(self, message: AgentMessage) -> Optional[AgentMessage]:
        """Process availability and pricing requests"""
        if message.message_type == MessageType.REQUEST:
            action = message.content.get("action")
            
            if action == "check_availability":
                return self._check_availability(message)
            elif action == "calculate_price":
                return self._calculate_price(message)
                
        return None
    
    def _check_availability(self, message: AgentMessage) -> AgentMessage:
        """Check if room is available for given dates"""
        try:
            reservation_data = message.content.get("reservation")
            room_type = RoomType(reservation_data["room_type"])
            check_in = datetime.fromisoformat(reservation_data["check_in_date"])
            check_out = datetime.fromisoformat(reservation_data["check_out_date"])
            
            # Simple availability check (in real system, would check database)
            is_available = self._is_room_available(room_type, check_in, check_out)
            
            if is_available:
                # Calculate price
                nights = (check_out - check_in).days
                price_per_night = self.ROOM_PRICES[room_type]
                total_price = nights * price_per_night
                
                return self.send_message(
                    receiver=message.sender,
                    message_type=MessageType.RESPONSE,
                    content={
                        "status": "success",
                        "available": True,
                        "room_type": room_type.value,
                        "total_price": total_price,
                        "price_per_night": price_per_night,
                        "nights": nights,
                        "message": f"Room available. Total: ${total_price:.2f} for {nights} night(s)"
                    },
                    reply_to=message.message_id
                )
            else:
                return self.send_message(
                    receiver=message.sender,
                    message_type=MessageType.RESPONSE,
                    content={
                        "status": "success",
                        "available": False,
                        "message": "Room not available for selected dates"
                    },
                    reply_to=message.message_id
                )
                
        except Exception as e:
            return self.send_message(
                receiver=message.sender,
                message_type=MessageType.ERROR,
                content={
                    "status": "error",
                    "message": f"Failed to check availability: {str(e)}"
                },
                reply_to=message.message_id
            )
    
    def _calculate_price(self, message: AgentMessage) -> AgentMessage:
        """Calculate total price for reservation"""
        try:
            reservation_data = message.content.get("reservation")
            room_type = RoomType(reservation_data["room_type"])
            check_in = datetime.fromisoformat(reservation_data["check_in_date"])
            check_out = datetime.fromisoformat(reservation_data["check_out_date"])
            
            nights = (check_out - check_in).days
            price_per_night = self.ROOM_PRICES[room_type]
            total_price = nights * price_per_night
            
            return self.send_message(
                receiver=message.sender,
                message_type=MessageType.RESPONSE,
                content={
                    "status": "success",
                    "total_price": total_price,
                    "price_per_night": price_per_night,
                    "nights": nights
                },
                reply_to=message.message_id
            )
            
        except Exception as e:
            return self.send_message(
                receiver=message.sender,
                message_type=MessageType.ERROR,
                content={
                    "status": "error",
                    "message": f"Failed to calculate price: {str(e)}"
                },
                reply_to=message.message_id
            )
    
    def _is_room_available(self, room_type: RoomType, check_in: datetime, check_out: datetime) -> bool:
        """Check if room is available (simplified logic)"""
        # In a real system, this would query a database
        # For demo, we assume rooms are available if inventory > 0
        return self.ROOM_INVENTORY.get(room_type, 0) > 0
