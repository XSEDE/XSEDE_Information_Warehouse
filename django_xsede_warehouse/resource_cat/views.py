from django.db.models.expressions import RawSQL
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from django.utils.dateparse import parse_date, parse_datetime
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework_xml.renderers import XMLRenderer
from rest_framework.response import Response
from rest_framework import status
from resource_cat.models import *
from resource_cat.serializers import *
from xsede_warehouse.exceptions import MyAPIException
from xsede_warehouse.responses import MyAPIResponse
import datetime
from datetime import datetime, timedelta
import pytz
Central = pytz.timezone("US/Central")
UTC = pytz.timezone("UTC")

def resource_categories_filter(input_objects, search_categories_set):
    # Inspect objects because we can't push this filter to the database
    filtered_objects = []
    for obj in input_objects:
        objcats = obj.EntityJSON.get('category', '')
        if len(objcats or '') < 1: # Skip objects without a category
            continue
        objcats_list = set(objcats.split(','))
        if not objcats_list.isdisjoint(search_categories_set):
            filtered_objects.append(obj)
    return(filtered_objects)

def resource_oldevents_filter(input_objects):
    # Inspect objects because we can't push this filter to the database
    cur_datetime = timezone.now().astimezone(UTC).strftime('%Y-%m-%dT%H:%M:%S%z')
    filtered_objects = []
    for obj in input_objects:
        if obj.Type == 'Event':
            edt = obj.EntityJSON.get('end_date_time', '')
            if edt < cur_datetime: # Skip events that ended in the past
                continue
        filtered_objects.append(obj)
    return(filtered_objects)

def resource_subtotals(input_objects):
    category_totals = {}
    provider_totals = {}
    provider_alt_id = {}
    for obj in input_objects:
        this_category = obj.EntityJSON.get('category', None)
        if this_category:
            for x in this_category.split(','):
                category_totals[x] = category_totals.get(x, 0) + 1
        this_provider = obj.ProviderID
        if this_provider:
            provider_totals[this_provider] = provider_totals.get(this_provider, 0) + 1
            provider_alt_id[this_provider] = obj.EntityJSON.get('provider', None)
    category_return = [ {'id': key, 'subtotal': value} for key, value in category_totals.items() ]
    provider_return = [ {'ProviderID': key, 'id': provider_alt_id[key], 'subtotal': value} for key, value in provider_totals.items() ]
    return({'categories': category_return, 'providers': provider_return})

def resource_terms_filtersort(input_objects, search_terms_set, sort_field='name'):
    # This function inspects and sorts objects using an algorithm that is too complex to do using SQL
    # Sorting algorithms requirements:
    #   First prioritize resources with a tag/keyword matching at least one search term
    #     Exampe: given search terms "frog spectrometer chuckles", resources with a "spectrometer" tag should
    #     be listed before resources with no tags matching a search term
    #   Second, prioritize resources with resource_name and resource_description matching ALL of the search terms.
    #     Example: gieven search terms "frog spectrometer chuckles", resources with ALL those words in
    #     resource_description and/or resource_name should be listed before resources with some matching terms.
    #   Third, prioritize resources with resource_name and resource_description matching SOME of the search terms.
    #     In this case, ordering sould be based on the total number of occurances of the search terms.
    #     For example, if the search term is "python", resources that have the term three times should be listed
    #     before resources with that term happening 2 times or once.

    # SORT_KEY fields:
    #   <B_RANK>:<C_RANK>:<D_RANK>:<D_RANK>:<SORT_SUFFIX>
    # Where:
    #   A_RANK: all terms matched Name; RANK=999 minus how many keywords matched
    #   B_RANK: keyword match; RANK=999 minus how many keywords matched
    #   C_RANK: all terms matched Name or Description; RANK=999 minus how many terms matched
    #   D_RANK: some terms matched Name or Description; RANK=999 minus total number of words matching terms
    # Where "999 minus match count" makes higher match counts sort firts alphabetically (996=999-3 before 998=999-1)
    sort_array = {}
    
    for obj in input_objects:
        name_words = obj.Name.replace(',', ' ').lower().split()
        name_rank = len(set(name_words).intersection(search_terms_set))                 # How many matches
        if name_rank == len(search_terms_set):                                          # All terms matched Name
            A_RANK = u'{:03d}'.format(999-name_rank)
        else:
            A_RANK = u'999'
        
        keyword_set = set((obj.Keywords or '').replace(',', ' ').lower().split())       # Empty string '' if Null
        keyword_rank = len(keyword_set.intersection(search_terms_set))                  # How many keyword matches
        B_RANK = u'{:03d}'.format(999-keyword_rank)

        name_desc_words = u' '.join((obj.Name, obj.Description)).replace(',', ' ').lower().split()
        name_desc_rank = len(set(name_desc_words).intersection(search_terms_set))       # How many matches
        if name_desc_rank == len(search_terms_set):                                     # All terms matched Name or Description
            C_RANK = u'{:03d}'.format(999-name_desc_rank)
        else:
            C_RANK = u'999'
                
        total_matches = [word in search_terms_set for word in name_desc_words].count(True)  # How many times terms appear
        D_RANK = u'{:03d}'.format(999-total_matches)

        all_RANKS = u':'.join((A_RANK, B_RANK, C_RANK, D_RANK))
        if all_RANKS == u'999:999:999:999':                                             # No matches
            continue                                                                    # Loop to discard this object

        if sort_field == 'start_date_time':
            SORT_SUFFIX = str(obj.EntityJSON.get('start_date_time', ''))
        else: # sort_field == 'name':
            SORT_SUFFIX = (obj.Name or '').lower()

        SORT_KEY = u':'.join((all_RANKS, SORT_SUFFIX, str(obj.ID)))
        sort_array[SORT_KEY] = obj

    filtered_objects = [sort_array[key] for key in sorted(sort_array.keys())]
    return(filtered_objects)

