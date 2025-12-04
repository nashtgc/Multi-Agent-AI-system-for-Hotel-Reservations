"""Main Hotel Reservation System"""

from typing import Dict, Any
from .agents import (
    ReceptionistAgent,
    AvailabilityAgent,
    PaymentAgent,
    ConfirmationAgent,
    CoordinatorAgent,
    AgentMessage,
    MessageType
)


class HotelReservationSystem:
    """Main system class that manages all agents"""
    
    def __init__(self):
        """Initialize all agents"""
        self.receptionist = ReceptionistAgent()
        self.availability = AvailabilityAgent()
        self.payment = PaymentAgent()
        self.confirmation = ConfirmationAgent()
        self.coordinator = CoordinatorAgent(
            receptionist=self.receptionist,
            availability=self.availability,
            payment=self.payment,
            confirmation=self.confirmation
        )
        
        print("Hotel Reservation System initialized with agents:")
        print(f"  - {self.receptionist}")
        print(f"  - {self.availability}")
        print(f"  - {self.payment}")
        print(f"  - {self.confirmation}")
        print(f"  - {self.coordinator}")
    
    def create_booking(self, customer_data: Dict[str, Any], 
                      booking_data: Dict[str, Any],
                      payment_method: str = "credit_card") -> Dict[str, Any]:
        """
        Create a new hotel booking
        
        Args:
            customer_data: Customer information (name, email, phone)
            booking_data: Booking details (room_type, check_in_date, check_out_date, number_of_guests)
            payment_method: Payment method (default: credit_card)
            
        Returns:
            Dict containing booking result
        """
        # Create request message
        request_msg = AgentMessage(
            message_id="system-request-001",
            sender="system",
            receiver=self.coordinator.agent_id,
            message_type=MessageType.REQUEST,
            content={
                "action": "start_booking",
                "customer": customer_data,
                "booking": booking_data,
                "payment_method": payment_method
            }
        )
        
        # Process through coordinator
        response = self.coordinator._start_booking_workflow(request_msg)
        
        return response.content
    
    def check_availability(self, room_type: str, check_in_date: str, 
                          check_out_date: str, number_of_guests: int) -> Dict[str, Any]:
        """
        Check room availability
        
        Args:
            room_type: Type of room
            check_in_date: Check-in date (ISO format)
            check_out_date: Check-out date (ISO format)
            number_of_guests: Number of guests
            
        Returns:
            Dict containing availability information
        """
        request_msg = AgentMessage(
            message_id="system-avail-001",
            sender="system",
            receiver=self.availability.agent_id,
            message_type=MessageType.REQUEST,
            content={
                "action": "check_availability",
                "reservation": {
                    "room_type": room_type,
                    "check_in_date": check_in_date,
                    "check_out_date": check_out_date,
                    "number_of_guests": number_of_guests
                }
            }
        )
        
        response = self.availability.process_message(request_msg)
        return response.content
    
    def get_booking_status(self, reservation_id: str) -> Dict[str, Any]:
        """
        Get status of a booking
        
        Args:
            reservation_id: Reservation ID
            
        Returns:
            Dict containing booking status
        """
        status = self.coordinator.get_booking_status(reservation_id)
        if status:
            return {"status": "success", "booking": status}
        else:
            return {"status": "not_found", "message": "Reservation not found"}
    
    def get_room_info(self) -> Dict[str, Any]:
        """Get information about available room types and pricing"""
        return {
            "room_types": {
                "single": {
                    "name": "Single Room",
                    "price_per_night": self.availability.ROOM_PRICES["single"],
                    "capacity": 1,
                    "amenities": ["WiFi", "TV", "Air Conditioning", "Breakfast"]
                },
                "double": {
                    "name": "Double Room",
                    "price_per_night": self.availability.ROOM_PRICES["double"],
                    "capacity": 2,
                    "amenities": ["WiFi", "TV", "Air Conditioning", "Breakfast", "Mini Bar"]
                },
                "suite": {
                    "name": "Suite",
                    "price_per_night": self.availability.ROOM_PRICES["suite"],
                    "capacity": 4,
                    "amenities": ["WiFi", "TV", "Air Conditioning", "Breakfast", "Mini Bar", "Living Area"]
                },
                "deluxe": {
                    "name": "Deluxe Room",
                    "price_per_night": self.availability.ROOM_PRICES["deluxe"],
                    "capacity": 4,
                    "amenities": ["WiFi", "TV", "Air Conditioning", "Breakfast", "Mini Bar", "Living Area", "Jacuzzi"]
                }
            }
        }
