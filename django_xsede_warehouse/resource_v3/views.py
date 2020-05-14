from django.db.models.expressions import RawSQL
from django.db.models import Count
from django.conf import settings as django_settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from django.utils.dateparse import parse_date, parse_datetime
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework_xml.renderers import XMLRenderer
from rest_framework.response import Response
from rest_framework import status
from .models import *
from .serializers import *
from xsede_warehouse.exceptions import MyAPIException
from xsede_warehouse.responses import MyAPIResponse
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q
import datetime
from datetime import datetime, timedelta
import pytz
Central = pytz.timezone("US/Central")
UTC = pytz.timezone("UTC")
import logging
logg2 = logging.getLogger('xsede.logger')
#
# Catalog Views
#
class Catalog_Search(APIView):
    '''
        ### Catalog search and list
        
        Optional selection argument(s):
        ```
            affiliations=<comma-separated-list>
        ```
        Optional response argument(s):
        ```
            format={json,xml,html}              (json default)
        ```
        <a href="https://docs.google.com/document/d/1kh_0JCwRr7J2LiNlkQgfjopkHV4UbxB_UpXNhgt3vzc"
            target="_blank">More API documentation</a>
    '''
    permission_classes = (IsAuthenticatedOrReadOnly,)
    renderer_classes = (JSONRenderer,TemplateHTMLRenderer,XMLRenderer,)
    def get(self, request, format=None, **kwargs):
        arg_affiliations = request.GET.get('affiliations', kwargs.get('affiliations', None))
        if arg_affiliations and arg_affiliations not in ['_all_', '*']:
            want_affiliations = set(arg_affiliations.split(','))
        else:
            want_affiliations = set()

        try:
            if len(want_affiliations) == 0:
                final_objects = ResourceV3Catalog.objects.all()
            else:
                final_objects = ResourceV3Catalog.objects.filter(Affiliation__in=want_affiliations)
        except Exception as exc:
            raise MyAPIException(code=status.HTTP_400_BAD_REQUEST, detail='{}: {}'.format(type(exc).__name__, exc))

        context={'request': request}
        serializer = Catalog_List_Serializer(final_objects, context=context, many=True)
        response_obj = {'results': serializer.data}
        return MyAPIResponse(response_obj, template_name='resource_v3/catalog_list.html')

class Catalog_Detail(APIView):
    '''
        ### Single Catalog access by Global ID
        
        Optional response argument(s):
        ```
            format={json,xml,html}              (json default)
        ```
        <a href="https://docs.google.com/document/d/1kh_0JCwRr7J2LiNlkQgfjopkHV4UbxB_UpXNhgt3vzc"
            target="_blank">More API documentation</a>
    '''
    permission_classes = (IsAuthenticatedOrReadOnly,)
    renderer_classes = (JSONRenderer,TemplateHTMLRenderer,XMLRenderer,)
    def get(self, request, format=None, **kwargs):
        arg_id = request.GET.get('id', kwargs.get('id', None))
        if not arg_id:
            raise MyAPIException(code=status.HTTP_404_NOT_FOUND, detail='Missing Global ID argument')

        try:
            final_objects = [ResourceV3Catalog.objects.get(pk=arg_id)]
        except ResourceV3Catalog.DoesNotExist:
            raise MyAPIException(code=status.HTTP_404_NOT_FOUND, detail='Specified Global ID not found')

        context = {}
        serializer = Catalog_Detail_Serializer(final_objects, context=context, many=True)
        response_obj = {'results': serializer.data}
        return MyAPIResponse(response_obj, template_name='resource_v3/catalog_detail.html')
