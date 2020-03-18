"""
Get Job ilst in indeed using python
"""

import requests
from bs4 import BeautifulSoup

LANG = f"python"
LIMIT = 50
URL = f"https://www.indeed.com/jobs?q={LANG}&limit={LIMIT}"

def extract_indeed_pages():
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, 'html.parser')

    # Extract "pagination" class in html source
    pagination = soup.find("div", {"class": "pagination"})

    # Extract anchhor in pagination
    links = pagination.find_all("a")

    # Extract page ilst in links
    pages = []
    for link in links[:-1]:
        pages.append(int(link.find("span").string))

    max_page = pages[-1]

    return max_page

def extract_job(html):
    # Extract Job title
    title = html.find("div", {"class": "title"}).find("a")["title"]

    # Extract Company
    company = html.find("span", {"class": "company"})
    if company :
        company_anchor = company.find("a")
        company_name = None
        if company_anchor is not None:
            company_name = str(company_anchor.string)
        else:
            company_name = str(company.string)
        company_name = company_name.strip()
    else:
        company_name = ""
    company_loc = html.find("div", {"class": "recJobLoc"})['data-rc-loc']

    job_id = html['data-jk']

    return {'title': title, 'company': company_name, 'location': company_loc, 'link': f"https://www.indeed.com/viewjob?jk={job_id}"}

def extract_indeed_jobs(last_page):
    jobs = []
    for page in range(last_page):
        print(f"Scrapping page {page} / {last_page}")
        start = f"&start={page*LIMIT}"
        result = requests.get(f"{URL}{start}")
        soup = BeautifulSoup(result.text, 'html.parser')
        results = soup.find_all("div", {"class": "jobsearch-SerpJobCard"})
        
        for result in results:
            job = extract_job(result)
            jobs.append(job)
    return jobs

        # print(f"title: {title}, company: {company_name}")

    # return jobs

last_indeed_page = extract_indeed_pages()
indeed_jobs = extract_indeed_jobs(last_indeed_page)
print(indeed_jobs)