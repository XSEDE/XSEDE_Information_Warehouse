from django.urls import include, path
from xcsr_db.views import *

# Define our custom URLs
# Additionally, we include login URLs for the browseable API.
urlpatterns = [
    path(r'componentsprequirement/', ComponentSPRequirement_List.as_view(), name='componentsprequirement-list'),
    path(r'componentsprequirement/component/<str:component>/spclass/<str:spclass>/', ComponentSPRequirement_Detail.as_view(), name='componentsprequirement-detail'),
    path(r'supportcontacts/', SupportContacts_List.as_view(), name='supportcontacts-list'),
    path(r'supportcontacts/globalid/<str:globalid>/', SupportContacts_Detail.as_view(), name='supportcontacts-detail'),
]