#
# Local Views
#
class Local_Search(APIView):
    '''
        ### Local resource search and list
        
        Required selection argument(s):
        ```
            affiliation=<value>
        ```
        
        Optional selection argument(s):
        ```
            localids=<list of local ids>
            localtypes=<listof local types>
        ```
        Optional response argument(s):
        ```
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
        arg_affiliation = request.GET.get('affiliation', kwargs.get('affiliation', None))
        if not arg_affiliation:
            raise MyAPIException(code=status.HTTP_400_BAD_REQUEST, detail='Required affiliation not specified')
        arg_localids = request.GET.get('localids', kwargs.get('localids', None))
        if arg_localids:
            want_localids = set(arg_localids.split(','))
        else:
            want_localids = set()
        arg_localtypes = request.GET.get('localtypes', kwargs.get('localtypes', None))
        if arg_localtypes:
            want_localtypes = set(arg_localtypes.split(','))
        else:
            want_localtypes = set()
        page = request.GET.get('page', None)
        page_size = request.GET.get('results_per_page', 25)

        try:
            objects = ResourceV3Local.objects.filter(Affiliation__exact=arg_affiliation)
            if want_localids:
                objects = objects.filter(LocalID__in=want_localids)
            if want_localtypes:
                objects = objects.filter(LocalType__in=want_localtypes)
            if page:
                paginator = Paginator(objects, page_size)
                final_objects = paginator.page(page)
                response_obj['page'] = int(page)
                response_obj['total_pages'] = paginator.num_pages
            else:
                final_objects = objects
        except Exception as exc:
            raise MyAPIException(code=status.HTTP_400_BAD_REQUEST, detail='{}: {}'.format(type(exc).__name__, exc))

        context={'request': request}
        serializer = Local_List_Serializer(final_objects, context=context, many=True)
        response_obj = {'results': serializer.data}
        return MyAPIResponse(response_obj, template_name='resource_v3/local_list.html')

class Local_Detail(APIView):
    '''
        ### Single Local resource access by Global ID
        
        Optional response argument(s):
        ```
            format={json,xml,html}              (json default)
        ```
        <a href="https://docs.google.com/document/d/1kh_0JCwRr7J2LiNlkQgfjopkHV4UbxB_UpXNhgt3vzc"
            target="_blank">More API documentation</a>
    '''
    permission_classes = (IsAuthenticatedOrReadOnly,)
    renderer_classes = (JSONRenderer,TemplateHTMLRenderer,XMLRenderer,)
    def get(self, request, format=None, **kwargs):
        arg_id = request.GET.get('id', kwargs.get('id', None))
        if not arg_id:
            raise MyAPIException(code=status.HTTP_404_NOT_FOUND, detail='Missing Global ID argument')

        try:
            final_objects = [ResourceV3Local.objects.get(pk=arg_id)]
        except ResourceV3Local.DoesNotExist:
            raise MyAPIException(code=status.HTTP_404_NOT_FOUND, detail='Specified Global ID not found')

        context = {}
        serializer = Local_Detail_Serializer(final_objects, context=context, many=True)
        response_obj = {'results': serializer.data}
        return MyAPIResponse(response_obj, template_name='resource_v3/local_detail.html')
#
# Provider Views
#
class Provider_Detail(APIView):
    '''
        Single Provider access by Global ID (TODO: or by Affiliation and Local ID)
        
        ### Optional response argument(s):<br>
        ```
            format={json,xml,html}              (json default)
        ```
        <a href="https://docs.google.com/document/d/1kh_0JCwRr7J2LiNlkQgfjopkHV4UbxB_UpXNhgt3vzc"
            target="_blank">More API documentation</a>
    '''
    permission_classes = (IsAuthenticatedOrReadOnly,)
    renderer_classes = (JSONRenderer,TemplateHTMLRenderer,XMLRenderer,)
    def get(self, request, format=None, **kwargs):
        arg_id = request.GET.get('id', kwargs.get('id', None))
        if not arg_id:
            raise MyAPIException(code=status.HTTP_404_NOT_FOUND, detail='Missing Global ID argument')

        try:
            final_objects = [ResourceV3.objects.get(pk=arg_id)]
        except ResourceV3.DoesNotExist:
            raise MyAPIException(code=status.HTTP_404_NOT_FOUND, detail='Specified Global ID not found')
            
        if len(final_objects) != 1:
            raise MyAPIException(code=status.HTTP_404_NOT_FOUND, detail='Too many providers found')

        obj = final_objects[0]
        if obj.ResourceGroup != 'Organizations' or obj.Type != 'Resource Provider':
            raise MyAPIException(code=status.HTTP_404_NOT_FOUND, detail='Selected item is not a Provider')
        
        serializer = Provider_Detail_Serializer(final_objects, many=True)
        response_obj = {'results': serializer.data}
        return MyAPIResponse(response_obj, template_name='resource_v3/provider_detail.html')

class Provider_Search(APIView):
    '''
        ### Resource Provider search and list
        
        Optional selection argument(s):
        ```
            affiliations=<comma-delimited-list>
        ```
        Optional response format argument(s):
        ```
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
        arg_affiliations = request.GET.get('affiliations', kwargs.get('affiliations', None))
        if arg_affiliations:
            want_affiliations = set(arg_affiliations.split(','))
        else:
            want_affiliations = set()

        page = request.GET.get('page', None)
        page_size = request.GET.get('results_per_page', 25)
        response_obj = {}

        Base_Filter = ResourceV3.objects.filter(ResourceGroup__exact='Organizations').filter(Type__exact='Resource Provider')
        try:
            if want_affiliations:
                objects = Base_Filter.filter(Affiliation__in=want_affiliations).order_by('Name')
            else:
                objects = Base_Filter.order_by('Name')
            response_obj['total_results'] = len(objects)
            if page:
                paginator = Paginator(objects, page_size)
                final_objects = paginator.page(page)
                response_obj['page'] = int(page)
                response_obj['total_pages'] = paginator.num_pages
            else:
                final_objects = objects
        except Exception as exc:
            raise MyAPIException(code=status.HTTP_400_BAD_REQUEST, detail='{}: {}'.format(type(exc).__name__, exc))

        context = {}
        serializer = Provider_List_Serializer(final_objects, context=context, many=True)
        response_obj['results'] = serializer.data
        return MyAPIResponse(response_obj, template_name='resource_v3/provider_list.html')
#
# List Resource Groups, Types, and counts in each combination
#
class Resource_Types_List(APIView):
    '''
        ### Resource Group and Types search and list
        
        Optional selection argument(s):
        ```
            affiliations=<comma-delimited-list>
        ```
        Optional response format argument(s):
        ```
            fields=<local_fields>               (return named fields)
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
        arg_affiliations = request.GET.get('affiliations', kwargs.get('affiliations', None))
        if arg_affiliations:
            want_affiliations = set(arg_affiliations.split(','))
        else:
            want_affiliations = set()

        arg_fields = request.GET.get('fields', None)
        if arg_fields:
            want_fields = set(arg_fields.lower().split(','))
        else:
            want_fields = set()

        page = request.GET.get('page', None)
        page_size = request.GET.get('results_per_page', 25)
        response_obj = {}

        try:
            if want_affiliations:
                objects = ResourceV3.objects.filter(Affiliation__in=want_affiliations).\
                    values('ResourceGroup','Type').annotate(count=Count(['ResourceGroup','Type']))
            else:
                objects = ResourceV3.objects.all().\
                    values('ResourceGroup','Type').annotate(count=Count(['ResourceGroup','Type']))

            response_obj['total_results'] = len(objects)
            if page:
                paginator = Paginator(objects, page_size)
                final_objects = paginator.page(page)
                response_obj['page'] = int(page)
                response_obj['total_pages'] = paginator.num_pages
            else:
                final_objects = objects
        except Exception as exc:
            raise MyAPIException(code=status.HTTP_400_BAD_REQUEST, detail='{}: {}'.format(type(exc).__name__, exc))
        context = {'fields': want_fields}
        serializer = Resource_Types_Serializer(final_objects, context=context, many=True)
        response_obj['results'] = serializer.data
        return MyAPIResponse(response_obj, template_name='resource_v3/types_list.html')
