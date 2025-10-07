#!/usr/bin/env python
# In[1]:


from typing import Any, Callable, Dict, List, Optional


# In[2]:


async def get_order_hotel_name(token: str) -> List[Dict[str, Any]]:
    """Get the hotel names from the user's existing bookings.

    Args:
        token: Authorization token for the user.

    Returns:
        A list of dictionaries, each containing an order_id and hotel_name.
    """
    # Simulate API call to retrieve order hotel names
    return [
        {"order_id": "ORD123", "hotel_name": "Grand Hyatt"},
        {"order_id": "ORD456", "hotel_name": "Hilton Garden Inn"}
    ]

async def get_order_status(token: str) -> List[Dict[str, Any]]:
    """Get the booking status of the user's hotel orders.

    Args:
        token: Authorization token for the user.

    Returns:
        A list of dictionaries, each containing an order_id and status.
    """
    # Simulate API call
    return [
        {"order_id": "ORD123", "status": "Confirmed"},
        {"order_id": "ORD456", "status": "Pending"}
    ]

async def get_order_guest_data(token: str) -> List[Dict[str, Any]]:
    """Get the guest information for the user's hotel orders.

    Args:
        token: Authorization token for the user.

    Returns:
        A list of dictionaries, each containing an order_id and guest_data.
    """
    # Simulate API call
    return [
        {"order_id": "ORD123", "guest_data": {"name": "John Doe", "email": "johndoe@example.com"}}
    ]

async def get_order_cancellation(token: str) -> List[Dict[str, Any]]:
    """Get the cancellation details for the user's hotel orders.

    Args:
        token: Authorization token for the user.

    Returns:
        A list of dictionaries, each containing an order_id and cancellation details.
    """
    # Simulate API call
    return [
        {"order_id": "ORD123", "cancellation": {"policy": "Free cancellation within 48 hours"}}
    ]

async def get_order_location(token: str) -> List[Dict[str, Any]]:
    """Get the location details of the user's hotel orders.

    Args:
        token: Authorization token for the user.

    Returns:
        A list of dictionaries, each containing an order_id, longitude, and latitude.
    """
    # Simulate API call
    return [
        {"order_id": "ORD123", "longitude": -73.9857, "latitude": 40.7484}
    ]

TOOLS: List[Callable[..., Any]] = [
    get_order_hotel_name,
    get_order_status,
    get_order_guest_data,
    get_order_cancellation,
    get_order_location
]


