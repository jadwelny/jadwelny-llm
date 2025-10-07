from typing import Any, Callable, Dict, List, Optional

async def search_activities(
    location: str,
    travel_dates: List[str],
    interests: List[str],
    budget_per_activity: Optional[str] = None
) -> Dict[str, Any]:
    """Search for activities based on specified criteria.

    Args:
        location: Location for activities
        travel_dates: List of available dates for activities
        interests: List of activity types or interests
        budget_per_activity: Budget range per activity

    Returns:
        Activity recommendations and booking options
    """
    # Simulate activity search API call
    activities = [
        {
            "activity_id": "ACT001",
            "name": "City Tour",
            "location": location,
            "price": 50,
            "rating": 4.8,
            "duration": "3 hours"
        },
        {
            "activity_id": "ACT002",
            "name": "Museum Visit",
            "location": location,
            "price": 20,
            "rating": 4.6,
            "duration": "2 hours"
        }
    ]
    return {
        "search_criteria": {
            "location": location,
            "travel_dates": travel_dates,
            "interests": interests,
            "budget_per_activity": budget_per_activity
        },
        "activities": activities,
        "total_results": len(activities)
    }

TOOLS: List[Callable[..., Any]] = [
    search_activities
]

