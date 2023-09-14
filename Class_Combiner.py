import csv
from pathlib import Path
from word2number import w2n


def InClassList(classname, classlist, mode):
    if classname == "Total Units":
        return True
    
    for i in range(len(classlist)):
        if type(classlist[i]) is list:
            if classname in classlist[i]:
                # If choice continue, if mandatory delete entire list
                if mode == 'm':
                    print(classlist.pop())
                    return 1
            
                elif mode == 'c':
                    return 2

        elif classname == classlist[i]:
            return 1
    
    # If not found
    return 0

def MandatoryLowerDiv(folderpath, filename, csv_writer, classlist):
    choose_state = False
    

    with open(f"{folderpath / filename}.csv", 'r') as read:
        reader = csv.reader(read)
        for i in range(3):
            reader.__next__()
        for index, row in enumerate(reader):
            # If upper div
            if row[0] == "Depth Subject Matter":
                break
            
            # If choose_state, give two paths
            elif "Choose" in row[0]:
                if choose_state: 
                    choose_state = False
                else: 
                    choose_state = True
            
            # Else its a lower div class
            elif not choose_state and row[0] not in classlist:
                classlist.append(row[0])
                csv_writer.writerow(row)

def ChoiceLowerDiv(folderpath, filename, csv_writer, classlist):
    choose_state = False
    class_taken = False
    tmp_choice_list = []

    with open(f"{folderpath / filename}.csv", 'r') as read:
        reader = csv.reader(read)
        for i in range(3):
            reader.__next__()
        

        rows = list(reader)
        index = 0
        for index in range(len(rows)):
            if rows[index][0] == "Depth Subject Matter":
                break
            
            # If choose_state, give two paths
            elif "Choose" in rows[index][0]:
                if choose_state: 
                    choose_state = False
                    
                    if not class_taken: 
                        writer.writerow(rows[choose_start])
                        
                        classlist.append(tmp_choice_list.copy())
                        for i in range(1, index - choose_start):
                            tmp_choice_list = rows[i + choose_start][:-1]
                            tmp_choice_list.extend(["", rows[i + choose_start][-1]])
                            writer.writerow(tmp_choice_list) 
                        

                    tmp_choice_list.clear() 
                    class_taken = False
                else: # Not currently in choose_state
                    choose_state = True
                    choose_start = index
            
            # If in a choose_state and not in classlist
            elif choose_state and not class_taken:
                if rows[index][0] in classlist:
                    class_taken = True
                else:
                    tmp_choice_list.append(rows[index][0])

def MandatoryUpperDiv(folderpath, filename, csv_writer, classlist):
    choose_state = False
    upper_div_classes = False
    
    with open(f"{folderpath / filename}.csv", 'r') as read:
        reader = csv.reader(read)
        
        for i in range(3):
            reader.__next__()
        
        rows = list(reader)
        for index in range(len(rows)):
            # Only starting when upper div classes
            if rows[index][0] == "Depth Subject Matter":
                upper_div_classes = True
                continue
            elif not upper_div_classes:
                continue


            # If choose_state, give two paths
            elif "Choose" in rows[index][0]:
                if "Choose a" in rows[index][0]:
                    classlist.append(rows[index][0])
                    writer.writerow(rows[index])
                elif choose_state: 
                    choose_state = False
                else: # Not choose_state
                    choose_state = True
            
            
            # Else its a lower div class
            elif not choose_state and not InClassList(rows[index][0], classlist, "m"):
                classlist.append(rows[index][0])
                writer.writerow(rows[index])

