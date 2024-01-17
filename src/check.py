from PIL import Image
import tkinter as tk
from tkinter import filedialog
import re

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

# Create Tkinter window
root = tk.Tk()
root.title("Image Fingerprint Checker")

# Create UI elements
label = tk.Label(root, text="Select an image:")
label.pack()

entry = tk.Entry(root, width=50)
entry.pack()

browse_button = tk.Button(root, text="Browse", command=sel_image)
browse_button.pack()

check_button = tk.Button(root, text="Check Image", command=check_image)
check_button.pack()

result_label = tk.Label(root, text="")
result_label.pack()

root.mainloop()
