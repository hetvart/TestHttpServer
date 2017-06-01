from unittest import TestCase, mock

from client import InitHttpClient


class GetRequestTestCase(TestCase):
    HOST = 'localhost'
    PORT = 8080

    def setUp(self):
        self.client = InitHttpClient(self.HOST, self.PORT)

    @mock.patch('client.HTTPConnection.request')
    @mock.patch('client.HTTPConnection.getresponse')
    def test_get_request_with_default_queue(self, mock_get_message, mock_get_response):
        mock_request = mock.Mock()
        mock_response = mock.Mock()

        mock_request.return_value = mock_response
        mock_get_message.return_value = mock_get_response

        queue = '0'
        expected_status = 200
        expected_message = 'hello'

        mock_get_response.status = expected_status
        mock_get_response.read.decode = expected_message

        resp = self.client.send_get_request(queue=queue)

        mock_get_message.assert_called_once(queue=queue)
        self.assertEqual(1, mock_get_message.call_count)
        self.assertEqual(1, mock_get_response.call_count)
        self.assertEqual(expected_status, resp.status)
        self.assertEqual(expected_message, resp.read.decode)

    # @mock.patch('client.HTTPConnection.getresponse')
    # def test_post_request_with_default_queue(self, mock_post_response):
    #     pass
        # exp_messages = ['hello', ]
        # queue_alias = '0'
        # post_message_to_queue_helper(self.DEFAULT_HOST, self.DEFAULT_PORT, exp_messages, queue_alias)
        # response, act_message = self.client.get_message(queue_alias)
        # self.assertEqual(200, response.status)
        # self.assertEqual(exp_messages[0], act_message)

    # def post_message_to_queue_helper(host, port, messages, queue_alias):
    #     client = InitHttpClient(host, port)
    #     for m in messages:
    #         client.post_message(m, queue_alias)
    #         client.close_connection()
    #
    #
    # class PostRequestTestCase(BaseTestCase):
    #     def setUp(self):
    #         self.client = InitHttpClient(self.DEFAULT_HOST, self.DEFAULT_PORT)
    #         return self.client
    #
    #     def tearDown(self):
    #         self.client.close_connection()
    #
    #     def test_post_request_with_no_message(self):
    #         exp_messages = 'have a good day!'
    #         queue_alias = '0'
    #         response = self.client.post_message(exp_messages, queue_alias)
    #         self.assertEqual(200, response.status)
    #
    #     def test_post_request_with_message(self):
    #         pass
    #
    #     def test_post_request_with_default_queue_alias(self):
    #         pass
    #
    #     def test_post_request_with_non_default_queue_alias(self):
    #         pass
    #
    #     def test_post_one_hundred_requests_to_queue(self):
    #         pass
    #
    #     def test_post_one_thousand_requests_to_one_thousand_diff_queues(self):
    #         pass
    #
    #     def test_post_request_to_out_of_range_queue_alias(self):
    #         pass


# class GetRequestTestCase(BaseTestCase):
#     def setUp(self):
#         self.client = InitHttpClient(self.DEFAULT_HOST, self.DEFAULT_PORT)
#         return self.client
#
#     def tearDown(self):
#         self.client.close_connection()
#
#     def test_get_request_with_default_queue(self):
#         exp_messages = ['hello', ]
#         queue_alias = '0'
#         post_message_to_queue_helper(self.DEFAULT_HOST, self.DEFAULT_PORT, exp_messages, queue_alias)
#         response, act_message = self.client.get_message(queue_alias)
#         self.assertEqual(200, response.status)
#         self.assertEqual(exp_messages[0], act_message)
#
#     def test_get_request_with_non_default_queue(self):
#         exp_messages = ['hi', ]
#         queue_alias = '12'
#         post_message_to_queue_helper(self.DEFAULT_HOST, self.DEFAULT_PORT, exp_messages, queue_alias)
#         response, data = self.client.get_message(queue_alias)
#         act_message = data
#         self.assertEqual(200, response.status)
#         self.assertEqual(exp_messages[0], act_message)
#
#     def test_get_all_messages_from_queue(self):
#         exp_messages = [str(i) + 'hello' for i in range(100)]
#         queue_alias = '0'
#         post_message_to_queue_helper(self.DEFAULT_HOST, self.DEFAULT_PORT, exp_messages, queue_alias)
#         for i in range(len(exp_messages)):
#             response, act_message = self.client.get_message(queue_alias)
#             self.assertEqual(200, response.status)
#             self.assertEqual(exp_messages[i], act_message)
#
#     def test_get_one_hundred_one_messages_from_queue(self):
#         exp_messages = [str(i) + 'hello' for i in range(100)]
#         queue_alias = '0'
#         post_message_to_queue_helper(self.DEFAULT_HOST, self.DEFAULT_PORT, exp_messages, queue_alias)
#         for i in range(len(exp_messages)):
#             response, act_message = self.client.get_message(queue_alias)
#             self.assertEqual(200, response.status)
#             self.assertEqual(exp_messages[i], act_message)
#         response, act_message = self.client.get_message(queue_alias)
#         self.assertEqual(200, response.status)
#         self.assertEqual('', act_message)
#
#     def test_get_message_from_out_of_range_queue(self):
#         exp_messages = ['', ]
#         queue_alias = '1001'
#         post_message_to_queue_helper(self.DEFAULT_HOST, self.DEFAULT_PORT, exp_messages, queue_alias)
#         response, act_message = self.client.get_message(queue_alias)
#         self.assertEqual(404, response.status)
#         self.assertEqual(exp_messages[0], act_message)
#
