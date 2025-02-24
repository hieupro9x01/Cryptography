




import numpy as np

# Các hàm cơ bản để tính toán ma trận và vector
def add_matrices(a, b, q):
    a = np.array(a)
    b = np.array(b)
    result = (a + b) % q
    return result.tolist()

def negate_matrix(a, q):
    a = np.array(a)
    result = (-a) % q
    return result.tolist()

def subtract_matrices(a, b, q):
    return add_matrices(a, negate_matrix(b, q), q)

def multiply_matrix_vector_simple(m, a, q):
    m = np.array(m)
    a = np.array(a)
    result = np.dot(m, a) % q
    return result.tolist()

def transpose_matrix(m):
    m = np.array(m)
    result = np.transpose(m)
    return result.tolist()

# Hàm tạo các tham số ngẫu nhiên
def create_random_matrix(size, q):
    return np.random.randint(0, q, size=size).tolist()

def create_random_vector(size, values=[-2, -1, 0, 1, 2]):
    return np.random.choice(values, size=size).tolist()

# Hàm mã hóa và giải mã
def encrypt(A, t, m_b, q, r, e_1, e_2):
    half_q = int(q / 2 + 0.5)
    m = [x * half_q for x in m_b]
    u = add_matrices(multiply_matrix_vector_simple(transpose_matrix(A), r, q), e_1, q)
    
    # Xử lý v như vector
    mult_result = multiply_matrix_vector_simple(transpose_matrix(t), r, q)
    v = [(mult_result + m[i]) % q for i in range(len(m))]
    v = add_matrices(v, e_2, q)
    return u, v

