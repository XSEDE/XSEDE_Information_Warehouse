from django.conf.urls import include, url
from xcsr_db.views import *

# Define our custom URLs
# Additionally, we include login URLs for the browseable API.
urlpatterns = [
    url(r'^componentsprequirement/$', ComponentSPRequirement_List.as_view(), name='componentsprequirement-list'),
    url(r'^componentsprequirement/component/(?P<component>[^/]+)/spclass/(?P<spclass>[^/]+)/$', ComponentSPRequirement_Detail.as_view(), name='componentsprequirement-detail'),
    url(r'^supportcontacts/$', SupportContacts_List.as_view(), name='supportcontacts-list'),
    url(r'^supportcontacts/globalid/(?P<globalid>[^/]+)/$', SupportContacts_Detail.as_view(), name='supportcontacts-detail'),
    #url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
