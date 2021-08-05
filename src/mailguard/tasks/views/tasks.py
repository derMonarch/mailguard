from django.http import JsonResponse
from mailguard.tasks.models.serializers.task_serializer import TaskSerializer
from rest_framework import status
from rest_framework.decorators import api_view


@api_view(["POST"])
def tasks_handler(request):
    if request.method == "POST":
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = {"id": serializer.instance.id, **serializer.data}

            return JsonResponse(response, status=status.HTTP_201_CREATED)

        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
