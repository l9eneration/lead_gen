from linkedin.linkedin_worker import get_company_info
from web.download.download import Downloader, get_cookies_from_file
from djinni import djinni
from dou import dou
from prelinked_handler.anticlone import anticlone

def run():
    djinni_companies = find_companies('djinni', {"days_ago":1})
    print('djinni result', len(djinni_companies))
    dou_companies = find_companies('dou', {"max_count":200})
    print('dou result', len(dou_companies))
    compaies = anticlone(dou_companies, djinni_companies).values()
    print('Common result', len(compaies))

    result = _go_to_linkedin(companies)
    return result

def find_companies(original_site, config):
    crawler = _crawler_factory(original_site)
    if crawler is None:
        return None
    
    crawler_downloader = _downloader_factiry(original_site)
    if crawler_downloader is None:
        return None

    companies = crawler(crawler_downloader, config)
    return companies

def _crawler_factory(original_site):
    if original_site == 'djinni':
        return djinni.get_companies
    if original_site == 'dou' :
        return dou.get_companies
    return None

def _downloader_factiry(site, is_api = False):
    if site == 'djinni' ot site == 'dou':
        return Downloader()
    elif site == 'linkedin':
        if is_api:
            cookies = get_cookies_from_file('people_cookies.txt')
            headers = { 'csrf-token' : 'ajax:0902358166529822868',
                       'x-restli-protocol-version': '2.0.0'}
            return Downloader(cookies=cookies, headers=headers, timeout=1)
        else:
            cookies = get_cookies_from_file('cookies.txt')
            return Downloader(cookies=cookies, timeout=1)

    return None

def _go_to_linkedin(companies):
    li_downloader = downloader_factiry('linkedin')
    li_downloader_api = downloader_factiry('linkedin', True)
    if not li_downloader or not li_downloader_api:
        return None

    for num, company in enumerate(companies, start=1):
        print('{} of {}'.format(num, len(companies)))
        info = get_company_info(li_downloader, li_downloader_api, company.name(), company.website())
        company.data.update(info)

    return [company.data for company in companies]


