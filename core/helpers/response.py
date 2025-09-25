from django.http import JsonResponse


def response(message=None, data=None, status_code=200, **kwargs):
    response_data = {}

    if status_code >= 400:
        response_data["success"] = False
        response_data["code"] = status_code

        if message:
            response_data["message"] = message
        if data:
            response_data["error"] = data
        
        response_data.update(kwargs)
    else:
        response_data["success"] = True
        
        if message:
            response_data["message"] = message
        if data:
            response_data["data"] = data
        
        response_data.update(kwargs)

    return JsonResponse(response_data, status=status_code)
