# Steganography Project Report

## 1. Project Overview

### 1.1 Project Title
Least Significant Bit (LSB) Image Steganography Tool

### 1.2 Objective
Develop a Python-based steganography tool that can hide and retrieve secret messages within digital images without visibly altering the image's appearance.

## 2. Technical Specifications

### 2.1 Implementation Language
- Python 3.x
- Libraries Used:
  - Pillow (PIL) for image processing

### 2.2 Supported Image Formats
- PNG
- JPEG
- BMP

## 3. Steganography Mechanism

### 3.1 Least Significant Bit (LSB) Technique
The core of the steganography implementation is the Least Significant Bit (LSB) technique, which involves modifying the least significant bit of each color channel in an image pixel.

#### Key Characteristics:
- Modifies only the least significant bit of pixel color values
- Minimal visual impact on the original image
- Allows embedding of hidden data without perceptible changes

### 3.2 Encoding Process
1. Convert the secret message to binary
2. Add message length and delimiter
3. Iteratively modify pixel color channels' least significant bits
4. Store modified pixels in a new image

#### Encoding Steps:
- Message length encoded in first 16 bits
- Message converted to 8-bit binary representation
- Special delimiter ('1111111111111110') added to mark message end
- LSB of Red, Green, and Blue channels modified sequentially

### 3.3 Decoding Process
1. Extract least significant bits from pixel color channels
2. Reconstruct binary message
3. Extract message length
4. Convert binary to text

## 4. Key Functions

### 4.1 `encode_image()`
```python
@staticmethod
def encode_image(input_image_path, secret_message, output_image_path):
    # Image opening and conversion
    image = Image.open(input_image_path).convert('RGB')
    
    # Binary message preparation
    binary_message = ''.join(format(ord(char), '08b') for char in secret_message)
    binary_message = f"{len(secret_message):016b}" + binary_message + '1111111111111110'
    
    # Pixel modification and encoding
    pixels = list(image.getdata())
    encoded_pixels = []
    message_index = 0
    
    for pixel in pixels:
        r, g, b = pixel
        
        # Embed message bits in pixel channels
        if message_index < len(binary_message):
            r = r & 0xFE | int(binary_message[message_index])
            message_index += 1
            
            if message_index < len(binary_message):
                g = g & 0xFE | int(binary_message[message_index])
                message_index += 1
            
            if message_index < len(binary_message):
                b = b & 0xFE | int(binary_message[message_index])
                message_index += 1
        
        encoded_pixels.append((r, g, b))
    
    # Create and save encoded image
    encoded_image = Image.new(image.mode, image.size)
    encoded_image.putdata(encoded_pixels)
    encoded_image.save(output_image_path)
```

### 4.2 `decode_image()`
```python
@staticmethod
def decode_image(image_path):
    # Image processing
    image = Image.open(image_path).convert('RGB')
    pixels = list(image.getdata())
    binary_message = ''
    
    # Bit extraction
    for pixel in pixels:
        r, g, b = pixel
        binary_message += str(r & 1)
        binary_message += str(g & 1)
        binary_message += str(b & 1)
        
        # Check for message delimiter
        if '1111111111111110' in binary_message:
            break
    
    # Message reconstruction
    message_length = int(binary_message[:16], 2)
    binary_message = binary_message[16:-16]
    
    # Binary to text conversion
    message = ''.join(chr(int(binary_message[i:i+8], 2)) for i in range(0, message_length * 8, 8))
    
    return message
```

## 5. Limitations and Considerations

### 5.1 Technical Limitations
- Message size restricted by image dimensions
- Only supports specific image formats
- No built-in encryption
- Potential detectability with advanced steganography analysis

### 5.2 Performance Constraints
- Linear time complexity O(n) for encoding and decoding
- Memory usage proportional to image size

## 6. Potential Improvements
1. Add encryption layer
2. Support more image formats
3. Implement advanced hiding techniques
4. Add error detection and correction mechanisms

## 7. Security Considerations
- Not recommended for highly sensitive information
- Easily detectable by specialized steganography detection tools
- Provides basic message concealment, not cryptographic security

## 8. Conclusion
The implemented steganography tool demonstrates a basic yet functional approach to hiding messages within digital images using the Least Significant Bit technique.

## 9. References
- Wayner, P. (2002). Disappearing Cryptography: Information Hiding: Steganography & Watermarking
- Fridrich, J. (2009). Steganography in Digital Media: Principles, Algorithms, and Applications