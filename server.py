import cgi
from argparse import ArgumentParser
from http.server import HTTPServer, BaseHTTPRequestHandler

import queue


class HttpRequestsHandler(BaseHTTPRequestHandler):
    ADDRESS = 'localhost'
    QUEUES_D = {
        0: queue.Queue(maxsize=100),
    }

    def do_GET(self):
        _queue = self.path.split('/')[-1]
        if _queue != '' and 0 <= int(_queue) <= 1000:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(bytes(self._get_item_from_queue(int(_queue)), 'utf-8'))
        return

    def do_POST(self):
        message = self.path.split('/')[-1]
        ctype, pdict = cgi.parse_header(self.headers['Queue'])
        if 0 <= int(ctype) <= 1000:
            self._add_item_to_queue(message, int(ctype))
            self.send_response(200)
            self.end_headers()
        return

    def _get_item_from_queue(self, queue_alias):
        if queue_alias == 0:
            try:
                return self.QUEUES_D[0].get(block=False)
            except queue.Empty:
                return ''

        if queue_alias in self.QUEUES_D:
            try:
                return self.QUEUES_D[queue_alias].get(block=False)
            except queue.Empty:
                return ''

    def _add_item_to_queue(self, item, queue_alias):
        if queue_alias == 0:
            try:
                self.QUEUES_D[0].put(item, block=False)
            except queue.Full:
                pass
        elif queue_alias in self.QUEUES_D:
            try:
                self.QUEUES_D[queue_alias].put(item, block=False)
            except queue.Full:
                pass
        else:
            self.QUEUES_D[queue_alias] = queue.Queue(maxsize=100)
            self.QUEUES_D[queue_alias].put(item, block=False)


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

