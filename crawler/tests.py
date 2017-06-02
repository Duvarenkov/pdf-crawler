import os
from django.test import TestCase

from .utils import get_links_from_pdf
from .models import DocumentModel, URLModel
from unittest.mock import Mock, patch

TEST_PDF = os.path.join(os.path.realpath(os.path.dirname(__file__)), 'test_files', 'sample-link.pdf')


class UtilsTestCase(TestCase):

    def test_get_links_from_pdf(self):
        links = get_links_from_pdf(open(TEST_PDF, 'rb'))
        expected = ['http://www.antennahouse.com/purchase.htm']
        self.assertEqual(expected, links)


class URLModelTestCase(TestCase):

    def test_is_alive_false(self):
        links = [
            URLModel.objects.create(url=url) for url in [
                'http://test_url',
                'http://google.com/fake_url',
            ]
        ]
        for link in links:
            self.assertFalse(link.is_alive())

    def test_is_alive_true(self):
        links = [
            URLModel.objects.create(url=url) for url in [
                'https://www.facebook.com/',  # Answer 200
                'http://www.facebook.com/',   # Answer 301
            ]
        ]
        for link in links:
            self.assertTrue(link.is_alive())


class DocumentViewSetTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.doc = DocumentModel.objects.create(name='test_name')

    def test_list(self):
        resp = self.client.get('/documents/')
        expected = [{
            'name': 'test_name',
            'urls_count': 0,
            'uuid': str(self.doc.uuid)
        }]
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(expected, resp.json())

    def test_retrieve_no_urls(self):
        resp = self.client.get('/documents/%s/' % self.doc.uuid)
        self.assertEqual(resp.status_code, 200)
        expected = []
        self.assertEqual(expected, resp.json())

    def test_retrieve_with_urls(self):
        url = URLModel.objects.create(url='http://test_url')
        url.documents.add(self.doc)
        resp = self.client.get('/documents/%s/' % self.doc.uuid)
        expected = ['http://test_url']
        self.assertEqual(expected, resp.json())


class URLViewSetTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.url = URLModel.objects.create(url='http://test_url')

    def test_list(self):
        resp = self.client.get('/urls/')
        expected = [{
            'documents_count': 0,
            'is_alive': False,
            'url': 'http://test_url',
            'uuid': str(self.url.uuid)
        }]
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(expected, resp.json())

    def test_retrieve_no_docs(self):
        resp = self.client.get('/urls/%s/' % self.url.uuid)
        self.assertEqual(resp.status_code, 200)
        expected = {
            'documents_count': 0,
            'is_alive': False,
            'url': 'http://test_url',
            'uuid': str(self.url.uuid)
        }
        self.assertEqual(expected, resp.json())

    def test_retrieve_with_doc(self):
        doc = DocumentModel.objects.create(name='test_name')
        self.url.documents.add(doc)
        resp = self.client.get('/urls/%s/' % self.url.uuid)
        self.assertEqual(resp.status_code, 200)
        expected = {
            'documents_count': 1,
            'is_alive': False,
            'url': 'http://test_url',
            'uuid': str(self.url.uuid)
        }
        self.assertEqual(expected, resp.json())


class FileUploadViewTestCase(TestCase):

    @patch('crawler.utils.get_links_from_pdf')
    def test_post(self, mock_get_links_from_pdf):
        with open(TEST_PDF, 'rb') as pdf:
            resp = self.client.post(
                '/upload/somename.pdf',
                {'attachment': pdf}
            )
        assert mock_get_links_from_pdf.called
