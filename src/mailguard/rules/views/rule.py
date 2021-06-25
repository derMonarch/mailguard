from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from ..models.serializers.task_to_rule_serializer import TaskToRuleSerializer


@api_view(["POST"])
def rules_handler(request):
    if request.method == "POST":
        serializer = TaskToRuleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return JsonResponse({"message": "ok"}, status=status.HTTP_201_CREATED)

        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
