import re
import json

class EmployeesFinder:
    def __init__(self, downloader):
        self.donwloader = downloader

    def __call__(self, company_id: str, count):
        return self.get_employees(company_id, count)

    def get_employees(self, company_id: str, count):
        url = r'https://www.linkedin.com/voyager/api/search/hits?count={count}&facetCurrentCompany=List({company_id})&&maxFacetValues=15&origin=organization&q=people&start=0&supportedFacets=List(GEO_REGION,SCHOOL,CURRENT_COMPANY,CURRENT_FUNCTION,FIELD_OF_STUDY,SKILL_EXPLICIT,NETWORK)' 
        url = url.format(count = count, company_id = company_id)

        content, success = self.donwloader(url)

        if not success:
            error_message = 'Employees download fail. ' + content
            return {'status':'download_fail', 'error_message':error_message}

        json_data = json.loads(content)
        data = __extract_data__(json_data)

        return data

def __extract_data__(json_data):
    data = json_data['elements']
    result = []

    for element in data:
        hit_info = element['hitInfo']['com.linkedin.voyager.search.SearchProfile']
        mini_profile = hit_info['miniProfile']

        first_name = mini_profile['firstName']
        last_name = mini_profile['lastName']
        occupation = mini_profile['occupation']
        public_identifier = mini_profile['publicIdentifier']
        location = hit_info['location']

        info = {'first_name': first_name, 'last_name':last_name,
                 'occupation':occupation, 'public_identifier':public_identifier,
                 'location':location }
        result.append(info) 

    return result

    
"""
if __name__ == '__main__':
    data = get_employees('3310540', 27)

    f = open('testPage.txt', 'w')
    f.write(data.__str__())
"""

