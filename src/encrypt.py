import random

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def find_primes(start, end):
    return [p for p in range(start, end) if is_prime(p)]

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def mod_inverse(e, phi):
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

def encrypt(message, public_key):
    e, n = public_key
    # Convert message to list of character codes
    cipher = []
    for char in message:
        # Encrypt each character
        cipher.append(pow(ord(char), e, n))
    return cipher

def generate_keypair(p=None, q=None):
    # If primes not provided, choose randomly
    if p is None or q is None:
        primes = find_primes(100, 500)
        p = primes[random.randint(0, len(primes)//2)]
        q = primes[random.randint(len(primes)//2, len(primes)-1)]
    
    # Compute n and phi
    n = p * q
    phi = (p-1) * (q-1)
    
    # Choose e (public key)
    e = random.randrange(1, phi)
    while gcd(e, phi) != 1:
        e = random.randrange(1, phi)
    
    # Compute private key
    d = mod_inverse(e, phi)
    
    return ((e, n), (d, n))