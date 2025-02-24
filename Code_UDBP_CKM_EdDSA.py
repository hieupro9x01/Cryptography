import os
import tkinter as tk
from tkinter import messagebox
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization

# Tạo cặp khóa EdDSA cho máy chủ
server_private_key = Ed25519PrivateKey.generate()
server_public_key = server_private_key.public_key()

# Hiển thị khóa bí mật và công khai dưới dạng PEM
private_key_pem = server_private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)
public_key_pem = server_public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

print("Khóa bí mật (private key):")
print(private_key_pem.decode())
print("\nKhóa công khai (public key):")
print(public_key_pem.decode())

# Danh sách lưu phiếu bầu đã ký
signed_votes = []

# Hàm làm mù thông điệp
def blind_message(voter_id, candidate):
    """
    Kết hợp số định danh và ứng viên để tạo thông điệp.
    Làm mù thông điệp bằng một giá trị ngẫu nhiên (blinding factor).
    """
    message = f"{voter_id}:{candidate}".encode()
    blinding_factor = os.urandom(32)  # Giá trị ngẫu nhiên 256-bit
    hashed_message = hashes.Hash(hashes.SHA256())
    hashed_message.update(message + blinding_factor)
    blinded_message = hashed_message.finalize()

    # In thông tin làm mù
    print("\n--- Làm mù thông điệp ---")
    print(f"Số định danh: {voter_id}")
    print(f"Ứng viên: {candidate}")
    print(f"Blinding factor: {blinding_factor.hex()}")
    print(f"Blinded message: {blinded_message.hex()}")

    return blinded_message, blinding_factor

# Hàm ký thông điệp đã làm mù
def sign_blinded_message(blinded_message):
    """
    Máy chủ ký thông điệp đã được làm mù.
    """
    signature = server_private_key.sign(blinded_message)

    # In chữ ký
    print("\n--- Chữ ký ---")
    print(f"Blinded message: {blinded_message.hex()}")
    print(f"Signature: {signature.hex()}")

    return signature

# Hàm xác minh chữ ký
def unblind_and_verify(signature, voter_id, candidate, blinding_factor):
    """
    Gỡ bỏ che giấu và xác thực chữ ký của phiếu bầu.
    """
    message = f"{voter_id}:{candidate}".encode()
    hashed_message = hashes.Hash(hashes.SHA256())
    hashed_message.update(message + blinding_factor)
    original_message = hashed_message.finalize()

    # Xác minh chữ ký
    server_public_key.verify(signature, original_message)
    print("\n--- Xác minh thành công ---")
    print(f"Thông điệp gốc: {original_message.hex()}")
    return True

# Hàm gửi phiếu bầu
def submit_vote(voter_id, candidate):
    try:
        # Kiểm tra xem người bỏ phiếu đã bỏ phiếu chưa
        if any(vote["voter_id"] == voter_id for vote in signed_votes):
            messagebox.showerror("Lỗi", "Bạn đã bỏ phiếu trước đó!")
            return

        # Bước 1: Tạo phiếu bầu và làm mù
        blinded_message, blinding_factor = blind_message(voter_id, candidate)

        # Bước 2: Gửi phiếu bầu đã làm mù đến máy chủ để ký
        signature = sign_blinded_message(blinded_message)

        # Bước 3: Gỡ mù và lưu phiếu bầu
        unblind_and_verify(signature, voter_id, candidate, blinding_factor)
        signed_votes.append({
            "voter_id": voter_id,
            "candidate": candidate,
            "signature": signature.hex(),
            "blinding_factor": blinding_factor.hex(),
        })

        # Hiển thị thông tin phiếu bầu
        print("\n--- Phiếu bầu đã lưu ---")
        print(signed_votes[-1])

        messagebox.showinfo("Thành công", f"Bỏ phiếu cho {candidate} thành công!")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Đã xảy ra lỗi: {str(e)}")

# Hàm xử lý giao diện khi bỏ phiếu
def handle_vote(candidate):
    voter_id = voter_id_entry.get()
    if not voter_id:
        messagebox.showerror("Lỗi", "Vui lòng nhập số định danh!")
        return
    submit_vote(voter_id, candidate)

# Tạo giao diện bằng Tkinter
root = tk.Tk()
root.title("Hệ thống bầu cử")

# Tiêu đề
label = tk.Label(root, text="Nhập số định danh và chọn ứng viên bạn muốn bầu:", font=("Arial", 14))
label.pack(pady=10)

# Ô nhập số định danh
voter_id_label = tk.Label(root, text="Số định danh:", font=("Arial", 12))
voter_id_label.pack()
voter_id_entry = tk.Entry(root, font=("Arial", 12))
voter_id_entry.pack(pady=5)

# Nút chọn ứng viên A
button_a = tk.Button(root, text="Ứng viên A", font=("Arial", 12), command=lambda: handle_vote("Candidate_A"))
button_a.pack(pady=5)

# Nút chọn ứng viên B
button_b = tk.Button(root, text="Ứng viên B", font=("Arial", 12), command=lambda: handle_vote("Candidate_B"))
button_b.pack(pady=5)

# Nút chọn ứng viên C
button_c = tk.Button(root, text="Ứng viên C", font=("Arial", 12), command=lambda: handle_vote("Candidate_C"))
button_c.pack(pady=5)

# Nút thoát
button_exit = tk.Button(root, text="Thoát", font=("Arial", 12), command=root.quit)
button_exit.pack(pady=10)

# Chạy giao diện
root.mainloop()
