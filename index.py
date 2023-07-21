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
taskItems = [["Walk the dog", "Done"], ["Go to School", "Incomplete"], ["Do Homework", "Done"], ["Test", "In Process"]]

# for task in taskItems:
#     canvas= tk.Canvas(window, height= 20, width= 400, bg="gray", highlightthickness=0)

#     # Add a text in Canvas
#     canvas.create_text(0, 0, text=task, fill="white", font=('Helvetica 15 bold', 10, 'bold'))
#     canvas.pack(anchor="w", pady=5, padx=20)


# -------------------------------------------

def update_time():
    currentTime = time.localtime()
    timeNow = time.strftime("%-I:%M %p %Z ", currentTime)
    label["text"] = timeNow
    window.after(1000, update_time)

def angle(n):
    return n

def calculations(done, incomplete, inProcess, total):
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
    degrees = calculations(done, incomplete, inProcess, total)
    tk.Label(frame, text="Pie Chart").pack()
    canvas = tk.Canvas(window, width=200, height=200, bg="black", highlightthickness=0)
    canvas.pack(anchor="ne")
    canvas.place(x=490, y=30)
    canvas.create_arc((2,2,150,150), fill="green", outline="green", start=angle(0), extent=angle(degrees[0]))
    canvas.create_arc((2,2,150,150), fill="red", outline="red", start=angle(degrees[0]), extent=angle(degrees[1]))
    canvas.create_arc((2,2,150,150), fill="orange", outline="orange", start=angle(degrees[0] + degrees[1]), extent=angle(degrees[2]))

# -------------------------------------------

pie_chart()

btn1 = tk.Button(window, text="Add New Task",
fg="white",
bg="#0066FF")
btn1.pack(anchor="s", pady=100)

# Every second, the function update_time is called, updating time
window.after(1000, update_time)

# Run main loop
window.mainloop()