import csv
from pathlib import Path


data_folder = Path("C:/Users/diego/OneDrive/Documents/Coding/Web Scrape/Analysis/Merged.csv")

with open(data_folder, 'r') as read:
    reader = csv.reader(read)
    for i in range(2): # Skip header
        reader.__next__()

    rows = list(reader)
    total_units, low_end, high_end = 0, 0, 0
    choose_state = False

    for index in range(len(rows)):
        first_val = rows[index][0]
        if ("Mandatory" in first_val) or ("Choice" in first_val):
            choose_state = False
            continue

        elif ("Choose" in first_val) and not ("Choose a" in first_val):
            choose_state = True
            
            if len(str(rows[index][2])) <= 2: # If one val
                total_units += int(rows[index][2])

            else: # If range
                tmp_strip_ls = rows[index][2].split("-") 
                low_end += int(tmp_strip_ls[0])
                high_end += int(tmp_strip_ls[1])

        elif "Choose a" in first_val: 
            if len(str(rows[index][2])) <= 2: # If one val
                total_units += int(rows[index][2])

            else: # If range
                tmp_strip_ls = rows[index][2].split("-") 
                low_end += int(tmp_strip_ls[0])
                high_end += int(tmp_strip_ls[1])

        elif not choose_state:
            total_units += int(rows[index][2])
    
    low_end += total_units
    high_end += total_units

    print("The high end of units taken for both majors is", high_end)
    print("The low end of units taken for both majors is", low_end)




        
