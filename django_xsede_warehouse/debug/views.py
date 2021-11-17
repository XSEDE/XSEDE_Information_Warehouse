from django.views import debug
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
import sys

# Create your views here.

class Debug_Detail(APIView):
    '''
        Dump DEBUG technical_500_response
    '''
    permission_classes = (IsAuthenticatedOrReadOnly,)
    @extend_schema(request=None, responses={400: OpenApiTypes.OBJECT})
    def get(self, request, format=None, **kwargs):
        return debug.technical_500_response(request, *sys.exc_info(), status_code=400)
