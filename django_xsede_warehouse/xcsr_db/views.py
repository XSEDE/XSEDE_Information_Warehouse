from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response
from xcsr_db.models import *
from xcsr_db.serializers import *

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
