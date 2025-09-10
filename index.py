# Import library to create GUI (Graphical user Interface)
import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox

from datetime import date
import time

import data

# Variables 
done = 0
incomplete = 0
inProcess = 0
ontop = False

# Create window Tkinter
window = tk.Tk()
 
# Name our Tkinter application title
window.title(" Task Manager ")
 
# Define window size in Tkinter python
window.geometry("700x500")
window.update_idletasks() # Redraw widgets without calling any callbacks *Updates size of window*

# Define window background color
window['background'] = 'black'
window['highlightbackground'] = 'black'

today = date.today().strftime("%b %d, %Y")
weekday = date.today().strftime("%A")
currentTime = time.localtime()
timeNow = time.strftime("%I:%M %p %Z ", currentTime)

# Create a label widget in Tkinter
label = tk.Label(window, text=weekday + " " + today,
fg = "white",
bg = "black",
font=('Calibri 15 bold'))
label.pack(pady=5, padx=20, anchor="w")

label = tk.Label(window, text=timeNow,
fg = "white",
bg = "black",
font=('Calibri 15 bold'))
label.pack(pady=5, padx=20, anchor="w")

# FRAME FOR TODAY 
frame = tk.Frame(window, height=20, width=393, bg="blue")
frame.place(x=20, y=90)
label2 = tk.Label(frame, text="Today", bg="blue", fg="white").pack(anchor="w", pady=5, padx=20)
frame.pack_propagate(0)

# TASK ITEMS
taskItemLabels = []

message_label = tk.Label(window, text= "No Current Tasks", bg="black", fg="white", width=49, height=2, anchor="nw")

tasklist_frame = tk.Frame(window, height=300, width=400, bg="orange", borderwidth= 0, highlightthickness=0)
tasklist_canvas = tk.Canvas(tasklist_frame, height=300, width=400, bg="red", borderwidth= 0, highlightthickness=0)

scrollbar = tk.Scrollbar(tasklist_frame, orient="vertical", command=tasklist_canvas.yview, borderwidth= 0, highlightthickness=0, width=5)
scrollable_frame = tk.Frame(tasklist_canvas, background="black", borderwidth= 0, highlightthickness=0)

scrollable_frame.bind("<Configure>", lambda e : tasklist_canvas.configure(scrollregion=tasklist_canvas.bbox("all")))
tasklist_canvas.create_window((0,0), window=scrollable_frame, anchor="nw")

tasklist_canvas.configure(yscrollcommand=scrollbar.set)
tasklist_canvas.config(background="black")

pop_up = tk.Frame(bg="red")
deleteTask = tk.Button(window, text="Delete Task", fg="white", bg="darkgray", activebackground="gray", activeforeground="white", highlightthickness=0)
deleteTask.place(x=250, y=450)

editTask = tk.Button(window, text="Edit Task", fg="white", bg="darkgray", activebackground="gray", activeforeground="white", highlightthickness=0)
editTask.pack(anchor="s")
editTask.place(x=150, y=450)

status_values = tk.OptionMenu(pop_up, None, None)

# Pie Chart Data + Summary
pie_data = tk.Canvas(window, width=200, height=450, bg="black", highlightthickness=0)
data_visuals = tk.Canvas(window, width=200, height=250, bg="black", highlightthickness=0)
task_data = tk.Canvas(window, width=200, height=250, bg="black", highlightthickness=0)

# Task Data information
task_name = tk.Label()
task_description = tk.Label()

# -------------------------------------------   

def update_time():
    currentTime = time.localtime()
    timeNow = time.strftime("%I:%M %p %Z ", currentTime)
    label["text"] = timeNow
    window.after(1000, update_time)

def angle(n):
    return n

def update_status():
    global done, incomplete, inProcess
    done = 0 
    incomplete = 0
    inProcess = 0

    for key, val in data.taskItems.items():
        if val[2] == 'Done':
            done += 1
        elif val[2] == 'Incomplete':
            incomplete += 1
        elif val[2] == 'InProcess':
            inProcess += 1

