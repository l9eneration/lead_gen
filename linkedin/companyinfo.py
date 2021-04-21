from linkedin.search_employees import EmployeesFinder
from linkedin.about_company import AboutCompanyDownloader

class CompanyInfoDownloader:
    def __init__(self, downloader, downloader_api):
        self.downloader = downloader
        self.downloader_api = downloader_api

    def __call__(self, url, linkedin_id, max_staff_count = 50, website = None):
        about_company = AboutCompanyDownloader(self.downloader)

        data = {'status':'failed'}

        data.update(about_company(url))

        if int(data['staff_count']) > max_staff_count:
            data['status'] = 'filtered'
            data['error_message'] = 'staff_count exceeds {}. staff_count = {}'.format(max_staff_count, data['staff_count'])
            return  data

        if website and data['website'] and not (website in data['website'] or data['website'] in website):
            data['status'] = 'filtered'
            data['error_message'] = "Websites aren't equal {} <> {}".format(website, data['website'])
            return  data

        employees_finder = EmployeesFinder(self.downloader_api)
        employees = employees_finder(linkedin_id, data['staff_count']) 
        if 'status' in employees:
            return employees
        data['employees'] = employees
        data['status'] = 'success'
        
        return data