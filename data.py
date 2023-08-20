import os
name = "data.txt"
name2 = "updated_data.txt"
total = 0

def add_task(task):
    try:
        file = open(name,'a')
        file.write(task + "\n")

    except:
        print('Error')

def delete_task(selectedLabel):
    try:
        with open(name, "r") as original_data:
            with open(name2, "w") as new_data: 
                for line in original_data:
                    if str(selectedLabel) not in line.strip("\n"):
                        new_data.write(line)
    except:
        print('Error')

    open(name, "w") # removes all text
    os.rename(name2, name)  #rename updated file to original
    original_data = new_data
    new_data.close()
            
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
                        new_data.write(str(selectedLabel) + " " + task + ", " + status + "\n")
    except:
        print('Error')

    open(name, "w") # removes all text
    os.rename(name2, name)  #rename updated file to original
    original_data = new_data
    new_data.close()

# def total_tasks():
#     global total
#     with open(name, "r") as original_data:
#         for line in original_data:
#             total += 1

    # return total