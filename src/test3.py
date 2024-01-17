from hashlib import sha256
import json
import time
from PIL import Image, ImageTk
from flask import Flask
import tkinter as tk
from tkinter import filedialog, messagebox

# Classes and functions...

class LeastSB:
    def d_image(self, img):
        width, height = img.size
        msg = ""
        index = 0
        for row in range(height):
            for col in range(width):
                if img.mode != 'RGB':
                    r, g, b, a = img.getpixel((col, row))
                elif img.mode == 'RGB':
                    r, g, b = img.getpixel((col, row))
                if row == 0 and col == 0:
                    length = b
                elif index <= length:
                    msg += chr(b)
                index += 1
        return msg

def sel_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp")])
    entry.delete(0, tk.END)
    entry.insert(0, file_path)

def check_image():
    image_path = entry.get()
    try:
        image_to_check = Image.open(image_path)
        lsb_decoder = LeastSB()
        hidden_message = lsb_decoder.d_image(image_to_check)

        valid_fingerprint_format = re.match(r"^[a-f0-9]{64}$", hidden_message)

        if valid_fingerprint_format:
            result_label.config(text="The image contains a valid digital fingerprint.\nFingerprint: " + hidden_message)
        else:
            result_label.config(text="The image does not contain a valid digital fingerprint.")
    except Exception as e:
        result_label.config(text="Error: " + str(e))

def check_image_for_fingerprint():
    fingerprint_check_window = tk.Toplevel(root)
    fingerprint_check_window.title("Image Fingerprint Checker")

    label = tk.Label(fingerprint_check_window, text="Select an image:")
    label.pack()

    entry = tk.Entry(fingerprint_check_window, width=50)
    entry.pack()

    browse_button = tk.Button(fingerprint_check_window, text="Browse", command=sel_image)
    browse_button.pack()

    check_button = tk.Button(fingerprint_check_window, text="Check Image", command=check_image)
    check_button.pack()

    result_label = tk.Label(fingerprint_check_window, text="")
    result_label.pack()

# ... (existing classes and functions)

blockchain = Blockchain()
image2 = None  # Initialize image2 as None

root = tk.Tk()
root.title("Image Processor")

button_frame = tk.Frame(root)
button_frame.pack(padx=20, pady=10)

select_button = tk.Button(button_frame, text="Select Image", command=select_image)
select_button.pack(side=tk.LEFT, padx=5)

process_button = tk.Button(button_frame, text="Process Image", command=process_image)
process_button.pack(side=tk.LEFT, padx=5)

another_button = tk.Button(button_frame, text="Another Function", command=another_function)
another_button.pack(side=tk.LEFT, padx=5)

yet_another_button = tk.Button(button_frame, text="Yet Another Function", command=yet_another_function)
yet_another_button.pack(side=tk.LEFT, padx=5)

one_more_button = tk.Button(button_frame, text="One More Function", command=one_more_function)
one_more_button.pack(side=tk.LEFT, padx=5)

third_button = tk.Button(button_frame, text="Check Fingerprint", command=check_image_for_fingerprint)
third_button.pack(side=tk.LEFT, padx=5)

image_frame = tk.Frame(root, bd=2, relief=tk.SUNKEN)
image_frame.pack(padx=20, pady=(0, 10))

photo = None
img_label = tk.Label(image_frame)
img_label.pack()

status_label = tk.Label(root, text="No image loaded", bd=1, relief=tk.SUNKEN, anchor=tk.W)
status_label.pack(fill=tk.X, padx=20)

root.mainloop()
