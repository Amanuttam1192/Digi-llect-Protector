from PIL import Image

class LSB:
    def decode_image(self, img):
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

# Load the image to check
image_path_to_check = "newPepper.png"
image_to_check = Image.open(image_path_to_check)

# Create an instance of the LSB class
lsb_decoder = LSB()

hidden_message = lsb_decoder.decode_image(image_to_check)

import re

valid_fingerprint_format = re.match(r"^[a-f0-9]{64}$", hidden_message)

if valid_fingerprint_format:
    print("The image contains a valid digital fingerprint.")
    print("Fingerprint:", hidden_message)
else:
    print("The image does not contain a valid digital fingerprint.")
