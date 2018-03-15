import sys
from django.views import debug
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.views import APIView

# Create your views here.

class Debug_Detail(APIView):
    '''
        Dump DEBUG technical_500_response
    '''
    permission_classes = (IsAuthenticatedOrReadOnly,)
    exclude_from_schema = True
    def get(self, request, format=None, **kwargs):
        return debug.technical_500_response(request, *sys.exc_info(), status_code=400)
