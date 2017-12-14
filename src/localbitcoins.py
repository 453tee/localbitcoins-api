import hashlib
import hmac
import json
import urllib
from datetime import datetime

import requests


class API(object):
    """ Localbitcoins API """

    base_url = 'https://localbitcoins.com'

    def __init__(self, hmac_auth_key, hmac_auth_secret, debug=False):
        self.hmac_auth_key = hmac_auth_key
        self.hmac_auth_secret = hmac_auth_secret
        self.debug = debug

    def request(self, endpoint, method='get', **params):
        encoded_params = ''
        if params:
            encoded_params = urllib.urlencode(params)
            if method == 'get':
                encoded_params = '?' + encoded_params

        now = datetime.utcnow()
        epoch = datetime.utcfromtimestamp(0)
        delta = now - epoch
        nonce = int(delta.total_seconds() * 1000)

        message = str(nonce) + self.hmac_auth_key + endpoint + encoded_params
        signature = hmac.new(
            self.hmac_auth_secret, msg=message,
            digestmod=hashlib.sha256).hexdigest().upper()

        headers = {
            'Apiauth-key': self.hmac_auth_key,
            'Apiauth-Nonce': str(nonce),
            'Apiauth-Signature': signature}
        if method == 'get':
            response = requests.get(
                self.base_url + endpoint, headers=headers, params=params)
        else:
            response = requests.post(
                self.base_url + endpoint, headers=headers, data=params)

        if self.debug is True:
            print 'REQUEST: ' + self.base_url + endpoint
            print 'PARAMS: ' + str(params)
            print 'METHOD: ' + method
            print 'RESPONSE: ' + response.text

        return json.loads(response.text)

    # Advertisements
    def ads(self, **params):
        """ Returns all advertisements of the authenticated user.

        Kwargs:
            params(dict): https://localbitcoins.com/api-docs/#ads

        """
        return self.request('/api/ads/', **params)

    def ad_get(self, ad_id):
        """ Returns information on a single advertisement.

        Args:
            ad_id(int): advertisement ID.

        """
        return self.request('/api/ad-get/{}/'.format(ad_id))

    def ad_get_list(self, ads):
        """ Returns all ads from a list of comma separated ad ID's

        Args:
            ads(str): comma separated list of advertisement IDs.

        """
        return self.request('/api/ad-get/', ads=ads)

    def ad_update(self, ad_id, **params):
        """

        Args:
            ad_id(int): advertisement ID.

        Kwargs:
            params(dict): https://localbitcoins.com/api-docs/#ad-id

        """
        return self.request('/api/ad/{}/'.format(ad_id), method='post', **params)

    def ad_create(self, **params):
        """ Create a new advertisement.

        Kwargs:
            params(dict): https://localbitcoins.com/api-docs/#ad-create

        """
        return self.request('/api/ad-create/', method='post', **params)

    def ad_equation(self, ad_id, **params):
        """ Update equation of an advertisement.

        Args:
            ad_id(int): advertisement ID.

        Kwargs:
            params(dict): https://localbitcoins.com/api-docs/#ad-equation-id

        """
        return self.request(
            '/api/ad-equation/{}/'.format(ad_id), method='post', **params)

    def ad_delete(self, ad_id):
        """ Remove an advertisement.

        Args:
            ad_id(int): advertiesement ID.

        """
        return self.request('/api/ad-delete/{}'.format(ad_id), method='post')

    def payment_methods(self):
        """ Returns a list of valid payment methods. """
        return self.request('/api/payment_methods/')

    def payment_methods_countrycode(self, countrycode):
        """ Returns a list of valid payment methods for a specific country code.

        Args:
            countrycode(str): country code

        """
        return self.request('/api/payment_methods/{}/'.format(countrycode))

    def countrycodes(self):
        """ List of valid countrycodes for LocalBitcoins. """
        return self.request('/api/countrycodes/')

    def currencies(self):
        """ List of valid and recognized fiat currencies for LocalBitcoins. """
        return self.request('/api/currencies/')

    def places(self, **params):
        """
        Looks up places near lat, lon and provides full URLs to buy and
        sell listings.

        Kwargs:
            params(dict): https://localbitcoins.com/api-docs/#places

        """
        return self.request('/api/places/', **params)
