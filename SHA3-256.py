
# import hashlib
# from cryptography.hazmat.backends import default_backend
# from cryptography.hazmat.primitives import hashes, serialization
# from cryptography.hazmat.primitives.asymmetric import rsa, padding

# def generate_key_pair(file_prefix):
#     # Kiểm tra sự tồn tại của khóa bí mật
#     try:
#         with open(f"{file_prefix}_private_key.pem", "rb") as f:
#             private_key = serialization.load_pem_private_key(
#                 f.read(),
#                 password=None,
#                 backend=default_backend()
#             )
#     except FileNotFoundError:
#     # Tạo khóa bí mật mới nếu không tồn tại
#         private_key = rsa.generate_private_key(
#             public_exponent=65537,
#             key_size=2048,
#             backend=default_backend()
#         )

#         private_pem = private_key.private_bytes(
#             encoding=serialization.Encoding.PEM,
#             format=serialization.PrivateFormat.PKCS8,
#             encryption_algorithm=serialization.NoEncryption()
#         )

#         with open(f"{file_prefix}_private_key.pem", "wb") as f:
#             f.write(private_pem)
#     # Tạo khóa công khai từ khóa bí mật
#     public_key = private_key.public_key()

#     public_pem = public_key.public_bytes(
#         encoding=serialization.Encoding.PEM,
#         format=serialization.PublicFormat.SubjectPublicKeyInfo
#     )

#     with open(f"{file_prefix}_public_key.pem", "wb") as f:
#         f.write(public_pem)

#     return public_key, private_key

# def sign_message(private_key, message):
#     hashed_message = hashlib.sha3_256(message).digest()

#     signature = private_key.sign(
#         hashed_message,
#         padding.PSS(
#             mgf=padding.MGF1(hashes.SHA3_256()),
#             salt_length=padding.PSS.MAX_LENGTH
#         ),
#         hashes.SHA3_256()
#     )

#     with open("signature.bin", "wb") as f:
#         f.write(signature)

#     print("Giá trị băm trước khi ký:", hashlib.sha3_256(message).hexdigest())
#     print("Chữ ký điện tử:", signature)

#     return signature

# def verify_signature(public_key, signature, message):
#     hashed_message = hashlib.sha3_256(message).digest()

#     try:
#         public_key.verify(
#             signature,
#             hashed_message,
#             padding.PSS(
#                 mgf=padding.MGF1(hashes.SHA3_256()),
#                 salt_length=padding.PSS.MAX_LENGTH
#             ),
#             hashes.SHA3_256()
#         )
#         print("Chữ ký hợp lệ. Thông điệp toàn vẹn.")
#         return True
#     except Exception as e:
#         print(f"Lỗi xác minh chữ ký: {e}")
#         return False

# # Bước 1: Sử dụng khóa bí mật A để tạo chữ ký điện tử
# public_key_A, private_key_A = generate_key_pair("A")

# # Nhập thông điệp từ màn hình
# message_to_sign = input("Nhập thông điệp muốn ký số: ").encode()

# # Tạo chữ ký điện tử cho thông điệp
# signature_A = sign_message(private_key_A, message_to_sign)

# # Bước 2: Sử dụng khóa công khai A để xác minh chữ ký
# is_valid = verify_signature(public_key_A, signature_A, message_to_sign)

# if is_valid:
#     print("Chữ ký A thành công.")
# else:
#     print("Chữ ký A không hợp lệ.")

# # Bước 3: Mô phỏng quá trình B nhận được thông điệp từ A và thay đổi thông điệp
# received_message_B = message_to_sign
# received_signature_B = signature_A
# modified_message_B = input("Nhập thông điệp mới: ").encode()

# # Hiển thị giá trị băm của thông điệp mới
# print("Giá trị băm của thông điệp mới:", hashlib.sha3_256(modified_message_B).hexdigest())

# # Bước 4: B sử dụng khóa công khai A để xác minh chữ ký với thông điệp thay đổi
# is_valid_modified_B = verify_signature(public_key_A, received_signature_B, modified_message_B)

# if is_valid_modified_B:
#     print("Chữ ký B trên thông điệp thay đổi là hợp lệ.")
# else:
#     print("Chữ ký B trên thông điệp thay đổi không hợp lệ.")


