"""Tools for the hotel order details agent."""

import uuid
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional

async def process_hotel_booking(
    hotel_id: str,
    guest_details: Dict[str, Any],
    room_preferences: Dict[str, Any],
    payment_method: str,
    special_requests: Optional[str] = None
) -> Dict[str, Any]:
    """Process a complete hotel booking with all guest and payment details.
    
    Args:
        hotel_id: Selected hotel identifier
        guest_details: Complete guest information
        room_preferences: Room type and specific preferences
        payment_method: Payment method information
        special_requests: Any special requests or accommodations
    
    Returns:
        Complete booking confirmation with reservation details
    """
    # Generate booking confirmation
    booking_id = f"BK{uuid.uuid4().hex[:8].upper()}"
    confirmation_number = f"CNF{uuid.uuid4().hex[:6].upper()}"
    
    booking_details = {
        "booking_id": booking_id,
        "confirmation_number": confirmation_number,
        "hotel_id": hotel_id,
        "status": "confirmed",
        "guest_details": guest_details,
        "room_details": {
            "room_type": room_preferences.get("room_type", "Standard"),
            "bed_type": room_preferences.get("bed_type", "King"),
            "smoking": room_preferences.get("smoking", False),
            "floor_preference": room_preferences.get("floor_preference", "High floor")
        },
        "special_requests": special_requests,
        "booking_date": datetime.now().isoformat(),
        "total_amount": room_preferences.get("total_price", 0),
        "payment_status": "processed"
    }
    
    return {
        "success": True,
        "booking_details": booking_details,
        "next_steps": [
            "Confirmation email sent to guest",
            "Hotel notified of booking",
            "Check-in instructions will be sent 24h before arrival"
        ]
    }

async def validate_guest_information(guest_details: Dict[str, Any]) -> Dict[str, Any]:
    """Validate guest information for hotel booking requirements.
    
    Args:
        guest_details: Guest information to validate
    
    Returns:
        Validation results and any required corrections
    """
    required_fields = ["first_name", "last_name", "email", "phone", "check_in_date", "check_out_date"]
    missing_fields = []
    validation_errors = []
    
    for field in required_fields:
        if field not in guest_details or not guest_details[field]:
            missing_fields.append(field)
    
    # Email validation
    if "email" in guest_details and "@" not in guest_details["email"]:
        validation_errors.append("Invalid email format")
    
    # Phone validation
    if "phone" in guest_details and len(guest_details["phone"]) < 10:
        validation_errors.append("Phone number must be at least 10 digits")
    
    return {
        "is_valid": len(missing_fields) == 0 and len(validation_errors) == 0,
        "missing_fields": missing_fields,
        "validation_errors": validation_errors,
        "guest_details": guest_details
    }

async def calculate_booking_total(
    hotel_id: str,
    check_in_date: str,
    check_out_date: str,
    room_type: str,
    guests: int,
    rooms: int
) -> Dict[str, Any]:
    """Calculate the total cost for a hotel booking including taxes and fees.
    
    Args:
        hotel_id: Hotel identifier
        check_in_date: Check-in date (YYYY-MM-DD)
        check_out_date: Check-out date (YYYY-MM-DD)
        room_type: Selected room type
        guests: Number of guests
        rooms: Number of rooms
    
    Returns:
        Detailed cost breakdown with total amount
    """
    # Calculate number of nights
    from datetime import datetime
    check_in = datetime.strptime(check_in_date, "%Y-%m-%d")
    check_out = datetime.strptime(check_out_date, "%Y-%m-%d")
    nights = (check_out - check_in).days
    
    # Base room rates (simplified)
    room_rates = {
        "Standard": 120,
        "Deluxe": 180,
        "Suite": 350,
        "Presidential": 800
    }
    
    base_rate = room_rates.get(room_type, 120)
    subtotal = base_rate * nights * rooms
    
    # Calculate taxes and fees
    tax_rate = 0.12  # 12% tax
    service_fee = 25 * rooms  # Per room service fee
    
    taxes = subtotal * tax_rate
    total_amount = subtotal + taxes + service_fee
    
    return {
        "cost_breakdown": {
            "base_rate_per_night": base_rate,
            "nights": nights,
            "rooms": rooms,
            "subtotal": subtotal,
            "taxes": round(taxes, 2),
            "service_fees": service_fee,
            "total_amount": round(total_amount, 2)
        },
        "payment_due": "At check-in",
        "cancellation_deadline": check_in_date
    }

async def generate_booking_confirmation(booking_details: Dict[str, Any]) -> Dict[str, Any]:
    """Generate a formatted booking confirmation document.
    
    Args:
        booking_details: Complete booking information
    
    Returns:
        Formatted confirmation document and delivery information
    """
    confirmation_document = {
        "confirmation_number": booking_details["confirmation_number"],
        "guest_name": f"{booking_details['guest_details']['first_name']} {booking_details['guest_details']['last_name']}",
        "hotel_information": {
            "hotel_id": booking_details["hotel_id"],
            "check_in_date": booking_details["guest_details"]["check_in_date"],
            "check_out_date": booking_details["guest_details"]["check_out_date"],
            "room_type": booking_details["room_details"]["room_type"]
        },
        "important_information": [
            "Check-in time: 3:00 PM",
            "Check-out time: 11:00 AM", 
            "Valid photo ID required at check-in",
            "Credit card required for incidentals"
        ],
        "contact_information": {
            "hotel_phone": "+1-555-HOTEL-01",
            "customer_service": "+1-555-SUPPORT"
        }
    }
    
    return {
        "confirmation_document": confirmation_document,
        "delivery_method": "Email",
        "delivery_status": "Sent",
        "backup_delivery": "SMS confirmation code sent"
    }

async def handle_special_requests(
    booking_id: str,
    special_requests: str
) -> Dict[str, Any]:
    """Process and validate special requests for hotel booking.
    
    Args:
        booking_id: Booking identifier
        special_requests: Guest special requests
    
    Returns:
        Processing status and hotel notification details
    """
    # Categorize requests
    request_categories = {
        "room_preferences": ["high floor", "quiet room", "city view", "ocean view"],
        "accessibility": ["wheelchair accessible", "hearing impaired", "visual impaired"],
        "dietary": ["vegetarian", "vegan", "gluten-free", "kosher", "halal"],
        "celebration": ["honeymoon", "anniversary", "birthday", "business"]
    }
    
    categorized_requests = []
    for category, keywords in request_categories.items():
        if any(keyword in special_requests.lower() for keyword in keywords):
            categorized_requests.append(category)
    
    return {
        "booking_id": booking_id,
        "original_request": special_requests,
        "categorized_requests": categorized_requests,
        "processing_status": "forwarded_to_hotel",
        "hotel_response_expected": "Within 24 hours",
        "guest_notification": "You will be contacted if any requests cannot be accommodated"
    }

TOOLS: List[Callable[..., Any]] = [
    process_hotel_booking,
    validate_guest_information,
    calculate_booking_total,
    generate_booking_confirmation,
    handle_special_requests
]