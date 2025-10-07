from typing import Any, Callable, Dict, List, Optional

async def search_esim_plans(
    destination_country: str,
    travel_duration: int,
    data_needs: str = "moderate"
) -> Dict[str, Any]:
    """Search for eSIM plans based on specified criteria.

    Args:
        destination_country: Country or region for eSIM coverage
        travel_duration: Duration of travel in days
        data_needs: Data usage level (light, moderate, heavy)

    Returns:
        eSIM plan options and activation instructions
    """
    # Simulate eSIM search API call
    plans = [
        {
            "plan_id": "ESIM001",
            "provider": "ConnectData",
            "country": destination_country,
            "data_allowance": "10 GB",
            "validity_days": 30,
            "price": 25
        },
        {
            "plan_id": "ESIM002",
            "provider": "GlobalRoam",
            "country": destination_country,
            "data_allowance": "5 GB",
            "validity_days": 15,
            "price": 15
        }
    ]
    return {
        "search_criteria": {
            "destination_country": destination_country,
            "travel_duration": travel_duration,
            "data_needs": data_needs
        },
        "plans": plans,
        "total_results": len(plans)
    }

TOOLS: List[Callable[..., Any]] = [
    search_esim_plans
]

