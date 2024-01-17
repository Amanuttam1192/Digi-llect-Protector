from hashlib import sha256
import json
import time
from PIL import Image,ImageTk
from flask import Flask
import tkinter as tk
import re
from tkinter import filedialog,messagebox,ttk
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

def check_image_for_fingerprint():
    def sel_image():
        nonlocal entry
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
class LSB():
    def encode_image(self,img, msg):
        length = len(msg)
        if length > 255:
            print("text too long! (don't exeed 255 characters)")
            return False
        encoded = img.copy()
        width, height = img.size
        index = 0
        for row in range(height):
            for col in range(width):
                if img.mode != 'RGB':
                    r, g, b ,a = img.getpixel((col, row))
                elif img.mode == 'RGB':
                    r, g, b = img.getpixel((col, row))
                # first value is length of msg
                if row == 0 and col == 0 and index < length:
                    asc = length
                elif index <= length:
                    c = msg[index -1]
                    asc = ord(c)
                else:
                    asc = b
                encoded.putpixel((col, row), (r, g , asc))
                index += 1
        return encoded

    def decode_image(self,img):
        width, height = img.size
        msg = ""
        index = 0
        for row in range(height):
            for col in range(width):
                if img.mode != 'RGB':
                    r, g, b ,a = img.getpixel((col, row))
                elif img.mode == 'RGB':
                    r, g, b = img.getpixel((col, row))
                if row == 0 and col == 0:
                    length = b
                elif index <= length:
                    msg += chr(b)
                index += 1
        return msg

class Block:
    def __init__(self, ID, images, timestamp, previousHash):
        self.ID = ID
        self.images = images
        self.timestamp = timestamp
        self.previousHash = previousHash
        self.nonce = 0

    def compute_hash(self):
        data = json.dumps(self.__dict__, sort_keys=True)
        return sha256(data.encode()).hexdigest()


class Blockchain:
    difficulty = 4

    def __init__(self):
        self.chain = []
        self.create_firstBlock()

    def create_firstBlock(self):
        firstBlock = Block(0, [], time.time(), "0")
        firstBlock.hash = firstBlock.compute_hash()
        self.chain.append(firstBlock)

    @property
    def lastBlock(self):
        return self.chain[-1]

    def add_block(self, block, proof):

        previous = self.lastBlock.hash

        if previous != block.previousHash:
            return False

        if not self.is_valid(block, proof):
            return False

        block.hash = proof
        self.chain.append(block)
        return True

    def is_valid(self, block, hashN):

        return (hashN.startswith('0' * Blockchain.difficulty) and
                hashN == block.compute_hash())

    def pOw(self, block):

        block.nonce = 0

        computedHash = block.compute_hash()
        while not computedHash.startswith('0' * Blockchain.difficulty):
            block.nonce += 1
            computedHash = block.compute_hash()

        return computedHash

    def add_new_transaction(self, image,seller,buyer):
        self.unconfirmedImages = image
        self.seller = seller
        self.buyer = buyer

    def mineBlock(self):
        imageS = Image.open(self.unconfirmedImages)
        fingerPrint = LSB().decode_image(imageS)
        if not self.unconfirmedImages:
            return False
        if fingerPrint != self.seller.fingerprint:
            print("false")
            return False
        imageB = LSB().encode_image(image2, self.buyer.fingerprint)
        imageB.save("encoded.png")
        lastBlock = self.lastBlock

        newBlock = Block(ID=lastBlock.ID + 1,
                         images=self.unconfirmedImages,
                         timestamp=time.time(),
                         previousHash=lastBlock.hash)
        proof = self.pOw(newBlock)
        self.add_block(newBlock, proof)

        self.unconfirmedImages = []
        return newBlock.ID

class User:
    def __init__(self,name,fingerprint):
        self.name = name
        self.fingerprint = sha256(fingerprint.encode()).hexdigest()

def show_message(message):
    messagebox.showinfo("Message", message)
def select_image():
    file_path = filedialog.askopenfilename()
    if file_path:
        global image2
        image2 = Image.open(file_path)
        status_label.config(text="Image selected")
        photo = ImageTk.PhotoImage(image2)
        img_label.config(image=photo)
        img_label.image2 = photo
        show_message("Image loaded successfully")
        # Do something with the selected image, like display it
        # For instance, display the image in a label or process it further

def process_image():
    status_label.config(text="Image Processed, Please Check the root folder")
    show_message("Image Processed, Please Check the root folder")
    global image2
    if image2:
        seller1 = User("Aman", "Aman35")
        buyer1 = User("Aishwary", "Aishwary25")
        image1 = LSB().encode_image(image2, seller1.fingerprint)
        image1.save("encoded.png")
        blockchain.add_new_transaction("encoded.png", seller1, buyer1)
        blockchain.mineBlock()
    else:
        print("Please select an image first.")

blockchain = Blockchain()
image2 = None  # Initialize image2 as None

# Tkinter UI setup
root = tk.Tk()
root.title("Image Processor")

# Styling using the 'clam' theme
style = ttk.Style()
style.theme_use("clam")

# Creating a container frame for buttons
button_frame = ttk.Frame(root, padding=10)
button_frame.pack()

# Adding icons for buttons
select_icon = Image.open('select_icon.png').resize((25, 25))
select_photo = ImageTk.PhotoImage(select_icon)

process_icon = Image.open('process_icon.png').resize((25, 25))
process_photo = ImageTk.PhotoImage(process_icon)

fingerprint_icon = Image.open('fingerprint_icon.png').resize((25, 25))
fingerprint_photo = ImageTk.PhotoImage(fingerprint_icon)

# Select Image button
select_button = ttk.Button(button_frame, text="Select Image", command=select_image, image=select_photo, compound=tk.LEFT)
select_button.image = select_photo  # Retain reference to the image
select_button.pack(side=tk.LEFT, padx=10)

# Process Image button
process_button = ttk.Button(button_frame, text="Process Image", command=process_image, image=process_photo, compound=tk.LEFT)
process_button.image = process_photo  # Retain reference to the image
process_button.pack(side=tk.LEFT, padx=10)

# Check Fingerprint button
third_button = ttk.Button(button_frame, text="Check Fingerprint", command=check_image_for_fingerprint, image=fingerprint_photo, compound=tk.LEFT)
third_button.image = fingerprint_photo  # Retain reference to the image
third_button.pack(side=tk.LEFT, padx=10)

image_frame = tk.Frame(root, bd=2, relief=tk.SUNKEN)
image_frame.pack(padx=20, pady=(0, 10))

photo = None
img_label = tk.Label(image_frame)
img_label.pack()

status_label = tk.Label(root, text="No image loaded", bd=1, relief=tk.SUNKEN, anchor=tk.W)
status_label.pack(fill=tk.X, padx=20)

root.mainloop()



app = Flask(__name__)
@app.route('/chain', methods=['GET'])
def get_chain():
    chain_data = []
    for block in blockchain.chain:
        chain_data.append(block.__dict__)
    return json.dumps({"length": len(chain_data),
                       "chain": chain_data})

app.run(debug=True, port=3000)