# Algorithm thru 2018-03-11
#    sort_array = {}
#    for obj in input_objects:
#        if sort_field == 'start_date_time':
#            SORT_SUFFIX = str(obj.EntityJSON.get('start_date_time', '')) + ':' + obj.ID
#        else: # sort_field == 'name':
#            SORT_SUFFIX = (obj.Name or '').lower() + ':' + str(obj.ID)
#        keyword_set = set((obj.Keywords or '').replace(',', ' ').lower().split())       # Empty string '' if Null
#        keyword_rank = len(keyword_set.intersection(search_terms_set))                  # How many matches
#        if keyword_rank > 0:                                                            # PRIORITY=A, keyword match
#            SORT_KEY = u'A{:02d}:'.format(99-keyword_rank) + SORT_SUFFIX
#        else:
#            name_words = (obj.Name or '').replace(',', ' ').lower().split()
#            name_rank = len(set(name_words).intersection(search_terms_set))             # How many matches
#            if name_rank == len(search_terms_set):                                      # PRIORITY=B, all terms matched Name
#                SORT_KEY = u'B{:02d}:'.format(99-name_rank) + SORT_SUFFIX
#            else:
#                desc_words = (obj.Description or '').replace(',', ' ').lower().split()
#                desc_rank = len(set(desc_words).intersection(search_terms_set))         # How many matches
#                if desc_rank == len(search_terms_set):                                  # PRIORITY=B, all terms matched Description
#                    SORT_KEY = u'B{:02d}:'.format(99-desc_rank) + SORT_SUFFIX
#                else:   # Total Name and Description words that match
#                    total_matches = [word in search_terms_set for word in name_words + desc_words].count(True)
#                    if total_matches > 0:                                               # PRIORITY=C, some terms matched
#                        SORT_KEY = u'C{:02d}:'.format(99-total_matches) + SORT_SUFFIX
#                    else:
#                        continue                                                        # Loop and discard this object
#        sort_array[SORT_KEY] = obj
#
#    filtered_objects = [sort_array[key] for key in sorted(sort_array.keys())]
#    return(filtered_objects)

