import warnings
from ecdsa.util import bit_length
from ecdsa import( ellipticcurve, numbertheory ,
    NIST192p, NIST224p, NIST256p, NIST384p, NIST521p,
    SECP256k1, 
    BRAINPOOLP160r1, BRAINPOOLP192r1, BRAINPOOLP224r1, BRAINPOOLP256r1, BRAINPOOLP320r1, BRAINPOOLP384r1, BRAINPOOLP512r1,
    SECP112r1, SECP112r2, SECP128r1, SECP160r1 )
from hashlib import sha256 
from random import randrange 

class RSZeroError(RuntimeError):
    pass

class InvalidPointError(RuntimeError):
    pass

class Signature(object):
    def __init__(self, r, s):
        self.r = r
        self.s = s

class Public_key(object):
    def __init__(self, generator, point, verify=True):
        self.curve = generator.curve()
        self.generator = generator
        self.point = point
        n = generator.order()
        p = self.curve.p()
        if not (0 <= point.x() < p) or not (0 <= point.y() < p):
            raise InvalidPointError("Điểm công khai có giá trị x hoặc y nằm ngoài phạm vi cho phép.")
        if verify and not self.curve.contains_point(point.x(), point.y()):
            raise InvalidPointError("Điểm không nằm trên đường cong")
        if not n:
            raise InvalidPointError("Điểm khởi tạo phải có bậc.")
        if verify and self.curve.cofactor() != 1 and not n * point == ellipticcurve.INFINITY:
            raise InvalidPointError("Bậc của điểm khởi tạo không hợp lệ.")

    def verifies(self, hash, signature):
        G = self.generator
        n = G.order()
        r = signature.r
        s = signature.s
        if r < 1 or r > n - 1:
            return False
        if s < 1 or s > n - 1:
            return False
        c = numbertheory.inverse_mod(s, n)
        u1 = (hash * c) % n
        u2 = (r * c) % n
        if hasattr(G, "mul_add"):
            xy = G.mul_add(u1, self.point, u2)
        else:
            xy = u1 * G + u2 * self.point
        v = xy.x() % n
        return v == r

class Private_key(object):
    def __init__(self, public_key, secret_multiplier):
        self.public_key = public_key
        self.secret_multiplier = secret_multiplier

    def sign(self, hash, random_k):
        G = self.public_key.generator
        n = G.order()
        k = random_k % n
        ks = k + n
        kt = ks + n
        if bit_length(ks) == bit_length(n):
            p1 = kt * G
        else:
            p1 = ks * G
        r = p1.x() % n
        if r == 0:
            raise RSZeroError("Số ngẫu nhiên r cực kỳ không may mắn")
        s = (numbertheory.inverse_mod(k, n) * (hash + (self.secret_multiplier * r) % n)) % n
        if s == 0:
            raise RSZeroError("số ngẫu nhiên s cực kỳ không may mắn")
        return Signature(r, s)

def generate_keys(curve):
    generator = curve.generator
    order = generator.order()
    secret_multiplier = randrange(1, order)
    public_point = secret_multiplier * generator
    public_key = Public_key(generator, public_point)
    private_key = Private_key(public_key, secret_multiplier)
    return private_key, public_key

def sign_message(private_key, message):
    hash_value = int.from_bytes(sha256(message.encode()).digest(), 'big')
    random_k = randrange(1, private_key.public_key.generator.order())
    signature = private_key.sign(hash_value, random_k)
    return signature

def verify_signature(public_key, signature, message):
    hash_value = int.from_bytes(sha256(message.encode()).digest(), 'big')
    return public_key.verifies(hash_value, signature)

if __name__ == "__main__":
    print(
        "Danh sách các tham số đường cong: \n" , 
        "NIST192p = 1 \n",
        "NIST224p = 2 \n",
        "NIST256p = 3 \n",
        "NIST384p = 4 \n",
        "NIST521p = 5 \n",
        "SECP256k1 = 6 \n",
        "BRAINPOOLP160r1 = 7 \n",
        "BRAINPOOLP192r1 = 8 \n",
        "BRAINPOOLP224r1 = 9 \n",
        "BRAINPOOLP256r1 = 10 \n",
        "BRAINPOOLP320r1 = 11 \n",
        "BRAINPOOLP384r1 = 12 \n",
        "BRAINPOOLP512r1 = 13 \n",
        "SECP112r1 = 14 \n",
        "SECP112r2 = 15 \n",
        "SECP128r1 = 16 \n",
        "SECP160r1 = 17 \n"
    )

    curves_map = {
        "1": NIST192p,
        "2": NIST224p,
        "3": NIST256p,
        "4": NIST384p,
        "5": NIST521p,
        "6": SECP256k1,
        "7": BRAINPOOLP160r1,
        "8": BRAINPOOLP192r1,
        "9": BRAINPOOLP224r1,
        "10": BRAINPOOLP256r1,
        "11": BRAINPOOLP320r1,
        "12": BRAINPOOLP384r1,
        "13": BRAINPOOLP512r1,
        "14": SECP112r1,
        "15": SECP112r2,
        "16": SECP128r1,
        "17": SECP160r1
    }

    curve_name = input("Nhập tham số đường cong mong muốn: ")

    if curve_name in curves_map:
        selected_curve = curves_map[curve_name]
        private_key, public_key = generate_keys(selected_curve)
        print("Đã tạo khóa bí mật và công khai từ đường cong", curve_name)
    else:
        print("Tham số đường cong không hợp lệ.")
        exit(1)

    print("Khóa công khai:", public_key.point.y())
    print("Khóa bí mật:", private_key.secret_multiplier)

    message = input("Nhập thông điệp cần ký: ")
    signature = sign_message(private_key, message)
    print("Thông điệp:", message)
    print("Chữ ký: (r={}, s={})".format(signature.r, signature.s))

    if verify_signature(public_key, signature, message):
        print("Chữ ký hợp lệ!")
    else:
        print("Chữ ký không hợp lệ.")
