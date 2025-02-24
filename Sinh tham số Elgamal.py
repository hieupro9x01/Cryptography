


import random
import math
import time

class ElGamalPrivateKey(object):
    def __init__(self, p=None, g=None, x=None, k=0):
        self.p = p
        self.g = g
        self.x = x
        self.k = k

class ElGamalPublicKey(object):
    def __init__(self, p=None, g=None, h=None, k=0):
        self.p = p
        self.g = g
        self.h = h
        self.k = k

def is_prime(num, k=5):
    # Kiểm tra xem một số có phải là số nguyên tố hay không bằng thuật toán Miller-Rabin.
    if num == 2 or num == 3:
        return True
    if num <= 1 or num % 2 == 0:
        return False

    r, s = 0, num - 1
    while s % 2 == 0:
        r += 1
        s //= 2

    for _ in range(k):
        a = random.randint(2, num - 1)
        x = pow(a, s, num)

        if x == 1 or x == num - 1:
            continue

        for _ in range(r - 1):
            x = pow(x, 2, num)
            if x == num - 1:
                break
        else:
            return False

    return True

def is_subprime(q, p):
    # Kiểm tra xem q có phải là số nguyên tố con của p - 1 hay không.
    if q <= 1 or q >= p:
        return False
    
    a, b = p - 1, q
    while b:
        a, b = b, a % b
    
    return a == 1

###### Thực hiện thuật toán sinh số nguyên tố của Maurer.
def generate_prime_q_r(k, L, M):
    # Sinh số nguyên tố q và số ngẫu nhiên r
    start_time = time.time()

    if k < 2:
        raise ValueError("Độ dài bit phải ít nhất là 2.")
    

    while True:
        q = random.getrandbits(k)
        q |= (1 << (k - 1)) | 1  # Kiểm tra q sinh ra đúng độ dài k bit và đảm bảo giá trị sinh ra là số lẻ 
        if is_prime(q):
            break

    print(f"Generated random q: {q}")

    while True:
        s = random.random() # nằm (0,1)
        r = 2 ** (s - 1)

        if k - r * k > M:
            break

    print(f"Generated random r: {r}")

    return q, r

def generate_prime_p(q, r, k):
    # Sinh số nguyên tố p từ q, r và k.
    t = 2 ** (k - 1) // (2 * q)

    start_time = time.time()
    while True:
        R = random.randint(t, 2 * t)
        p0 = 2 * R * q + 1
        if is_prime(p0):
            break

    print(f"Generated random p0: {p0}")

    return p0

def generate_prime_q_p(q, p0, k):
    start_time = time.time()
    x = random.randint(2 ** (k - 1), 2 ** k)
    t = x // (2 * p0 * q)
    while True:
        if (2 * t * p0 * q) + 1 > 2 ** k:
            t = 2 ** (k - 1) // (2 * p0 * q)
        p = (2 * t * p0 * q) + 1
        a = random.randint(2, p - 2)
        z = pow(a, (2 * t * q), p )
        if pow(z, p0, p) == 1 and math.gcd(z - 1, p) == 1:
            break
        else:
            t = t + 1
            if (2 * t * p0 * q) + 1 > 2 ** k:
                t = 2 ** (k - 1) // (2 * p0 * q)
            p = (2 * t * p0 * q) + 1
            a = random.randint(2, p - 2)
            z = pow(a, (2 * t * q), p )
            if pow(z, p0, p) == 1 and math.gcd(z - 1, p) == 1:
                break

    print(f"Generated random p: {p}")
    print(f"Generated random a: {a}")

    return p, a        


def generate_g(p, q):
    # Sinh số nguyên g.
    start_time = time.time()

    e = (p - 1) // q
    p1 = p - 2

    g = 1
    while g == 1:
        a = random.randrange(2, p1)
        g = pow(a, e, p)

    print(f"Generated random g: {g}")
    print(f"Generated random e: {e}")
    return g

