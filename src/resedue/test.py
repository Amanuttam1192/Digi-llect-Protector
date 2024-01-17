from hashlib import sha256
import tkinter as tk
from tkinter import filedialog
import json
import time
from PIL import Image, ImageTk
from flask import Flask

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
    """""
    we will be implementing an algorithm with a dynamic difficulty later on!
    """""

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
        imageB.save("newPepper.png")
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


def select_image():
    global image21
    file_path = filedialog.askopenfilename(initialdir="/Desktop", title="Select Image File",
                                           filetypes=(("Image files", "*.png;*.jpg;*.jpeg;*.gif"), ("All files", "*.*")))
    if file_path:
        image21 = Image.open(file_path)
        image21.thumbnail((300, 300))  # Resize image if needed
        
        # Update the label to display the selected image
        photo = ImageTk.PhotoImage(image21)
        image_label.config(image=photo)
        image_label.image = photo  # Keep a reference to the image to prevent garbage collection

def save_image():
    global image21
    if image21:
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=(("PNG files", "*.png"), ("All files", "*.*")))
        if file_path:
            image21.save(file_path)
            print("Image saved as", file_path)

def mineBlock(self):
        imageS = Image.open(self.unconfirmedImages)
        fingerPrint = LSB().decode_image(imageS)
        if not self.unconfirmedImages:
            return False
        if fingerPrint != self.seller.fingerprint:
            print("false")
            return False
        imageB = LSB().encode_image(image21, self.buyer.fingerprint)
        imageB.save("newPepper.png")
        lastBlock = self.lastBlock

        newBlock = Block(ID=lastBlock.ID + 1,
                         images=self.unconfirmedImages,
                         timestamp=time.time(),
                         previousHash=lastBlock.hash)
        proof = self.pOw(newBlock)
        self.add_block(newBlock, proof)

        self.unconfirmedImages = []
        return newBlock.ID

    # Flask code (starting from app.run...) remains the same

root = tk.Tk()
root.title("Image Selector")

image21 = None

select_button = tk.Button(root, text="Select Image", command=select_image)
select_button.pack(pady=10)

save_button = tk.Button(root, text="Save Image", command=save_image)
save_button.pack(pady=5)

image_label = tk.Label(root)
image_label.pack(padx=10, pady=10)

root.mainloop()

blockchain = Blockchain()
seller1 = User("Alice", "ALice17")
buyer1 = User("Bob", "Bob25")

app = Flask(__name__)

@app.route('/chain', methods=['GET'])
def get_chain():
    chain_data = []
    for block in blockchain.chain:
        chain_data.append(block.__dict__)
    return json.dumps({"length": len(chain_data),
                       "chain": chain_data})

app.run(debug=True, port=3000)


