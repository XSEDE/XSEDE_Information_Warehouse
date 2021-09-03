from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from xsede_warehouse.abstract_test_api import abstract_api_call

# Create your tests here.
class ProjectResourceTests(APITestCase):
    databases = ('xcsr', 'xcsr.read')

    @classmethod
    def setUp(self):
        pass
        
    def test_get_all_resources(self):
        url = reverse('projectresources-list')
        (status, data, data_json) = abstract_api_call(self, 'GET', url, {}, 'json')
        self.assertTrue(status == 200, msg='status not 200 ({})'.format(status))
        self.assertGreater(len(data), 1000, msg='Response was less than 1000 bytes ({})'.format(len(data)))
        self.assertTrue(data_json is not None, msg='Response was not valid JSON')

    def test_get_by_resource(self):
        args = ['stampede2.tacc.xsede.org']
        url = reverse('projectresources-by-resource', args=args)
        (status, data, data_json) = abstract_api_call(self, 'GET', url, {}, 'json')
        self.assertTrue(status == 200, msg='status not 200 ({})'.format(status))
        self.assertGreater(len(data), 100, msg='Response was less than 100 bytes ({})'.format(len(data)))
        self.assertTrue(data_json is not None, msg='Response was not valid JSON')

    def test_get_by_project(self):
        args = ['TG-EAR190005']
        url = reverse('projectresources-by-number', args=args)
        (status, data, data_json) = abstract_api_call(self, 'GET', url, {}, 'json')
        self.assertTrue(status == 200, msg='status not 200 ({})'.format(status))
        self.assertGreater(len(data), 100, msg='Response was less than 100 bytes ({})'.format(len(data)))
        self.assertTrue(data_json is not None, msg='Response was not valid JSON')
