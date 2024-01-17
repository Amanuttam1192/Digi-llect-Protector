import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

root = tk.Tk()
root.title("Beautiful Tkinter UI")

# Applying a theme
style = ttk.Style()
style.theme_use("clam")

# Creating a custom style for buttons
style.configure('Custom.TButton', foreground='blue', font=('Arial', 12))

# Themed button
themed_button = ttk.Button(root, text="Themed Button", style='Custom.TButton')
themed_button.pack(pady=10)

# Image
img = Image.open('image.png')
img = img.resize((100, 100))
tk_image = ImageTk.PhotoImage(img)
image_label = tk.Label(root, image=tk_image)
image_label.pack(pady=10)

root.mainloop()