def ChoiceUpperDiv(folderpath, filename, csv_writer, classlist):
    upper_div_classes = False
    tmp_choice_list = []
    choose_state = False
    choose_num = 0 
    class_taken = False
    choice_taken_num = []

    with open(f"{folderpath / filename}.csv", 'r') as read:
        reader = csv.reader(read)
        
        
        for i in range(3):
            reader.__next__()
        
        rows = list(reader)
        for index in range(len(rows)):
            # Only starting when upper div classes
            if rows[index][0] == "Depth Subject Matter":
                upper_div_classes = True
                continue
            elif not upper_div_classes:
                continue


            # If choose_state, give two paths
            elif "Choose" in rows[index][0] and "Choose a" not in rows[index][0]:
                if choose_state: 
                    choose_state = False
                    
                    if not class_taken: 
                        tmp_strip_ls = rows[choose_start][0].split()
                        tmp_strip_ls[1] = choose_num
                        restrung = tmp_strip_ls[0]
                        for i in range(1,len(tmp_strip_ls)):
                            restrung += " " + str(tmp_strip_ls[i])
                        rows[choose_start][0] = restrung

                        writer.writerow(rows[choose_start])
                        
                        classlist.append(tmp_choice_list.copy())
                        for i in range(1, index - choose_start):                      
                            if (i + choose_start) in choice_taken_num:
                                continue

                            tmp_choice_list = rows[i + choose_start][:2]
                            tmp_choice_list.extend([""])
                            for i in rows[i + choose_start][2:]:
                                tmp_choice_list.extend([i])
                                
                            writer.writerow(tmp_choice_list)                           

                    tmp_choice_list.clear() 
                    class_taken = False
                
                else: # Not currently in choose_state
                    choose_state = True
                    choose_start = index
                    choose_num = w2n.word_to_num(rows[index][0].split()[1].replace(":",""))
            
            # If in a choose_state and not in classlist
            elif choose_state and not class_taken:
                result = InClassList(rows[index][0], classlist, "c")
                if result == 1:
                    choose_num -= 1
                    choice_taken_num.append(index)
                    if len(str(rows[choose_start][2])) <= 2:
                        rows[choose_start][2] = int(rows[choose_start][2]) - 4
                    
                    else:
                        tmp_strip_ls = rows[choose_start][2].split("-")
                        for i in range(len(tmp_strip_ls)):
                            tmp_strip_ls[i] = int(tmp_strip_ls[i]) - 4
                        rows[choose_start][2] = str(tmp_strip_ls[0]) + "-" + str(tmp_strip_ls[1])

                        
                    if choose_num == 0:
                        class_taken = True
                
                elif result == 2:
                    rows[index].append("Shared with another choose")
                    tmp_choice_list.append(rows[index][0])

                else:
                    tmp_choice_list.append(rows[index][0])


data_folder = Path("C:/Users/diego/OneDrive/Documents/Coding/Web Scrape")
stripped_folder = data_folder / 'Stripped'
classes = []
# Start by writing mandatory lover divs
with open(f"{data_folder / 'Analysis' / 'Merged'}.csv", 'w', newline='') as f:
    writer = csv.writer(f) 

    writer.writerow(["CS and Cog Sci Combined", '', ''])
    writer.writerow(["Course Code", "Class Name", "Units"])

    writer.writerow(["Mandatory Lower Div", "", "", ""])
    MandatoryLowerDiv(stripped_folder, 'Cog Sci Comments', writer, classes)
    MandatoryLowerDiv(stripped_folder, 'CS Comments', writer, classes)

    writer.writerow(["Choice Lower Div", "", "", ""])
    ChoiceLowerDiv(stripped_folder, 'Cog Sci Comments', writer, classes)
    ChoiceLowerDiv(stripped_folder, 'CS Comments', writer, classes)

    writer.writerow(["Mandatory Upper Div", "", "", ""])
    MandatoryUpperDiv(stripped_folder, 'Cog Sci Comments', writer, classes)
    MandatoryUpperDiv(stripped_folder, 'CS Comments', writer, classes)

    writer.writerow(["Choice Upper Div", "", "", ""])
    ChoiceUpperDiv(stripped_folder, 'Cog Sci Comments', writer, classes)
    ChoiceUpperDiv(stripped_folder, 'CS Comments', writer, classes)

# Merge into a 3rd new csv, removing and choosing as needed