def calculations():
    global done, incomplete, inProcess
    update_status()

    return [(done/data.totalTasks)*360, (incomplete/data.totalTasks)*360, (inProcess/data.totalTasks)*360]

def data_visualization():
    global pie_data, data_visuals

    if data.totalTasks == 0:
        update_status()
        pie_data.create_arc((2,2,150,150), fill="green", outline="green", start=angle(0), extent=angle(359))
    else:
        degrees = calculations()
        pie_data.create_arc((2,2,150,150), fill="green", outline="green", start=angle(0), extent=angle(degrees[0] - 0.000001))
        pie_data.create_arc((2,2,150,150), fill="red", outline="red", start=angle(degrees[0]), extent=angle(degrees[1] - 0.000001))
        pie_data.create_arc((2,2,150,150), fill="orange", outline="orange", start=angle(degrees[0] + degrees[1]), extent=angle(degrees[2] -  0.000001))

    y_ = 165

    colors = [["red", "Incomplete"], ["orange", "InProcess"], ["green", "Done"],["gray", "None"]]
    for i in range(0, len(colors)):
        square = pie_data.create_rectangle(0, 0, 10, 10, fill=colors[i][0], outline=colors[i][0])  # Make the rectangle larger
        pie_data.move(square, 30, y_)
        label = tk.Label(pie_data, text=colors[i][1], font=("Arial Bold", 7), bg="black", fg="white")
        label.place(x=50, y=y_)  # Adjust the position of the label within the canvas
        y_ += 20

    y_ = 10

    # SUMMARY DATA 
    summary_label = tk.Label(data_visuals, text="Status Summary", font=("Arial Bold", 10), bg="blue", fg="white", padx= 50)
    summary_label.place(x=0, y=y_)  # Adjust the position of the label within the canvas

    y_ += 40

    arr = [["Total Tasks:      ", len(data.taskItems)], ["Completed:       ", done], ["In Process:        ", inProcess], ["Missing:            ", incomplete]]
    for item, count in arr:
        # Create a label widget in Tkinter
        label = tk.Label(data_visuals, text = item + " " + str(count),
        fg = "white",
        bg = "black",
        font=('Calibri 10'))
        label.pack()
        label.place(x=45, y=y_)
        y_ += 20


    # PIE CHART
    pie_data.pack(anchor="ne")
    pie_data.place(x=490, y=30)

    # PIE CHART DATA SUMMARY
    data_visuals.pack(anchor="center")
    data_visuals.place(x=475, y=280)

def check_task_status(status):
    if status == "Done" or status == "Done":
        return "green"
    elif status == "Incomplete" or status == "Incomplete":
        return "red"
    elif status == "InProcess" or status == "InProcess" :
        return "orange"
    return "gray"

selectedLabel = -1 # Item in TaskList that is clicked (-1 means unselected)

def label_clicked(event, text, num):
    global selectedLabel, deleteTask

    deleteTaskColor = "red"
    editTaskColor = "orange"
    defaultColor = "gray"

    if selectedLabel == -1:
        selectedLabel = num 
        taskItemLabels[selectedLabel].config(relief="raised") 
        deleteTask.config(bg=deleteTaskColor, activebackground="#D6001C", activeforeground="white")
        editTask.config(bg=editTaskColor, activebackground="dark" + editTaskColor, activeforeground="white")

        task_item_pop_up(selectedLabel)

    elif selectedLabel == num: # if same label is clicked twice, unselect label
        if taskItemLabels[selectedLabel]['relief'] == "raised":
            taskItemLabels[selectedLabel].config(relief="flat") 
            deleteTask.config(bg=defaultColor, activebackground=defaultColor, activeforeground="white")
            editTask.config(bg=defaultColor, activebackground=defaultColor, activeforeground="white")

            data_visualization_pop_up()

        else:
            taskItemLabels[selectedLabel].config(relief="raised") 
            deleteTask.config(bg=deleteTaskColor, activebackground="dark" + deleteTaskColor, activeforeground="white")
            editTask.config(bg=editTaskColor, activebackground="dark" + editTaskColor, activeforeground="white")

            task_item_pop_up(selectedLabel)


    else: # if different label is clicked and previous is selected
        taskItemLabels[selectedLabel].config(relief="flat") 
        taskItemLabels[num].config(relief="raised")
        selectedLabel = num
        deleteTask.config(bg=deleteTaskColor, activebackground="dark" + deleteTaskColor, activeforeground="white")
        editTask.config(bg=editTaskColor, activebackground="dark" + editTaskColor, activeforeground="white")

        task_item_pop_up(selectedLabel)

