from worker import find_companies

companies_info = find_companies('djinni')

f = open('testPage.txt', 'w')
f.write('\n'.join([info.__str__() for info in companies_info]))
#f.write(info.__str__())

