# Import library to create GUI (Graphical user Interface)
import tkinter as tk
from datetime import date
import time
 
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

# Task Items
taskItems = ["Walk the dog", "Go to School", "Do Homework", "TESTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT"]

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

btn1 = tk.Button(window, text="Add New Task",
fg="white",
bg="#0066FF")
btn1.pack(anchor="s", pady=200)

# Every second, the function update_time is called, updating time
window.after(1000, update_time)

# Run main loop
window.mainloop()
