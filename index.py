# Import library to create GUI (Graphical user Interface)
import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox

from datetime import date
import time

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
timeNow = time.strftime("%-I:%M %p %Z ", currentTime)

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
frame = tk.Frame(window, height=20, width=400, bg="blue")
frame.place(x=20, y=90)
label2 = tk.Label(frame, text="Today", bg="blue", fg="white").pack(anchor="w", pady=5, padx=20)
frame.pack_propagate(0)

# Task Items (Matrix)
# taskItems = [["Walk the dog", "Done"], ["Go to School", "Incomplete"], ["Do Homework", "Done"], ["Test", "InProcess"], ["Code", "InProcess"],["Go shopping", "Done"], ["Buy Food", "Done"]]
# taskItems.sort(key=lambda x: x[1])

taskItems = []
taskItemLabels = []

message_frame = tk.Frame(window, height=60, width=400, bg="black")
message_label = tk.Label(message_frame, text= "No Current Tasks", bg="black", fg="white", width=45, height=2, anchor="nw")

tasklist_frame = tk.Frame(window, height=300, width=400, bg="orange", borderwidth= 0, highlightthickness=0)
tasklist_canvas = tk.Canvas(tasklist_frame, height=300, width=400, bg="red", borderwidth= 0, highlightthickness=0)

scrollbar = tk.Scrollbar(tasklist_frame, orient="vertical", command=tasklist_canvas.yview, borderwidth= 0, highlightthickness=0, width=5)
scrollable_frame = tk.Frame(tasklist_canvas, background="black", borderwidth= 0, highlightthickness=0)

scrollable_frame.bind("<Configure>", lambda e : tasklist_canvas.configure(scrollregion=tasklist_canvas.bbox("all")))
tasklist_canvas.create_window((0,0), window=scrollable_frame, anchor="nw")

tasklist_canvas.configure(yscrollcommand=scrollbar.set)
tasklist_canvas.config(background="black")

pop_up = tk.Frame(bg="red")
deleteTask = tk.Button(window, text="Delete Task", fg="white", bg="darkgray", activebackground="gray", activeforeground="white")
deleteTask.place(x=250, y=450)

editTask = tk.Button(window, text="Edit Task", fg="white", bg="darkgray", activebackground="gray", activeforeground="white")
editTask.pack(anchor="s")
editTask.place(x=150, y=450)

status_values = tk.OptionMenu(pop_up, None, None)

# -------------------------------------------
def update_time():
    currentTime = time.localtime()
    timeNow = time.strftime("%-I:%M %p %Z ", currentTime)
    label["text"] = timeNow
    window.after(1000, update_time)

def angle(n):
    return n

def update_status():
    global done, incomplete, inProcess
    done = 0 
    incomplete = 0
    inProcess = 0
    
    for item, status in taskItems:
        if status == "Done":
            done += 1
        elif status == "Incomplete":
            incomplete += 1
        elif status == "InProcess":
            inProcess += 1

def calculations():
    global done, incomplete, inProcess
    totalTasks = len(taskItems)
    update_status()

    return [(done/totalTasks)*360, (incomplete/totalTasks)*360, (inProcess/totalTasks)*360]

def pie_chart():
    tk.Label(frame, text="Pie Chart").pack()
    canvas = tk.Canvas(window, width=200, height=150, bg="black", highlightthickness=0)
    canvas.pack(anchor="ne")
    canvas.place(x=490, y=30)

    if len(taskItems) == 0:
        update_status()
        canvas.create_arc((2,2,150,150), fill="green", outline="green", start=angle(0), extent=angle(359))
    else:
        degrees = calculations()
        canvas.create_arc((2,2,150,150), fill="green", outline="green", start=angle(0), extent=angle(degrees[0] - 0.000001))
        canvas.create_arc((2,2,150,150), fill="red", outline="red", start=angle(degrees[0]), extent=angle(degrees[1] - 0.000001))
        canvas.create_arc((2,2,150,150), fill="orange", outline="orange", start=angle(degrees[0] + degrees[1]), extent=angle(degrees[2] -  0.000001))