#
# Create your views here.
#
# About Dynamic fields:
# https://stackoverflow.com/questions/23643204/django-rest-framework-dynamically-return-subset-of-fields
#
class Resource_Detail(APIView):
    '''
        Single Resource access by Global ID or by Affiliation and Local ID
        
        ### Optional response argument(s):<br>
        ```
            fields=<local_fielda>               (return named fields)
            format={json,xml,html}              (json default)
        ```
        <a href="https://docs.google.com/document/d/1kh_0JCwRr7J2LiNlkQgfjopkHV4UbxB_UpXNhgt3vzc"
            target="_blank">More API documentation</a>
    '''
    permission_classes = (IsAuthenticatedOrReadOnly,)
    renderer_classes = (JSONRenderer,TemplateHTMLRenderer,XMLRenderer,)
    def get(self, request, format=None, **kwargs):
        # Process optional arguments
        arg_fields = request.GET.get('fields', None)
        if arg_fields:
            want_fields = set(arg_fields.lower().split(','))
        else:
            want_fields = set()

        if 'id' in self.kwargs:
            try:
                final_objects = [Resource.objects.get(pk=self.kwargs['id'])]
            except Resource.DoesNotExist:
                raise MyAPIException(code=status.HTTP_404_NOT_FOUND, detail='Specified Global ID not found')
        elif 'affiliation' in self.kwargs and 'localid' in self.kwargs:
            try:
                final_objects = Resource.objects.filter(Affiliation__exact=kwargs['affiliation']).filter(LocalID__exact=kwargs['localid'])
            except Exception as exc:
                raise MyAPIException(code=status.HTTP_400_BAD_REQUEST, detail='{}: {}'.format(type(exc).__name__, exc.message))
        else:
            raise MyAPIException(code=status.HTTP_404_NOT_FOUND, detail='Missing selection arguments')

        assoc_resources = []                   # Retrieve associated resources
        for each_object in final_objects:      # Loop forces evaluation, required in order to execute another Resources query
            assoc_ids = (each_object.Associations or '').split(',')
            assoc_res = Resource.objects.filter(Affiliation__exact=each_object.Affiliation).filter(LocalID__in=assoc_ids)
            for res in assoc_res:
                assoc_hash = {
                    'id': res.LocalID,
                    'resource_name': res.Name,
                    'resource_desc': res.Description,
                    'categories': res.EntityJSON.get('category', ''),
                }
                assoc_resources.append(assoc_hash)
            break # breaking because we should have only have one item processed by this loop

        context = {'associated_resources': assoc_resources, 'fields': want_fields}
        serializer = Resource_Detail_Serializer(final_objects, context=context, many=True)
        response_obj = {'results': serializer.data}
        return MyAPIResponse(response_obj, template_name='resource_cat/resource_detail.html')

class Resource_Search(APIView):
    '''
        ### Resource search and list
        
        Optional selection argument(s):
        ```
            search_terms=<whitespace_delimited_search_terms>
            affiliation={uiuc.edu, xsede.org, ...}
            categories=<category1>[,<category2>[...]]
            providers=<provider1>[,<provider2>[...]]
        ```
        Optional response argument(s):
        ```
            fields=<local_fielda>               (return named fields)
            format={json,xml,html}              (json default)
            sort=<local_field>                  (default global Name)
            page=<number>
            results_per_page=<number>           (default=25)
            subtotals={only,include}            (default no totals)
        ```
        <a href="https://docs.google.com/document/d/1kh_0JCwRr7J2LiNlkQgfjopkHV4UbxB_UpXNhgt3vzc"
            target="_blank">More API documentation</a>
    '''
    permission_classes = (IsAuthenticatedOrReadOnly,)
    renderer_classes = (JSONRenderer,TemplateHTMLRenderer,XMLRenderer,)
    def get(self, request, format=None, **kwargs):
        # Process optional arguments
        if 'affiliation' in self.kwargs:
            arg_affiliation = kwargs['affiliation']
        else:
            arg_affiliation = request.GET.get('affiliation', None)
        if arg_affiliation:
            want_affiliation = set(arg_affiliation.split(','))
        else:
            want_affiliation = set()

        arg_terms = request.GET.get('search_terms', None)
        if arg_terms:
            want_terms = set(arg_terms.replace(',', ' ').lower().split())
        else:
            want_terms = set()
        
        arg_categories = request.GET.get('categories', None)
        if arg_categories:
            want_categories = set(arg_categories.split(','))
        else:
            want_categories = set()
        
        arg_providers = request.GET.get('providers', None)
        if arg_providers:
            want_providers = [int(x) for x in arg_providers.split(',') if x.strip().isdigit()]
        else:
            want_providers = []

        arg_fields = request.GET.get('fields', None)
        if arg_fields:
            want_fields = set(arg_fields.lower().split(','))
        else:
            want_fields = set()

        sort = request.GET.get('sort', 'resource_name')
        page = request.GET.get('page', None)
        page_size = request.GET.get('results_per_page', 25)

        arg_subtotals = request.GET.get('subtotals', None)
        if arg_subtotals:
            arg_subtotals = arg_subtotals.lower()

        response_obj = {}
        try:
            # These filters are handled by the database; they are first
            objects = Resource.objects.filter(EntityJSON__record_status__exact=1)
            if want_affiliation:
                objects = objects.filter(Affiliation__in=want_affiliation)
            if want_providers:
                objects = objects.filter(EntityJSON__provider__in=want_providers)
            if not want_terms:                  # Becase terms search does its own ranked sort
                local_global_map = {'resource_name': 'Name',
                                    'resource_type': 'Type',
                                    'resource_description': 'Description',
                                    'id': 'LocalID'}
                if sort in local_global_map:
                    objects = objects.order_by(local_global_map[sort])
                elif sort is not None:
                    objects = objects.order_by(RawSQL('"EntityJSON"->>\'{}\''.format(sort), ()))

            # These filters have to be handled with code; they must be after the previous database filters
            if want_categories:
                objects = resource_categories_filter(objects, want_categories)
            if want_terms:
                objects = resource_terms_filtersort(objects, want_terms, sort_field='name')
            objects = resource_oldevents_filter(objects)

            response_obj['total_results'] = len(objects)
            if arg_subtotals in ('only', 'include'):
                response_obj['subtotals'] = resource_subtotals(objects)
                if arg_subtotals == 'only':
                    return MyAPIResponse(response_obj, template_name='resource_cat/resource_list.html')

            if page:
                paginator = Paginator(objects, page_size)
                final_objects = paginator.page(page)
                response_obj['page'] = int(page)
                response_obj['total_pages'] = paginator.num_pages
            else:
                final_objects = objects
        except Exception as exc:
            if hasattr(exc, 'message'):
                raise MyAPIException(code=status.HTTP_400_BAD_REQUEST, detail='{}: {}'.format(type(exc).__name__, exc.message))
            else:
                raise MyAPIException(code=status.HTTP_400_BAD_REQUEST, detail='{}: {}'.format(type(exc).__name__, exc))

        context = {'fields': want_fields}
        serializer = Resource_Search_Serializer(final_objects, context=context, many=True)
        response_obj['results'] = serializer.data
        return MyAPIResponse(response_obj, template_name='resource_cat/resource_list.html')

