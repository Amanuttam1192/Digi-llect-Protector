import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from hashlib import sha256
from lsb import LSB

class LSBApp:
    def __init__(self, root):
        self.root = root
        self.root.title("LSB Image Encryption")
        self.image_path = ""
        self.result_image = None

        self.create_widgets()
    
    def create_widgets(self):
        self.label = tk.Label(self.root, text="Select an image:")
        self.label.pack()

        self.browse_button = tk.Button(self.root, text="Browse", command=self.browse_image)
        self.browse_button.pack()

        self.encrypt_button = tk.Button(self.root, text="Encrypt", command=self.encrypt_image)
        self.encrypt_button.pack()

        self.output_label = tk.Label(self.root, text="Output Image:")
        self.output_label.pack()

        self.output_image_label = tk.Label(self.root)
        self.output_image_label.pack()

    def browse_image(self):
        self.image_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp")])

    def encrypt_image(self):
        if not self.image_path:
            return

        user_input = sha256(input("Enter your message: ").encode()).hexdigest()
        original_image = Image.open(self.image_path)
        encoded_image = LSB().encode_image(original_image, user_input)

        self.result_image = ImageTk.PhotoImage(encoded_image)
        self.output_image_label.config(image=self.result_image)
        self.output_image_label.image = self.result_image

def main():
    root = tk.Tk()
    app = LSBApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
