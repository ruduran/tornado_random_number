import tornado.httpclient
import tornado.web


class MainHandler(tornado.web.RequestHandler):

    URL = "https://qrng.anu.edu.au/API/jsonI.php?length=1&type=uint8"
    ERROR_RET = "ERROR"

    @tornado.web.asynchronous
    def get(self):
        http_client = tornado.httpclient.AsyncHTTPClient()
        http_client.fetch(self.URL, self.response_handler)

    def response_handler(self, response):
        if response.error:
            self.write(self.ERROR_RET)
        else:
            self.write(self.process_json(response.body))

        self.finish()

    def process_json(self, json):
        json_dict = self.decode_json(json)
        success = json_dict.get('success', False)
        if success:
            data = json_dict.get('data', [])
            if len(data) >= 1:
                ret = data[0]
        else:
            ret = self.ERROR_RET

        return str(ret)

    def decode_json(self, json):
        ret = {}
        try:
            ret = tornado.escape.json_decode(json)
        except:
            pass
        return ret