# p = 21765276232179136398377468141495420548863341987560946206017796842974460752233040487133898337172264163563486889094043899207248016432042637956915784883971213686873694366815794807632708316204202128023899544086597149430594547669196446097021391104575445432753820185396446764650773556643775757507168333170970306964961071980953872449766437983796771308762272484211528173030048329038564683984284582194814821425430660434832413472165294389297542540564567518983199308330114132470135820459453031355881581086908430146610953922092057385765207916185976275697010407634377417939419574058005820654708818272769665710571548388459883509281

# length_of_p_binary = len(bin(p)) - 2  # Trừ đi 2 để loại bỏ tiền tố '0b'

# print(f"Chiều dài của biểu diễn nhị phân của p là: {length_of_p_binary} bit")

from sympy import isprime

def kiem_tra_so_nguyen_to(p, q):
    if isprime(p):
        print(f"{p} là số nguyên tố.")
    else:
        print(f"{p} không là số nguyên tố.")

    if isprime(q):
        print(f"{q} là số nguyên tố.")
    else:
        print(f"{q} không là số nguyên tố.")

# Sử dụng hàm kiểm tra
p = 5091409619846078468437834005948486530453413512178780847279435490002955669197766770315099425840376154567404844310537516677176845610937350385493098521486588041027632766646165546299694277400654063933982295878227569076321799144641005353885038359966791322946518776209736244753269949563415460641380116843017949202676915596788856219535844554042384849687941398074401667285487411527867495010324304457364394015920908356937730847947563500741483280513228275205397489243037066360279221074010388036611538665519864177622561513226910397375457691781574808089397400737600582989399069975511434978550353652027264316100026283693061324637954561472227913839649850764356871104784618540218033440824684843263633259078743689020792766262080752775141550963211437053490158472429963554855489984126520265394021009540993426756815338642343275261371235561670977750172021762016338516941473716919010032360526960058570473534540180937804221423584106474026775066993
q = 83687114414523962972558915322984087246756953803561151430746425733376067798999

length_of_p_binary = len(bin(p)) - 2  # Trừ đi 2 để loại bỏ tiền tố '0b'
length_of_q_binary = len(bin(q)) - 2  # Trừ đi 2 để loại bỏ tiền tố '0b'
print(f"Chiều dài của biểu diễn nhị phân của p là: {length_of_p_binary} bit")
print(f"Chiều dài của biểu diễn nhị phân của q là: {length_of_q_binary} bit")

kiem_tra_so_nguyen_to(p, q)

import random

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

def kiem_tra_tham_so_pq_fips(p, q):
    # Kiểm tra các tham số theo tiêu chuẩn FIPS 186-3.

    nlen_p = len(bin(p)) - 2
    nlen_q = len(bin(q)) - 2
    if not (2048 <= nlen_p <= 3072 and 224 <= nlen_q <= 256):
        return False, "FIPS 186-3: Độ dài của p và q không đáp ứng."

    if not (is_prime(q) and is_prime(p)):
        return False, "FIPS 186-3: Ít nhất một trong số p và q không phải là số nguyên tố."
        
    if not is_subprime(q,p - 1):
        return False, "FIPS 186-3: q không là số nguyên tố con của p - 1."

    return True, "Các tham số đáp ứng tiêu chuẩn FIPS 186-3."

if p and q:
    kq, thong_bao = kiem_tra_tham_so_pq_fips(p, q)
    print(f"\nKiểm tra tham số theo tiêu chuẩn FIPS 186-3: {'Successful (Thành công) ' if kq else 'Failed (Thất bại)'}")
    print(f"Thông báo: {thong_bao}")

# from Crypto.Util import number

# def sinhq(k):
#     return number.getPrime(k)

# def maurer(k):
#     while True:
#         q = sinhq(k)
#         q2 = 2 * q
#         k1 = 2**(k - 1)
#         t = 2 * k1

#         while True:
#             R = number.getRandomRange(t, 2 * t)
#             R2 = 2 * R
#             p = 2 * R * q + 1
#             p1 = p - 1
#             a = number.getRandomRange(2, p - 2)
#             w = pow(a, p1, p)
#             tmp = pow(a, R2, p)

#             if tmp == 1:
#                 tmp = p1
#             else:
#                 tmp -= 1

#             if number.GCD(tmp, p) == 1 and pow(tmp, q, p) == 1:
#                 return p

# def sinh_p_qn(l, n):
#     if not (2048 <= l <= 3072) or not (224 <= n <= 256):
#         return None, None, 0

