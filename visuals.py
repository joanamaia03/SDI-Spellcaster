import tkinter as tk
import spellcaster

def start_program():
    spellcaster.run()

def quit_program():
    root.destroy()

# Create the main window
root = tk.Tk()
root.title("Spellcaster")
root.geometry("640x350") 

# Load the background image
bg_photo = tk.PhotoImage(file="mainmenu.png")
bg_photo = bg_photo.subsample(3, 3)

# Create a canvas and set the background image
canvas = tk.Canvas(root, width=640, height=350)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=bg_photo, anchor="nw")

# Start Button
start_button = tk.Button(root, text="Start", font=("Helvetica", 16), command=start_program, bg="lightpink", fg="black", width=20)
start_button_window = canvas.create_window(320, 205, window=start_button)

# Quit Button
quit_button = tk.Button(root, text="Quit", font=("Helvetica", 16), command=quit_program, bg="blue", fg="white", width=20)
quit_button_window = canvas.create_window(320, 255, window=quit_button)

root.mainloop()