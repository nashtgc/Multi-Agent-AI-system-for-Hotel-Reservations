# Multi-Agent AI System for Hotel Reservations

A sophisticated multi-agent system for managing hotel reservations using specialized AI agents that work together to handle the complete booking workflow.

## Overview

This system implements a distributed multi-agent architecture where each agent has a specific responsibility in the hotel reservation process. The agents communicate with each other through a message-passing protocol to coordinate and complete booking tasks.

## Architecture

### Agents

The system consists of five specialized agents:

1. **Receptionist Agent**: Handles customer inquiries and initial booking requests
2. **Availability Agent**: Checks room availability and calculates pricing
3. **Payment Agent**: Processes payment transactions
4. **Confirmation Agent**: Sends booking confirmations to customers
5. **Coordinator Agent**: Orchestrates the workflow between all agents

### Workflow

```
Customer Request → Receptionist → Coordinator
                                    ↓
                    Availability ← Check availability
                                    ↓
                    Payment ← Process payment
                                    ↓
                    Confirmation ← Send confirmation
                                    ↓
                    Customer ← Booking complete
```

## Features

- **Multi-Agent Architecture**: Distributed system with specialized agents
- **Message-Based Communication**: Agents communicate through structured messages
- **Complete Booking Workflow**: From inquiry to confirmation
- **Room Availability Management**: Real-time availability checking
- **Payment Processing**: Simulated payment gateway integration
- **Automated Confirmations**: Email confirmations for bookings
- **Extensible Design**: Easy to add new agents or modify existing ones

## Installation

1. Clone the repository:
```bash
git clone https://github.com/nashtgc/Multi-Agent-AI-system-for-Hotel-Reservations.git
cd Multi-Agent-AI-system-for-Hotel-Reservations
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Booking Example

```python
from hotel_reservation_system.system import HotelReservationSystem

# Initialize the system
system = HotelReservationSystem()

# Define customer information
customer_data = {
    "name": "John Doe",
    "email": "john.doe@example.com",
    "phone": "+1-555-0123",
    "id_number": "ID12345"
}

# Define booking details
booking_data = {
    "room_type": "double",
    "check_in_date": "2025-12-15T15:00:00",
    "check_out_date": "2025-12-18T11:00:00",
    "number_of_guests": 2,
    "special_requests": "Non-smoking room"
}

# Create booking
result = system.create_booking(
    customer_data=customer_data,
    booking_data=booking_data,
    payment_method="credit_card"
)

print(f"Booking Status: {result['status']}")
print(f"Reservation ID: {result['reservation']['reservation_id']}")
```

### Running the Demo

```bash
python examples/basic_booking.py
```

## Room Types and Pricing

| Room Type | Price/Night | Capacity | Amenities |
|-----------|-------------|----------|-----------|
| Single    | $100        | 1 guest  | WiFi, TV, AC, Breakfast |
| Double    | $150        | 2 guests | WiFi, TV, AC, Breakfast, Mini Bar |
| Suite     | $250        | 4 guests | WiFi, TV, AC, Breakfast, Mini Bar, Living Area |
| Deluxe    | $350        | 4 guests | WiFi, TV, AC, Breakfast, Mini Bar, Living Area, Jacuzzi |

## API Reference

### HotelReservationSystem

Main system class for managing hotel reservations.

#### Methods

- `create_booking(customer_data, booking_data, payment_method)`: Create a new booking
- `check_availability(room_type, check_in_date, check_out_date, number_of_guests)`: Check room availability
- `get_booking_status(reservation_id)`: Get booking status
- `get_room_info()`: Get room types and pricing information

## Project Structure

```
Multi-Agent-AI-system-for-Hotel-Reservations/
├── hotel_reservation_system/
│   ├── __init__.py
│   ├── system.py              # Main system class
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── base_agent.py      # Base agent class
│   │   ├── receptionist_agent.py
│   │   ├── availability_agent.py
│   │   ├── payment_agent.py
│   │   ├── confirmation_agent.py
│   │   └── coordinator_agent.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── reservation.py     # Data models
│   └── utils/
├── examples/
│   └── basic_booking.py       # Example usage
├── tests/                     # Unit tests
├── requirements.txt
└── README.md
```

## Data Models

### Customer
- `name`: Customer name
- `email`: Email address
- `phone`: Phone number
- `id_number`: ID/Passport number (optional)

### Reservation
- `reservation_id`: Unique reservation identifier
- `customer`: Customer information
- `room_type`: Type of room (single/double/suite/deluxe)
- `check_in_date`: Check-in date and time
- `check_out_date`: Check-out date and time
- `number_of_guests`: Number of guests
- `total_price`: Total booking price
- `booking_status`: Status (pending/confirmed/cancelled/completed)
- `payment_status`: Payment status (pending/processing/completed/failed/refunded)
- `special_requests`: Special requests from customer

## Agent Communication Protocol

Agents communicate using structured messages:

```python
class AgentMessage:
    message_id: str          # Unique message identifier
    sender: str              # Sender agent ID
    receiver: str            # Receiver agent ID
    message_type: MessageType # REQUEST/RESPONSE/NOTIFICATION/ERROR
    content: Dict            # Message payload
    timestamp: datetime      # Message timestamp
    reply_to: Optional[str]  # ID of message being replied to
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Contact

For questions or support, please open an issue on GitHub.