# SHOW LABEL ITEM DATA AND HIDE PIE CHART DATA + SUMMARY
def task_item_pop_up(selectedLabel):
    global task_name, task_description

    pie_data.pack_forget()
    pie_data.place_forget()

    # task_data = tk.Canvas(window, width=200, height=250, bg="black", highlightthickness=0)

    task_data.pack(anchor="center")
    task_data.place(x=475, y=30)

    task_info = tk.Label(task_data, text="Task Information", font=("Arial Bold", 10), bg="blue", fg="white", padx=50)
    task_info.place(x=0, y=10)  # Adjust the position of the label within the canvas

    task_name = tk.Label(task_data, text="Task Name: " + data.taskItems[selectedLabel][0], font=("Arial Bold", 9), bg="black", fg="white")
    task_description = tk.Label(task_data, text="Task Description: " + data.taskItems[selectedLabel][1], font=("Arial Bold", 9), bg="black", fg="white", wraplength= 200, justify="left")

    task_name.place(x=0, y=50)
    task_description.place(x=0, y=70)


# RESHOW PIE CHART DATA AND SUMMARY
def data_visualization_pop_up():
    global task_name, task_description

    # task_name.destroy()
    # task_description.destroy()

    task_data.pack_forget()
    task_data.place_forget()

    # task_data.destroy()

    # PIE CHART
    pie_data.pack(anchor="ne")
    pie_data.place(x=490, y=30)

def bind_task_item(task, num, command):

    # Scrolling with mouse wheel 
    # task.bind("<Enter>", lambda _: task.bind_all('MouseWheel', command))
    # task.bind("<Leave>", lambda _: task.unbind_all('<MouseWheel>'))

    # task.bind("<Enter>", lambda _: task.config(text="welcome"))
    # task.bind('<Leave>', lambda _: task.config(text="thanks"))

    # Clicking labels
    task.bind("<Button-1>", lambda e: label_clicked(e, data.taskItems[num][0], num))
    task.pack(pady=5)  

def destroy_task_labels():
    for i in range(0, len(taskItemLabels)):
       taskItemLabels[i].destroy()

def display_task_list():
    global message_label

    if data.totalTasks == 0:
        tasklist_frame.pack_forget()
        tasklist_canvas.pack_forget()
        message_label.place(x=20, y=120)

    else:
        message_label.pack_forget()
        task_list_items()

def sort_taskItemDict():
    sortedTasks = []

    # SORT DICTIONARY 
    for key, val in data.taskItems.items():
        sortedTasks.append([key, val[0], val[1], val[2]])
        sortedTasks.sort(key=lambda x: x[3], reverse=True)

    modifiedDict = {}

    for info in sortedTasks:
        modifiedDict[info[0]] = [info[1], info[2], info[3]]

    # COPY SORTED DICTIONARY TO ORIGINAL UNSORTED DICTIONARY
    data.taskItems = modifiedDict
    modifiedDict = {}

    count = 0
    for key, val in data.taskItems.items():
        modifiedDict[count] = val
        count += 1

    data.taskItems = modifiedDict