def pie_chart_legend():
    canvas = tk.Canvas(window, height=80, width=150, bg="black", highlightthickness=0)
    y_ = 0

    colors = [["red", "Incomplete"], ["orange", "InProcess"], ["green", "Done"],["gray", "None"]]
    for i in range(0, len(colors)):
        square = canvas.create_rectangle(0, 0, 10, 10, fill=colors[i][0], outline=colors[i][0])  # Make the rectangle larger
        canvas.move(square, 30, y_)
        label = tk.Label(canvas, text=colors[i][1], font=("Arial Bold", 7), bg="black", fg="white")
        label.place(x=50, y=y_)  # Adjust the position of the label within the canvas
        y_ += 20

    canvas.pack(anchor="center")
    canvas.place(x=490, y=200)


def summary_data():
    # FRAME FOR SUMMARY
    frame = tk.Frame(window, height=20, width=150, bg="blue")
    frame.place(x=490, y=290)
    tk.Label(frame, text="Summary", bg="blue", fg="white").pack(anchor="n")
    frame.pack_propagate(0)
    _y = 320

    arr = [["Total Tasks:      ", len(taskItems)], ["Completed:       ", done], ["In Process:        ", inProcess], ["Missing:            ", incomplete]]
    for item, count in arr:
        # Create a label widget in Tkinter
        label = tk.Label(window, text = item + " " + str(count),
        fg = "white",
        bg = "black",
        font=('Calibri 10'))
        label.pack()
        label.place(x=500, y=_y)
        _y += 20

def check_task_status(status):
    if status == "Done":
        return "green"
    elif status == "Incomplete":
        return "red"
    elif status == "InProcess":
        return "orange"
    return "gray"

selectedLabel = -1 # Item in TaskList that is clicked (-1 means unselected)

def label_clicked(event, text, num):
    global selectedLabel, deleteTask
    if selectedLabel == -1:
        selectedLabel = num 
        taskItemLabels[selectedLabel].config(relief="raised") 
        deleteTask.config(bg="red", activebackground="red", activeforeground="white")
        editTask.config(bg="orange", activebackground="darkorange", activeforeground="white")

    elif selectedLabel == num: # if same label is clicked twice, unselect label
        if taskItemLabels[selectedLabel]['relief'] == "raised":
            taskItemLabels[selectedLabel].config(relief="flat") 
            deleteTask.config(bg="gray", activebackground="gray", activeforeground="white")
            editTask.config(bg="gray", activebackground="gray", activeforeground="white")

        else:
            taskItemLabels[selectedLabel].config(relief="raised") 
            deleteTask.config(bg="red", activebackground="red", activeforeground="white")
            editTask.config(bg="orange", activebackground="darkorange", activeforeground="white")


    else: # if different label is clicked and previous is selected
        taskItemLabels[selectedLabel].config(relief="flat") 
        taskItemLabels[num].config(relief="raised")
        selectedLabel = num
        deleteTask.config(bg="red", activebackground="red", activeforeground="white")
        editTask.config(bg="orange", activebackground="darkorange", activeforeground="white")

        

def bind_task_item(task, num, command):

    # Scrolling with mouse wheel 
    # task.bind("<Enter>", lambda _: task.bind_all('MouseWheel', command))
    # task.bind("<Leave>", lambda _: task.unbind_all('<MouseWheel>'))

    # task.bind("<Enter>", lambda _: task.config(text="welcome"))
    # task.bind('<Leave>', lambda _: task.config(text="thanks"))

    # Clicking labels
    task.bind("<Button-1>", lambda e: label_clicked(e, taskItems[num][0], num))
    task.pack(pady=5)  

def destroy_task_labels():
    for i in range(0, len(taskItemLabels)):
       taskItemLabels[i].destroy()

def display_task_list():
    global message_frame, message_label

    if len(taskItems) == 0:
        message_frame.pack(anchor="nw", padx=20, pady=40) 
        message_label.pack(anchor="nw")

    else:
        message_frame.pack_forget()
        message_label.pack_forget()
        task_list_items()

def task_list_items():
    global taskItemLabels, inProcess, incomplete, done
    destroy_task_labels()
    taskItems.sort(key=lambda x: x[1])
    taskItemLabels = []
    inProcess = 0
    incomplete = 0
    done = 0

    for i in range(0, len(taskItems)):
        item = tk.Label(scrollable_frame, text= taskItems[i][0], bg=check_task_status(taskItems[i][1]), fg="white", width=140, height=2, highlightthickness=0, borderwidth=4, anchor="nw")
        taskItemLabels.append(item)
        bind_task_item(item, i, lambda e: item.config(text= 'Works')) 
    
    tasklist_frame.pack(side="left",anchor="nw", padx=20, pady=40) # Modify 'pady' to change spacing for tasklist list
    tasklist_canvas.pack(side="left",anchor="nw", fill="both", expand=True)

    scrollbar.pack(side="right", fill="both")

    pie_chart()
    summary_data()

