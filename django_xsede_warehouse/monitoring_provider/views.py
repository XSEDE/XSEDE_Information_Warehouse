from django.utils import timezone

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response
from monitoring_provider.process import Glue2ProcessRawMonitoring
import pdb

class Glue2ProcessDoc(APIView):
#    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticatedOrReadOnly,)
    def post(self, request, doctype, resourceid, format=None):
        proc = Glue2ProcessRawMonitoring(application='monitoring_provider.views', function='Glue2ProcessDoc')
        ts = timezone.now()
        (code, message) = proc.process(ts, doctype, resourceid, request.data)
        if code is True:
            return Response(message, status=status.HTTP_201_CREATED)
        else:
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