class Resource_Provider_List(APIView):
    '''
        ### Resource Provider search and list
        
        Optional selection argument(s):
        ```
            affiliation={uiuc.edu, xsede.org, etc.}
        ```
        Optional response format argument(s):
        ```
            fields=<local_fielda>               (return named fields)
            format={json,xml,html}              (json default)
            page=<number>
            results_per_page=<number>           (default=25)
        ```
        <a href="https://docs.google.com/document/d/1kh_0JCwRr7J2LiNlkQgfjopkHV4UbxB_UpXNhgt3vzc"
            target="_blank">More API documentation</a>
    '''
    permission_classes = (IsAuthenticatedOrReadOnly,)
    renderer_classes = (JSONRenderer,TemplateHTMLRenderer,XMLRenderer,)
    def get(self, request, format=None, **kwargs):
        if 'affiliation' in self.kwargs:
            arg_affiliation = kwargs['affiliation']
        else:
            arg_affiliation = request.GET.get('affiliation', None)
        if arg_affiliation:
            want_affiliation = set(arg_affiliation.split(','))
        else:
            want_affiliation = set()

        arg_fields = request.GET.get('fields', None)
        if arg_fields:
            want_fields = set(arg_fields.lower().split(','))
        else:
            want_fields = set()

        page = request.GET.get('page', None)
        page_size = request.GET.get('results_per_page', 25)
        response_obj = {}

        try:
            if want_affiliation:
                objects = ResourceProvider.objects.filter(Affiliation__in=want_affiliation).order_by('Name')
            else:
                objects = ResourceProvider.objects.all().order_by('Name')

            response_obj['total_results'] = len(objects)
            if page:
                paginator = Paginator(objects, page_size)
                final_objects = paginator.page(page)
                response_obj['page'] = int(page)
                response_obj['total_pages'] = paginator.num_pages
            else:
                final_objects = objects
        except Exception as exc:
            raise MyAPIException(code=status.HTTP_400_BAD_REQUEST, detail='{}: {}'.format(type(exc).__name__, exc.message))

        context = {'fields': want_fields}
        serializer = ResourceProvider_Search_Serializer(final_objects, context=context, many=True)
        response_obj['results'] = serializer.data
        return MyAPIResponse(response_obj, template_name='resource_cat/provider_list.html')

