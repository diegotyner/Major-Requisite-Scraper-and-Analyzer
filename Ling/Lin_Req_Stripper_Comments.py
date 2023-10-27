from bs4 import BeautifulSoup
from pathlib import Path
import requests
import csv

data_folder = Path("C:/Users/diego/OneDrive/Documents/Coding/Web Scrape/Stripped")
with open(f"{data_folder / 'Ling Comments'}.csv", 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["Ling", '', ''])
    writer.writerow(["Course Code", "Class Name", "Units"])

    html_text = requests.get('https://catalog.ucdavis.edu/departments-programs-degrees/linguistics/linguistics-ab/#requirementstext').text
    soup = BeautifulSoup(html_text, 'lxml')
    body = soup.find("tbody")

    choose = 0
    for header in body:
        # If header is courselist comment
        if '"courselistcomment"' in str(header) :
            course_comment = header.find('span', class_ = 'courselistcomment').text.strip()
            course_hours = header.find('td', class_ = 'hourscol').text.strip()

            if choose > 0:
                choose -= 1
                if choose == 0:
                    writer.writerow(["Choose done",'' ,''])
                    print("Choose comment done")
                print(choose)

            # Choose comment
            if ("Choose" in course_comment) :
                if ("or" in course_comment):
                    choose = 3
                else: 
                    choose = 1

                writer.writerow([course_comment,'' ,course_hours])
                print("Choose comment", choose)
                continue  

        elif 'codecol' in str(header) and 'orclass' not in str(header):
            search = header.a['href']
            catalog_text = requests.get(f'https://catalog.ucdavis.edu{search}').text
            stew = BeautifulSoup(catalog_text, 'lxml')
            course_code = stew.find('span', class_ = 'text courseblockdetail detail-code margin--span text--semibold text--big').text.strip()
            course_name = stew.find('span', class_ = 'text courseblockdetail detail-title margin--span text--semibold text--big').text.strip()
            course_hours = stew.find('span', class_ = 'text courseblockdetail detail-hours_html margin--span text--semibold text--big').text.strip()
            
            if course_code == "MAT 022A":  # Edge Case
                writer.writerow(["Choose done",'' ,''])
                print("Choose comment done")
                choose = 0

            writer.writerow([course_code, course_name[2:], course_hours[1]])
            print("Class")

        elif "commentindent" in str(header):    
            course_comment = header.find('span', class_ = 'courselistcomment commentindent').text.strip()
            if course_comment == "OR":
                continue
            writer.writerow([course_comment,'' ,'4'])
            print("Courselist comment header")

        elif "courselistcomment" in str(header):
            if choose > 0:
                choose -= 1
                if choose == 0:
                    writer.writerow(["Choose done",'' ,''])
                    print("Choose comment done")
                print(choose) 
            
            if "areaheader" in str(header):
                course_comment = header.find('span', class_ = 'courselistcomment').text.strip()
                writer.writerow([course_comment,'' ,''])
                print("Courselist comment header")

        # Literally just for the last line
        if "listsum" in str(header):
            course_comment = header.find('td', colspan = "2").text.strip()
            course_hours = header.find('td', class_ = "hourscol").text.strip()
            writer.writerow([course_comment,'' ,course_hours])
            print("Last courselist comment")