def task_list_items():
    global taskItemLabels, inProcess, incomplete, done

    destroy_task_labels()
    sort_taskItemDict()

    taskItemLabels = []
    inProcess = 0
    incomplete = 0
    done = 0

    for i in range(len(data.taskItems)):
        item = tk.Label(scrollable_frame, text= data.taskItems[i][0], bg=check_task_status(data.taskItems[i][2]), fg="white", width=48, height=2, highlightthickness=0, borderwidth=4, anchor="nw")
        taskItemLabels.append(item)
        bind_task_item(item, i, lambda e: item.config(text= 'Works')) 
    
    tasklist_frame.pack(side="left",anchor="nw", padx=20, pady=40) # Modify 'pady' to change spacing for tasklist list
    tasklist_canvas.pack(side="left",anchor="nw", fill="both", expand=True)

    # Only display scrollbar if height exceeds certain num (220)
    if scrollable_frame.winfo_height() > 220:
        scrollbar.pack(side="right", fill="both")

    data_visualization()

def close_pop_up(event):
    global ontop
    ontop = False
    pop_up.destroy()

def check_pop_window(event, title, color, action):
    global ontop, editTask
    if ontop == False:
        if action == "Add Task":
            ontop = True
            pop_up_window(event, title, color, action)
        elif action == "Edit Task" and editTask['bg'] != "darkgray":
            ontop = True
            pop_up_window(event, title, color, action)


def disable_event():
    pass

def option_menu_update(event, status_values, option_values_with_status, chosen_status):
    status_values.config(highlightthickness=0, fg="white", bg=option_values_with_status[chosen_status], activebackground=option_values_with_status[chosen_status], activeforeground="white")

def pop_up_window(event, title, color, action):
    global pop_up, status_values
    pop_up = tk.Toplevel(bg="black")

    pop_up.title(title)

    # center pop_up window
    screen_width = window.winfo_rootx()
    screen_height = window.winfo_rooty()

    pop_up_x = screen_width + 40
    pop_up_y = screen_height + 40

    pop_up.geometry("600x400")
    pop_up.geometry(f'+{pop_up_x}+{pop_up_y}')

    task_name = tk.Label(pop_up, text= "Task Name",
    fg = "white",
    bg = "black",
    font=('Calibri 10 bold'))
    task_name.pack()
    task_name.place(x=10, y=15)

    task_status = tk.Label(pop_up, text= "Status",
    fg = "white",
    bg = "black",
    font=('Calibri 10 bold'))
    task_status.pack()
    task_status.place(x=420, y=15)

    newTask = tk.Entry(pop_up, width=40)
    newTask.pack()
    newTask.place(x=10, y=40)

    option_values = ["Incomplete", "InProcess","Done"]
    option_values_with_status = {"Incomplete":"Red", "InProcess": "Orange", "Done":"Green"}

    option_var = tk.StringVar()
    chosen_color = ""

    if action == "Edit Task":
        newTask.insert(0, str(data.taskItems[selectedLabel][0]))
        for key, val in option_values_with_status.items():
            if key == str(data.taskItems[selectedLabel][2]):
                option_var = tk.StringVar(value=key)
                chosen_color = val
    else:
        option_var = tk.StringVar(value=option_values[0])
        chosen_color = option_values_with_status[option_values[0]]

    status_values = tk.OptionMenu(pop_up, option_var, *option_values, command= lambda event: option_menu_update(event, status_values, option_values_with_status, option_var.get()))
    status_values.config(highlightthickness=0, fg="white", bg=chosen_color, activebackground=chosen_color, activeforeground="white")
    status_values.pack()
    status_values.place(x=420, y=35)

    task_description = tk.Label(pop_up, text= "Task Description",
    fg = "white",
    bg = "black",
    font=('Calibri 10 bold'))
    task_description.pack()
    task_description.place(x=10, y=95)   
  
    task_descr_text = tk.Text(pop_up, width=70, height=10)
    task_descr_text.pack()
    task_descr_text.place(x=10, y=120)

    if action == "Edit Task":
        task_descr_text.insert("end", data.taskItems[selectedLabel][1])

    # NEW TASK BUTTONS
    actionButton = tk.Button(pop_up, text=action, fg="white", bg="#0066FF", activebackground= "blue", activeforeground="white", highlightthickness=0)
    actionButton.pack()
    actionButton.place(x=485, y=350)  
    actionButton.bind("<Button-1>", lambda event: choose_action(event, action, newTask.get(), task_descr_text.get("1.0", "end-1c"), option_var.get()))

    cancelNewTask = tk.Button(pop_up, text="Cancel", fg="white", bg="darkgray", activebackground="gray", activeforeground="white", highlightthickness=0)
    cancelNewTask.pack()   
    cancelNewTask.place(x=400, y=350)    
    cancelNewTask.bind("<Button-1>", lambda event: close_pop_up(event))

    pop_up.protocol("WM_DELETE_WINDOW", disable_event)
    pop_up.mainloop()

