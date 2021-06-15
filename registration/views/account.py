from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models.serializers.account_serializer import AccountSerializer


@api_view(['POST'])
def account_handler(request):
    if request.method == 'POST':
        serializer = AccountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response("OK", status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
