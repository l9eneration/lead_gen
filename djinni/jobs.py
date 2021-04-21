import re
from .date_helper import how_many_days_ago, date_str_2_datetime
from string import ascii_letters

class DjinniJobsDowloader:
    def __init__(self, downloader, max_pages = 600):
        self.downloader = downloader
        self.max_pages = max_pages

    def __call__(self,max_days_ago = 0):
        url = 'https://djinni.co/jobs/?page={}'
        
        result = []
        for page_counter in range(1,self.max_pages):
            page, _ = self.downloader(url.format(page_counter))
            result += _parse_main_jobs_page(page)
            print("DjinniJobs page {} results {}".format(page_counter, len(result)))

            last_date = result[-1]['date']
            if result and how_many_days_ago(result[-1]['date']) > max_days_ago :
                break

        return result

def _parse_main_jobs_page(page):
    regex_date = r"class=\"inbox-date pull-right\">[\s]+?(\S.+?)[\s]+?<"
    regex_job_url_and_title = r"[\s\W\w]+?class=\"profile\" href=\"(.+?)\">(.+?)</a>"
    regex_owner = r'[\s\W\w]+?</a>,[\n\s]+(.+?)\n'
    regex_company_name = r"[\s\W\w]+?href=\"/jobs/company[\W\w]+?\">(.+?)<"
    regex_location = r'[\s\W\w]+?<i.+?;(.+)\n'

    regex = regex_date + regex_job_url_and_title + regex_owner + regex_company_name + regex_location

    matches = re.finditer(regex, page, re.MULTILINE)

    groups = ('date', 'url', 'job_title', 'owner', 'company', 'location')
    result = [dict(zip(groups, match.groups())) for match in matches]

    result = _filtration_by_company_name(result)
    result = _conver_all_dates(result)

    return result       

def _filtration_by_company_name(jobs):
    return [job for job in jobs if __validate(job['company'])]

def __validate(name):
    return any(map(lambda c: c in ascii_letters, name))

def _conver_all_dates(data):
    result = []
    for job in data:
        job['date'] = date_str_2_datetime(job['date'])
        result.append(job)
    return result