#
# Resource Views and supporting functions
#
def resource_topics_filter(input_objects, search_topics_set):
    # Inspect objects because we can't push this filter to the database
    filtered_objects = []
    for obj in input_objects:
        objtopics = obj.Topics
        if len(objtopics or '') < 1: # Skip objects without a topics
            continue
        objtopics_list = set(objtopics.split(','))
        if not objtopics_list.isdisjoint(search_topics_set):
            filtered_objects.append(obj)
    return(filtered_objects)

def resource_oldevents_filter(input_objects):
    # Inspect objects because we can't push this filter to the database
    cur_datetime = timezone.now().astimezone(UTC).replace(second=0, microsecond=0)
    filtered_objects = []
    for obj in input_objects:
        if obj.ResourceGroup == 'Live Events' and obj.EndDateTime is not None:
            if obj.EndDateTime.replace(second=0, microsecond=0) < cur_datetime:
                continue # Filter out old events
        filtered_objects.append(obj)
    return(filtered_objects)

def resource_subtotals(input_objects):
    affiliation_totals = {}
    topic_totals    = {}
    type_totals     = {}
    provider_totals = {}
    for obj in input_objects:
        this_affiliation = obj.Affiliation
        affiliation_totals[this_affiliation] = affiliation_totals.get(this_affiliation, 0) + 1
        this_topics = obj.Topics
        if this_topics:
            for x in this_topics.split(','):
                topics_totals[x] = topics_totals.get(x, 0) + 1
        this_provider = obj.ProviderID
        if this_provider:
            provider_totals[this_provider] = provider_totals.get(this_provider, 0) + 1
        this_type = obj.ResourceGroup + ':' + obj.Type
        type_totals[this_type] = type_totals.get(this_type, 0) + 1
    affiliation_return = [ {'Affiliation': key, 'subtotal': value} for key, value in affiliation_totals.items() ]
    topics_return = [ {'id': key, 'subtotal': value} for key, value in topics_totals.items() ]
    provider_return = [ {'ProviderID': key, 'subtotal': value} for key, value in provider_totals.items() ]
    type_return = [ {'id': key, 'subtotal': value} for key, value in type_totals.items() ]
    return({'affiliations': affiliation_return, 'topics': topics_return,
           'types': type_return, 'providers': provider_return})

def resource_terms_filtersort(input_objects, search_terms_set, sort_field='name'):
    # This function inspects and sorts objects using an algorithm that is too complex to do using SQL
    # Sorting algorithms requirements:
    #   First prioritize resources with a tag/keyword matching at least one search term
    #     Example: given search terms "frog spectrometer chuckles", resources with a "spectrometer" tag should
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
    #   C_RANK: all terms matched Name, Short Description, or Description; RANK=999 minus how many terms matched
    #   D_RANK: some terms matched Name, Short Description, or Description; RANK=999 minus total number of words matching terms
    # Where "999 minus match count" makes higher match counts sort firts alphabetically (996=999-3 before 998=999-1)
    sort_array = {}
    
    for obj in input_objects:
        name_words_set = set(obj.Name.replace(',', ' ').lower().split())
        name_rank = len(name_words_set.intersection(search_terms_set))                  # How many matches
        if name_rank == len(search_terms_set):                                          # All terms matched Name
            A_RANK = u'{:03d}'.format(999-name_rank)
        else:
            A_RANK = u'999'
        
        keyword_set = set((obj.Keywords or '').replace(',', ' ').lower().split())       # Empty string '' if Null
        keyword_rank = len(keyword_set.intersection(search_terms_set))                  # How many keyword matches
        B_RANK = u'{:03d}'.format(999-keyword_rank)

        name_desc_words = u' '.join((obj.Name, (obj.ShortDescription or ''), (obj.Description or ''))).replace(',', ' ').lower().split()
        name_desc_rank = len(set(name_desc_words).intersection(search_terms_set))       # How many matches
        if name_desc_rank == len(search_terms_set):                                     # All terms matched Name, Short Description or Description
            C_RANK = u'{:03d}'.format(999-name_desc_rank)
        else:
            C_RANK = u'999'
                
        total_matches = [word in search_terms_set for word in name_desc_words].count(True)  # How many times terms appear
        D_RANK = u'{:03d}'.format(999-total_matches)

        all_RANKS = u':'.join((A_RANK, B_RANK, C_RANK, D_RANK))
        if all_RANKS == u'999:999:999:999':                                             # No matches
            continue                                                                    # Loop to discard this object

        if sort_field == 'StartDateTime':
            SORT_SUFFIX = obj.StartDateTime.astimezone(UTC).strftime('%Y-%m-%dT%H:%M:%S%z')
        else: # sort_field == 'name':
            SORT_SUFFIX = (obj.Name or '').lower()

        SORT_KEY = u':'.join((all_RANKS, SORT_SUFFIX, str(obj.ID)))
        sort_array[SORT_KEY] = obj

    filtered_objects = [sort_array[key] for key in sorted(sort_array.keys())]
    return(filtered_objects)

