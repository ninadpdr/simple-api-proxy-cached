# encoding=utf-8
# Author: ninadpage

import unittest

from app import application


class HelloWorldTest(unittest.TestCase):

    def setUp(self):
        self.endpoint = '/'

    def test_service_is_up(self):
        with application.test_client() as cli:
            rv = cli.get(self.endpoint)
            self.assertTrue(rv.status_code == 200)


if __name__ == '__main__':
    unittest.main()
