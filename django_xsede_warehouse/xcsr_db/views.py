from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework_xml.renderers import XMLRenderer
from rest_framework.response import Response
from xcsr_db.models import *
from glue2_db.models import AdminDomain
from xcsr_db.serializers import *
from xsede_warehouse.exceptions import MyAPIException
from xsede_warehouse.responses import MyAPIResponse
import pdb

# Create your views here.
class ComponentSPRequirement_List(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    def get(self, request, format=None):
        objects = ComponentSPRequirement.objects.all()
        serializer = ComponentSPRequirement_Serializer(objects, many=True)
        return Response(serializer.data)

class ComponentSPRequirement_Detail(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    def get(self, request, component, spclass, format=None):
        object = ComponentSPRequirement.objects.all()
        object = object.filter(ComponentName__exact=component).filter(SPClass__exact=spclass)
        serializer = ComponentSPRequirement_Serializer(object, many=True)
        return Response(serializer.data)

class SupportContacts_List(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    renderer_classes = (JSONRenderer,TemplateHTMLRenderer,XMLRenderer,)
    def get(self, request, format=None):
        objects = AdminDomain.objects.all()
        serializer = SupportContacts_Serializer(objects, context={'request': request}, many=True)
        response_obj = {'results': serializer.data}
        return MyAPIResponse(response_obj, template_name='xcsr_db/supportcontact_list.html')

class SupportContacts_Detail(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    renderer_classes = (JSONRenderer,TemplateHTMLRenderer,XMLRenderer,)
    def get(self, request, format=None, **kwargs):
        if 'globalid' in self.kwargs:
            try:
                objects = AdminDomain.objects.filter(EntityJSON__GlobalID__exact=self.kwargs['globalid'])
            except AdminDomain.DoesNotExist:
                raise MyAPIException(code=status.HTTP_404_NOT_FOUND, detail='Specified Global ID not found')
        if len(objects) > 1:
            raise MyAPIException(code=status.HTTP_404_NOT_FOUND, detail='Unexpected multiple Global IDs found')
        serializer = SupportContacts_Serializer(objects, context={'request': request}, many=True)
        response_obj = {'results': serializer.data}
        return MyAPIResponse(response_obj, template_name='xcsr_db/supportcontact_detail.html')