def resource_strings_filtersort(input_objects, search_strings_set, sort_field='name'):
    # This function inspects and sorts objects using an algorithm that is too complex to do using SQL
    # Sorting algorithms requirements:
    #   First prioritize resources with a tag/keyword matching at least one search string
    #     Example: given search strings "spec soft", resources with a "software" tag should
    #     be listed before resources with no tags matching a search string
    #   Second, prioritize resources with resource_name and resource_description matching ALL of the search strings.
    #     Example: gieven search terms "spec soft", resources with ALL those strings in
    #     resource_description and/or resource_name should be listed before resources matching one strings.
    #   Third, prioritize resources with resource_name and resource_description matching SOME of the search strings.
    #     In this case, ordering sould be based on the total number of occurances of the search strings.
    #     For example, if the search strings is "soft", resources that have the term three times should be listed
    #     before resources with that string happening 2 times or once.

    # SORT_KEY fields:
    #   <B_RANK>:<C_RANK>:<D_RANK>:<D_RANK>:<SORT_SUFFIX>
    # Where:
    #   A_RANK: all strings matched Name; RANK=999 minus how many strings matched
    #   B_RANK: keyword match; RANK=999 minus how many keywords matched
    #   C_RANK: all strings matched Name or Description; RANK=999 minus how many strings matched
    #   D_RANK: some strings matched Name or Description; RANK=999 minus total number of words matching strings
    # Where "999 minus match count" makes higher match counts sort firts alphabetically (996=999-3 before 998=999-1)
    sort_array = {}
    search_for_set = set([x.lower() for x in search_strings_set])
    
    for obj in input_objects:
        search_in = obj.Name.lower()
        name_rank = [search_for in search_in for search_for in search_for_set].count(True)
        if name_rank != len(search_for_set):                                                # All terms matched Name
            name_rank = 0
        A_RANK = u'{:03d}'.format(999-name_rank)
    
        search_in_set = set((obj.Keywords or '').replace(',', ' ').lower().split())         # Empty string '' if Null
        keyword_rank = 0
        for search_in in search_in_set:
            if [search_for in search_in for search_for in search_for_set].count(True) > 0:
                keyword_rank += 1
        B_RANK = u'{:03d}'.format(999-keyword_rank)

        search_in = u' '.join((obj.Name, (obj.ShortDescription or ''), obj.Description)).replace(',', ' ').lower()
        name_desc_rank = [search_for in search_in for search_for in search_for_set].count(True)
        if name_desc_rank != len(search_for_set):                                       # All terms matched Name, Short Description, or Description
            name_desc_rank = 0
        C_RANK = u'{:03d}'.format(999-name_desc_rank)

        total_matches = 0
        for search_for in search_for_set:
            total_matches += search_in.count(search_for)
        D_RANK = u'{:03d}'.format(999-total_matches)

        all_RANKS = u':'.join((A_RANK, B_RANK, C_RANK, D_RANK))
        if all_RANKS == u'999:999:999:999':                                             # No matches
            continue                                                                    # Loop to discard this object

        if sort_field == 'StartDateTime':
            SORT_SUFFIX = obj.StartDateTime.strftime('%Y-%m-%dT%H:%M:%S%z')
        else: # sort_field == 'name':
            SORT_SUFFIX = (obj.Name or '').lower()

        SORT_KEY = u':'.join((all_RANKS, SORT_SUFFIX, str(obj.ID)))
        sort_array[SORT_KEY] = obj

    filtered_objects = [sort_array[key] for key in sorted(sort_array.keys())]
    return(filtered_objects)

class Resource_Detail(APIView):
    '''
        Single Resource access by Global ID or by Affiliation and Local ID
        
        ### Optional response argument(s):<br>
        ```
            format={json,xml,html}              (json default)
        ```
        <a href="https://docs.google.com/document/d/1kh_0JCwRr7J2LiNlkQgfjopkHV4UbxB_UpXNhgt3vzc"
            target="_blank">More API documentation</a>
    '''
    permission_classes = (IsAuthenticatedOrReadOnly,)
    renderer_classes = (JSONRenderer,TemplateHTMLRenderer,XMLRenderer,)
    def get(self, request, format=None, **kwargs):
        arg_id = request.GET.get('id', kwargs.get('id', None))
        if not arg_id:
            raise MyAPIException(code=status.HTTP_404_NOT_FOUND, detail='Missing Global ID argument')
            
        try:
            final_objects = [ResourceV3.objects.get(pk=arg_id)]
        except ResourceV3.DoesNotExist:
            raise MyAPIException(code=status.HTTP_404_NOT_FOUND, detail='Specified Global ID not found')

        assoc_resources = []                   # Retrieve associated resources
        # TODO: convert to RelationRelation
#        for each_object in final_objects:      # Loop forces evaluation, required in order to execute another Resources query
#            assoc_ids = (each_object.Associations or '').split(',')
#            assoc_res = ResourceV3.objects.filter(Affiliation__exact=each_object.Affiliation).filter(LocalID__in=assoc_ids)
#            for res in assoc_res:
#                assoc_hash = {
#                    'id': res.LocalID,
#                    'resource_name': res.Name,
#                    'resource_desc': res.Description,
#                    'topics': res.Topics,
#                }
#                assoc_resources.append(assoc_hash)
#            break # breaking because we should have only have one item processed by this loop

#        context = {'associated_resources': assoc_resources}
        context = {}
        serializer = Resource_Detail_Serializer(final_objects, context=context, many=True)
        response_obj = {'results': serializer.data}
        return MyAPIResponse(response_obj, template_name='resource_v3/resource_detail.html')

