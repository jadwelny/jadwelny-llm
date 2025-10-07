"""Tools for the flight agent."""

import json
from datetime import datetime, timedelta
from typing import Any, Callable, Dict, List, Optional

async def search_flights(
    origin: str,
    destination: str, 
    departure_date: str,
    return_date: Optional[str] = None,
    passengers: int = 1,
    class_preference: str = "economy"
) -> Dict[str, Any]:
    """Search for flights based on specified criteria.
    
    Args:
        origin: Departure airport code or city
        destination: Arrival airport code or city
        departure_date: Departure date (YYYY-MM-DD)
        return_date: Return date for round-trip (YYYY-MM-DD)
        passengers: Number of passengers
        class_preference: Flight class (economy, business, first)
    
    Returns:
        Flight search results with pricing and availability
    """
    # Simulate flight search API call
    flights = [
        {
            "flight_id": "FL001",
            "airline": "SkyLine Airways",
            "origin": origin,
            "destination": destination,
            "departure_time": "08:30",
            "arrival_time": "14:45",
            "duration": "6h 15m",
            "price": 450,
            "class": class_preference,
            "stops": 0,
            "aircraft": "Boeing 737"
        },
        {
            "flight_id": "FL002", 
            "airline": "Global Wings",
            "origin": origin,
            "destination": destination,
            "departure_time": "15:20",
            "arrival_time": "21:10",
            "duration": "5h 50m",
            "price": 520,
            "class": class_preference,
            "stops": 0,
            "aircraft": "Airbus A320"
        }
    ]
    
    return {
        "search_criteria": {
            "origin": origin,
            "destination": destination,
            "departure_date": departure_date,
            "return_date": return_date,
            "passengers": passengers,
            "class": class_preference
        },
        "flights": flights,
        "total_results": len(flights)
    }

async def get_flight_details(flight_id: str) -> Dict[str, Any]:
    """Get detailed information about a specific flight.
    
    Args:
        flight_id: Unique flight identifier
    
    Returns:
        Detailed flight information including baggage, amenities, and policies
    """
    # Simulate detailed flight information
    return {
        "flight_id": flight_id,
        "detailed_info": {
            "baggage_allowance": {
                "carry_on": "1 piece, 8kg max",
                "checked": "1 piece, 23kg max"
            },
            "amenities": ["WiFi", "In-flight entertainment", "Meal service"],
            "cancellation_policy": "Free cancellation up to 24 hours before departure",
            "seat_map_available": True,
            "upgrade_options": ["Premium Economy (+$150)", "Business Class (+$800)"]
        }
    }

async def check_flight_status(flight_id: str, date: str) -> Dict[str, Any]:
    """Check real-time flight status.
    
    Args:
        flight_id: Flight identifier
        date: Flight date (YYYY-MM-DD)
    
    Returns:
        Current flight status and any delays or changes
    """
    return {
        "flight_id": flight_id,
        "date": date,
        "status": "On Time",
        "departure_gate": "A12",
        "arrival_gate": "B8",
        "estimated_departure": "08:30",
        "estimated_arrival": "14:45"
    }

TOOLS: List[Callable[..., Any]] = [
    search_flights,
    get_flight_details,
    check_flight_status
]