def decrypt(s, u, v, q):
    mult_result = multiply_matrix_vector_simple(s, u, q)
    u_mult_result = [mult_result] * len(v)

    m_n = subtract_matrices(v, u_mult_result, q)
    half_q = int(q / 2 + 0.5)

    def round_value(val, mid, limit):
        mid_distance = np.abs(mid - val)
        limit_distance = min(val, limit - val)
        return mid if mid_distance < limit_distance else 0

    m_n = [round_value(x, half_q, q) for x in m_n]
    m_b = [x // half_q for x in m_n]
    return m_b

# Các hàm mã hóa và giải mã văn bản
def encrypt_text(text, A, t, q, r, e_1, e_2):
    text_bytes = text.encode('utf-8')
    binary_message = []
    for byte in text_bytes:
        binary_message += [int(bit) for bit in format(byte, '08b')]
    
    block_size = len(r)  # Kích thước của khối phải phù hợp với kích thước của r
    encrypted_blocks = []
    for i in range(0, len(binary_message), block_size):
        block = binary_message[i:i + block_size]
        if len(block) < block_size:
            block += [0] * (block_size - len(block))
        u, v = encrypt(A, t, block, q, r, e_1, e_2)
        encrypted_blocks.append((u, v))
    return encrypted_blocks

def decrypt_text(encrypted_blocks, s, q):
    binary_message = []
    for u, v in encrypted_blocks:
        block = decrypt(s, u, v, q)
        binary_message += block
    text_bytes = bytearray()
    for i in range(0, len(binary_message), 8):
        byte = binary_message[i:i + 8]
        text_bytes.append(int(''.join(map(str, byte)), 2))
    return text_bytes.decode('utf-8')


# Hàm mã hóa file
def encrypt_file(input_file, output_file, A, t, q, r, e_1, e_2):
    with open(input_file, 'rb') as f:
        file_bytes = f.read()

    binary_message = []
    for byte in file_bytes:
        binary_message += [int(bit) for bit in format(byte, '08b')]
    block_size = len(r)  # Kích thước của khối phải phù hợp với kích thước của r
    encrypted_blocks = []
    for i in range(0, len(binary_message), block_size):
        block = binary_message[i:i+block_size]
        if (len(block) < block_size):
            block += [0] * (block_size - len(block))
        u, v = encrypt(A, t, block, q, r, e_1, e_2)
        encrypted_blocks.append((u, v))

    # Ghi bản mã vào file
    with open(output_file, 'w') as f:
        for u, v in encrypted_blocks:
            f.write(' '.join(map(str, u)) + '\n')
            f.write(' '.join(map(str, v)) + '\n')

# Hàm giải mã file
def decrypt_file(input_file, output_file, s, q):
    encrypted_blocks = []

    # Đọc bản mã từ file
    with open(input_file, 'r') as f:
        lines = f.readlines()

    for i in range(0, len(lines), 2):
        u = list(map(int, lines[i].strip().split()))
        v = list(map(int, lines[i+1].strip().split()))
        encrypted_blocks.append((u, v))

    binary_message = []
    for u, v in encrypted_blocks:
        block = decrypt(s, u, v, q)
        binary_message += block

    text_bytes = bytearray()
    for i in range(0, len(binary_message), 8):
        byte = binary_message[i:i+8]
        text_bytes.append(int(''.join(map(str, byte)), 2))

    with open(output_file, 'wb') as f:
        f.write(text_bytes)


# Các hàm in dữ liệu
def print_matrix(matrix):
    for row in matrix:
        print(" ".join(f"{val:4}" for val in row))
    print()

def print_vector_as_column(vector):
    for val in vector:
        print(f"{val:4}")
    print()

def print_matrix_with_vector(matrix, vector):
    for i in range(len(matrix)):
        print(" ".join(f"{val:4}" for val in matrix[i]), end="   ")
        print(f"{vector[i]:4}")
    print()

def print_cipher_blocks(encrypted_text):
    for block_num, (u, v) in enumerate(encrypted_text, start=1):
        print(f"Bản mã khối {block_num}:")
        print(f"giá trị u:    giá trị v:")
        for u_val, v_val in zip(u, v):
            print(f"{u_val:10} {v_val:10}")
        print()  # Dòng trống giữa các khối

# Hàm main với ví dụ mới
def main():
    q = 3329  # Sử dụng giá trị Q tương ứng với Kyber
    
    # Nhập kích thước của ma trận A từ người dùng
    n = int(input("Nhập kích thước của ma trận A (tối đa 256): "))

    if n > 256:
        print("Kích thước quá lớn. Vui lòng nhập giá trị từ 1 đến 256.")
        return

    A = create_random_matrix((n, n), q)
    s = create_random_vector(n)
    e = create_random_vector(n)

    multiplied_vectors = multiply_matrix_vector_simple(A, s, q)
    t = add_matrices(multiplied_vectors, e, q)

    r = create_random_vector(n)
    e_1 = create_random_vector(n)
    e_2 = create_random_vector(n)

    print("Khóa công khai (Public Key A):")
    print_matrix(A)
    print("Khóa công khai (Public Key t):")
    print_vector_as_column(t)
    print("Khóa bí mật (Private Key):")
    print_vector_as_column(s)

    # Chọn hành động
    print("Chọn hành động:")
    print("1. Mã hóa văn bản")
    print("2. Mã hóa file")
    choice = input("Lựa chọn của bạn (1/2): ")

    if choice == '1':
        text = input("Nhập văn bản cần mã hóa: ")
        encrypted_text = encrypt_text(text, A, t, q, r, e_1, e_2)
        
        print("Bản mã (Ciphertext):")
        print_cipher_blocks(encrypted_text)

        decrypted_text = decrypt_text(encrypted_text, s, q)
        print("Văn bản sau giải mã (Decrypted Text):", decrypted_text)

        if text == decrypted_text:
            print("Giải mã thành công! Văn bản sau giải mã giống với văn bản ban đầu.")
        else:
            print("Giải mã thất bại! Văn bản sau giải mã không giống với văn bản ban đầu.")

    elif choice == '2':
        input_file = input("Nhập tên file cần mã hóa: ")
        output_file = input("Nhập tên file lưu trữ bản mã: ")

        encrypt_file(input_file, output_file, A, t, q, r, e_1, e_2)
        print(f"File {input_file} đã được mã hóa thành công và lưu trữ dưới tên {output_file}")

        decrypted_output_file = input("Nhập tên file lưu trữ kết quả giải mã: ")
        decrypt_file(output_file, decrypted_output_file, s, q)
        print(f"File {output_file} đã được giải mã thành công và lưu trữ dưới tên {decrypted_output_file}")

if __name__ == "__main__":
    main()




