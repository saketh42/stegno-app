from src.encrypt import generate_keypair
from src.encoding import encode_image
from src.decoding import decode_image

def main():
    while True:
        print("\n--- RSA Steganography Tool ---")
        print("1. Encode Message")
        print("2. Decode Message")
        print("3. Exit")
        
        choice = input("Enter your choice (1/2/3): ")
        

        
        if choice == '1':
            # Generate key pair first
            public_key, private_key = generate_keypair()
            
            input_image = input("Enter input image path: ")
            message = input("Enter message to hide: ")
            
            try:
                encode_image(input_image, message, public_key, 'output.png')
                print("Private Key (for decryption):", private_key)
            except Exception as e:
                print(f"Encoding error: {e}")
        
        elif choice == '2':
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
        
        elif choice == '3':
            print("Exiting...")
            break
        
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()