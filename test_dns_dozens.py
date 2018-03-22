#!/usr/bin/python -B

import unittest
from dns_dozens import ChallangeRecord, DozensDNS


class TestChallangeRecord(unittest.TestCase):
    def setUp(self):
        self.record = ChallangeRecord('example.com', 'validation_string')
        self.sub_domain_record = ChallangeRecord('sub.example.com',
            'validation_string')

    def test_challange_fqdn(self):
        self.assertEqual('_acme-challenge.example.com',
            self.record.challange_fqdn())

    def test_validation(self):
        self.assertEqual('validation_string',
            self.record.validation())

    def test_is_in_zone(self):
        self.assertTrue(self.record.is_in_zone('example.com'))
        self.assertFalse(self.record.is_in_zone('example.net'))
        self.assertTrue(self.sub_domain_record.is_in_zone('example.com'))
        self.assertTrue(self.sub_domain_record.is_in_zone('sub.example.com'))
        self.assertFalse(self.sub_domain_record.is_in_zone('ub.example.com'))


class DozensDNS_for_test_empty_record(DozensDNS):
    def __init__(self, id, key):
        self._token = ''

    def _do_request(self, sub_uri, method='GET', body=''):
        return []


class TestDozensDNS(unittest.TestCase):
    def setUp(self):
        self.dozens = DozensDNS_for_test_empty_record(None, None)

    def test__delete_record(self):
        self.assertEqual(None, self.dozens._delete_record(''))

    def test__record_ids(self):
        self.assertEqual([], self.dozens._record_ids('', None))

if __name__ == "__main__":
    unittest.main()
