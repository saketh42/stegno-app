def decrypt(cipher, private_key):
    # private exponent and modulus
    d, n = private_key

    # Decrypt each number back to character
    message = ''.join(
        chr(
            pow(char, d, n)  # Decrypt each character using RSA: m = c^d mod n
        )   
        for char in cipher  # Iterate over each encrypted character in the cipher
    )

    return message