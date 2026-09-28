from __future__ import annotations
import time
import uuid
from collections import defaultdict, deque
from threading import Lock
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse


class RequestContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = request.headers.get('X-Request-ID') or str(uuid.uuid4())
        request.state.request_id = request_id
        started = time.perf_counter()
        response = await call_next(request)
        response.headers['X-Request-ID'] = request_id
        response.headers['Server-Timing'] = f'app;dur={(time.perf_counter() - started) * 1000:.1f}'
        return response


class InMemoryRateLimitMiddleware(BaseHTTPMiddleware):
    """Development safety net only. Production should use a shared Redis/API-gateway limiter."""
    def __init__(self, app, requests_per_minute: int = 120):
        super().__init__(app)
        self.requests_per_minute = requests_per_minute
        self._hits = defaultdict(deque)
        self._lock = Lock()

    async def dispatch(self, request: Request, call_next):
        if request.url.path in {'/health', '/ready'}:
            return await call_next(request)
        key = request.client.host if request.client else 'unknown'
        now = time.monotonic()
        with self._lock:
            q = self._hits[key]
            while q and q[0] <= now - 60:
                q.popleft()
            if len(q) >= self.requests_per_minute:
                return JSONResponse(status_code=429, content={'detail': 'Rate limit exceeded'})
            q.append(now)
        return await call_next(request)
