import csv
from bs4 import BeautifulSoup
from selenium import webdriver
from datetime import date

def get_url(search_type,country,page):
    search_type = search_type.replace(" ","+")
    target = f"https://in.indeed.com/jobs?q={search_type}&l={country}&start={page}"
    return target

    
#Generalize the pattern 
def extract_record(item):
    atag = item.h2.a
    job_title = atag.get('title')
    job_url = "https://in.indeed.com"+atag.get('href')
    job_company = item.find('span','company').text.strip()
    job_location = item.find('div','recJobLoc').get('data-rc-loc')
    job_summary = item.find('div','summary').text.strip()
    job_posting_date= item.find('span','date').text
    today = date.today().strftime('%Y-%m-%d')
    try:
        job_salary = item.find('span','salaryText').text.strip()
    except AttributeError:
        job_salary =""

    result = (job_title,job_company,job_summary,job_location,job_salary,job_posting_date,today,job_url)
    return result


def main(search_type,country):
    driver = webdriver.Chrome("C:\\Program Files (x86)\\Google\\Chrome\\Application\\chromedriver.exe")

    records =[]
    page = 0
    while True:
        
        driver.get(get_url(search_type,country,page))
        soup = BeautifulSoup(driver.page_source,'html.parser')
        results = soup.find_all('div','jobsearch-SerpJobCard')
        for item in results:
            record = extract_record(item)
            if record:
                records.append(record)
        
        try:
            end_url = soup.find('a',{'aria-label':'Next'}).get('href')
        except AttributeError:
            break
        page += 10
    driver.close()

    with open('results.csv', 'w',newline="",encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(['job_title','job_company','job_summary','job_location','job_salary','job_posting_date','today','job_url'])
        writer.writerows(records)

main('software developer','chhattisgarh')