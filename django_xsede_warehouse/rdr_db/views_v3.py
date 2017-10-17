from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.renderers import JSONRenderer
from rest_framework_xml.renderers import XMLRenderer
from rdr_db.filters import RDR_Active_Resources
from rdr_db.serializers import RDRResource_Serializer
from xsede_warehouse.responses import MyAPIResponse

# Create your views here.
class RDRResource_XUP_v3_List(APIView):
    '''
        Selected RDR resources: affiliated with XSEDE, active, and allocated
    '''
    permission_classes = (IsAuthenticatedOrReadOnly,)
    renderer_classes = (JSONRenderer,XMLRenderer,)
    def get(self, request):
        objects = RDR_Active_Resources(affiliation='XSEDE', allocated=True, type='ALL', result='OBJECTS')
        serializer = RDRResource_Serializer(objects, many=True)
        return MyAPIResponse({'result_set': serializer.data})
