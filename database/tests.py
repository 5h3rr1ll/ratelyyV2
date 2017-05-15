from django.test import TestCase
from .models import brandsCrawler, companyCrawler
# Create your tests here.

class BrandCrawlerMethodTest(TestCase):
    def test_show_brand_list(self):
        crawler = brandsCrawler()
        self.assertIs(crawler.showCrawledBrands(), is not [] == True)
