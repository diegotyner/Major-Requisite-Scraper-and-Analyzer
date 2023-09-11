from bs4 import BeautifulSoup
from pathlib import Path
import requests
import csv

data_folder = Path("C:/Users/diego/OneDrive/Documents/Coding/Web Scrape/Stripped")
with open(f"{data_folder / 'CS2'}.csv", 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["Course Code", "Class Name", "Units"])


    html_text = requests.get('https://catalog.ucdavis.edu/departments-programs-degrees/computer-science-engineering/computer-science-bs/#requirementstext').text
    soup = BeautifulSoup(html_text, 'lxml')
    courses = soup.find_all('td', class_ = "codecol")

    for course in courses:
        search = course.a['href']
        catalog_text = requests.get(f'https://catalog.ucdavis.edu{search}').text
        stew = BeautifulSoup(catalog_text, 'lxml')
        course_code = stew.find('span', class_ = 'text courseblockdetail detail-code margin--span text--semibold text--big').text.strip()
        course_name = stew.find('span', class_ = 'text courseblockdetail detail-title margin--span text--semibold text--big').text.strip()
        course_hours = stew.find('span', class_ = 'text courseblockdetail detail-hours_html margin--span text--semibold text--big').text.strip()
        
        print("Wrote:", course_code, course_name[2:], course_hours[1])
        writer.writerow([course_code, course_name[2:], course_hours[1]])