# ---- TASK ACTION FUNCTIONS ---- 
def choose_action(event, action, taskText, description, optionVal):
    if action == "Add Task":
        add_new_task(event, taskText, description, optionVal)
    elif action == "Edit Task":
        edit_task_item_label(event, taskText, description, optionVal)

def add_new_task(event, newTask, description, newTaskStatus):
    global pop_up, ontop
    
    data.add_task(str(data.totalTasks) + "," + newTask + "," + description + "," + newTaskStatus) # Add data to txt file
    data.taskItems[data.totalTasks] = [newTask, description, newTaskStatus]

    pop_up.destroy()
    ontop = False

    display_task_list()
    
def delete_task_item_label(event):
    global selectedLabel

    if selectedLabel != -1 and deleteTask['bg'] != "gray":

        data.delete_task(selectedLabel)
        data.taskItems.pop(selectedLabel)
        taskItemLabels[selectedLabel].destroy()

        selectedLabel = -1
        data.totalTasks -= 1

        deleteTask.config(bg="darkgray", activebackground="gray", activeforeground="white")
        editTask.config(bg="darkgray", activebackground="gray", activeforeground="white")

        display_task_list()
        data_visualization()

def edit_task_item_label(event, taskText, description, optionVal):
    global pop_up, ontop

    if selectedLabel != -1 and editTask['bg'] != "gray":
        editTask.config(bg="darkgray", activebackground="gray", activeforeground="white")
        pop_up.destroy()
        ontop = False

        # Modify Edited Text
        data.taskItems[selectedLabel][0] = taskText
        data.taskItems[selectedLabel][1] = description
        data.taskItems[selectedLabel][2] = optionVal

        # Sort data above so we can use to update txt file item order correctly
        sort_taskItemDict()

        # Modify Text in Txt File
        data.edit_task(str(selectedLabel), taskText, description,  optionVal, data.taskItems)

        # Update Data Displayed
        display_task_list()
        data_visualization()

def task_list_actions():
    global deleteTask
    global editTask
    # Add a New Task
    addNewTask = tk.Button(window, text="Add New Task", fg="white", bg="#0066FF", activebackground="blue", activeforeground="white", highlightthickness=0)
    addNewTask.pack(anchor="s")
    addNewTask.place(x=20, y=450)
    addNewTask.bind("<Button-1>", lambda event: check_pop_window(event, "Add New Task", "#0066FF", "Add Task"))

    # Remove a Task
    deleteTask.update_idletasks()
    deleteTask.bind("<Button-1>", lambda event: delete_task_item_label(event))

    # Edit a Task
    editTask.bind("<Button-1>", lambda event: check_pop_window(event, "Edit Task", "orange", "Edit Task"))




# ------------------------------------------- FUNCTION CALLS -------------------------------------------
data_visualization()
display_task_list()
task_list_actions()


# Every second, the function update_time is called, updating time
window.after(1000, update_time)

# Run main loop
window.mainloop()