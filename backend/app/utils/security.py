from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

API_CSP = "default-src 'none'; frame-ancestors 'none'; base-uri 'none'"
# Swagger UI and ReDoc load their assets from jsDelivr. They are disabled in production.
DOCS_CSP = (
    "default-src 'none'; script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
    "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://fonts.googleapis.com; "
    "font-src https://fonts.gstatic.com; img-src 'self' data: https://fastapi.tiangolo.com https://cdn.redoc.ly; "
    "connect-src 'self'; worker-src blob:; frame-ancestors 'none'; base-uri 'none'"
)
DOCS_PATHS = {'/docs', '/redoc', '/docs/oauth2-redirect'}


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        response.headers['Permissions-Policy'] = 'camera=(), microphone=(), geolocation=()'
        response.headers['Content-Security-Policy'] = DOCS_CSP if request.url.path in DOCS_PATHS else API_CSP
        return response
