from django.http import JsonResponse


def response(message=None, data=None, status_code=200):
    response_data = {}

    if message:
        if status_code >= 400:
            response_data["error"] = message
        else:
            response_data["success"] = True
            response_data["message"] = message

    if data:
        if status_code >= 400:
            response_data["details"] = data
        else:
            response_data["data"] = data

    return JsonResponse(response_data, status=status_code)
