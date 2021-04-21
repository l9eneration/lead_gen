from .jobs import DjinniJobsDowloader
from .job_info import DjinniJobInfoDowloader
from commom.base.company import CompanyBase


def get_companies(downloader, config):
    print('Finding jobs on Djinni...')
    jobs_dowloader = DjinniJobsDowloader(downloader)
    jobs = jobs_dowloader(config['days_ago'])

    print('Finish find jobs Djinni:', len(jobs))
    print('Finding additional info and group companies...')
    jobinfo_dowloader = DjinniJobInfoDowloader(downloader)
    companies = _make_groups_by_jobs(jobs, jobinfo_dowloader)
    print('Finish find companies Djinni, companies:', len(companies))

    return companies

def _make_groups_by_jobs(jobs, info_dowloader):
    result = {}
    for job in jobs:
        company_name = job.pop('company')
        if company_name not in result:
            result[company_name] = CompanyBase(name=company_name)
            
        company = result[company_name]
        company.add_job(job['job_title'])
        company.add_job_owner(job['owner'])
        company.add_location(job['location'])
        if not company.website():
            url = job['url']
            website, _ =  info_dowloader('https://djinni.co'+url)
            company.set_website(website)

    return result
