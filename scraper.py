import requests
from bs4 import BeautifulSoup
from json import dump
import threading

def scrape_jobberman():
  found_jobz = None
  all_jobs = []
  working = True
  page_num = 1

  while working:
    if page_num < 7:
       page_num += 1
    else:
      working = False

    url = f'https://www.jobberman.com/jobs?page={page_num}'
    html_text = requests.get(url).text
    beautiful_soup = BeautifulSoup(html_text, 'lxml')
    job_postings = beautiful_soup.find_all('div', class_='flex flex-grow-0 flex-shrink-0 w-full')

    for postings in job_postings:
      found_jobz = {}
      job_name = postings.find('p', class_='text-lg font-medium break-words text-link-500').text
      company_name = postings.find('p', class_='text-sm text-link-500').text
      location = postings.find('span', class_='mb-3 px-3 py-1 rounded bg-brand-secondary-100 mr-2 text-loading-hide').text
      link = postings.find('a', href=True, class_='relative mb-3 text-lg font-medium break-words focus:outline-none metrics-apply-now text-link-500 text-loading-animate')['href']
    
      found_jobz['job_name'] = job_name.strip('\n')
      found_jobz['company_name'] = company_name.strip('\n')
      found_jobz['location'] = location.strip('\n')
      found_jobz['link'] = link.strip('\n')
      try:
        salary = postings.find('span', class_='mr-1').text
        found_jobz['salary'] = salary.strip('\n')
        all_jobs.append(found_jobz)
      except AttributeError:
        found_jobz['salary'] = None
        all_jobs.append(found_jobz)
        continue
     
  with open('jobberman.json', 'w') as f:
    dump(all_jobs, f, indent=4)
    print(len(all_jobs))

def job_gurus_scrapper():
  page_num = 1
  working = True

  found_jobz = None
  all_jobs = []

  while working:
    if page_num < 7:
      page_num += 1
    else:
      working = False


    url = f'https://www.jobgurus.com.ng/jobs/index/{page_num}?search_keyword=&specialization=&work_level='
    html_text = requests.get(url).text
    beautiful_soup = BeautifulSoup(html_text, 'lxml')
    job_postings = beautiful_soup.find_all('div', class_='panel panel-default job-post-panel')
  

    for postings in job_postings:
      found_jobz = {}
      job_name = postings.h2.text.strip()
      description = postings.find('div', class_='job-brief').text.strip()
      apply = postings.a['href']
      date_published = postings.find('div', class_='job-footer_text').text.strip()
      
      found_jobz['job_name'] = job_name.strip('\n')
      found_jobz['description'] = description.strip('\n')
      found_jobz['apply'] = apply.strip('\n')
      found_jobz['date_published'] = date_published.strip('\n')
      all_jobs.append(found_jobz)

  with open('job_gurus.json', 'w') as f:
    dump(all_jobs, f, indent=4)
    print(len(all_jobs))

      

def main():
  jobberman_thread = threading.Thread(target=scrape_jobberman)
  job_gurus_thread = threading.Thread(target=job_gurus_scrapper)
  jobberman_thread.start()
  job_gurus_thread.start()

if __name__ == '__main__':
  main()
