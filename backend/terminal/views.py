from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .executor import executor
import json

@csrf_exempt
def run_command(request):
    if request.method == "POST":
        data = json.loads(request.body)
        command = data.get("command", "")
        tab_id  = data.get("tab_id", "default")
        result  = executor.execute(command, tab_id)
        return JsonResponse(result)
    return JsonResponse({"error": "POST only"}, status=405)

@csrf_exempt
def get_history(request):
    tab_id = request.GET.get("tab_id", None)
    return JsonResponse({"history": executor.get_history(tab_id)})

@csrf_exempt
def get_cwd(request):
    return JsonResponse({"cwd": executor.cwd})