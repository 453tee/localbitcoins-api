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
        """ Returns information on a single advertisement. """
        return self.request('/api/ad-get/{}/'.format(ad_id))

    def ad_get_list(self, ads):
        """ Returns all ads from a list of comma separated ad ID's. """
        return self.request('/api/ad-get/', ads=ads)

    def ad_update(self, ad_id, **params):
        """ Update advertisement.

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

        Kwargs:
            params(dict): https://localbitcoins.com/api-docs/#ad-equation-id

        """
        return self.request(
            '/api/ad-equation/{}/'.format(ad_id), method='post', **params)

    def ad_delete(self, ad_id):
        """ Remove an advertisement. """
        return self.request('/api/ad-delete/{}/'.format(ad_id), method='post')

    def payment_methods(self):
        """ Returns a list of valid payment methods. """
        return self.request('/api/payment_methods/')

    def payment_methods_countrycode(self, countrycode):
        """
        Returns a list of valid payment methods for a specific country code.
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

    # Trades
    def feedback(self, username, **params):
        """ Gives feedback to a user.

        Kwargs:
            params(dict): https://localbitcoins.com/api-docs/#feedback
        """
        return self.request(
            '/api/feedback/{}/'.format(username), method='post', **params)

    def contact_release(self, contact_id, **params):
        """ Release a trade (does not require money_pin).

        Kwargs:
            params(dict): https://localbitcoins.com/api-docs/#contact-release

        """
        return self.request(
            '/api/contact_release/{}/'.format(contact_id), method='post',
            **params)

    def contact_release_pin(self, contact_id, **params):
        """ Release a trade (Requires money_pin).

        Kwargs:
            params(dict): https://localbitcoins.com/api-docs/#contact-release-pin

        """
        return self.request(
            '/api/contact_release_pin/{}/'.format(contact_id), method='post',
            **params)

    def contact_mark_as_paid(self, contact_id):
        """ Mark a trade as paid. """
        return self.request(
            '/api/contact_mark_as_paid/{}/'.format(contact_id), method='post')

    def contact_messages(self, contact_id):
        """ Return all chat messages from a specific trade ID. """
        return self.request('/api/contact_messages/{}/'.format(contact_id))

    def contact_message_post(self, contact_id, **params):
        """ Post a chat message to a specific trade ID.

        Kwargs:
            params(dict): https://localbitcoins.com/api-docs/#contact-post
        """
        return self.request(
            '/api/contact_message_post/{}/'.format(contact_id), method='post',
            **params)

    def contact_dispute(self, contact_id, **params):
        """ Starts a dispute on the trade ID.

        Kwargs:
            params(dict): https://localbitcoins.com/api-docs/#contact-dispute

        """
        return self.request(
            '/api/contact_dispute/{}/'.format(contact_id), method='post',
            **params)

    def contact_cancel(self, contact_id):
        """ Cancels the trade. """
        return self.request(
            '/api/contact_cancel/{}/'.format(contact_id), method='post')

    def contact_fund(self, contact_id):
        """ Fund an unfunded Local trade from your LocalBitcoins wallet. """
        return self.request(
            '/api/contact_fund/{}/'.format(contact_id), method='post')

    def contact_mark_realname(self, contact_id, **params):
        """ Mark realname confirmation.

        Kwargs:
            params(dict): https://localbitcoins.com/api-docs/#contact-mark-realname

        """
        return self.request(
            '/api/contact_mark_realname/{}/'.format(contact_id), method='post',
            **params)

    def contact_mark_identified(self, contact_id):
        """ Mark verification of trade partner as confirmed. """
        return self.request(
            '/api/contact_mark_identified/{}/'.format(contact_id), method='post')

    def contact_create(self, ad_id, **params):
        """ Start a trade from an advertisement.

        Kwargs:
            params(dict): https://localbitcoins.com/api-docs/#contact-create
        """
        return self.request(
            '/api/contact_create/{}/'.format(ad_id), method='post', **params)

    def contact_info(self, contact_id):
        """ Return information about a single trade ID. """
        return self.request('/api/contact_info/{}/'.format(contact_id))

    def contact_info_list(self, contacts):
        """
        Return information on your trades using a comma separated list input.
        """
        return self.request('/api/contact_info/', contacts=contacts)
