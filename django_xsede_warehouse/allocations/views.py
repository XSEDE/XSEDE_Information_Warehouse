from drf_spectacular.utils import extend_schema

# Create your views here.
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework_xml.renderers import XMLRenderer
from xsede_warehouse.exceptions import MyAPIException
from xsede_warehouse.responses import MyAPIResponse
from projectresources.models import *
from projectresources.serializers import *

# Create your views here.
class AllocationResources_List(APIView):
    '''
        ### Allocation Resources list
        
        Optional response argument(s):
        ```
            format={json,xml,html}              (json default)
        ```
    '''
    permission_classes = (IsAuthenticatedOrReadOnly,)
    renderer_classes = (JSONRenderer,TemplateHTMLRenderer,XMLRenderer,)
    @extend_schema(responses=ProjectResource_Serializer)
    def get(self, request, format=None, **kwargs):
        if 'ResourceID' in self.kwargs:
            try:
                objects = ProjectResource.objects.filter(ResourceID=self.kwargs['ResourceID'])
            except ProjectResource.DoesNotExist:
                raise MyAPIException(code=status.HTTP_404_NOT_FOUND, detail='Allocation resources not found')
        elif 'project_number' in self.kwargs:
            try:
                objects = ProjectResource.objects.filter(project_number=self.kwargs['project_number'])
            except ProjectResource.DoesNotExist:
                raise MyAPIException(code=status.HTTP_404_NOT_FOUND, detail='Allocation resources not found')
        else:
            objects = ProjectResource.objects.all()
        serializer = ProjectResource_Serializer(objects, context={'request': request}, many=True)
        response_obj = {'results': serializer.data}
        return MyAPIResponse(response_obj, template_name='allocations/allocationresources_list.html')
