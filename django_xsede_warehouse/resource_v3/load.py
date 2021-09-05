from resource_v2.models import *
from resource_v2.serializers import *
from resource_v3.models import *
from django.forms.models import model_to_dict

import pdb
def copy_v2_to_v3():
    pdb.set_trace()
#    for item in ResourceV2Provider.objects.all().iterator():
#        new_obj, created = ResourceV3Provider.objects.update_or_create(ID=item.ID)
#        item_dict = model_to_dict(item)
#        for field in ResourceV2Provider._meta.fields:
#            setattr(new_obj, field.name, item_dict[field.name])
##            if field.get_internal_type() == "DateTimeField":
##                setattr(new_obj, field.name, getattr(ResourceV2Provider.data, field.name).strftime('%Y-%m-%dT%H:%M:%S%z'))
##            else:
##                setattr(new_obj, field.name, getattr(ResourceV2Provider, field.name))
#        new_obj.save()
#
#    for item in ResourceV2.objects.all().iterator():
#        new_obj, created = ResourceV3.objects.update_or_create(ID=item.ID)
#        item_dict = model_to_dict(item)
#        for field in ResourceV2._meta.fields:
#            setattr(new_obj, field.name, item_dict[field.name])
##            if field.get_internal_type() == "DateTimeField":
##                setattr(new_obj, field.name, getattr(ResourceV2Provider, field.name).strftime('%Y-%m-%dT%H:%M:%S%z'))
##            else:
##                setattr(new_obj, field.name, getattr(ResourceV2, field.name))
#        new_obj.save()
