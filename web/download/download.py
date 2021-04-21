import urllib.request, urllib.error, urllib.parse
import time

class Downloader:
    def __init__(self, cookies = None, headers = None, timeout = 0, max_try_count = 3):
        self.cookies = cookies
        self.headers = headers
        self.timeout = timeout
        self.max_try_count = max_try_count
    
    def __call__(self, url, cookies=None, headers=None, decoder_type = 'utf-8',
                 request_type = 'get', payload=None, response_info=False, method='GET'):
        current_cookies = cookies if cookies else self.cookies
        current_headers = headers if headers else self.headers

        return self._request(url, current_cookies, current_headers, decoder_type,
                             response_info=response_info, payload=payload, method=method)
        
    def _request(self, url, cookies, headers: dict,
                decoder_type, method, response_info, payload):    
        if self.timeout:
            print("timeout {} sec for url:".format(self.timeout), url)
            time.sleep(self.timeout)
        
        request = _construct_request(url, cookies, headers, payload)
        
        try_counter = 0
        result = None
        while try_counter < self.max_try_count:
            result, success = _download_webcontent(request)
            if not success:
                try_counter += 1
                print('ERROR: Failed download {} . Error {}'.format(url, result))
                continue
            if decoder_type:
                result['content'] = result['content'].decode(decoder_type)
            if response_info:
                return result, True
            return result['content'], True
        else:
            error_message = 'Failed download {} . Error {}'.format(url, result)
            return result, False


def _construct_request(url, cookies, headers, payload = None):
    if payload:
        payload = urllib.parse.urlencode(payload).encode()

    request = urllib.request.Request(url, payload)

    if cookies:
        request.add_header("Cookie", cookies)

    request.add_header('User-Agent', r'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36')
    request.add_header('Accept-Language', 'en-US,en')
    if headers:
        for key, value in headers.items():
            request.add_header(key, value)
    
    return request
    
def _download_webcontent(request):
    try:
       return __download_webcontent__(request)
    except Exception as e:
        error_message = str(e)
        return error_message, False
    except:
        error_message = 'Unknow download error'
        return error_message, False

def __download_webcontent__(request):
    response = urllib.request.urlopen(request)
    result = response.read()
    return {'content':result, 'info':response.info()}, True

def get_cookies_from_file(file_name):
    f = open(file_name, 'r')
    return f.read()

