from fastapi import HTTPException
from typing import Optional

VALID_API_KEYS = [
    "verysecureapikey",
    "anothersecureapi",
    "onemoresecureapi",
]


async def get_api_key(api_key: Optional[str]):
    if api_key not in VALID_API_KEYS:
        raise HTTPException(
            status_code=403, detail="Invalid API Key"
        )
    return api_key
