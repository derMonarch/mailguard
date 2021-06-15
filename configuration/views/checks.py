from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from ..models.serializers.checks_serializers import ChecksSerializer


@api_view(['POST'])
def checks_handler(request):
    if request.method == 'POST':
        serializer = ChecksSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response("OK", status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
