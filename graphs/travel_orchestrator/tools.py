"""Tools for the main travel orchestrator agent."""

import json
from typing import Any, Callable, Dict, List, Optional
from langgraph_sdk import get_client
from .context import Context

async def delegate_to_flight_agent(
    origin: str, 
    destination: str, 
    departure_date: str, 
    return_date: Optional[str] = None,
    passengers: int = 1,
    class_preference: str = "economy"
) -> Dict[str, Any]:
    """Delegate flight search and booking tasks to the specialized flight agent.
    
    Args:
        origin: Departure city or airport code
        destination: Arrival city or airport code  
        departure_date: Departure date in YYYY-MM-DD format
        return_date: Return date for round-trip flights (optional)
        passengers: Number of passengers
        class_preference: Flight class (economy, business, first)
    
    Returns:
        Flight search results and booking options
    """
    client = get_client(url="http://localhost:8000")
    
    # Create a new thread for the flight agent
    thread = await client.threads.create()
    
    # Prepare the request for the flight agent
    flight_request = {
        "origin": origin,
        "destination": destination,
        "departure_date": departure_date,
        "return_date": return_date,
        "passengers": passengers,
        "class_preference": class_preference
    }
    
    # Send request to flight agent
    response = await client.runs.create(
        thread_id=thread["thread_id"],
        assistant_id="flight_agent",
        input={
            "messages": [{
                "type": "human", 
                "content": [{"type": "text", "text": json.dumps(flight_request)}]
            }]
        }
    )
    
    return response

async def delegate_to_hotel_agent(
    location: str,
    check_in_date: str,
    check_out_date: str,
    guests: int = 1,
    rooms: int = 1,
    price_range: Optional[str] = None
) -> Dict[str, Any]:
    """Delegate hotel search and booking tasks to the specialized hotel agent.
    
    Args:
        location: Hotel location (city, address, or landmark)
        check_in_date: Check-in date in YYYY-MM-DD format
        check_out_date: Check-out date in YYYY-MM-DD format
        guests: Number of guests
        rooms: Number of rooms needed
        price_range: Budget preference (budget, mid-range, luxury)
    
    Returns:
        Hotel search results and booking options
    """
    client = get_client(url="http://localhost:8000")
    
    thread = await client.threads.create()
    
    hotel_request = {
        "location": location,
        "check_in_date": check_in_date,
        "check_out_date": check_out_date,
        "guests": guests,
        "rooms": rooms,
        "price_range": price_range
    }
    
    response = await client.runs.create(
        thread_id=thread["thread_id"],
        assistant_id="hotel_agent",
        input={
            "messages": [{
                "type": "human",
                "content": [{"type": "text", "text": json.dumps(hotel_request)}]
            }]
        }
    )
    
    return response

async def delegate_to_esim_agent(
    destination_country: str,
    travel_duration: int,
    data_needs: str = "moderate"
) -> Dict[str, Any]:
    """Delegate eSIM search and activation to the specialized eSIM agent.
    
    Args:
        destination_country: Country or region for eSIM coverage
        travel_duration: Duration of travel in days
        data_needs: Data usage level (light, moderate, heavy)
    
    Returns:
        eSIM plan options and activation instructions
    """
    client = get_client(url="http://localhost:8000")
    
    thread = await client.threads.create()
    
    esim_request = {
        "destination_country": destination_country,
        "travel_duration": travel_duration,
        "data_needs": data_needs
    }
    
    response = await client.runs.create(
        thread_id=thread["thread_id"],
        assistant_id="esim_agent",
        input={
            "messages": [{
                "type": "human",
                "content": [{"type": "text", "text": json.dumps(esim_request)}]
            }]
        }
    )
    
    return response

async def delegate_to_activities_agent(
    location: str,
    travel_dates: List[str],
    interests: List[str],
    budget_per_activity: Optional[str] = None
) -> Dict[str, Any]:
    """Delegate activity search and booking to the specialized activities agent.
    
    Args:
        location: Location for activities
        travel_dates: List of available dates for activities
        interests: List of activity types or interests
        budget_per_activity: Budget range per activity
    
    Returns:
        Activity recommendations and booking options
    """
    client = get_client(url="http://localhost:8000")
    
    thread = await client.threads.create()
    
    activities_request = {
        "location": location,
        "travel_dates": travel_dates,
        "interests": interests,
        "budget_per_activity": budget_per_activity
    }
    
    response = await client.runs.create(
        thread_id=thread["thread_id"],
        assistant_id="activities_agent",
        input={
            "messages": [{
                "type": "human",
                "content": [{"type": "text", "text": json.dumps(activities_request)}]
            }]
        }
    )
    
    return response

async def analyze_travel_request(user_message: str) -> Dict[str, Any]:
    """Analyze the user's travel request to determine which sub-agents to involve.
    
    Args:
        user_message: The user's travel request message
    
    Returns:
        Analysis of the request including required agents and extracted parameters
    """
    # This would typically use NLP to extract intent and entities
    # For this example, we'll use simple keyword matching
    
    analysis = {
        "requires_flights": False,
        "requires_hotels": False,
        "requires_esim": False,
        "requires_activities": False,
        "extracted_entities": {},
        "confidence": 0.0
    }
    
    message_lower = user_message.lower()
    
    # Flight keywords
    if any(keyword in message_lower for keyword in ["flight", "fly", "airline", "airport", "departure", "arrival"]):
        analysis["requires_flights"] = True
    
    # Hotel keywords
    if any(keyword in message_lower for keyword in ["hotel", "accommodation", "stay", "room", "check-in", "check-out"]):
        analysis["requires_hotels"] = True
    
    # eSIM keywords
    if any(keyword in message_lower for keyword in ["esim", "sim card", "data plan", "mobile data", "internet"]):
        analysis["requires_esim"] = True
    
    # Activities keywords
    if any(keyword in message_lower for keyword in ["activity", "tour", "attraction", "sightseeing", "experience"]):
        analysis["requires_activities"] = True
    
    # Calculate confidence based on keyword matches
    matches = sum([
        analysis["requires_flights"],
        analysis["requires_hotels"], 
        analysis["requires_esim"],
        analysis["requires_activities"]
    ])
    analysis["confidence"] = min(matches * 0.25, 1.0)
    
    return analysis

TOOLS: List[Callable[..., Any]] = [
    delegate_to_flight_agent,
    delegate_to_hotel_agent,
    delegate_to_esim_agent,
    delegate_to_activities_agent,
    analyze_travel_request
]