import re

class DjinniJobInfoDowloader:
    def __init__(self, downloader):
        self.downloader = downloader
    
    def __call__(self, url):
        page, _ = self.downloader(url)
        website = _get_company_wedside(page)
        description = _get_job_description(page)

        return website, description    

def _get_company_wedside(page: str):
    regex = r"(Company website|Сайт компании):</strong><br>[\s]+?<a href=\"(.+?)\""
    m = re.findall(regex, page, re.MULTILINE)
    if(m):
        return(m[0][1])
    return None

def _get_job_description(page: str):
    regex = r"class=\"profile-page-section\">([\s\W\w]+?)</div"
    job_desc = re.findall(regex, page, re.MULTILINE)

    if(job_desc):
        job_desc = [re.sub(r'<[\w\W\s]+?>|</.+?>|[\n\s]{2,}',' ',s) for s in job_desc]
        return '\n'.join(job_desc)
    return None
