# RSA Steganography Tool

## Overview

This project is a Python-based steganography tool that combines RSA encryption with image steganography. It allows users to hide encrypted messages within image files, providing an extra layer of security through encryption and concealment.

## Features

- 🔐 RSA Key Generation
- 🖼️ Image-based Message Hiding
- 🔒 End-to-End Encryption
- 📤 Message Encoding
- 📥 Message Decoding

## How It Works

The tool uses a two-step process:
1. **Encryption**: Messages are first encrypted using RSA algorithm
2. **Steganography**: Encrypted messages are hidden within image pixel data

### Key Components

- `encrypt.py`: RSA key generation and encryption
- `decrypt.py`: Message decryption
- `encode.py`: Image steganography encoding
- `decode.py`: Image steganography decoding
- `main.py`: Interactive CLI

## Prerequisites

- Python 3.7+
- Pillow Library

## Installation

1. Clone the repository:
```bash
git clone https://github.com/saketh42/stegno-app.git
cd stegno-app
```

2. Install required dependencies:
```bash
pip install Pillow
```

## Usage

Run the main script:
```bash
python main.py
```

### Menu Options

1. Encode Message into Image
2. Decode Message from Image
3. Exit

## Example Workflow

1. Generate a key pair
2. Select an input image
3. Enter your secret message
4. The tool will create a new image with the hidden message
5. To decode, use the corresponding private key

## Security Notes

- Uses RSA for message encryption
- Hides encrypted message in least significant bits of image pixels
- Visually imperceptible image modification

## Limitations

- Message length is constrained by image size
- Supports text messages
- Requires careful private key management
