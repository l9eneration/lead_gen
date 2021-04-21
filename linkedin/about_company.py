import re

class AboutCompanyDownloader:
    def __init__(self, downloader):
        self.downloader = downloader

    def __call__(self, company_url):
        return self.get_company_info(company_url)

    def get_company_info(self, company_url) -> dict:
        company_url+= r'about/'

        if not company_url.startswith(r'http://'):
            company_url = r'http://' + company_url

        page, success = self.downloader(company_url)
        if not success:
            return {'status':'download_fail', 'error_message': page}
        
        page = __clear_search_page__(page)
        data = __parse_searched_data__(page)

        return data

    
def __clear_search_page__(page: str):
    page = page.replace('&quot;',' ')

    return page

def __parse_searched_data__(data: str) -> dict:
    regex = r'staffCount :(\d+?),'
    matches = re.findall(regex, data, re.MULTILINE)
    staff_count = matches[0] if matches else 0

    regex = r'companyPageUrl : http://(.+?)[/\s]'
    matches = re.findall(regex, data, re.MULTILINE)
    company_url = matches[0] if matches else ''

    return {'staff_count': staff_count, 'website': company_url}