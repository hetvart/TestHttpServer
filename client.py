import sys
from argparse import ArgumentParser

from http.client import HTTPConnection

from utils import test_print
from server import DEFAULT_PORT, DEFAULT_HOST


CONNECTION_REFUSE_PHRASE = 'Connection refused. Please check that the server is being run or ' \
                           'check host/port configuration.'
DEFAULT_QUEUE_ALIAS = '0'


class InitHttpClient(object):
    def __init__(self, address, port):
        self._conn = HTTPConnection(address, port)

    def get_message(self, queue):
        try:
            headers = {'Queue': queue}
            self._conn.request('GET', '', headers=headers)
            resp = self._conn.getresponse()
            data = resp.read()
        except ConnectionRefusedError:
            test_print(CONNECTION_REFUSE_PHRASE)
            sys.exit(2)
        if resp.status == 200 and data != b'':
            test_print(data.decode())
            test_print('[done]')
            return resp, data.decode()
        if resp.status == 403:
            test_print('%s: incorrect queue alias or maximum queue aliases exceeded' % resp.reason)
            return resp, data.decode()
        else:
            test_print('[done]')
            return resp, data.decode()

    def post_message(self, message, queue):
        try:
            headers = {'Message': message, 'Queue': queue}
            self._conn.request('POST', '', headers=headers)
            resp = self._conn.getresponse()
        except ConnectionRefusedError:
            test_print(CONNECTION_REFUSE_PHRASE)
            sys.exit(2)
        if resp.status == 200:
            test_print('[done]')
            return resp
        if resp.status == 403:
            test_print('%s: attempt to send an empty message or maximum queue aliases exceeded' % resp.reason)
            return resp

    def close_connection(self):
        self._conn.close()


def create_client_parser():
    port_parser = ArgumentParser(add_help=False)
    port_parser.add_argument('-p', '--port',
                             metavar='',
                             default=DEFAULT_PORT,
                             action='store',
                             help='specifies a port to listen at (default: 8080)',
                             type=int)

    queue_parser = ArgumentParser(add_help=False)
    queue_parser.add_argument('-q', '--queue',
                              default=DEFAULT_QUEUE_ALIAS,
                              metavar='',
                              type=str,
                              action='store',
                              dest='queue',
                              help='provide a queue alias number to read a message from it (default: 0)')

    message_parser = ArgumentParser(add_help=False)
    message_parser.add_argument('-m', '--message',
                                metavar='',
                                action='store',
                                required=True,
                                help='provide a message to send to the server')

    main_parser = ArgumentParser(description='The application is used to add/retrieve messages to/from queues')
    sub_parsers = main_parser.add_subparsers(help='commands')

    get_parser = sub_parsers.add_parser('get', help='to retrieve a message from the server',
                                        parents=[queue_parser, port_parser])
    get_parser.set_defaults(func='get')

    post_parser = sub_parsers.add_parser('post', help='to send a message to the server',
                                         parents=[message_parser, queue_parser, port_parser])
    post_parser.set_defaults(func='post')

    return main_parser


def create_client(host, port):

    client = InitHttpClient(host, port)
    return client


def main():
    parser = create_client_parser()
    args = parser.parse_args()
    client = create_client(DEFAULT_HOST, args.port)
    if args.func == 'get':
        client.get_message(args.queue)
        client.close_connection()
    if args.func == 'post':
        client.post_message(args.message, args.queue)
        client.close_connection()


if __name__ == '__main__':
    try:
        main()
    except AttributeError:
        test_print('Nothing to parse.\nYou did not provide any arguments.')
