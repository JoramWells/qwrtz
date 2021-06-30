from django.test import SimpleTestCase
from django.urls import resolve,reverse
from stepapp.views import home

class TestUrls(SimpleTestCase):
    def test_urls_is_resolved(self):
        url = reverse('index')
        print(resolve(url))