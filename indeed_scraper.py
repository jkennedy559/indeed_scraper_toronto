from selenium import webdriver
from bs4 import BeautifulSoup

#TODO - Investigate picked object to ensure scraping done correctly
#TODO - define range for all available posting
#TODO - need to protect spider from detection
#TODO - if hyperlink returned for company look at scraping that page

def ReturnJobs():
    base_url='https://ca.indeed.com/jobs?q=&l=Toronto%2C+ON&rbl=Toronto%2C+ON&jlid=aaab304de0fc22ae&jt=fulltime&lang=en&sort=date'
    url_list = [base_url + f'&start{i}' for i in range(10,100,10)]
    url_list.insert(0,base_url)
    browser = webdriver.Chrome()
    browser.implicitly_wait(5)
    all_jobs = []
    for url in url_list:
        browser.get(url)
        html_doc = browser.page_source
        soup = BeautifulSoup(html_doc, 'html.parser')
        jobs = soup.find_all('div', class_='jobsearch-SerpJobCard unifiedRow row result clickcard')
        all_jobs += jobs
    return(all_jobs)

#TODO - add rest of url to partial link

def ParseJobs(jobs):
    postings = []
    for job in jobs:
        posting=dict()
        posting['job_title'] = job.find(class_='title').find('a').text.strip()
        posting['job_link'] = job.find(class_='title').find('a')['href']
        try:
            posting['hiring_company'] = job.find(class_='company').find('a').text.strip()
        except AttributeError:
            posting['hiring_company'] = job.find(class_='company').text.strip()
        posting['location'] = job.find(class_='location').text.strip()
        posting['brief_sumary'] = job.find(class_='summary').text.strip()
        postings.append(posting)
    return(postings)

#TODO - Function that returns additional data from a specific job url 

if __name__ == '__main__':
    pass



