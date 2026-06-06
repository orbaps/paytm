import time
from collections import defaultdict, deque

from fastapi import HTTPException, Request, status

from .config import get_settings


_requests: dict[str, deque[float]] = defaultdict(deque)


def enforce_rate_limit(request: Request) -> None:
    settings = get_settings()
    if not settings.rate_limit_enabled:
        return

    client = request.client.host if request.client else "unknown"
    now = time.time()
    window_start = now - settings.rate_limit_window_seconds
    bucket = _requests[client]

    while bucket and bucket[0] < window_start:
        bucket.popleft()

    if len(bucket) >= settings.rate_limit_requests:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded",
        )

    bucket.append(now)
