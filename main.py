from src.encrypt import generate_keypair
from src.encoding import encode_image
from src.decoding import decode_image

def main():
    while True:
        print("\n--- RSA Steganography Tool ---")
        print("1. Generate Keys")
        print("2. Encode Message")
        print("3. Decode Message")
        print("4. Exit")
        
        choice = input("Enter your choice (1/2/3/4): ")
        
        if choice == '1':
            # Generating key pair
            public_key, private_key = generate_keypair()
            print("Public Key (for encryption):", public_key)
            print("Private Key (for decryption):", private_key)


        # Encoding
        elif choice == '2':
            # Input for the image and the msg
            input_image = input("Enter input image path: ")
            message = input("Enter message to hide: ")
            e = int(input("Enter public key e: "))
            n = int(input("Enter public key n: "))
            public_key = (e, n)

            try:
                encode_image(input_image, message, public_key, 'output.png')            # output.png is the output file name

            except Exception as e:
                print(f"Encoding error: {e}")
        
        # Decoding
        elif choice == '3':
            # Input for the image to decode
            input_image = input("Enter image with hidden message: ")
            
            # Prompt for private key components
            d = int(input("Enter private key d: "))
            n = int(input("Enter private key n: "))
            private_key = (d, n)
            
            try:
                message = decode_image(input_image, private_key)
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