class Events_List(APIView):
    '''
        ### Event resource search and list
        
        Optional selection argument(s):
        ```
            search_terms=<whitespace_delimited_search_terms>
            affiliation={uiuc.edu, xsede.org, etc.}
            start_date=<yyyy-mm-dd>
            end_date=<yyyy-mm-dd>
        ```
        Optional response format argument(s):
        ```
            fields=<local_fielda>               (return named fields)
            format={json,xml,html}              (json default)
            page=<number>
            results_per_page=<number>           (default=25)
        ```
        <a href="https://docs.google.com/document/d/1kh_0JCwRr7J2LiNlkQgfjopkHV4UbxB_UpXNhgt3vzc"
            target="_blank">More API documentation</a>
    '''
    permission_classes = (IsAuthenticatedOrReadOnly,)
    renderer_classes = (JSONRenderer,TemplateHTMLRenderer,XMLRenderer,)
    def get(self, request, format=None, **kwargs):
        if 'affiliation' in self.kwargs:
            arg_affiliation = kwargs['affiliation']
        else:
            arg_affiliation = request.GET.get('affiliation', None)
        if arg_affiliation:
            want_affiliation = set(arg_affiliation.split(','))
        else:
            want_affiliation = set()

        arg_fields = request.GET.get('fields', None)
        if arg_fields:
            want_fields = set(arg_fields.lower().split(','))
        else:
            want_fields = set()

        arg_terms = request.GET.get('search_terms', None)
        if arg_terms:
            want_terms = set(arg_terms.replace(',', ' ').lower().split())
        else:
            want_terms = set()
        
        try:
            dt = request.GET.get('start_date', None)
            pdt = parse_datetime(dt)
            if pdt is None: # If it was only a date try adding the time
                pdt = parse_datetime(dt + 'T00:00:00.0+00:00')
            if pdt is None:
                raise Exception
            arg_startdate = pdt.astimezone(UTC).strftime('%Y-%m-%dT%H:%M:%S%z')
        except:
            arg_startdate = timezone.now().astimezone(UTC).strftime('%Y-%m-%dT%H:%M:%S%z')
        
        try:
            # Search for less than end_date + 1/second
            dt = request.GET.get('end_date', None)
            pdt = parse_datetime(dt)
            if pdt is None:  # If it was only a date try adding the time
                pdt = parse_datetime(dt + 'T23:59:59.9+00:00')
            if pdt is None:
                raise Exception
            arg_enddate = (pdt.astimezone(UTC) + timedelta(seconds=1)).strftime('%Y-%m-%dT%H:%M:%S%z')
        except:
            arg_enddate = (timezone.now().astimezone(UTC) + timedelta(days=365*10)).strftime('%Y-%m-%dT%H:%M:%S%z')

        page = request.GET.get('page', None)
        page_size = request.GET.get('results_per_page', 25)
        fields = request.GET.get('fields', None)
        response_obj = {}

        try:
            objects = Resource.objects.filter(Type__exact='Event').filter(EntityJSON__record_status__in=[1,2])
            if want_affiliation:
                objects = objects.filter(Affiliation__in=want_affiliation)
            # resource.start_date_time <= end_date && resource.end_date_time >= start_date
            if arg_startdate:
                objects = objects.filter(EntityJSON__end_date_time__gte=arg_startdate)      # String comparison
            if arg_enddate:
                objects = objects.filter(EntityJSON__start_date_time__lt=arg_enddate)       # String comparison
            if want_terms:
                objects = resource_terms_filtersort(objects, want_terms, sort_field='start_date_time')
            else:
                objects = objects.order_by(RawSQL('"EntityJSON"->>\'{}\''.format('start_date_time'), ()))
            response_obj['total_results'] = len(objects)
            if page:
                paginator = Paginator(objects, page_size)
                final_objects = paginator.page(page)
                response_obj['page'] = int(page)
                response_obj['total_pages'] = paginator.num_pages
            else:
                final_objects = objects
        except Exception as exc:
            raise MyAPIException(code=status.HTTP_400_BAD_REQUEST, detail='{}: {}'.format(type(exc).__name__, exc.message))

        context = {'fields': want_fields}
        serializer = Resource_Event_Serializer(final_objects, context=context, many=True)
        response_obj['results'] = serializer.data
        return MyAPIResponse(response_obj, template_name='resource_cat/event_list.html')
