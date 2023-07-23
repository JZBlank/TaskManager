# Import library to create GUI (Graphical user Interface)
import tkinter as tk
from datetime import date
import time

# Variables 
done = 0
incomplete = 0
inProcess = 0
total = 0

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
taskItems = [["Walk the dog", "Done"], ["Go to School", "Incomplete"], ["Do Homework", "Done"], ["Test", "In Process"], ["Code", "In Process"],["Go shopping", "Done"], ["Buy Food", "Done"]]
taskItems.sort(key=lambda x: x[1])

tasks = []

# -------------------------------------------

def extract_task_data():
    for task, status in taskItems:
        tasks.append(task)

def update_time():
    currentTime = time.localtime()
    timeNow = time.strftime("%-I:%M %p %Z ", currentTime)
    label["text"] = timeNow
    window.after(1000, update_time)

def angle(n):
    return n

def calculations():
    global done, incomplete, inProcess, total
    for item, status in taskItems:
        if status == "Done":
            done += 1
            total += 1
        elif status == "Incomplete":
            incomplete += 1
            total += 1
        elif status == "In Process":
            inProcess += 1
            total += 1
    return [(done/total)*360, (incomplete/total)*360, (inProcess/total)*360]

def pie_chart():
    degrees = calculations()
    tk.Label(frame, text="Pie Chart").pack()
    canvas = tk.Canvas(window, width=200, height=200, bg="black", highlightthickness=0)
    canvas.pack(anchor="ne")
    canvas.place(x=490, y=30)
    canvas.create_arc((2,2,150,150), fill="green", outline="green", start=angle(0), extent=angle(degrees[0]))
    canvas.create_arc((2,2,150,150), fill="red", outline="red", start=angle(degrees[0]), extent=angle(degrees[1]))
    canvas.create_arc((2,2,150,150), fill="orange", outline="orange", start=angle(degrees[0] + degrees[1]), extent=angle(degrees[2]))


def summary_data():
    # FRAME FOR SUMMARY
    frame = tk.Frame(window, height=20, width=150, bg="blue")
    frame.place(x=490, y=230)
    tk.Label(frame, text="Summary", bg="blue", fg="white").pack(anchor="n")
    frame.pack_propagate(0)
    _y = 270

    arr = [["Total Tasks:      ", total], ["Completed:       ", done], ["In Process:        ", inProcess], ["Missing:            ", incomplete]]
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
    elif status == "In Process":
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
    task.bind("<Button-1>", lambda e: label_clicked(e, tasks[num]))
    task.pack(pady=5)  

def display_task_list():
    frame = tk.Frame(window, height=300, width=400, bg="black", borderwidth= 0, highlightthickness=0)
    canvas = tk.Canvas(frame, height=300, width=400, bg="black", borderwidth= 0, highlightthickness=0)

    scrollbar = tk.Scrollbar(frame, orient="vertical", command=canvas.yview, borderwidth= 0, highlightthickness=0, width=5)
    scrollable_frame = tk.Frame(canvas, background="black", borderwidth= 0, highlightthickness=0)

    scrollable_frame.bind("<Configure>", lambda e : canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0,0), window=scrollable_frame, anchor="nw")

    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.config(background="black")

    for i in range(0, total):
        item = tk.Label(scrollable_frame, text= taskItems[i][0], bg=check_task_status(taskItems[i][1]), fg="white", width=140, height=2,highlightthickness=0, borderwidth=4, anchor="nw")
        bind_task_item(item, i, lambda e: item.config(text= 'Works')) 

    frame.pack(side="left", padx=20)
    canvas.pack(side="left", fill="both", expand=True, ipady=15)
    scrollbar.pack(side="right",fill="both")

# -------------------------------------------

extract_task_data()
pie_chart()
summary_data()
display_task_list()


btn1 = tk.Button(window, text="Add New Task",
fg="white",
bg="#0066FF")
btn1.pack(anchor="s")
btn1.place(x=150, y=460)

# Every second, the function update_time is called, updating time
window.after(1000, update_time)

# Run main loop
window.mainloop()