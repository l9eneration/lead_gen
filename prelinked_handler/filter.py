def _filtration_by_job_owner(jobs):
    black_owners = {'recruiter', 'hr', 'talent', 'aquisition', 'sourcer',
                     'recruiting', 'recruitment', 'human recourses', 'searcher',
                     'рекрутер', 'human resources', 'recruter', 'research', 'human resource',
                     'sourcing',}
    return [job for job in jobs if not any(b_o in job['owner'].lower() for b_o in black_owners)]

def _filtration_by_job_title(jobs):
    good_jobs = {'developer', 'front-end', 'frontend', 'front end', 'admin',
                 'engineer', 'qa', 'devops', 'designer', 'product manager',
                  'team lead', 'tl', 'site manager', 'pm', 'backend', 'back-end', 'back end',
                  'dev', 'fullstack', 'full-stack', 'full stack',
                  'ios', 'javascript', 'python', 'js', 'android', 'react', '.net', 'java'}
    return [job for job in jobs if any(g_j in job['job_title'].lower() for g_j in good_jobs)]