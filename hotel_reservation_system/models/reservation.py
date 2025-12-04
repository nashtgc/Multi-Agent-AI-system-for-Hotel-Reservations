"""Reservation data models"""

from enum import Enum
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class RoomType(str, Enum):
    """Available room types"""
    SINGLE = "single"
    DOUBLE = "double"
    SUITE = "suite"
    DELUXE = "deluxe"


class BookingStatus(str, Enum):
    """Booking status states"""
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"


class PaymentStatus(str, Enum):
    """Payment status states"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"


class Customer(BaseModel):
    """Customer information"""
    name: str
    email: str
    phone: str
    id_number: Optional[str] = None


class Reservation(BaseModel):
    """Hotel reservation model"""
    reservation_id: str = Field(default_factory=lambda: f"RES{datetime.now().strftime('%Y%m%d%H%M%S')}")
    customer: Customer
    room_type: RoomType
    check_in_date: datetime
    check_out_date: datetime
    number_of_guests: int = Field(ge=1, le=10)
    total_price: Optional[float] = None
    booking_status: BookingStatus = BookingStatus.PENDING
    payment_status: PaymentStatus = PaymentStatus.PENDING
    special_requests: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)
    
    def calculate_nights(self) -> int:
        """Calculate number of nights"""
        return (self.check_out_date - self.check_in_date).days
