# -*- coding: utf-8 -*-

import httplib2
import urllib
import django.utils.simplejson as json

import inspect
line = lambda: inspect.currentframe().f_back.f_lineno if inspect else ''

class InvalidResponseException(Exception):
    pass

class OAuth2(object):
    version = '2.0'
    response_type = ''
    grant_type = ''

    @classmethod
    def request(cls, uri, method="GET", body='', headers=None,
        redirections=httplib2.DEFAULT_MAX_REDIRECTS, connection_type=None):

        DEFAULT_POST_CONTENT_TYPE = 'application/x-www-form-urlencoded'

        if not isinstance(headers, dict):
            headers = {}

        if method == "POST":
            headers['Content-Type'] = headers.get('Content-Type',
                DEFAULT_POST_CONTENT_TYPE)

        return httplib2.Http(disable_ssl_certificate_validation=True).request(uri, method=method, body=body,
        #return httplib2.Http().request(uri, method=method, body=body,
            headers=headers, redirections=redirections,
            connection_type=connection_type)

    def login(self):
        qs = {
            'client_id':        self.APIKEY,
            'redirect_uri':     self.callback_url,
            'response_type':    self.response_type,
        }
        if self.scope:
            qs['scope'] = self.scope
        qs = urllib.urlencode(qs)
        uri = "%s?%s" %(self.authenticate_url, qs)
        return uri

    # must overide by subclass
    def authenticated(self, code):
        qs = {
            'client_id':        self.APIKEY,
            'client_secret':    self.APISECRET,
            'redirect_uri':     self.callback_url,
            'grant_type':       self.grant_type,
            'code':             code
        }
        if self.scope:
            qs['scope'] = self.scope
        #import pdb; pdb.set_trace()
        qs = urllib.urlencode(qs)
        uri = "%s?%s" %(self.access_token_url, qs)
        resp, content = self.request(uri, method='POST')

        if resp.status != 200:
            raise InvalidResponseException('oauth2.authenticated %s: Invalid response, HTTP status = %s' \
                % (line(), resp.status))
        r = json.loads(content)
        return r

    def user_info(self, access_token):
        qs = {
            'Authorization': "Bearer %s" % access_token,
        }
        uri = self.user_info_url
        resp, content = self.request(uri, headers=qs)

        if resp.status != 200:
            raise InvalidResponseException('oauth2.user_info %s: Invalid response, HTTP status = %s' \
                % (line(), resp.status))
        r = json.loads(content)
        return r