def kiem_tra_tham_so_pq_fips(p, q):
    # Kiểm tra các tham số theo tiêu chuẩn FIPS 186-3.
    start_time = time.time()

    nlen_p = len(bin(p)) - 2
    nlen_q = len(bin(q)) - 2
    if not (2048 <= nlen_p <= 3072 and 224 <= nlen_q <= 256):
        return False, "FIPS 186-3: Độ dài của p và q không đáp ứng."

    if not (is_prime(q) and is_prime(p)):
        return False, "FIPS 186-3: Ít nhất một trong số p và q không phải là số nguyên tố."
        
    if not is_subprime(q,p - 1):
        return False, "FIPS 186-3: q không là số nguyên tố con của p - 1."

    end_time = time.time()
    print(f"Thời gian kiểm tra tham số: {end_time - start_time} giây")
    return True, "Các tham số đáp ứng tiêu chuẩn FIPS 186-3."

def generate_keys(q, r, k):
    # Sinh khóa công khai và khóa riêng tư ElGamal.
    start_time = time.time()
    p0 = generate_prime_p(q, r, (k//2) + 1)
    p, a = generate_prime_q_p(q, p0, k)
    g = generate_g(p, q)
    x = random.randint(1, p - 1)
    h = pow(g, x, p)

    end_time = time.time()
    print(f"Thời gian sinh khóa: {end_time - start_time} giây")

    if p and q and g:
        print(f"\np = {p}\nq = {q}\ng = {g}")
        print(f"Certificate: {(p, q, a)}")
        kq, thong_bao = kiem_tra_tham_so_pq_fips(p, q)
        print(f"\nKiểm tra tham số theo tiêu chuẩn FIPS 186-3: {'Successful (Thành công) ' if kq else 'Failed (Thất bại)'}")
        print(f"Thông báo: {thong_bao}")

    publicKey = ElGamalPublicKey(p, g, h, k)
    privateKey = ElGamalPrivateKey(p, g, x, k)

    return {'privateKey': privateKey, 'publicKey': publicKey}

def elgamal_encrypt(plaintext, public_key):
    # Mã hóa ElGamal.
    start_time = time.time()

    p, g, h = public_key.p, public_key.g, public_key.h
    k = public_key.k
    y = random.randint(1, p - 1)
    c1 = pow(g, y, p)
    s = pow(h, y, p)
    c2 = (plaintext * s) % p

    end_time = time.time()
    print(f"Thời gian mã hóa: {end_time - start_time} giây")

    return (c1, c2)

def elgamal_decrypt(ciphertext, private_key):
    # Giải mã ElGamal.
    start_time = time.time()

    p, x = private_key.p, private_key.x
    c1, c2 = ciphertext
    s = pow(c1, x, p)
    s_inv = pow(s, -1, p)
    plaintext = (c2 * s_inv) % p

    end_time = time.time()
    print(f"Thời gian giải mã: {end_time - start_time} giây")

    return plaintext

if __name__ == "__main__":

    bit_length_p = int(input(f"Nhập độ dài bit của p (2048 - 3072): "))
    bit_length_q = int(input(f"Nhập độ dài bit của q (224 - 256): "))

    q, r = generate_prime_q_r(bit_length_q, 2**16, 20)

        
    keys = generate_keys(q, r, bit_length_p)
    print("\nElGamal Key Pair:")
    print("Private Key:")
    print(f"  p = {keys['privateKey'].p}")
    print(f"  g = {keys['privateKey'].g}")
    print(f"  x = {keys['privateKey'].x}")
    print("\nPublic Key:")
    print(f"  p = {keys['publicKey'].p}")
    print(f"  g = {keys['publicKey'].g}")
    print(f"  h = {keys['publicKey'].h}")

    plaintext = int(input("Nhập thông điệp cần mã hóa: "))
    ciphertext = elgamal_encrypt(plaintext, keys['publicKey'])
    print(f"Bản mã ElGamal: {ciphertext}")

    decrypted_text = elgamal_decrypt(ciphertext, keys['privateKey'])
    print(f"Thông điệp giải mã: {decrypted_text}")





