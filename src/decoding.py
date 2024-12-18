from PIL import Image
from src.decrypt import decrypt

def decode_image(image_path, private_key):
    """
    Extract and decrypt hidden message from an image
    
    Args:
        image_path (str): Path to the image with hidden message
        private_key (tuple): RSA private key
    
    Returns:
        str: Decrypted original message
    """
    # Open the image
    image = Image.open(image_path)
    image = image.convert('RGB')
    
    # Extract binary data
    pixels = list(image.getdata())
    binary_message = ''
    
    # Decoding process
    for pixel in pixels:
        # Extract LSB from each channel
        r, g, b = pixel
        binary_message += str(r & 1)
        binary_message += str(g & 1)
        binary_message += str(b & 1)
        
        # Check for message delimiter
        if '1111111111111110' in binary_message:
            break
    
    # Extract message length
    message_length = int(binary_message[:16], 2)
    
    # Extract actual encrypted message
    binary_message = binary_message[16:-16]
    
    # Convert binary to encrypted text
    encrypted_str = ''
    for i in range(0, message_length * 8, 8):
        byte = binary_message[i:i+8]
        encrypted_str += chr(int(byte, 2))
    
    # Convert back to list of integers
    encrypted_message = list(map(int, encrypted_str.split(',')))
    
    # Decrypt the message
    return decrypt(encrypted_message, private_key)