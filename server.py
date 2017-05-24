import cgi
from argparse import ArgumentParser
from http.server import HTTPServer, BaseHTTPRequestHandler

import queue


QUEUE_SIZE = 100
QUEUE_ALIAS_MIN = 0
QUEUE_ALIAS_MAX = 1000


class HttpRequestsHandler(BaseHTTPRequestHandler):
    ADDRESS = 'localhost'
    QUEUES = {
        0: queue.Queue(maxsize=QUEUE_SIZE),
    }

    def do_GET(self):
        _queue = self.path.split('/')[-1]
        if QUEUE_ALIAS_MIN <= int(_queue) <= QUEUE_ALIAS_MAX:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(bytes(self._get_item_from_queue(int(_queue)), 'utf-8'))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        message = self.path.split('/')[-1]
        ctype, pdict = cgi.parse_header(self.headers['Queue'])
        if QUEUE_ALIAS_MIN <= int(ctype) <= QUEUE_ALIAS_MAX:
            self._add_item_to_queue(message, int(ctype))
            self.send_response(200)
            self.end_headers()
        else:
            self.send_response(403)
            self.end_headers()

    def _get_item_from_queue(self, queue_alias):
        if queue_alias == 0:
            try:
                return self.QUEUES[0].get(block=False)
            except queue.Empty:
                return ''

        elif queue_alias in self.QUEUES:
            try:
                return self.QUEUES[queue_alias].get(block=False)
            except queue.Empty:
                return ''
        else:
            return ''

    def _add_item_to_queue(self, item, queue_alias):
        if queue_alias == 0:
            try:
                self.QUEUES[0].put(item, block=False)
            except queue.Full:
                pass
        elif queue_alias in self.QUEUES:
            try:
                self.QUEUES[queue_alias].put(item, block=False)
            except queue.Full:
                pass
        else:
            self.QUEUES[queue_alias] = queue.Queue(maxsize=QUEUE_SIZE)
            self.QUEUES[queue_alias].put(item, block=False)


def create_server_parser():
    parser = ArgumentParser(description='Run http server to receive and store messages in queues')
    parser.add_argument('port',
                        action='store',
                        default=8080,
                        nargs='?',
                        const=8080,
                        help='specifies a port to listen at (default: 8080)',
                        type=int)
    return parser


def main():
    try:
        parser = create_server_parser()
        args = parser.parse_args()
        server = HTTPServer((HttpRequestsHandler.ADDRESS, args.port), HttpRequestsHandler)
        server.serve_forever()
    except KeyboardInterrupt:
        server.server_close()


if __name__ == '__main__':
    main()

