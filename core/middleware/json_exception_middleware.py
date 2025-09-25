import json
import traceback
from django.http import Http404
from django.core.exceptions import PermissionDenied, ValidationError
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from core.helpers.response import response


class JsonExceptionMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        if isinstance(exception, Http404):
            return response(message="Not found", data=str(exception), status_code=404)

        elif isinstance(exception, PermissionDenied):
            return response(
                message="Permission denied", data=str(exception), status_code=403
            )

        elif isinstance(exception, ValidationError):
            return response(
                message="Validation error", data=str(exception), status_code=400
            )

        else:
            if settings.DEBUG:
                return response(
                    message="Internal server error",
                    data=str(exception),
                    traceback=traceback.format_exc(),
                    status_code=500,
                )
            else:
                return response(message="Internal server error", status_code=500)

    def process_response(self, request, django_response):
        if django_response.status_code >= 400:
            if hasattr(django_response, "content") and django_response.content:
                try:
                    content = json.loads(django_response.content.decode("utf-8"))
                    if isinstance(content, dict) and "success" not in content:
                        return response(
                            message=content.get("detail", "Error occurred"),
                            data=content,
                            status_code=django_response.status_code,
                        )
                except (json.JSONDecodeError, UnicodeDecodeError):
                    pass

            if response.status_code == 404:
                return JsonResponse(
                    {"success": False, "code": 404, "message": "Not found"}, status=404
                )
            elif response.status_code == 500:
                return JsonResponse(
                    {"success": False, "code": 500, "message": "Internal server error"},
                    status=500,
                )
            elif response.status_code == 400:
                return JsonResponse(
                    {"success": False, "code": 400, "message": "Bad request"},
                    status=400,
                )
            elif response.status_code == 403:
                return JsonResponse(
                    {"success": False, "code": 403, "message": "Forbidden"}, status=403
                )
            elif response.status_code == 401:
                return JsonResponse(
                    {"success": False, "code": 401, "message": "Unauthorized"},
                    status=401,
                )

        return response
