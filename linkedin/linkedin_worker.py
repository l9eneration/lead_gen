
from .search_company import CompanySearcher
from .companyinfo import CompanyInfoDownloader



def get_company_info(downloader, downloader_api, company_name, website = None):
    print('Finding info about', company_name,'...')

    searcher = CompanySearcher(downloader)
    companies = searcher(company_name)
    if 'status' in companies:
        print(" Searching failed.".format(company_name))
        return companies
    if not companies:
        print(" Company <{}> wasn't found".format(company_name))
        return {'status':'failed', 'error_message':"Company wasn't found on LinkedIn"}

    companies_check = [company for company in companies if company_name.lower() == company['name'].lower()]

    info_downloader = CompanyInfoDownloader(downloader, downloader_api)
    if len(companies_check) == 0 or len(companies_check) > 1:
        print(" Finded {} results or more. Filtering...".format(len(companies)))
        for company in companies:
            info = info_downloader(company['url'], linkedin_id=company['linkedin_id'], website=website)
            company.update(info)

        if all([company['status'] == 'download_fail' for company in companies]):
            print(" Download fail")
            return {'status':'download_fail','error_message': company.get('error_message', 'Download error')}

        if all([company['status'] == 'filtered' for company in companies]):
            print(" All results was filtered")
            return {'status':'filtered','error_message':"More than one result."}

        companies = [company for company in companies if company['status'] == 'success']
        if not companies or len(companies)>1:
            print(" All results was failed")
            return {'status':'failed','error_message':"More than one result."}

        print(" Filtering was finished. Info was finded")
        return companies[0]
    else:
        company = companies_check[0]
        info = info_downloader(company['url'], linkedin_id=company['linkedin_id'])
        company.update(info)
        print(" Info was finded")
        return company