def close_pop_up(event):
    global ontop
    ontop = False
    pop_up.destroy()

def check_pop_window(event, title, action):
    global ontop, editTask
    if ontop == False:
        if action == "Add Task":
            ontop = True
            pop_up_window(event, title, action)
        elif action == "Edit Task" and editTask['bg'] != "darkgray":
            ontop = True
            pop_up_window(event, title, action)

def disable_event():
    pass

def option_menu_update(event, status_values, option_values_with_status, chosen_status):
    status_values.config(highlightthickness=0, fg="white", bg=option_values_with_status[chosen_status], activebackground=option_values_with_status[chosen_status], activeforeground="white")

def pop_up_window(event, title, action):
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
        newTask.insert(0, str(taskItems[selectedLabel][0]))
        for key, val in option_values_with_status.items():
            if key == str(taskItems[selectedLabel][1]):
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

    # NEW TASK BUTTONS
    actionButton = tk.Button(pop_up, text=action, fg="white", bg="#0066FF", activebackground="blue", activeforeground="white")
    actionButton.pack()
    actionButton.place(x=485, y=350)  
    
    actionButton.bind("<Button-1>", lambda event: choose_action(event, action, newTask.get(), option_var.get()))

    cancelNewTask = tk.Button(pop_up, text="Cancel", fg="white", bg="darkgray", activebackground="gray", activeforeground="white")
    cancelNewTask.pack()   
    cancelNewTask.place(x=400, y=350)    

    cancelNewTask.bind("<Button-1>", lambda event: close_pop_up(event))

    pop_up.protocol("WM_DELETE_WINDOW", disable_event)

    pop_up.mainloop()

# ---- TASK ACTION FUNCTIONS ---- 
def choose_action(event, action, taskText, optionVal):
    if action == "Add Task":
        add_new_task(event, taskText, optionVal)
    elif action == "Edit Task":
        edit_task_item_label(event, taskText, optionVal)

def add_new_task(event, newTask, newTaskStatus):
    global pop_up, ontop
    taskItems.append([newTask, newTaskStatus])
    display_task_list()
    pop_up.destroy()
    ontop = False

def delete_task_item_label(event):
    global selectedLabel
    if selectedLabel != -1 and deleteTask['bg'] != "gray":
        taskItemLabels[selectedLabel].destroy()
        selectedLabel = -1
        deleteTask.config(bg="darkgray", activebackground="gray", activeforeground="white")
        editTask.config(bg="darkgray", activebackground="gray", activeforeground="white")
        taskItems.remove(taskItems[selectedLabel])
        pie_chart()
        summary_data()

def edit_task_item_label(event):
    if selectedLabel != -1 and editTask['bg'] != "gray":
        editTask.config(bg="darkgray", activebackground="gray", activeforeground="white")
        pop_up_window(event, "Edit Task", "Edit Task")

        pie_chart()
        summary_data()

def task_list_actions():
    global deleteTask
    global editTask
    # Add a New Task
    addNewTask = tk.Button(window, text="Add New Task", fg="white", bg="#0066FF", activebackground="blue", activeforeground="white")
    addNewTask.pack(anchor="s")
    addNewTask.place(x=20, y=450)
    addNewTask.bind("<Button-1>", lambda event: check_pop_window(event, "Add New Task", "Add Task"))

    # Remove a Task
    deleteTask.update_idletasks()
    deleteTask.bind("<Button-1>", lambda event: delete_task_item_label(event))

    # Edit a Task
    editTask.bind("<Button-1>", lambda event: check_pop_window(event, "Edit Task", "Edit Task"))




# ------------------------------------------- FUNCTION CALLS -------------------------------------------
pie_chart()
pie_chart_legend()
summary_data()
display_task_list()
task_list_actions()


# Every second, the function update_time is called, updating time
window.after(1000, update_time)

# Run main loop
window.mainloop()