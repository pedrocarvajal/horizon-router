from django.conf import settings
from core.helpers.response import response


class ApiKeyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        exempt_paths = getattr(settings, "API_KEY_EXEMPT_EXACT_PATHS", [])
        exempt_prefixes = getattr(settings, "API_KEY_EXEMPT_PATH_PREFIXES", [])

        is_exempt = request.path in exempt_paths or any(
            request.path.startswith(prefix) for prefix in exempt_prefixes
        )

        if not is_exempt and request.path.startswith("/api/"):
            api_key_header = getattr(settings, "API_KEY_HEADER_NAME", "X-API-Key")
            expected_api_key = getattr(
                settings, "API_KEY_SECRET", "horizon-router-api-key"
            )

            provided_api_key = request.META.get(
                f"HTTP_{api_key_header.upper().replace('-', '_')}"
            )

            if not provided_api_key:
                return response(
                    message=f"Missing {api_key_header} header", status_code=401
                )

            if provided_api_key != expected_api_key:
                return response(message="Invalid API key", status_code=401)

        django_response = self.get_response(request)
        return django_response
