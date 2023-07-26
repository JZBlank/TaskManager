# Import library to create GUI (Graphical user Interface)
import tkinter as tk
from tkinter import simpledialog

from datetime import date
import time

# Variables 
done = 0
incomplete = 0
inProcess = 0
isVisible = False

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

# -------------------------------------------
def update_time():
    currentTime = time.localtime()
    timeNow = time.strftime("%-I:%M %p %Z ", currentTime)
    label["text"] = timeNow
    window.after(1000, update_time)

def angle(n):
    return n

def calculations():
    global done, incomplete, inProcess
    totalTasks = len(taskItems)
    for item, status in taskItems:
        if status == "Done":
            done += 1
        elif status == "Incomplete":
            incomplete += 1
        elif status == "InProcess":
            inProcess += 1

    return [(done/totalTasks)*360, (incomplete/totalTasks)*360, (inProcess/totalTasks)*360]

def pie_chart():
    tk.Label(frame, text="Pie Chart").pack()
    canvas = tk.Canvas(window, width=200, height=200, bg="black", highlightthickness=0)
    canvas.pack(anchor="ne")
    canvas.place(x=490, y=30)

    if len(taskItems) == 0:
        canvas.create_arc((2,2,150,150), fill="green", outline="green", start=angle(0), extent=angle(359))
    else:
        degrees = calculations()
        canvas.create_arc((2,2,150,150), fill="green", outline="green", start=angle(0), extent=angle(degrees[0] - 0.000001))
        canvas.create_arc((2,2,150,150), fill="red", outline="red", start=angle(degrees[0]), extent=angle(degrees[1] - 0.000001))
        canvas.create_arc((2,2,150,150), fill="orange", outline="orange", start=angle(degrees[0] + degrees[1]), extent=angle(degrees[2] -  0.000001))


def summary_data():
    # FRAME FOR SUMMARY
    frame = tk.Frame(window, height=20, width=150, bg="blue")
    frame.place(x=490, y=230)
    tk.Label(frame, text="Summary", bg="blue", fg="white").pack(anchor="n")
    frame.pack_propagate(0)
    _y = 270

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

def list_data():
    # FRAME FOR EACH ITEM
    frame = tk.Frame(window, height=100, width=150, bg="blue")
    frame.place(x=490, y=230)
    tk.Label(frame, text="RANDOM TEXT", bg="green", fg="white").pack(anchor="n")
    frame.pack_propagate(0)

def check_task_status(status):
    if status == "Done":
        return "green"
    elif status == "Incomplete":
        return "red"
    elif status == "InProcess":
        return "orange"
    return "gray"

previousClicked = ""
isClicked = False

def label_clicked(event, text):
    global isClicked, previousClicked
    if isClicked == False:
        event.widget.config(relief="raised") 
        previousClicked = event.widget
        isClicked = True 
        
    elif isClicked == True:
        if previousClicked == event.widget:
            event.widget.config( relief="flat") 
            isClicked = False
        else:
            previousClicked.config(relief="flat") 
            event.widget.config(relief="raised") 
            previousClicked = event.widget

def bind_task_item(task, num, command):

    # Scrolling with mouse wheel 
    # task.bind("<Enter>", lambda _: task.bind_all('MouseWheel', command))
    # task.bind("<Leave>", lambda _: task.unbind_all('<MouseWheel>'))

    # task.bind("<Enter>", lambda _: task.config(text="welcome"))
    # task.bind('<Leave>', lambda _: task.config(text="thanks"))

    # Clicking labels
    task.bind("<Button-1>", lambda e: label_clicked(e, taskItems[num][0]))
    task.pack(pady=5)  

def destroy_task_labels():
    for i in range(0, len(taskItemLabels)):
       taskItemLabels[i].destroy()

def display_task_list():
    global isVisible 
    global message_frame, message_label

    if len(taskItems) == 0:
        isVisible = True
        message_frame.pack(anchor="nw", padx=20, pady=40) 
        message_label.pack(anchor="nw")

    else:
        if isVisible == True:
            message_frame.pack_forget()
            message_label.pack_forget()
        isVisible = False
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

def pop_up_window(event):
    newTask = tk.simpledialog.askstring(title="Add Task", parent=window, prompt="Enter New Task")
    taskInfo = newTask.split()
    taskItems.append(taskInfo)
    display_task_list()

def task_list_actions():

    # Add a New Task
    addNewTask = tk.Button(window, text="Add New Task", fg="white", bg="#0066FF")
    addNewTask.pack(anchor="s")
    addNewTask.place(x=20, y=450)
    addNewTask.bind("<Button-1>", lambda event: pop_up_window(event))

    # Remove a Task

    # Edit a Task

# ------------------------------------------- FUNCTION CALLS -------------------------------------------
pie_chart()
summary_data()
display_task_list()
task_list_actions()


# Every second, the function update_time is called, updating time
window.after(1000, update_time)

# Run main loop
window.mainloop()