import requests

from exceptions import MissingCompanyError, MissingNameError, FinderApiError


class FinderAPIWrapper:
    def __init__(self, api_key, secret_key):
        self.api_key = api_key
        self.base_params = {'api_key': api_key, 'secret_key':secret_key}
        self.base_endpoint = 'https://findthat.email/api_json/{}'

    def _query_finder(self, endpoint, params = None, request_type='post',
                        payload=None, headers=None, raw=False):

        request_kwargs = dict(params=params, json=payload, headers=headers)
        res = getattr(requests, request_type)(endpoint, **request_kwargs)
        res.raise_for_status()

        if raw:
            return res

        try:
            data = res.json()['message']
        except KeyError:
            raise FinderApiError(res.json())

        return data

    def email_finder(self, domain=None, first_name=None,
                     last_name=None, raw=False):

        payload = self.base_params

        if domain:
            payload["company_domain"] = domain
        else:
            raise MissingCompanyError('You must supply at least a domain name')

        if first_name and last_name:
            payload["first_name"] = first_name
            payload["last_name"] = last_name
        else:
            raise MissingNameError(
                'You must supply a first name AND a last name OR a full name'
            )

        endpoint = self.base_endpoint.format('find_email')

        headers = {'Content-Type': 'application/json'}
        res = self._query_finder(endpoint, payload=payload, headers=headers)

        email = res['email']

        return email

if __name__ == '__main__':
    finder = FinderAPIWrapper('','')
    result = finder.email_finder('Microsoft.com','Bill','Gates')
    print(result)