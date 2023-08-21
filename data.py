import os

name = "data.txt"
name2 = "updated_data.txt"

taskItems = {}
totalTasks = 0


def add_task(task):
    try:
        file = open(name,'a')
        file.write(task + "\n")

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

    print(os.path.getsize(name2))
    if os.path.getsize(name2) > 0:
        with open(name2, "r") as updated_data:
            with open(name, "w") as copy: 
                for line in updated_data:
                    copy.write(line)
    else:
        open(name, "w") 

    open(name2, "w") # removes all text
    
            
def delete_all():
    open(name, "w")

def edit_task(selectedLabel, task, status):
    try:
        with open(name, "r") as original_data:
            with open(name2, "w") as new_data: 
                for line in original_data:
                    if str(selectedLabel) not in line.strip("\n"):
                        new_data.write(line)
                    else:
                        new_data.write(str(selectedLabel) + "," + task + "," + status + "\n")
    except:
        print('Error')

    open(name, "w") # removes all text
    os.rename(name2, name)  #rename updated file to original
    original_data = new_data
    new_data.close()

def task_list():
    if totalTasks > 0:
        with open(name) as data_file:
            for line in data_file:
                line_split = line.split(",")
                if line_split:
                    taskItems[line_split[0]] = [line_split[1], line_split[2].strip("\n")]
    
def total_tasks():
    global totalTasks
    totalTasks = 0
    for key in taskItems:
        totalTasks += 1

task_list()
total_tasks()
