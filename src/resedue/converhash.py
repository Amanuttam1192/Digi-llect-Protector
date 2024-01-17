import hashlib

# Function to calculate the SHA-256 hash of a list of numbers
def calculate_sha256_hash(numbers):
    # Convert the list to a string representation
    numbers_str = ','.join(map(str, numbers))
    
    # Convert the string to bytes (UTF-8 encoding)
    numbers_bytes = numbers_str.encode('utf-8')
    
    # Calculate the SHA-256 hash
    sha256_hash = hashlib.sha256(numbers_bytes).hexdigest()
    
    return sha256_hash

# Custom list of numbers
custom_numbers = [42, 123, 890]

# Calculate the SHA-256 hash of the custom numbers
sha256_hash = calculate_sha256_hash(custom_numbers)

# Display the result
print("Custom Numbers:", custom_numbers)
print("SHA-256 Hash:", sha256_hash)
