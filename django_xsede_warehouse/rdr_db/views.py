from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework_xml.renderers import XMLRenderer
from rest_framework.response import Response
from rest_framework import status
from rdr_db.models import *
from rdr_db.serializers import *
from xsede_warehouse.exceptions import MyAPIException
from xsede_warehouse.responses import MyAPIResponse

# Create your views here.
class RDRResource_List(APIView):
    '''
        All RDR resources
    '''
    permission_classes = (IsAuthenticatedOrReadOnly,)
    renderer_classes = (JSONRenderer,TemplateHTMLRenderer,XMLRenderer,)
    def get(self, request, format=None, **kwargs):
        if 'resourceid' in self.kwargs:
            objects = RDRResource.objects.filter(info_resourceid__exact=self.kwargs['resourceid'])
        elif 'siteid' in self.kwargs:
            objects = RDRResource.objects.filter(info_siteid__exact=self.kwargs['siteid'])
        elif 'rdrtype' in self.kwargs:
            objects = RDRResource.objects.filter(rdr_type__exact=self.kwargs['rdrtype'])
        else:
            objects = RDRResource.objects.all()
        try:
            sort_by = request.GET.get('sort')
            objects_sorted = objects.order_by(sort_by)
        except:
            objects_sorted = objects
        serializer = RDRResource_Serializer_Plus(objects_sorted, context={'request': request}, many=True)
        return MyAPIResponse({'result_set': serializer.data}, template_name='rdr_db/list.html')

class RDRResource_Detail(APIView):
    '''
        A specific resource
    '''
    permission_classes = (IsAuthenticatedOrReadOnly,)
    renderer_classes = (JSONRenderer,TemplateHTMLRenderer,XMLRenderer,)
    def get(self, request, format=None, **kwargs):
        try:
            int(self.kwargs['id'])
            object = RDRResource.objects.get(pk=self.kwargs['id'])
        except ValueError:
            raise MyAPIException(code=status.HTTP_400_BAD_REQUEST, detail='ID parameter is not valid')
        except RDRResource.DoesNotExist:
            raise MyAPIException(code=status.HTTP_404_NOT_FOUND, detail='Specified ID not found')
        serializer = RDRResource_Serializer(object)
        return MyAPIResponse({'result_set': [serializer.data]}, template_name='rdr_db/detail.html')

class RDRResource_XUP_List(APIView):
    '''
        All RDR resources for the XUP
    '''
    permission_classes = (IsAuthenticatedOrReadOnly,)
    renderer_classes = (JSONRenderer,XMLRenderer,)
    def get(self, request, format=None):
        objects = RDRResource.objects.all()
        serializer = RDRResource_Serializer(objects, many=True)
        return Response(serializer.data)

class RDRResource_XUP_Detail(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    renderer_classes = (JSONRenderer,XMLRenderer,)
    def get(self, request, format=None, **kwargs):
        try:
            int(self.kwargs['id'])
            object = RDRResource.objects.get(pk=self.kwargs['id'])
        except ValueError:
            raise MyAPIException(code=status.HTTP_400_BAD_REQUEST, detail='ID parameter is not valid')
        except RDRResource.DoesNotExist:
            raise MyAPIException(code=status.HTTP_404_NOT_FOUND, detail='ID not found')
        serializer = RDRResource_Serializer(object)
        return Response({'result_set': [serializer.data]}, template_name='rdr_db/detail.html')
