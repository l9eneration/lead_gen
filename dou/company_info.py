import re

def get_company_info(downloader, url):
    content, success = downloader(url=url, cookies = 'lang=en')
    if not success:
        return content, False

    employees = _get_company_employee_count(content)
    wedside = _get_company_wedside(content)
    return employees, wedside

def _get_company_employee_count(page):
    regex = r'(\d+)(\+|[.\d]{5,}) employees'
    m = re.findall(regex, page, re.MULTILINE)
    if m:
        return(m[0][0])
    if 'less than 20 employees' in page:
        return 19
    return None

def _get_company_wedside(page: str):
    regex = r'class="site"[.\s\S]+?<.+?>(.+?)<'
    m = re.findall(regex, page, re.MULTILINE)
    if m:
        return(m[0])
    return None