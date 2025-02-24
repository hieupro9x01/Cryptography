import math
import random
from sympy.ntheory.modular import crt
from sympy.ntheory.factor_ import factorint
from math import ceil, sqrt

# Hàm tính lũy thừa mod (Modular Exponentiation)
def powmod(base, exp, mod):
    result = 1
    base = base % mod
    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod
        exp = exp >> 1
        base = (base * base) % mod
    return result

# Vét cạn (Brute Force)
def brute_force_log(g, h, p):
    for x in range(p):
        if pow(g, x, p) == h:
            return x
    return None

# Bước nhỏ bước lớn (Baby-Step Giant-Step)
def baby_step_giant_step(g, h, p):
    m = math.isqrt(p) + 1
    table = {pow(g, j, p): j for j in range(m)}
    inv = pow(g, -m, p)
    for i in range(m):
        y = (h * pow(inv, i, p)) % p
        if y in table:
            return i * m + table[y]
    return None

# Pollard's Rho
def ext_euclid(a, b):
    if b == 0:
        return a, 1, 0
    else:
        d, xx, yy = ext_euclid(b, a % b)
        x = yy
        y = xx - (a // b) * yy
        return d, x, y

def inverse(a, n):
    return ext_euclid(a, n)[1]
# hàm tính tập giá trị x, a, b theo tập thuộc S1, S2, S3
def xab(x, a, b, params):
    G, H, P, Q = params
    sub = x % 3
    if sub == 0:
        x = x * G % P
        a = (a + 1) % Q
    elif sub == 1:
        x = x * H % P
        b = (b + 1) % Q
    elif sub == 2:
        x = x * x % P
        a = a * 2 % Q
        b = b * 2 % Q
    return x, a, b
# Hàm chức năng chính của pollard
def pollard(G, H, P):
    Q = (P - 1) // 2
    x = G * H
    a = 1
    b = 1
    X = x
    A = a
    B = b
    for i in range(1, P):
        x, a, b = xab(x, a, b, (G, H, P, Q))
        X, A, B = xab(X, A, B, (G, H, P, Q))
        X, A, B = xab(X, A, B, (G, H, P, Q))
        if x == X:
            break
    nom = a - A
    denom = B - b
    res = (inverse(denom, Q) * nom) % Q
    if verify(G, H, P, res):
        return res
    return res + Q
def verify(g, h, p, x):
    return pow(g, x, p) == h

# Pohling-Hellman
# Tìm tất cả các thừa số nguyên tố của số p
def PrimeFactorization(p):

    d, primeFactors = 2, []
    while d*d <= p:
        while (p % d) == 0:
            primeFactors.append(d)
            p //= d
        d += 1
    if p > 1:
       primeFactors.append(p)
    return primeFactors

# Đếm số lần xuất hiện của từng thừa số nguyên tố
def CountOccurences(primeFactors):

    return [[x, primeFactors.count(x)] for x in set(primeFactors)]

# Thuật toán Euclidian mở rộng để tìm GCD
def ExtendedGCD(a, b):

    a2, a1 = 1, 0
    b2, b1 = 0, 1
    while b:
        q, r = divmod(a, b)
        a1, a2 = a2 - q * a1, a1
        b1, b2 = b2 - q * b1, b1
        a, b = b, r
    return a, a2, b2

# Return x s.t. x ≡ a^(-1) (mod n)
def ModularInverse(b, n):

    g, x, _ = ExtendedGCD(b, n)
    if g == 1:
        return x % n

# Định lý số dư Trung Hoa giải hệ phương trình
def ChineseRemainder(pairs):

    N, X = pairs[0][1], 0
    for ni in pairs[1:]:
        N *= ni[1]
    for (ai, ni) in pairs:
        mi = (N / ni)
        X += mi * ai * ExtendedGCD(mi, ni)[1]
    return X % N

# Trả về x s.t. beta ≡ alpha^(x) (mod n)
def ShanksAlgorithm(alpha, beta, n):

    m = int(ceil(sqrt(n - 1)))
    a = pow(alpha, m, n)
    b = ExtendedGCD(alpha, n)[1]
    L1 = [(j, pow(a, j, n)) for j in range(0, m)]
    L2 = [(i, beta * (b ** i) % n) for i in range(0, m)]
    L1.sort(key = lambda tup: tup[1])
    L2.sort(key = lambda tup: tup[1])
    i, j, Found = 0, 0, False
    while (not Found) and (i < m) and (j < m):
        if L1[j][1] == L2[i][1]:
            return m * L1[j][0] + L2[i][0] % n
        elif abs(L1[j][1]) > abs(L2[i][1]):
            i = i + 1
        else:
            j = j + 1

# Cặp trả về (x, q ** e) đại diện cho một sự đồng đẳng
def CongruencePair(g, h, p, q, e, e1, e2):

    alphaInverse = ModularInverse(e1, p)
    x = 0 # x = x_{0} + x_{1} * q + x_{2} * q^{2} + ... + x_{e - 1} * q^{e - 1}
    for i in range(1, e + 1):
        a = pow(e1, q ** (e - 1), p)
        b = pow(e2 * (alphaInverse ** x), q ** (e - i), p)
        x += ShanksAlgorithm(a, b, p) * (q ** (i - 1))
    return (x, q ** e)


# Chức năng chính của thuật toán Pohling-Hellman
def PohlingHellman(h, g, p):


    CountOccurencesList = CountOccurences(PrimeFactorization(p - 1))
    CongruenceList = []


    for i in range(len(CountOccurencesList)):
        e1 = (h ** ((p - 1) // (CountOccurencesList[i][0] ** CountOccurencesList[i][1]))) % p # e1 = g^((p-1)/q^e)
        e2 = (g ** ((p - 1) // (CountOccurencesList[i][0] ** CountOccurencesList[i][1]))) % p # e2 = h^((p-1)/q^e)
        # Add new congruence
        CongruenceList.append(CongruencePair(g, h, p, CountOccurencesList[i][0], CountOccurencesList[i][1], e1, e2))
        e3 = CongruenceList[len(CongruenceList) - 1][0] % CongruenceList[len(CongruenceList) - 1][1] # e3 = (g^((p-1)/q^e))^x
        e4 = CongruenceList[len(CongruenceList) - 1][1] # e4 = h^((p-1)/q^e)

# Giải hệ phương trình đồng đẳng
    print(" Kết quả: %d" % ChineseRemainder(CongruenceList))



# Hàm tính logarit rời rạc bằng thuật toán chỉ số
def index_calculus(alpha, beta, p):
    # Tạo danh sách các phần tử của nhóm G
    G = [powmod(alpha, i, p) for i in range(p)]
    n = p - 1
    # Bước 1: Chọn cơ sở phân tích S
    S = random.sample(G, min(10, len(G)))  # Chọn 10 phần tử cơ sở ngẫu nhiên
    log_alpha = {s: random.randint(0, n-1) for s in S}
    # Bước 2: Chọn quan hệ tuyến tính
    linear_relations = []
    for _ in range(20):  # Lặp để có nhiều quan hệ tuyến tính
        k = random.randint(0, n-1)
        alpha_k = powmod(alpha, k, p)
        # Thử biểu diễn alpha^k dưới dạng tích của các phần tử trong S
        representation = {}
        for s in S:
            while alpha_k % s == 0:
                if s in representation:
                    representation[s] += 1
                else:
                    representation[s] = 1
                alpha_k //= s
        
        if alpha_k == 1:
            coefficients = [representation.get(p, 0) for p in S]
            linear_relations.append((k, coefficients))
    # Bước 3: Giải hệ phương trình tuyến tính
    A = []
    b = []
    for k, coeffs in linear_relations:
        A.append(coeffs)
        b.append(k)
    # Nếu có hệ phương trình, giải nó
    if len(A) > 0:
        try:
            A = [[log_alpha.get(p, 0) for p in S] for _ in A]
            solution = solve_congruence(list(zip(b, [mod_inverse(row, p) for row in A])))
            log_alpha.update(dict(zip(S, solution)))
        except:
            print("Không thể giải hệ phương trình.")
            return None
    # Bước 4: Tính toán log_alpha_beta
    beta_value = powmod(beta, 1, p)
    for i, s in enumerate(S):
        if beta_value % s == 0:
            d_i = log_alpha.get(s, 0)
        else:
            d_i = 0
        k = (d_i - log_alpha.get(s, 0)) % n

    return k

# Hàm giao diện lựa chọn thuật toán
def run_algorithms():
    while True:
        print("\n=== Chọn thuật toán ===")
        print("1. Vét cạn (Brute Force)")
        print("2. Baby-Step Giant-Step")
        print("3. Pollard's Rho")
        print("4. Pohling-Hellman")
        print("5. Chỉ số (Index Calculus)")
        print("6. Thoát")

        choice = input("Nhập lựa chọn của bạn (1-6): ")
        if choice == '6':
            print("Chương trình kết thúc.")
            break

        if choice in ['1', '2', '3', '4', '5']:
            h = int(input("Nhập beta: "))
            g = int(input("Nhập alpha: "))
            p = int(input("Nhập p (số nguyên tố): "))

            if choice == '1':
                print("\n=== Kết quả thuật toán Vét cạn (Brute Force) ===")
                res_brute = brute_force_log(g, h, p)
                print(f"Kết quả: {res_brute}\n")

            elif choice == '2':
                print("\n=== Kết quả thuật toán Baby-Step Giant-Step ===")
                res_bsgs = baby_step_giant_step(g, h, p)
                print(f"Kết quả: {res_bsgs}\n")

            elif choice == '3':
                print("\n=== Kết quả thuật toán Pollard's Rho ===")
                res_pollard = pollard(g, h, p)
                print(f"Kết quả: {res_pollard}\n")

            elif choice == '4':
                print("\n=== Kết quả thuật toán Pohling-Hellman ===")
                res_ph = PohlingHellman(g, h, p)
                print(f"Kết quả: {res_ph}\n")
            
            elif choice == '5':
                print("\n=== Kết quả thuật toán Chỉ số (Index Calculus) ===")
                result = index_calculus(g, h, p)
                if result is not None:
                    print(f"Kết quả: {result}\n")
                else:
                    print("Không thể tính toán kết quả với thuật toán chỉ số.\n")
        else:
            print("Lựa chọn không hợp lệ. Vui lòng nhập lại.")
# Chạy chương trình
run_algorithms()



