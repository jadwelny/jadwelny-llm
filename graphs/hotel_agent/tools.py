"""Tools for the hotel agent."""

import json
from typing import Any, Callable, Dict, List, Optional
from langgraph_sdk import get_client

async def search_hotels(
    location: str,
    check_in_date: str,
    check_out_date: str,
    guests: int = 1,
    rooms: int = 1,
    price_range: Optional[str] = None
) -> Dict[str, Any]:
    """Search for hotels in the specified location and date range.
    
    Args:
        location: Hotel location (city, address, landmark)
        check_in_date: Check-in date (YYYY-MM-DD)
        check_out_date: Check-out date (YYYY-MM-DD)
        guests: Number of guests
        rooms: Number of rooms
        price_range: Budget preference (budget, mid-range, luxury)
    
    Returns:
        Hotel search results with availability and pricing
    """
    # Simulate hotel search
    hotels = [
        {
            "hotel_id": "HTL001",
            "name": "Grand Plaza Hotel",
            "location": location,
            "rating": 4.5,
            "price_per_night": 180,
            "total_price": 540,  # 3 nights
            "amenities": ["Pool", "Gym", "WiFi", "Restaurant", "Spa"],
            "room_type": "Deluxe King Room",
            "cancellation": "Free cancellation until 24h before check-in",
            "distance_to_center": "0.5 km"
        },
        {
            "hotel_id": "HTL002",
            "name": "City Center Inn",
            "location": location,
            "rating": 4.2,
            "price_per_night": 120,
            "total_price": 360,
            "amenities": ["WiFi", "Restaurant", "24h Front Desk"],
            "room_type": "Standard Double Room",
            "cancellation": "Free cancellation until 48h before check-in",
            "distance_to_center": "0.2 km"
        }
    ]
    
    return {
        "search_criteria": {
            "location": location,
            "check_in_date": check_in_date,
            "check_out_date": check_out_date,
            "guests": guests,
            "rooms": rooms,
            "price_range": price_range
        },
        "hotels": hotels,
        "total_results": len(hotels)
    }

async def get_hotel_details(hotel_id: str) -> Dict[str, Any]:
    """Get detailed information about a specific hotel.
    
    Args:
        hotel_id: Unique hotel identifier
    
    Returns:
        Detailed hotel information including photos, reviews, and policies
    """
    return {
        "hotel_id": hotel_id,
        "detailed_info": {
            "description": "Luxury hotel in the heart of the city with modern amenities",
            "photos": ["lobby.jpg", "room.jpg", "pool.jpg"],
            "reviews": {
                "average_rating": 4.5,
                "total_reviews": 1247,
                "recent_reviews": [
                    "Excellent service and location",
                    "Clean rooms and great breakfast",
                    "Perfect for business travel"
                ]
            },
            "policies": {
                "check_in": "15:00",
                "check_out": "11:00",
                "pets": "Not allowed",
                "smoking": "Non-smoking property"
            }
        }
    }

async def delegate_to_hotel_order_agent(
    hotel_id: str,
    guest_details: Dict[str, Any],
    room_preferences: Dict[str, Any],
    special_requests: Optional[str] = None
) -> Dict[str, Any]:
    """Delegate hotel booking order processing to the hotel order details agent.
    
    Args:
        hotel_id: Selected hotel identifier
        guest_details: Guest information for booking
        room_preferences: Room type and preferences
        special_requests: Any special requests or notes
    
    Returns:
        Booking confirmation and order details
    """
    client = get_client(url="http://localhost:8000")
    
    thread = await client.threads.create()
    
    order_request = {
        "hotel_id": hotel_id,
        "guest_details": guest_details,
        "room_preferences": room_preferences,
        "special_requests": special_requests
    }
    
    response = await client.runs.create(
        thread_id=thread["thread_id"],
        assistant_id="hotel_order_agent",
        input={
            "messages": [{
                "type": "human",
                "content": [{"type": "text", "text": json.dumps(order_request)}]
            }]
        }
    )
    
    return response

TOOLS: List[Callable[..., Any]] = [
    search_hotels,
    get_hotel_details,
    delegate_to_hotel_order_agent
]