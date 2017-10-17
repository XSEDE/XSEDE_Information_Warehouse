from rest_framework import status
from rest_framework.response import Response

def MyAPIResponse(data, code=None, template_name=None):
    if data is None:
        my_data = {}
    else:
        my_data = data
    my_data['status_code'] = code or status.HTTP_200_OK
    return Response(my_data, template_name=template_name)
