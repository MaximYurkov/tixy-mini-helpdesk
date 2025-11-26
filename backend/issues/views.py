from django.http import JsonResponse

def health(request):
    return JsonResponse({"status": "ok"})

from rmq.tasks import fetch_cat_fact_task
from celery.result import AsyncResult
from rmq.celery_app import app as celery_app

def create_cat_fact_task(request):
    if request.method != "POST":
        return JsonResponse({"error": "only POST allowed"}, status=405)
    task = fetch_cat_fact_task.delay()
    return JsonResponse({"task_id": task.id})

def get_task_status(request, task_id):
    result = AsyncResult(task_id, app=celery_app)
    data = {
        "task_id": task_id,
        "state": result.state,
    }
    if result.ready():
        data["result"] = result.result
    return JsonResponse(data)
