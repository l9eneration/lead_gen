from .jobs import JobsDowloader
from dou.company_info import get_company_info
from commom.base.company import CompanyBase

def get_companies(downloader, config):
    jobs_dowloader = JobsDowloader(downloader)
    jobs = jobs_dowloader(config['max_count'])
    return _group_companies(jobs, downloader)

def _group_companies(jobs, downloader):
    result = dict()
    for job in jobs:
        company_name = job['company']
        company = result.get(company_name, None)
        if not company:
            company = result[company_name] = CompanyBase(name=company_name)
        company.add_job(job['job_title'])
        if not company.website() and not company.number_employees():
            number, wedside = get_company_info(downloader, job['company_dou_url'])
            company.set_number_employees(number)
            company.set_website(wedside)
    
    print("Dou: {} companies found.".format(len(result)))
    return result