class Resource_Search(APIView):
    '''
        ### Resource search and list
        
        Optional selection argument(s):
        ```
            search_terms=<comma_delimited_search_terms>
            search_strings=<comma_delimited_search_strings>
            affiliations=<comma-delimited-list>
            resource_groups=<group1>[, <group2>[...]]
            topics=<topic1>[,<topic2>[...]]
            types=<type1>[,<type2>[...]]
            providers=<provider1>[,<provider2>[...]]
        ```
        Optional response argument(s):
        ```
            fields=<local_fields>               (return named fields)
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
        arg_affiliations = request.GET.get('affiliations', kwargs.get('affiliations', None))
        if arg_affiliations:
            want_affiliations = set(arg_affiliations.split(','))
        else:
            want_affiliations = set()

        arg_resource_groups = request.GET.get('resource_groups', None)
        if arg_resource_groups:
            want_resource_groups = set(arg_resource_groups.split(','))
        else:
            want_resource_groups = set()

        arg_terms = request.GET.get('search_terms', None)
        if arg_terms:
            want_terms = set(arg_terms.replace(',', ' ').lower().split())
        else:
            want_terms = set()

        arg_strings = request.GET.get('search_strings', None)
        if arg_strings:
            want_strings = set(arg_strings.replace(',', ' ').lower().split())
        else:
            want_strings = set()

        arg_topics = request.GET.get('topics', None)
        if arg_topics:
            want_topics = set(arg_topics.split(','))
        else:
            want_topics = set()

        arg_types = request.GET.get('types', None)
        if arg_types:
            want_types = set(arg_types.split(','))
        else:
            want_types = set()

        arg_providers = request.GET.get('providers', None)
        # Search in ProviderID field if possible rather than Provider in JSONField
        if arg_providers:
            if set(arg_providers).issubset(set('0123456789,')):
                # Handle numeric providers for uiuc.edu
                if want_affiliations and len(want_affiliations) == 1:
                    this_affiliation = next(iter(want_affiliations))
                    want_providerids = ['urn:glue2:GlobalResourceProvider:{}.{}'.format(x.strip(), this_affiliation) for x in arg_providers.split(',')]
                    want_providers = []
                else:
                    want_providerids = []
                    want_providers = [int(x) for x in arg_providers.split(',') if x.strip().isdigit()]
            else:
                want_providerids = set(arg_providers.split(','))
                want_providers = []
        else:
            want_providerids = []
            want_providers = []

        arg_fields = request.GET.get('fields', None)
        if arg_fields:
            want_fields = set(arg_fields.lower().split(','))
        else:
            want_fields = set()

        sort = request.GET.get('sort', 'Name')
        page = request.GET.get('page', None)
        page_size = request.GET.get('results_per_page', 25)

        arg_subtotals = request.GET.get('subtotals', None)
        if arg_subtotals:
            arg_subtotals = arg_subtotals.lower()

        response_obj = {}
        try:
            # These filters are handled by the database; they are first
            objects = ResourceV3.objects.filter(QualityLevel__exact='Production')
            if want_affiliations:
                objects = objects.filter(Affiliation__in=want_affiliations)
            if want_resource_groups:
                objects = objects.filter(ResourceGroup__in=want_resource_groups)
            if want_types:
                objects = objects.filter(Type__in=want_types)
            if want_providerids:
                objects = objects.filter(ProviderID__in=want_providerids)
#            elif want_providers:
#                objects = objects.filter(EntityJSON__provider__in=want_providers)
            if not want_terms and sort is not None: # Becase terms search does its own ranked sort
                objects = objects.order_by(sort)

            # These filters have to be handled with code; they must be after the previous database filters
            if want_topics:
                objects = resource_topics_filter(objects, want_topics)
            if want_terms:
                objects = resource_terms_filtersort(objects, want_terms, sort_field='name')
            elif want_strings:
                objects = resource_strings_filtersort(objects, want_strings, sort_field='name')
            objects = resource_oldevents_filter(objects)

            response_obj['total_results'] = len(objects)
            if arg_subtotals in ('only', 'include'):
                response_obj['subtotals'] = resource_subtotals(objects)
                if arg_subtotals == 'only':
                    return MyAPIResponse(response_obj, template_name='resource_v3/resource_list.html')

            if page:
                paginator = Paginator(objects, page_size)
                final_objects = paginator.page(page)
                response_obj['page'] = int(page)
                response_obj['total_pages'] = paginator.num_pages
            else:
                final_objects = objects
        except Exception as exc:
            logg2.info(exc, exc_info=True)
            raise MyAPIException(code=status.HTTP_400_BAD_REQUEST, detail='{}: {}'.format(type(exc).__name__, exc))

        context = {'fields': want_fields}
        serializer = Resource_Search_Serializer(final_objects, context=context, many=True)
        response_obj['results'] = serializer.data
        return MyAPIResponse(response_obj, template_name='resource_v3/resource_list.html')
class Resource_ESearch(APIView):
    '''
        ### Resource Elastic search and list
        
        Optional selection argument(s):
        ```
            search_terms=<comma_delimited_search_terms>
            affiliations=<comma-delimited-list>
            resource_groups=<group1>[, <group2>[...]]
            topics=<topic1>[,<topic2>[...]]
            types=<type1>[,<type2>[...]]
            providers=<provider1>[,<provider2>[...]]
            relation=[!]<type>:<id>
        ```
        Optional response argument(s):
        ```
            format={json,xml,html}              (json default)
            sort=<field>                  (default Name.Keyword)
            page=<number>
            results_per_page=<number>           (default=25)
        ```
        <a href="https://docs.google.com/document/d/1kh_0JCwRr7J2LiNlkQgfjopkHV4UbxB_UpXNhgt3vzc"
            target="_blank">More API documentation</a>
    '''
    permission_classes = (IsAuthenticatedOrReadOnly,)
    renderer_classes = (JSONRenderer,TemplateHTMLRenderer,XMLRenderer,)
    def get(self, request, format=None, **kwargs):
        if not django_settings.ESCON:
            raise MyAPIException(code=status.HTTP_503_SERVICE_UNAVAILABLE, detail='Elasticsearch not configured')
        ESCON = django_settings.ESCON
        
        # Process optional arguments
        arg_affiliations = request.GET.get('affiliations', kwargs.get('affiliations', None))
        if arg_affiliations:
            want_affiliations = list(arg_affiliations.split(','))
        else:
            want_affiliations = list()

        arg_resource_groups = request.GET.get('resource_groups', None)
        if arg_resource_groups:
            want_resource_groups = list(arg_resource_groups.split(','))
        else:
            want_resource_groups = list()

        arg_terms = request.GET.get('search_terms', None)
        if arg_terms:
            want_terms = list(arg_terms.replace(',', ' ').lower().split())
        else:
            want_terms = list()

        arg_topics = request.GET.get('topics', None)
        if arg_topics:
            want_topics = list(arg_topics.split(','))
        else:
            want_topics = list()

        arg_types = request.GET.get('types', None)
        if arg_types:
            want_types = list(arg_types.split(','))
        else:
            want_types = list()

        arg_providers = request.GET.get('providers', None)
        # Search in ProviderID field if possible rather than Provider in JSONField
        if arg_providers:
            want_providerids = list(arg_providers.split(','))
        else:
            want_providerids = list()

        arg_relation = request.GET.get('relation', None)
        if arg_relation:
            want_relationinvert = (arg_relation[0] == '!')
            if want_relationinvert:
                arg_relation = arg_relation[1:]
            want_relationid = arg_relation
        else:
            want_relationid = False

        sort = request.GET.get('sort', None)
        page = request.GET.get('page', 0)
        page_size = int(request.GET.get('results_per_page', 25))

        response_obj = {}

        import pdb
        pdb.set_trace()
        
        try:
            # These filters are handled by the database; they are first
            ES = Search(index=ResourceV3Index.Index.name).using(ESCON)
            ES = ES.query('match', QualityLevel='Production')
            if want_affiliations:
                ES = ES.query('terms', Affiliation=want_affiliations)
            if want_resource_groups:
                ES = ES.query('terms', ResourceGroup=want_resource_groups)
            if want_types:
                ES = ES.query('terms', Type=want_types)
            if want_providerids:
                ES = ES.query('terms', ProviderID=want_providerids)
            if want_topics:
                ES = ES.query('terms', Topics=want_topics)
            if want_terms:
                ES = ES.query('multi_match', query=' '.join(want_terms), fields=['Name', 'Keywords', 'ShortDescription', 'Description'])
            if want_relationid:
                if want_relationinvert:
                    ES = ES.query('nested', path='Relations',
                            query=~Q('match', Relations__RelatedID=want_relationid)
                        )
                else:
                    ES = ES.query('nested', path='Relations',
                            query=Q('match', Relations__RelatedID=want_relationid)
                        )
#                    ES = ES.query('match', Relations__RelationID=want_relationid)

            if sort:
                ES = ES.sort(sort)

            if page:
                page_start = page_size * int(page)
                page_end = page_start + page_size
                ES = ES[page_start:page_end]

            response = ES.execute()

            objects = []
            for row in response.to_dict()['hits']['hits']:
                objects.append(row['_source'])

            response_obj['total_results'] = ES.count()

        except Exception as exc:
            logg2.info(exc, exc_info=True)
            raise MyAPIException(code=status.HTTP_400_BAD_REQUEST, detail='{}: {}'.format(type(exc).__name__, exc))

#        context = {'fields': want_fields}
#        serializer = Resource_ESearch_Serializer(final_objects, context=context, many=True)
        response_obj['results'] = objects
        return MyAPIResponse(response_obj, template_name='resource_v3/resource_list.html')
#
# Event Views
#
class Event_Detail(APIView):
    '''
        Single Catalog access by Global ID
        
        ### Optional response argument(s):<br>
        ```
            format={json,xml,html}              (json default)
        ```
        <a href="https://docs.google.com/document/d/1kh_0JCwRr7J2LiNlkQgfjopkHV4UbxB_UpXNhgt3vzc"
            target="_blank">More API documentation</a>
    '''
    permission_classes = (IsAuthenticatedOrReadOnly,)
    renderer_classes = (JSONRenderer,TemplateHTMLRenderer,XMLRenderer,)
    def get(self, request, format=None, **kwargs):
        return

class Event_Search(APIView):
    '''
        ### Event resource search and list
        
        Optional selection argument(s):
        ```
            search_terms=<whitespace_delimited_search_terms>
            affiliations=<comma-delimited-list>
            topics=<topic1>[,<topic2>[...]]
            providers=<provider1>[,<provider2>[...]]
            topics=<topic1>[,<topic2>[...]]
            start_date=<yyyy-mm-dd>
            end_date=<yyyy-mm-dd>
        ```
        Optional response format argument(s):
        ```
            fields=<local_fields>               (return named fields)
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
        arg_affiliations = request.GET.get('affiliations', kwargs.get('affiliations', None))
        if arg_affiliations:
            want_affiliations = set(arg_affiliations.split(','))
        else:
            want_affiliations = set()

        arg_topics = request.GET.get('topics', None)
        if arg_topics:
            want_topics = set(arg_topics.split(','))
        else:
            want_topics = set()

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
 
        arg_providers = request.GET.get('providers', None)
        # Search in ProviderID field if possible rather than Provider in JSONField
        if arg_providers:
            if set(arg_providers).issubset(set('0123456789,')):
                # Handle numeric providers for uiuc.edu
                if want_affiliations and len(want_affiliations) == 1:
                    this_affiliation = next(iter(want_affiliations))
                    want_providerids = ['urn:glue2:GlobalResourceProvider:{}.{}'.format(x.strip(), this_affiliation) for x in arg_providers.split(',')]
                    want_providers = []
                else:
                    want_providerids = []
                    want_providers = [int(x) for x in arg_providers.split(',') if x.strip().isdigit()]
            else:
                want_providerids = set(arg_providers.split(','))
                want_providers = []
        else:
            want_providerids = []
            want_providers = []
 

        arg_topics = request.GET.get('topics', None)
        if arg_topics:
            want_topics = set(arg_topics.split(','))
        else:
            want_topics = set()

        try:
            dt = request.GET.get('start_date', None)
            pdt = parse_datetime(dt)
            if pdt is None: # If it was only a date try adding the time
                pdt = parse_datetime(dt + 'T00:00:00.0+00:00')
            if pdt is None:
                raise Exception
#            arg_startdate = pdt.astimezone(UTC).strftime('%Y-%m-%dT%H:%M:%S%z')
            arg_startdate = pdt.astimezone(UTC)
        except:
#            arg_startdate = timezone.now().astimezone(UTC).strftime('%Y-%m-%dT%H:%M:%S%z')
            arg_startdate = timezone.now().astimezone(UTC)
        
        try:
            # Search for less than end_date + 1/second
            dt = request.GET.get('end_date', None)
            pdt = parse_datetime(dt)
            if pdt is None:  # If it was only a date try adding the time
                pdt = parse_datetime(dt + 'T23:59:59.9+00:00')
            if pdt is None:
                raise Exception
#            arg_enddate = (pdt.astimezone(UTC) + timedelta(seconds=1)).strftime('%Y-%m-%dT%H:%M:%S%z')
            arg_enddate = (pdt.astimezone(UTC) + timedelta(seconds=1))
        except:
#            arg_enddate = (timezone.now().astimezone(UTC) + timedelta(days=365*10)).strftime('%Y-%m-%dT%H:%M:%S%z')
            arg_enddate = (timezone.now().astimezone(UTC) + timedelta(days=365*10))

        page = request.GET.get('page', None)
        page_size = request.GET.get('results_per_page', 25)
        fields = request.GET.get('fields', None)
        response_obj = {}

        try:
            objects = ResourceV3.objects.filter(ResourceGroup__exact='Live Events').filter(QualityLevel__exact='Production')
            if want_affiliations:
                objects = objects.filter(Affiliation__in=want_affiliations)
            if want_providerids:
                objects = objects.filter(ProviderID__in=want_providerids)
#            elif want_providers:
#                objects = objects.filter(EntityJSON__provider__in=want_providers)
            # Start <= End argument && End >= Start argument
            if arg_startdate:
                objects = objects.filter(EndDateTime__gte=arg_startdate)      # String comparison
            if arg_enddate:
                objects = objects.filter(StartDateTime__lt=arg_enddate)       # String comparison

            if want_terms:
                objects = resource_terms_filtersort(objects, want_terms, sort_field='StartDateTime')
            else:
                objects = objects.order_by(StartDateTime)
            
            # These filters have to be handled by looping thru rows; they must be after the previous database filters
            if want_topics:
                objects = resource_topics_filter(objects, want_topics)

            response_obj['total_results'] = len(objects)
            if page:
                paginator = Paginator(objects, page_size)
                final_objects = paginator.page(page)
                response_obj['page'] = int(page)
                response_obj['total_pages'] = paginator.num_pages
            else:
                final_objects = objects
        except Exception as exc:
            raise MyAPIException(code=status.HTTP_400_BAD_REQUEST, detail='{}: {}'.format(type(exc).__name__, str(exc)))

        context = {'fields': want_fields}
        serializer = Resource_Event_Serializer(final_objects, context=context, many=True)
        response_obj['results'] = serializer.data
        return MyAPIResponse(response_obj, template_name='resource_v3/event_list.html')
#
# Guide Views
#
class Guide_Detail(APIView):
    '''
        Single Guide access by Global ID or by Affiliation and Local ID
        
        ### Optional response argument(s):<br>
        ```
            fields=<local_fields>               (return named fields)
            format={json,xml,html}              (json default)
        ```
        <a href="https://docs.google.com/document/d/1kh_0JCwRr7J2LiNlkQgfjopkHV4UbxB_UpXNhgt3vzc"
            target="_blank">More API documentation</a>
    '''
    permission_classes = (IsAuthenticatedOrReadOnly,)
    renderer_classes = (JSONRenderer,TemplateHTMLRenderer,XMLRenderer,)
    def get(self, request, format=None, **kwargs):
        arg_id = request.GET.get('id', kwargs.get('id', None))
        if not arg_id:
            raise MyAPIException(code=status.HTTP_404_NOT_FOUND, detail='Missing Global ID argument')

        # Process optional arguments
        arg_fields = request.GET.get('fields', None)
        if arg_fields:
            want_fields = set(arg_fields.lower().split(','))
        else:
            want_fields = set()

        try:
            final_objects = [ResourceV3Guide.objects.get(pk=arg_id)]
        except ResourceV3Guide.DoesNotExist:
            raise MyAPIException(code=status.HTTP_404_NOT_FOUND, detail='Specified Global ID not found')

        context = {'fields': want_fields}
        serializer = Guide_Detail_Serializer(final_objects, context=context, many=True)
        response_obj = {'results': serializer.data}
        return MyAPIResponse(response_obj, template_name='resource_v3/guide_detail.html')

class Guide_Search(APIView):
    '''
        ### Guide search and list
        
        Optional Resource selection argument(s) to return related Guides:
        ```
            search_terms=<comma_delimited_search_terms>
            search_strings=<comma_delimited_search_strings>
            affiliations=<comma-delimited-list>
            resource_groups=<group1>[, <group2>[...]]
            topics=<topic1>[,<topic2>[...]]
            types=<type1>[,<type2>[...]]
            providers=<provider1>[,<provider2>[...]]
        ```
        Optional response argument(s):
        ```
            fields=<local_fields>               (return named fields)
            format={json,xml,html}              (json default)
            sort=<local_field>                  (default global Name)
            page=<number>
            results_per_page=<number>           (default=25)
        ```
        <a href="https://docs.google.com/document/d/1kh_0JCwRr7J2LiNlkQgfjopkHV4UbxB_UpXNhgt3vzc"
            target="_blank">More API documentation</a>
    '''
    permission_classes = (IsAuthenticatedOrReadOnly,)
    renderer_classes = (JSONRenderer,TemplateHTMLRenderer,XMLRenderer,)
    def get(self, request, format=None, **kwargs):
        # Process optional arguments
        arg_affiliations = request.GET.get('affiliations', kwargs.get('affiliations', None))
        if arg_affiliations:
            want_affiliations = set(arg_affiliations.split(','))
        else:
            want_affiliations = set()

        arg_resource_groups = request.GET.get('resource_groups', None)
        if arg_resource_groups:
            want_resource_groups = set(arg_resource_groups.split(','))
        else:
            want_resource_groups = set()

        arg_terms = request.GET.get('search_terms', None)
        if arg_terms:
            want_terms = set(arg_terms.replace(',', ' ').lower().split())
        else:
            want_terms = set()

        arg_strings = request.GET.get('search_strings', None)
        if arg_strings:
            want_strings = set(arg_strings.replace(',', ' ').lower().split())
        else:
            want_strings = set()

        arg_topics = request.GET.get('topics', None)
        if arg_topics:
            want_topics = set(arg_topics.split(','))
        else:
            want_topics = set()

        arg_types = request.GET.get('types', None)
        if arg_types:
            want_types = set(arg_types.split(','))
        else:
            want_types = set()

        arg_providers = request.GET.get('providers', None)
        # Search in ProviderID field if possible rather than Provider in JSONField
        if arg_providers:
            if set(arg_providers).issubset(set('0123456789,')):
                # Handle numeric providers for uiuc.edu
                if want_affiliations and len(want_affiliations) == 1:
                    this_affiliation = next(iter(want_affiliations))
                    want_providerids = ['urn:glue2:GlobalResourceProvider:{}.{}'.format(x.strip(), this_affiliation) for x in arg_providers.split(',')]
                    want_providers = []
                else:
                    want_providerids = []
                    want_providers = [int(x) for x in arg_providers.split(',') if x.strip().isdigit()]
            else:
                want_providerids = set(arg_providers.split(','))
                want_providers = []
        else:
            want_providerids = []
            want_providers = []

        arg_fields = request.GET.get('fields', None)
        if arg_fields:
            want_fields = set(arg_fields.lower().split(','))
        else:
            want_fields = set()

        sort = request.GET.get('sort', 'Name')
        page = request.GET.get('page', None)
        page_size = request.GET.get('results_per_page', 25)

        response_obj = {}
        try:
            # These filters are handled by the database; they are first
            RES = ResourceV3.objects.filter(QualityLevel__exact='Production')
            if want_affiliations:
                RES = RES.filter(Affiliation__in=want_affiliations)
            if want_resource_groups:
                RES = RES.filter(ResourceGroup__in=want_resource_groups)
            if want_types:
                RES = RES.filter(Type__in=want_types)
            if want_providerids:
                RES = RES.filter(ProviderID__in=want_providerids)
#            elif want_providers:
#                RES = RES.filter(EntityJSON__provider__in=want_providers)
#            if not want_terms:                  # Becase terms search does its own ranked sort
#                local_global_map = {'resource_name': 'Name',
#                                    'resource_type': 'Type',
#                                    'resource_description': 'Description',
#                                    'id': 'LocalID'}
#                if sort in local_global_map:
#                    RES = RES.order_by(local_global_map[sort])
#                elif sort is not None:
#                    RES = RES.order_by(RawSQL('"EntityJSON"->>\'{}\''.format(sort), ()))

            # These filters have to be handled with code; they must be after the previous database filters
            if want_topics:
                RES = resource_topics_filter(RES, want_topics)
            if want_terms:
                RES = resource_terms_filtersort(RES, want_terms, sort_field='name')
            elif want_strings:
                RES = resource_strings_filtersort(RES, want_strings, sort_field='name')
            RES = resource_oldevents_filter(RES)

            want_resources = set()
            for item in RES:
                want_resources.add(item.ID)

            want_guides = ResourceV3GuideResource.objects.filter(ResourceID__in=want_resources).order_by('CuratedGuideID').distinct('CuratedGuideID').values_list('CuratedGuideID', flat=True)

            objects = ResourceV3Guide.objects.filter(pk__in=want_guides).order_by('Name')
            response_obj['total_results'] = len(objects)

            if page:
                paginator = Paginator(objects, page_size)
                final_objects = paginator.page(page)
                response_obj['page'] = int(page)
                response_obj['total_pages'] = paginator.num_pages
            else:
                final_objects = objects
        except Exception as exc:
            raise MyAPIException(code=status.HTTP_400_BAD_REQUEST, detail='{}: {}'.format(type(exc).__name__, exc))

        context = {'fields': want_fields}
        serializer = Guide_Search_Serializer(final_objects, context=context, many=True)
        response_obj['results'] = serializer.data
        return MyAPIResponse(response_obj, template_name='resource_v3/guide_list.html')
