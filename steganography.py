from PIL import Image
import random

class RSASteganographyTool:
    @staticmethod
    def is_prime(n):
        """Check if a number is prime"""
        if n < 2:
            return False
        for i in range(2, int(n**0.5) + 1):
            if n % i == 0:
                return False
        return True

    @staticmethod
    def find_primes(start, end):
        """Find prime numbers in a range"""
        return [p for p in range(start, end) if RSASteganographyTool.is_prime(p)]

    @staticmethod
    def gcd(a, b):
        """Calculate Greatest Common Divisor"""
        while b:
            a, b = b, a % b
        return a

    @staticmethod
    def mod_inverse(e, phi):
        """Calculate modular multiplicative inverse"""
        def extended_gcd(a, b):
            if a == 0:
                return b, 0, 1
            else:
                gcd, x, y = extended_gcd(b % a, a)
                return gcd, y - (b // a) * x, x

        gcd, x, _ = extended_gcd(e, phi)
        if gcd != 1:
            raise ValueError('Modular inverse does not exist')
        else:
            return x % phi

    @staticmethod
    def generate_keypair(p=None, q=None):
        """
        Generate RSA public and private keys
        
        Args:
            p (int, optional): First prime number
            q (int, optional): Second prime number
        
        Returns:
            tuple: ((public_key, n), (private_key, n))
        """
        # If primes not provided, choose randomly
        if p is None or q is None:
            primes = RSASteganographyTool.find_primes(100, 500)
            p = primes[random.randint(0, len(primes)//2)]
            q = primes[random.randint(len(primes)//2, len(primes)-1)]
        
        # Compute n and phi
        n = p * q
        phi = (p-1) * (q-1)
        
        # Choose e (public key)
        e = random.randrange(1, phi)
        while RSASteganographyTool.gcd(e, phi) != 1:
            e = random.randrange(1, phi)
        
        # Compute private key
        d = RSASteganographyTool.mod_inverse(e, phi)
        
        return ((e, n), (d, n))

    @staticmethod
    def encrypt(message, public_key):
        """
        Encrypt message using RSA public key
        
        Args:
            message (str): Message to encrypt
            public_key (tuple): (e, n)
        
        Returns:
            list: Encrypted message as list of integers
        """
        e, n = public_key
        # Convert message to list of character codes
        cipher = []
        for char in message:
            # Encrypt each character
            cipher.append(pow(ord(char), e, n))
        return cipher

    @staticmethod
    def decrypt(cipher, private_key):
        """
        Decrypt message using RSA private key
        
        Args:
            cipher (list): Encrypted message
            private_key (tuple): (d, n)
        
        Returns:
            str: Decrypted message
        """
        d, n = private_key
        # Decrypt each number back to character
        message = ''.join(chr(pow(char, d, n)) for char in cipher)
        return message

    @staticmethod
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
        encrypted_message = RSASteganographyTool.encrypt(secret_message, public_key)
        
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

    @staticmethod
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
        return RSASteganographyTool.decrypt(encrypted_message, private_key)

def main():
    while True:
        print("\n--- RSA Steganography Tool ---")
        print("1. Generate Key Pair")
        print("2. Encode Message")
        print("3. Decode Message")
        print("4. Exit")
        
        choice = input("Enter your choice (1/2/3/4): ")
        
        if choice == '1':
            # Generate key pair
            public_key, private_key = RSASteganographyTool.generate_keypair()
            print("Public Key:", public_key)
            print("Private Key:", private_key)
        
        elif choice == '2':
            # Generate key pair first
            public_key, private_key = RSASteganographyTool.generate_keypair()
            
            input_image = input("Enter input image path: ")
            output_image = input("Enter output image path: ")
            message = input("Enter message to hide: ")
            
            try:
                RSASteganographyTool.encode_image(input_image, message, public_key, output_image)
                print("Encrypted message encoded successfully!")
                print("Public Key (for decryption):", public_key)
                print("Private Key (for decryption):", private_key)
            except Exception as e:
                print(f"Encoding error: {e}")
        
        elif choice == '3':
            input_image = input("Enter image with hidden message: ")
            # Prompt for private key components
            d = int(input("Enter private key d: "))
            n = int(input("Enter private key n: "))
            private_key = (d, n)
            
            try:
                message = RSASteganographyTool.decode_image(input_image, private_key)
                print(f"Decrypted Message: {message}")
            except Exception as e:
                print(f"Decoding error: {e}")
        
        elif choice == '4':
            print("Exiting...")
            break
        
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()