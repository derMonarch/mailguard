from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view

from ..models.serializers.task_serializer import TaskSerializer


@api_view(["POST"])
def tasks_handler(request):
    if request.method == "POST":
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return JsonResponse({"message": "ok"}, status=status.HTTP_201_CREATED)

        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
