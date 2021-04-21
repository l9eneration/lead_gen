import re

class CompanySearcher:
    def __init__(self, downloader):
        self.downloader = downloader

    def __call__(self, company_name: str):
        return self.search_companies(company_name)

    def search_companies(self, company_name: str):
        url = r'https://www.linkedin.com/search/results/companies/?keywords='
        company_name = company_name.replace(' ', '%20')
        url = url + company_name

        page, success = self.downloader(url)
        if not success:
            return {'name': company_name, 'status':'download_fail','error_message': page}

        page = self.__clear_search_page__(page)
        result = self.__parse_searched_data__(page)

        return result


    def __clear_search_page__(self, page: str):
        page = page.replace('&quot;',' ')

        first = page.find('{ data :{ metadata :{ primaryResultType : COMPANIES')
        second = page.find('</code>', first)
        page = page[first:second]

        first = page.find('included :[')
        second = page.find('{ entityUrn', first)
        page = page[first+len('included :['):second]

        page = page.replace('{ template','\n{ template')[1:]

        return page

    def __parse_searched_data__(self, data: str):
        regex = r'urn:li:company:(\d+?) .+? text : (.+?) , .+? url : https://(.+?) '

        matches = re.finditer(regex, data, re.MULTILINE)

        groups = ('linkedin_id','name','url')
        result = [dict(zip(groups, match.groups())) for match in matches]

        return result
