from django.conf.urls import url
from django.shortcuts import render
from rest_framework_swagger.views import get_swagger_view

def home(request):
    uuid = None
    access_token = None
    refresh_token = None
    if request.user.is_authenticated:
        uuid = request.user.social_auth.get(provider='globus').uid
        social = request.user.social_auth
        access_token = social.get(provider='globus').extra_data['access_token']
        refresh_token = social.get(provider='globus').extra_data['refresh_token']
    return render(request,
                  'home.html',
                  {'uuid': uuid,
                  'access_token': access_token,
                  'refresh_token': refresh_token})
