from rest_framework.decorators import api_view, renderer_classes, permission_classes
from rest_framework import renderers, response, schemas
from rest_framework_swagger.renderers import OpenAPIRenderer, SwaggerUIRenderer
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny

#@api_view()
#@renderer_classes([SwaggerUIRenderer, OpenAPIRenderer, renderers.CoreJSONRenderer])
#@permission_classes((IsAuthenticatedOrReadOnly,))
#def schema_view(request):
class Swagger_List(APIView):
    permission_classes = (AllowAny,)
    def get(self, request, format=None):
        generator = schemas.SchemaGenerator(title='XSEDE Warehouse API')
        return response.Response(generator.get_schema(request=request))