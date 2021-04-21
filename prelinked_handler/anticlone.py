from commom.base.company import CompanyBase
import copy


def anticlone(companies_a, companies_b):
    a_keys = set(companies_a.keys())
    b_keys = set(companies_b.keys())
    intersection = b_keys.intersection(a_keys)
    a_keys = a_keys.difference(intersection)
    b_keys = b_keys.difference(intersection)

    result = {key: companies_a[key] for key in a_keys}
    result.update({key: companies_b[key] for key in b_keys})
    result.update({key: join_companies(companies_a[key], companies_b[key]) for key in intersection})

    return result

def join_companies(company_a : CompanyBase, company_b : CompanyBase):
    print("Join company:", company_a.name())
    company = copy.deepcopy(company_a)

    if not company.website():
        company.set_website(company_b.website())
    if not company.number_employees() or (
        company_b.number_employees() and company.number_employees() > company_b.number_employees()
        ):
        company.set_number_employees(company_b.number_employees())
        
    if company_b.job_owner():
        company.add_job_owner(company_b.job_owner())

    if company_b.jobs():
        company.add_job(company_b.jobs())

    if company_b.location():
        company.add_location(company_b.location())
    
    return company



