import requests

from .hunterio_exceptions import MissingCompanyError, MissingNameError, HunterApiError


class HunrerIOAPIWrapper:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_params = {'api_key': api_key}
        self.base_endpoint = 'https://api.hunter.io/v2/{}'

    def _query_hunter(self, endpoint, params, request_type='get',
                        payload=None, headers=None, raw=False):

        request_kwargs = dict(params=params, json=payload, headers=headers)
        res = getattr(requests, request_type)(endpoint, **request_kwargs)
        res.raise_for_status()

        if raw:
            return res

        try:
            data = res.json()['data']
        except KeyError:
            raise HunterApiError(res.json())

        return data

    def email_finder(self, domain=None, company=None, first_name=None,
                     last_name=None, raw=False):
        """
        Find the email address of a person given its name and company's domain.
        :param domain: The domain of the company where the person works. Must
        be defined if company is not.
        :param company: The name of the company where the person works. Must
        be defined if domain is not.
        :param first_name: The first name of the person. Must be defined.
        :param last_name: The last name of the person. Must be defined.
        :param raw: Gives back the entire response instead of just email and score.
        :return: email and score as a tuple.
        """
        params = self.base_params

        if not domain and not company:
            raise MissingCompanyError(
                'You must supply at least a domain name or a company name'
            )

        if domain:
            params['domain'] = domain
        elif company:
            params['company'] = company

        if not(first_name and last_name):
            raise MissingNameError(
                'You must supply a first name AND a last name OR a full name'
            )

        if first_name and last_name:
            params['first_name'] = first_name
            params['last_name'] = last_name

        endpoint = self.base_endpoint.format('email-finder')

        res = self._query_hunter(endpoint, params, raw=raw)
        if raw:
            return res

        email = res['email']
        score = res['score']

        return email, score