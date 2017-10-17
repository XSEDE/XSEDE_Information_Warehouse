from django.db.models import Q
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.renderers import JSONRenderer
from rest_framework_xml.renderers import XMLRenderer
#from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rdr_db.models import *
from rdr_db.filters import *
from rdr_db.serializers import *
from itertools import chain

# Create your views here.
class RDRResource_XUP_v2_List(APIView):
    '''
        Selected RDR resources: affiliated with XSEDE, active, and allocated
    '''
    permission_classes = (IsAuthenticatedOrReadOnly,)
#    renderer_classes = (JSONRenderer,XMLRenderer,TemplateHTMLRenderer,)
    renderer_classes = (JSONRenderer,XMLRenderer,)
    def get(self, request, format=None):
        returnformat = request.query_params.get('format', 'json')
        all_resources = RDR_Active_Resources(affiliation='XSEDE', allocated=True, type='ALL', result='OBJECTS')
        serializer = RDRResource_Serializer(all_resources, many=True)
        #return Response(serializer.data)
        if returnformat != 'html':
            return Response(serializer.data)
        else:
            return render(request, 'rdr_db/rdr_resources.html', {'resource_list': serializer.data})
