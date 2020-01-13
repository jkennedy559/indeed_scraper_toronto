from selenium import webdriver
from bs4 import BeautifulSoup
import time
import pandas as pd


def ReturnJobs():
    url='https://ca.indeed.com/jobs?q=&l=Toronto%2C+ON&rbl=Toronto%2C+ON&jlid=aaab304de0fc22ae&jt=fulltime&lang=en&sort=date'
    browser = webdriver.Chrome()
    browser.implicitly_wait(10)
    all_jobs = []
    x = 1
    while x < 101:
        if x % 10 == 0: time.sleep(20)
        browser.get(url)
        html_doc = browser.page_source
        soup = BeautifulSoup(html_doc, 'html.parser')
        jobs = soup.find_all('div', class_='jobsearch-SerpJobCard unifiedRow row result clickcard')
        all_jobs += jobs
        partial_url = soup.find('div', class_='pagination').find('b').next_sibling.next_sibling['href']
        url = 'https://ca.indeed.com/' + partial_url
        x += 1
    return(all_jobs)


def ParseJobs(jobs):
    postings = []
    for job in jobs:
        posting=dict()
        posting['job_title'] = job.find(class_='title').find('a').text.strip()
        job_partial_url = job.find(class_='title').find('a')['href']
        posting['job_link'] = 'https://ca.indeed.com/' + job_partial_url
        try:
            posting['hiring_company'] = job.find(class_='company').find('a').text.strip()
        except AttributeError:
            posting['hiring_company'] = job.find(class_='company').text.strip()
        posting['location'] = job.find(class_='location').text.strip()
        posting['brief_sumary'] = job.find(class_='summary').text.strip()
        postings.append(posting)
    df_jobs = pd.DataFrame(postings)
    todays_date = time.strftime('%Y %m %d')
    df_jobs.to_csv(todays_date+'.csv')
    return


if __name__ == '__main__':
    pass



