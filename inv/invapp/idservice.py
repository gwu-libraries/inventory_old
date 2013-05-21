from copy import copy
from datetime import datetime

from django.conf import settings

import requests


def get_idservice(test=False):
    if test or settings.DEBUG:
        kwargs = copy(settings.TEST_IDSERVICE)        
    else:
        kwargs = copy(settings.IDSERVICE)
    return IDService(**kwargs)


def mintandbind(objtype, objurl, description=''):
    idservice = get_idservice()
    data = idservice.mint(1)
    id = data['identifier']
    idservice.bind(id=id, objurl=objurl, objtype=objtype,
        desc=description)
    return id


class IDService():

    def __init__(self, requester, minter, url, port=80):
        self.minter = minter
        self.url = url if url.startswith('http') else 'http://%s' % url
        self.port = port
        if port != 80:
            self.baseurl = '%s:%s' % (url, port)
        else:
            self.baseurl = url

    def __str__(self):
        return '<IDService %s@%s>' % (self.minter, self.url)

    def mint(self, quantity=1):
        url = '%s/mint/%s/%s' % (self.baseurl, self.minter, quantity)
        response = requests.get(url)
        if response.status_code != 200:
            raise self.IDServiceError(response.text)
        data = response.json()
        if quantity==1: data = data[0]
        return data

    def bind(self, id, objurl, objtype='', desc=''):
        url = '%s/bind/%s' % (self.baseurl, id)
        params = {'object_url': objurl, 'object_type': objtype,
            'description': desc}
        response = requests.get(url, params=params)
        if response.status_code != 200:
            raise self.IDServiceError(response.text)
        return response.json()[0]

    def lookup(self, id):
        url = '%s/lookup/%s' % (self.baseurl, id)
        response = requests.get(url)
        if response.status_code != 200:
            raise self.IDServiceError(response.text)
        return response.json()[0]

    class IDServiceError(Exception):

        def __init__(self, msg):
            self.msg = msg

        def __repr__(self):
            return self.msg
