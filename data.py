import os
import sys

name = "data.txt"
name2 = "updated_data.txt"

taskItems = {}
totalTasks = 0

def resource_path(relative_path):
    """ Get the absolute path to the resource, works for dev and PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

data_file = resource_path('data.txt')
data_file2 = resource_path('updated_data.txt')

with open(data_file, 'r') as f:
    content = f.read()

name = data_file
name2 = data_file2
#---------

def add_task(task):
    global totalTasks

    try:
        file = open(name,'a')
        file.write(task + "\n")
        totalTasks += 1

    except:
        print('Error')

def delete_task(selectedLabel):
    count = 0

    try:
        with open(name, "r") as original_data:
            with open(name2, "w") as new_data: 
                for line in original_data:
                    if str(selectedLabel) not in line.strip("\n"):
                        new_data.write(line)
    except:
        print('Error')


    open(name, "w") # removes all text

    if os.path.getsize(name2) > 0:
        with open(name2, "r") as updated_data:
            with open(name, "w") as copy: 
                for line in updated_data:
                    line_split = line.split(",")
                    copy.write(str(count) + "," + line_split[1] + "," + line_split[2] + "," + line_split[3])
                    count += 1
    else:
        open(name, "w") 

    open(name2, "w") # removes all text
  
def delete_all():
    open(name, "w")

def edit_task(selectedLabel, task, description, status, taskItems):
    try:
        with open(name, "r") as original_data:
            with open(name2, "w") as new_data: 
                index = 0
                for line in original_data:
                    new_data.write(str(index) + "," + str(taskItems[index][0]) + "," + description + "," + str(taskItems[index][2]) + "\n")
                    index += 1
    except:
        print('Error')

    open(name, "w") # removes all text
    if os.path.exists(name):
        os.remove(name)
        
    os.rename(name2, name)  #rename updated file to original
    original_data = new_data
    new_data.close()

def check_data():
    if os.path.getsize(name) > 0:
        data_to_dict()

def data_to_dict():
    global totalTasks

    data_file = open(name,'a')
    with open(name) as data_file:
        for line in data_file:
            totalTasks += 1 # keep track of total tasks in txt file
            line_split = line.split(",")
            if line_split:
                taskItems[line_split[0]] = [line_split[1], line_split[2], line_split[3].strip("\n")]

check_data()
