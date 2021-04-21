import re

class JobsDowloader:
    def __init__(self, downloader):
        self.downloader = downloader

    def __call__(self, max_result = 200):
        return self._get_jobs(max_result)
        
    def _get_jobs(self, max_result):
        url = 'https://jobs.dou.ua'

        content, success = self.downloader(url=url, response_info = True)
        if not success:
            return ':(', False
        page = content['content']
        info = content['info']

        result = _parse_main_jobs_page(page)

        csrfmiddlewaretoken = _get_token_from_page(page)
        csrftoken = _get_token_from_set_cookies(info)

        success = True
        counter = 25
        while counter < max_result and success:
            add_result, success = self._get_more_jobs(len(result), csrftoken, csrfmiddlewaretoken, cookie=info.get_all('Set-Cookie')[0])
            print('Dou results:', len(result), counter)
            if success:
                result+=add_result
                counter+=40
                if counter != len(result):
                    raise Exception('Dou.ua regex problem')
        
        print('Dou results:', len(result), counter)

        return result

    def _get_more_jobs(self, count, csrftoken, csrfmiddlewaretoken , cookie):
        url = r'https://jobs.dou.ua/vacancies/xhr-load/'

        cookies = 'csrftoken='+csrftoken
        payload = {'csrfmiddlewaretoken':csrfmiddlewaretoken, 'count': count}
        headers = {'Referer': r'https://jobs.dou.ua/'}
        content, success = self.downloader(url=url, cookies=cookies, headers=headers, 
                                            payload=payload)
        if not success:
            return content, False

        return _parse_additional_jobs_page(content), True

def _get_token_from_set_cookies(info):
    cookie = info.get_all('Set-Cookie')[0]

    first = cookie.find('csrftoken=') + len('csrftoken=')
    second = cookie.find(';', first)

    return cookie[first: second]

def _get_token_from_page(page):
    first = page.find('CSRF_TOKEN = "') + len('CSRF_TOKEN = "')
    second = page.find('"', first)

    return page[first:second]

def _parse_main_jobs_page(page):
    regex = r'href="(.+?)vacancies.+?>(.+?)</a.+?class="company".+?>([^<>].+?)</a'
    groups = ('company_dou_url', 'job_title', 'company')
    return _parse_page(page, regex, groups)     

def _parse_additional_jobs_page(page):
    page = page.replace(r'\u00a0',' ')
    regex = r'href=\\\"(.+?)vacancies.+?>(.+?)<.+?class=\\\"company\\\".+?\"{0,1}\s{0,1}>+?\s{0,1}([^<].+?)</a'
    groups = ('company_dou_url', 'job_title', 'company')
    return _parse_page(page, regex, groups) 

def _parse_page(page, regex, groups):
    page = page.replace('&nbsp;',' ')
    matches = re.finditer(regex, page, re.MULTILINE)
    result = [dict(zip(groups, match.groups())) for match in matches]
    return result