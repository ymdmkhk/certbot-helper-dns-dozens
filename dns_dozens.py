#!/usr/bin/env python

import os
import subprocess
import json


class DozensDNS:
    _dozens_base_uri = 'https://dozens.jp/api'

    def __init__(self, id, key):
        command = ['curl', '-s',
                   '-H', 'X-Auth-User: ' + id,
                   '-H', 'X-Auth-Key: ' + key,
                   self._dozens_base_uri + '/authorize.json'
                  ]
        result = subprocess.check_output(command).decode('utf-8')
        self._token = json.loads(result)['auth_token']

    def _do_request(self, sub_uri, method='GET', body=''):
        command = ['curl',
                   '-s',
                   '-H', 'X-Auth-Token: ' + self._token,
                   '-H', 'Content-Type:application/json',
                   '-X', method,
                   self._dozens_base_uri + sub_uri + '.json'
                  ]
        if len(body) > 0:
            command.insert(1, '-d')
            command.insert(2, body)
        result = subprocess.check_output(command).decode('utf-8')
        return json.loads(result)

    def set(self, record):
        self.delete(record)
        self._create(record)

    def _create(self, record):
        zone = self._zone(record)
        request_body = self._create_record_json(zone, record)
        result = self._do_request('/record/create', 'POST', request_body)
        result['record']

    def _create_record_json(self, zone, record):
        name_end = len(record.challange_fqdn()) - len(zone) - 1
        name = record.challange_fqdn()[:name_end]
        dict_for_json = {
            'domain': zone,
            'name': name,
            'type': 'TXT',
            'prio': None,
            'content': record.validation(),
            'ttl': '7200',
            }
        return json.dumps(dict_for_json)

    def delete(self, record):
        zone = self._zone(record)
        record_ids = self._record_ids(zone, record)
        for record_id in record_ids:
            self._delete_record(record_id)

    def _delete_record(self, record_id):
        result = self._do_request('/record/delete/' + record_id, 'DELETE')
        #when no records,response is empty array
        if isinstance(result, list):
            return
        result['record']

    def _zone(self, record):
        zones = self._do_request('/zone')['domain']
        for zone in zones:
            if record.is_in_zone(zone['name']):
                return zone['name']

    def _record_ids(self, zone, record):
        result = self._do_request('/record/' + zone)
        #when no records,response is empty array
        if isinstance(result, list):
            return []
        records = result['record']
        record_ids = []
        for a_record in records:
            if (a_record['type'] == 'TXT' and
                    a_record['name'] == record.challange_fqdn()):
                record_ids.append(a_record['id'])
        return record_ids


class ChallangeRecord:

    def __init__(self, domain, validation):
        self._domain = domain
        self._validation = validation

    def challange_fqdn(self):
        return '_acme-challenge.' + self._domain

    def validation(self):
        return self._validation

    def is_in_zone(self, zone):
        if self._domain == zone:
            return True
        if len(self._domain) > len(zone):
            if self._domain[-1 * (len(zone) + 1):] == '.' + zone:
                return True
        return False


def _auth_hook():
    auth_hook = False
    try:
        os.environ['CERTBOT_AUTH_OUTPUT']
    except KeyError:
        auth_hook = True
    return auth_hook


def main():
    dns_service = DozensDNS(os.environ['DOZENS_ID'], os.environ['DOZENS_KEY'])
    record = ChallangeRecord(os.environ['CERTBOT_DOMAIN'],
        os.environ['CERTBOT_VALIDATION'])
    if _auth_hook():
        dns_service.set(record)
    else:
        dns_service.delete(record)


if __name__ == '__main__':
    main()
