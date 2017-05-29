import cgi
from argparse import ArgumentParser
from http.server import HTTPServer, BaseHTTPRequestHandler

import queue

import sys

from utils import test_print

DEFAULT_HOST = 'localhost'
DEFAULT_PORT = 8080
QUEUE_SIZE = 100
QUEUES = {}
QUEUE_ALIAS_MIN = 0
QUEUE_ALIAS_MAX = 1000
CONNECTION_REFUSE_PHRASE = 'Could not run the server. Probably the port you provided is busy.' \
                           'Please check your host/port configuration.'


class HttpRequestsHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        _queue, pdict = cgi.parse_header(self.headers['Queue'])
        try:
            _queue = int(_queue)
        except ValueError:
            self.send_response(403)
            self.end_headers()
            return
        if QUEUE_ALIAS_MIN <= _queue <= QUEUE_ALIAS_MAX:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(bytes(self._get_item_from_queue(_queue), 'utf-8'))
        else:
            self.send_response(403)
            self.end_headers()

    def do_POST(self):
        message, pdict = cgi.parse_header(self.headers['Message'])
        _queue, pdict = cgi.parse_header(self.headers['Queue'])
        try:
            _queue = int(_queue)
        except ValueError:
            self.send_response(403)
            self.end_headers()
            return
        if QUEUE_ALIAS_MIN <= _queue <= QUEUE_ALIAS_MAX and message:
            self._add_item_to_queue(message, _queue)
            self.send_response(200)
            self.end_headers()
        else:
            self.send_response(403)
            self.end_headers()

    def _get_item_from_queue(self, queue_alias):
        if queue_alias in QUEUES.keys():
            try:
                return QUEUES[queue_alias].get(block=False)
            except queue.Empty:
                QUEUES.pop(queue_alias)
        return ''

    def _add_item_to_queue(self, item, queue_alias):
        if queue_alias in QUEUES.keys():
            try:
                QUEUES[queue_alias].put(item, block=False)
            except queue.Full:
                return
        QUEUES[queue_alias] = queue.Queue(maxsize=QUEUE_SIZE)
        QUEUES[queue_alias].put(item, block=False)


def create_server_parser():
    parser = ArgumentParser(description='Run http server to receive and store messages in queues')
    parser.add_argument('port',
                        action='store',
                        default=DEFAULT_PORT,
                        nargs='?',
                        const=DEFAULT_PORT,
                        help='specifies a port to listen at (default: %s)' % DEFAULT_PORT,
                        type=int)
    return parser


def run_server(port):
    try:
        server = HTTPServer((DEFAULT_HOST, port), HttpRequestsHandler)
        server.serve_forever()
    except OSError:
        test_print(CONNECTION_REFUSE_PHRASE)
        sys.exit(2)
    except KeyboardInterrupt:
        server.server_close()


def main():
    parser = create_server_parser()
    args = parser.parse_args()
    run_server(args.port)


if __name__ == '__main__':
    main()
