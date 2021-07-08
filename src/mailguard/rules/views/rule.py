from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view

from mailguard.rules.models.serializers.task_to_rule_serializer import TaskToRuleSerializer
from mailguard.rules.services import basic


@api_view(["POST"])
def task_rules_handler(request):
    if request.method == "POST":
        serializer = TaskToRuleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = {"id": serializer.instance.id, **serializer.data}

            return JsonResponse(response, status=status.HTTP_201_CREATED)

        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def rules_handler(request):
    # TODO: validate input, with custom schema?
    if request.method == "POST":
        created = basic.create_new_rule(request.data)

        return JsonResponse(created, status=status.HTTP_201_CREATED)
