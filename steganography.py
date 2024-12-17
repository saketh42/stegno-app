from PIL import Image
import os

class SteganographyTool:
    @staticmethod
    def encode_image(input_image_path, secret_message, output_image_path):
        """
        Hide a secret message inside an image
        
        Args:
            input_image_path (str): Path to the original image
            secret_message (str): Message to hide
            output_image_path (str): Path to save the modified image
        """
        # Open the image
        image = Image.open(input_image_path)
        
        # Convert image to RGB mode to ensure compatibility
        image = image.convert('RGB')
        
        # Convert message to binary
        binary_message = ''.join(format(ord(char), '08b') for char in secret_message)
        
        # Add message length and delimiter
        binary_message = f"{len(secret_message):016b}" + binary_message + '1111111111111110'
        
        # Check if the message fits in the image
        width, height = image.size
        max_bytes = width * height * 3 // 8  # 3 channels, 1 bit per channel
        if len(binary_message) // 8 > max_bytes:
            raise ValueError("Message too large for this image")
        
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
        print(f"Message encoded in {output_image_path}")

    @staticmethod
    def decode_image(image_path):
        """
        Extract hidden message from an image
        
        Args:
            image_path (str): Path to the image with hidden message
        
        Returns:
            str: Decoded secret message
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
        
        # Extract actual message
        binary_message = binary_message[16:-16]
        
        # Convert binary to text
        message = ''
        for i in range(0, message_length * 8, 8):
            byte = binary_message[i:i+8]
            message += chr(int(byte, 2))
        
        return message

def main():
    while True:
        print("\n--- Steganography Tool ---")
        print("1. Encode Message")
        print("2. Decode Message")
        print("3. Exit")
        
        choice = input("Enter your choice (1/2/3): ")
        
        if choice == '1':
            input_image = input("Enter input image path: ")
            output_image = input("Enter output image path: ")
            message = input("Enter message to hide: ")
            
            try:
                SteganographyTool.encode_image(input_image, message, output_image)
                print("Message encoded successfully!")
            except Exception as e:
                print(f"Encoding error: {e}")
        
        elif choice == '2':
            input_image = input("Enter image with hidden message: ")
            
            try:
                message = SteganographyTool.decode_image(input_image)
                print(f"Decoded Message: {message}")
            except Exception as e:
                print(f"Decoding error: {e}")
        
        elif choice == '3':
            print("Exiting...")
            break
        
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()