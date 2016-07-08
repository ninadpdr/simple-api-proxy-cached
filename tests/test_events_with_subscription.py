# encoding=utf-8
# Author: ninadpage

import unittest
import json

from app import app


class TestEventsWithSubscription(unittest.TestCase):

    def setUp(self):
        self.endpoint = '/events-with-subscriptions/{event_id}/'

    def test_success(self):
        event_id = '0069c02d7fa333a88b7e50d850b9bcf6_14677217380318'
        with app.test_client() as cli:
            rv = cli.get(self.endpoint.format(event_id=event_id))
            self.assertTrue(rv.status_code == 200)
            response = json.loads(rv.data.decode('utf-8'))
            self.assertIn('id', response)
            self.assertIn('title', response)
            self.assertIn('names', response)

    def test_not_found(self):
        event_id = '0069c02d7fa333a88b7e50d850b9bcf6_1467721738031'
        with app.test_client() as cli:
            rv = cli.get(self.endpoint.format(event_id=event_id))
            self.assertTrue(rv.status_code == 404)


if __name__ == '__main__':
    unittest.main()
