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
        self.data['jobs'].append(job_title)

    def job_owner(self):
        return self.data.get('job_owner', None)

    def add_job_owner(self, owner):
        if('job_owner' not in self.data):
            self.data['job_owner'] = set()
        self.data['job_owner'].add(owner)

    def location(self):
        return self.data.get('location', None)

    def add_location(self, owner):
        if('location' not in self.data):
            self.data['location'] = set()
        self.data['location'].add(owner)