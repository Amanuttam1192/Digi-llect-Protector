from PIL import Image

# Open an image
image = Image.open("newPepper.png")

# Convert the image to grayscale (optional)
#image = image.convert("L")

# Get the pixel data as a list of grayscale values
pixel_data = list(image.getdata())

# Create a new image to display the bits
width, height = image.size
bit_image = Image.new("L", (width, height))

# Convert grayscale values to bits and set the corresponding pixel in the new image
bit_data = [int(format(pixel_value, '08b'), 2) for pixel_value in pixel_data]

bit_image.putdata(bit_data)

# Display the bits (convert the list to a string for easier viewing)
bit_string = ''.join(str(bit) for bit in bit_data)
print("Bits:", bit_string)

# Display the new image with the bits
newPepper.png.show()
