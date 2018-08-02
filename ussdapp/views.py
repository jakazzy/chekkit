from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from ussdapp.processor import USSDProcessor


@api_view(['OPTIONS', 'GET', 'POST'])
def check_it(request):
    if request.method == 'OPTIONS':
        return Response({}, status=status.HTTP_200_OK)
    else:
        data = request.data
        processor = USSDProcessor(data=data)
        return processor.process_request()
