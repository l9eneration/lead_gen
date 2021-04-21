import copy

class CompanyBase:
    def __init__(self, data= None, name:str= None):
        self.data = dict()
        if data:
            self.data = copy.deepcopy(data)
        if name:
            self.data['name'] = copy.deepcopy(name)

    def name(self):
        return self.data['name']

    def website(self):
        return self.data.get('website')

    def set_website(self, url):
        self.data['website'] = url

    def jobs(self):
        return self.data['jobs']

    def add_job(self, job_title):
        if('jobs' not in self.data):
            self.data['jobs'] = []
        if not isinstance(job_title, str) and hasattr(job_title, '__iter__'):
            self.data['jobs'].extend(job_title)
        else:
            self.data['jobs'].append(job_title)

    def job_owner(self):
        return self.data.get('job_owner', None)

    def add_job_owner(self, owner):
        if('job_owner' not in self.data):
            self.data['job_owner'] = set()
        if not isinstance(owner, str) and hasattr(owner, '__iter__'):
            self.data['job_owner'].update(owner)
        self.data['job_owner'].add(owner)

    def location(self):
        return self.data.get('location', None)

    def add_location(self, location):
        if('location' not in self.data):
            self.data['location'] = set()
        if not isinstance(location, str) and hasattr(location, '__iter__'):
            self.data['location'].update(location)
        self.data['location'].add(location)

    def number_employees(self):
        return self.data.get('number_employees')

    def set_number_employees(self, number):
        self.data['number_employees'] = number

    def employees(self):
        return self.data.get('employees')

    def set_employees(self, employees):
        self.data['employees'] = employees