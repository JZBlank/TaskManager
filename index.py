# Import library to create GUI (Graphical user Interface)
import tkinter as tk
from datetime import date
import time
 
# Create window Tkinter
window = tk.Tk()
 
# Name our Tkinter application title
window.title(" MyWork ")
 
# Define window size in Tkinter python
window.geometry("700x500")
 
# Define window background color
window['background'] = 'black'
window['highlightbackground'] = 'black'

today = date.today().strftime("%b %d, %Y")
weekday = date.today().strftime("%A")
currentTime = time.localtime()
timeNow = time.strftime("%-I:%-M %p %Z ", currentTime)

# Create a label widget in Tkinter
label = tk.Label(window, text=weekday + " " + today,
fg = "white",
bg = "black",
font=('Calibri 15 bold'))
label.pack(pady=10, padx=20, anchor="w")

label = tk.Label(window, text=timeNow,
fg = "white",
bg = "black",
font=('Calibri 15 bold'))
label.pack(pady=5, padx=20, anchor="w")


# Create Frame 

todayLabel = tk.Label(window, text="Today",
borderwidth=10,
fg = "white",
bg = "#0066FF",
font=('Calibri 10 bold'))
todayLabel.pack(pady=10, padx=20, anchor="w")

def update_time():
    currentTime = time.localtime()
    timeNow = time.strftime("%-I:%-M %p %Z ", currentTime)
    label["text"] = timeNow
    window.after(1000, update_time)

btn1 = tk.Button(window, text="Add New Task",
fg="white",
bg="#0066FF")
btn1.pack(anchor="s")

# Every second, the function update_time is called, updating time
window.after(1000, update_time)

# Run main loop
window.mainloop()
