from rest_framework.decorators import api_view

from ussdapp.processor import USSDProcessor


@api_view(['GET', 'POST', 'OPTIONS'])
def check_it(request):
    data = request.data
    processor = USSDProcessor(data=data)
    return processor.process_request()
