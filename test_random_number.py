from io import StringIO
from unittest.mock import patch

import tornado.testing
from tornado.httpclient import HTTPResponse, HTTPRequest, HTTPError

from random_number import make_app


class TestMainHandler(tornado.testing.AsyncHTTPTestCase):

    def get_app(self):
        return make_app()

    def setUp(self):
        super(TestMainHandler, self).setUp()
        self.real_client = tornado.httpclient.AsyncHTTPClient(self.io_loop)
        self.async_patcher = patch('tornado.httpclient.AsyncHTTPClient')
        self.mock_client = self.async_patcher.start()

    def tearDown(self):
        self.async_patcher.stop()

    def fetch(self, url):
        self.real_client.fetch(self.get_url(url), self.stop)
        return self.wait()

    def set_client_response(self, body):
        request = HTTPRequest('/')
        response = HTTPResponse(request, 200,
                                buffer=StringIO(body))
        self.mock_client().fetch.side_effect = lambda x, y: y(response)

    def test_process_json(self):
        json = '{"type":"uint8","length":1,"data":[50],"success":true}'
        self.set_client_response(json)
        response = self.fetch('/')
        self.assertEqual(response.code, 200)
        self.assertEqual(response.body, b'50')

    def test_failed_json(self):
        self.set_client_response('{"success":false}')
        response = self.fetch('/')
        self.assertEqual(response.code, 200)
        self.assertEqual(response.body, b'ERROR')

    def test_empty_json(self):
        self.set_client_response('')
        response = self.fetch('/')
        self.assertEqual(response.code, 200)
        self.assertEqual(response.body, b'ERROR')
