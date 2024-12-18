from PIL import Image
from encrypt import encrypt

def encode_image(input_image_path, secret_message, public_key, output_image_path):
    """
    Encrypt and hide a secret message inside an image
    
    Args:
        input_image_path (str): Path to the original image
        secret_message (str): Message to hide
        public_key (tuple): RSA public key
        output_image_path (str): Path to save the modified image
    """
    # First encrypt the message with RSA
    encrypted_message = encrypt(secret_message, public_key)
    
    # Convert encrypted message to string for steganography
    encrypted_str = ','.join(map(str, encrypted_message))
    
    # Open the image
    image = Image.open(input_image_path)
    
    # Convert image to RGB mode to ensure compatibility
    image = image.convert('RGB')
    
    # Convert encrypted message to binary
    binary_message = ''.join(format(ord(char), '08b') for char in encrypted_str)
    
    # Add message length and delimiter
    binary_message = f"{len(encrypted_str):016b}" + binary_message + '1111111111111110'
    
    # Check if the message fits in the image
    width, height = image.size
    max_bytes = width * height * 3 // 8  # 3 channels, 1 bit per channel
    if len(binary_message) // 8 > max_bytes:
        raise ValueError("Encrypted message too large for this image")
    
    # Create a copy of the image pixels
    pixels = list(image.getdata())
    
    # Encoding process
    encoded_pixels = []
    message_index = 0
    
    for pixel in pixels:
        # Unpack RGB values
        r, g, b = pixel
        
        # If we have more message bits to encode
        if message_index < len(binary_message):
            # Encode in Red channel
            r = r & 0xFE | int(binary_message[message_index])
            message_index += 1
            
            # If more bits, encode in Green channel
            if message_index < len(binary_message):
                g = g & 0xFE | int(binary_message[message_index])
                message_index += 1
            
            # If more bits, encode in Blue channel
            if message_index < len(binary_message):
                b = b & 0xFE | int(binary_message[message_index])
                message_index += 1
        
        encoded_pixels.append((r, g, b))
    
    # Create a new image with encoded pixels
    encoded_image = Image.new(image.mode, image.size)
    encoded_image.putdata(encoded_pixels)
    
    # Save the encoded image
    encoded_image.save(output_image_path)
    print(f"Encrypted message encoded in {output_image_path}")