#     q = maurer(n)
#     p0 = maurer((l // 2) + 2)
#     l2 = 2**l
#     l21 = l2 // 2
#     x = number.getRandomRange(l2, l21)
#     tmp = 2 * p0 * q
#     t = x // tmp

#     while True:
#         tmp1 = 2 * t
#         if tmp1 + 1 > l2:
#             t = (2**(l - 1)) // tmp

#         p = tmp * t + 1
#         p1 = p - 2
#         p2 = p1 // 2

#         a = number.getRandomRange(2, p - 2)
#         z = pow(a, 2 * t * q, p)
#         w = pow(z, p0, p)
#         z -= 1

#         if number.GCD(z, p) == 1 and w == 1:
#             return p, q, 1

#         t += 1

#     return None, None, 0

# def sinh_gn(p, q):
#     e = (p - 1) // q
#     p1 = p - 1
#     g = 1

#     while g == 1:
#         a = number.getRandomRange(2, p - 1)
#         g = pow(a, e, p)

#     return g

# def sinh_tham_som(l, n):
#     p, q, success = sinh_p_qn(l, n)

#     if not success:
#         return None, None, None

#     g = sinh_gn(p, q)

#     return p, q, g

# def sinh_tham_so_el():
#     l, n = 3072, 256  # Chọn giá trị l và n tùy ý
#     p, q, g = sinh_tham_som(l, n)

#     if p is not None and q is not None and g is not None:
#         print("p:", p)
#         print("q:", q)
#         print("g:", g)
#     else:
#         print("Không thể sinh tham số.")

# if __name__ == "__main__":
#     sinh_tham_so_el()

# from Crypto.Util.number import getRandomRange
# import time

# def is_prime_miller_rabin(n, k=20):
#     """
#     Kiểm tra số nguyên tố bằng phương pháp Miller-Rabin.
#     :param n: Số cần kiểm tra
#     :param k: Số lần lặp (độ chính xác)
#     :return: True nếu là số nguyên tố, False nếu không chắc chắn là số nguyên tố
#     """
#     if n == 2 or n == 3:
#         return True
#     if n <= 1 or n % 2 == 0:
#         return False

#     r, s = 0, n - 1
#     while s % 2 == 0:
#         r += 1
#         s //= 2

#     for _ in range(k):
#         a = getRandomRange(2, n - 1)
#         x = pow(a, s, n)

#         if x == 1 or x == n - 1:
#             continue

#         for _ in range(r - 1):
#             x = pow(x, 2, n)
#             if x == n - 1:
#                 break
#         else:
#             return False

#     return True

# def maurer(k, max_attempts=1000):
#     for _ in range(max_attempts):
#         q = getRandomRange(2**(k-1), 2**k)
#         if is_prime_miller_rabin(q):
#             return q

#     return None

# def sinh_p_qn(l, n, max_attempts=1000):
#     if not (2048 <= l <= 3072) or not (224 <= n <= 256):
#         return None, None

#     q = maurer(n, max_attempts)
#     if q is None:
#         return None, None

#     p0 = getRandomRange(2**((l // 2) + 1 - 1), 2**((l // 2) + 1))
#     l2 = 2 ** l
#     l21 = l2 // 2
#     x = getRandomRange(l21, l2)
#     tmp = 2 * p0 * q
#     t = x // tmp

#     for _ in range(max_attempts):
#         tmp1 = 2 * t + 1
#         if tmp1 > l2:
#             t = (2 ** (l - 1)) // tmp

#         p = tmp * t + 1
#         p1 = p - 2
#         p2 = p1 // 2

#         a = getRandomRange(2, p - 2)
#         z = pow(a, 2 * t * q, p)
#         w = pow(z, p0, p)
#         z -= 1

#         if pow(w, p1, p) == 1 and pow(z, p, p) == 1:
#             return p, q

#         t += 1

#     return None, None

# if __name__ == "__main__":
#     start_time = time.time()
#     p, q = sinh_p_qn(2048, 256, max_attempts=5000)
#     if p is not None and q is not None:
#         print("p:", p)
#         print("q:", q)
#     else:
#         print("Không thể sinh tham số.")
#     end_time = time.time()
#     elapsed_time = end_time - start_time
#     print("Thời gian chạy: {} giây".format(elapsed_time))






