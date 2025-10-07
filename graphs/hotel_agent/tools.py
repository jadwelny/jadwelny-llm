from typing import Any, Dict, Optional


async def search_hotels(
    checkin: Optional[str] = None,
    checkout: Optional[str] = None,
    search_type: Optional[str] = None,
    region_id: Optional[str] = None,
    hotel_ids: Optional[list] = None,
    hotel_id: Optional[str] = None,
    geo: Optional[Dict[str, str]] = None,
    filter_stars: Optional[int] = None,
    filter_free_cancellation: Optional[bool] = None
) -> Dict[str, Any]:

    required_fields = ["checkin", "checkout", "search_type"]
    missing_fields = [field for field in required_fields if locals()[field] is None]

    if missing_fields:
        return {
            "type": "function",
            "function": {
                "name": "hotel_search",
                "description": "Collect missing search data from user.",
                "missing_fields": missing_fields
            }
        }

    # All required fields are present, return the full search JSON
    return {
        "type": "function",
        "function": {
            "name": "hotel_search",
            "description": "Start or continue the hotel booking flow.",
            "parameters": {
                "checkin": checkin,
                "checkout": checkout,
                "search_type": search_type,
                "region_id": region_id,
                "hotel_ids": hotel_ids,
                "hotel_id": hotel_id,
                "geo": geo,
                "filter": {
                    "stars": filter_stars,
                    "free_cancellation": filter_free_cancellation
                }
            }
        }
    }
