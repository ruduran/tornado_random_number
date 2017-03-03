import signal

import tornado.ioloop
import tornado.web

from main_handler import MainHandler


def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])


def stop_ioloop(signal, frame):
    tornado.ioloop.IOLoop.current().stop()


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)

    signal.signal(signal.SIGINT, stop_ioloop)
    tornado.ioloop.IOLoop.current().start()
