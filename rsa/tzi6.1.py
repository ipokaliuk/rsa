import random

# Pre generated primes
first_primes_list = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
                    31, 37, 41, 43, 47, 53, 59, 61, 67,
                    71, 73, 79, 83, 89, 97, 101, 103,
                    107, 109, 113, 127, 131, 137, 139,
                    149, 151, 157, 163, 167, 173, 179,
                    181, 191, 193, 197, 199, 211, 223,
                    227, 229, 233, 239, 241, 251, 257,
                    263, 269, 271, 277, 281, 283, 293,
                    307, 311, 313, 317, 331, 337, 347, 349]

def nBitRandom(n):
    return random.randrange(2**(n-1)+1, 2**n - 1)

def getLowLevelPrime(n):
    '''Generate a prime candidate divisible by first primes'''
    while True:
        # Obtain a random number
        pc = nBitRandom(n)

        # Test divisibility by pre-generated primes
        for divisor in first_primes_list:
            if pc % divisor == 0 and divisor**2 <= pc:
                break
        else:
            return pc

def isMillerRabinPassed(mrc):
    '''Run 20 iterations of Rabin Miller Primality test'''
    maxDivisionsByTwo = 0
    ec = mrc-1
    while ec % 2 == 0:
        ec >>= 1
        maxDivisionsByTwo += 1
    assert(2**maxDivisionsByTwo * ec == mrc-1)

    def trialComposite(round_tester):
        if pow(round_tester, ec, mrc) == 1:
            return False
        for i in range(maxDivisionsByTwo):
            if pow(round_tester, 2**i * ec, mrc) == mrc-1:
                return False
        return True

    # Set number of trials here
    numberOfRabinTrials = 20
    for i in range(numberOfRabinTrials):
        round_tester = random.randrange(2, mrc)
        if trialComposite(round_tester):
            return False
    return True

def generate_large_prime(n):
    while True:
        prime_candidate = getLowLevelPrime(n)
        if not isMillerRabinPassed(prime_candidate):
            continue
        else:
            return prime_candidate

# Функція для знаходження найбільшого спільного дільника (НСД)
def gcd_extended(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = gcd_extended(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

# Функція для перевірки простоти числа
def is_prime(num):
    if num < 2:
        return False
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True

# Генерація великих простих чисел p і q
p = generate_large_prime(1024)
q = generate_large_prime(1024)

# Обчислення n і m
n = p * q
m = (p - 1) * (q - 1)

# Вибір числа d взаємно простого з m
d = 17
gcd, x, y = gcd_extended(d, m)
while gcd != 1:
    d += 1
    gcd, x, y = gcd_extended(d, m)

# Обчислення числа e
e = x % m
if e < 0:
    e += m

# Функція для шифрування
def encrypt(message, e, n):
    return [pow(ord(char), e, n) for char in message]

# Функція для дешифрування
def decrypt(ciphertext, d, n):
    return ''.join([chr(pow(char, d, n)) for char in ciphertext])

# Функція для шифрування файлу
def encrypt_file(input_file, output_file, e, n):
    with open(input_file, 'r', encoding='utf-8') as f:
        message = f.read()
    ciphertext = encrypt(message, e, n)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(' '.join(map(str, ciphertext)))

# Функція для дешифрування файлу
def decrypt_file(input_file, output_file, d, n):
    with open(input_file, 'r', encoding='utf-8') as f:
        ciphertext = list(map(int, f.read().split()))
    decrypted_message = decrypt(ciphertext, d, n)
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(decrypted_message)

# Тестування алгоритму з файлами
encrypt_file('example.txt', 'encrypted.txt', e, n)
decrypt_file('encrypted.txt', 'decrypted.txt', d, n)
