from django.http import JsonResponse
from django.conf import settings


class ApiKeyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith("/api/"):
            api_key_header = getattr(settings, "API_KEY_HEADER_NAME", "X-API-Key")
            expected_api_key = getattr(
                settings, "API_KEY_SECRET", "horizon-router-api-key"
            )

            provided_api_key = request.META.get(
                f"HTTP_{api_key_header.upper().replace('-', '_')}"
            )

            if not provided_api_key:
                return JsonResponse(
                    {"error": f"Missing {api_key_header} header"}, status=401
                )

            if provided_api_key != expected_api_key:
                return JsonResponse({"error": "Invalid API key"}, status=401)

        response = self.get_response(request)
        return response
