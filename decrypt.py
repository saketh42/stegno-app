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