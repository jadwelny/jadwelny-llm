#!/usr/bin/env python
# In[1]:


import json
from typing import Any, Callable, Dict, List, Optional
from langgraph_sdk import get_client
from .context import Context


# In[2]:


async def delegate_to_flight_agent(
    origin: str,
    destination: str,
    departure_date: str,
    return_date: Optional[str] = None,
    passengers: int = 1,
    class_preference: str = "economy"
) -> Dict[str, Any]:
    """Delegate flight search and booking tasks to the specialized flight agent."""
    client = get_client(url="http://localhost:8000")
    thread = await client.threads.create()
    flight_request = {
        "origin": origin,
        "destination": destination,
        "departure_date": departure_date,
        "return_date": return_date,
        "passengers": passengers,
        "class_preference": class_preference
    }
    response = await client.runs.create(
        thread_id=thread["thread_id"],
        assistant_id="flight_agent",
        input={
            "messages": [{"type": "human", "content": [{"type": "text", "text": json.dumps(flight_request)}]}]
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
    """Delegate hotel search and booking tasks to the specialized hotel agent."""
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
            "messages": [{"type": "human", "content": [{"type": "text", "text": json.dumps(hotel_request)}]}]
        }
    )
    return response

async def delegate_to_esim_agent(
    destination_country: str,
    travel_duration: int,
    data_needs: str = "moderate"
) -> Dict[str, Any]:
    """Delegate eSIM search and activation to the specialized eSIM agent."""
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
            "messages": [{"type": "human", "content": [{"type": "text", "text": json.dumps(esim_request)}]}]
        }
    )
    return response

async def delegate_to_activities_agent(
    location: str,
    travel_dates: List[str],
    interests: List[str],
    budget_per_activity: Optional[str] = None
) -> Dict[str, Any]:
    """Delegate activity search and booking to the specialized activities agent."""
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
            "messages": [{"type": "human", "content": [{"type": "text", "text": json.dumps(activities_request)}]}]
        }
    )
    return response

async def analyze_travel_request(user_message: str) -> Dict[str, Any]:
    """Analyze the user's travel request to determine which sub-agents to involve."""
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

async def get_weather(city: str) -> Dict[str, Any]:
    """Get the current weather for a given city.

    Args:
        city: The city for which to get the weather.

    Returns:
        A dictionary containing weather information.
    """
    # Simulate weather API call
    weather_data = {
        "city": city,
        "temperature": "25°C",
        "condition": "Sunny",
        "humidity": "60%"
    }
    return weather_data

TOOLS: List[Callable[..., Any]] = [
    delegate_to_flight_agent,
    delegate_to_hotel_agent,
    delegate_to_esim_agent,
    delegate_to_activities_agent,
    analyze_travel_request,
    get_weather
]

