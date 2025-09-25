from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view


@api_view(["GET"])
def health(request):
    return JsonResponse({"status": "OK", "message": "Service is healthy"})
