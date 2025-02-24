
import os

from cryptography.hazmat.primitives.ciphers import Cipher
from cryptography.hazmat.primitives.ciphers.algorithms import AES
from cryptography.hazmat.primitives.ciphers.modes import ECB 
from cryptography.hazmat.primitives import padding

if __name__ == "__main__":

    # Bản rõ được giữ bí mật

    plaintext = b'Fundamental Cryptography in Python' 
    print(f"Plaintext: {plaintext}")

    # Khóa AES 256-bit

    key = os.urandom(256 // 8) # os.urandom()phương thức được sử dụng để tạo một chuỗi byte ngẫu nhiên có kích thước phù hợp cho việc sử dụng mật mã hoặc có thể nói phương thức này tạo ra một chuỗi chứa các ký tự ngẫu nhiên.

    # Tạo mật mã AES ECB

    aes_ecb_cipher = Cipher(AES(key), ECB())

    # mã hóa

    ciphertext = aes_ecb_cipher.encryptor().update(plaintext) # Mã hóa là quá trình mã hóa dữ liệu. tức là chuyển văn bản thuần thành bản mã. Việc chuyển đổi này được thực hiện với một khóa gọi là khóa mã hóa.
    print(f"Ciphertext: {ciphertext}")

    # giải mã

    recovered_plaintext = aes_ecb_cipher.decryptor().update(ciphertext) # Giải mã là quá trình giải mã dữ liệu được mã hóa. Chuyển đổi bản mã thành văn bản thuần túy. Quá trình này yêu cầu một khóa mà chúng tôi đã sử dụng để mã hóa.
    print(f"Recovered plaintext: {recovered_plaintext}")

    # Đệm bản rõ

    pkcs7_padder = padding.PKCS7(AES.block_size).padder() #  tạo "chữ ký tách rời PKCS #7 của tệp kê khai".  
                                                          # padder là một cách để lấy dữ liệu có thể là bội số của kích thước khối cho một mật mã và mở rộng dữ liệu đó ra như vậy. Điều này là bắt buộc đối với nhiều chế độ mật mã khối vì chúng yêu cầu dữ liệu được mã hóa là bội số chính xác của kích thước khối.  
    padded_plaintext = pkcs7_padder.update(plaintext) + pkcs7_padder.finalize() # phương thức finalize() được sử dụng để giải phóng tài nguyên được cấp phát cho một đối tượng Python khi nó không còn được sử dụng nữa.
    print(f"Padded plaintext: {padded_plaintext}")

    # Mã hóa bản rõ có đệm

    ciphertext=aes_ecb_cipher.encryptor().update(padded_plaintext)

    print(f"Ciphertext: {ciphertext}")

    # Giải mã thành văn bản đệm

    recovered_plaintext_with_padding = aes_ecb_cipher.decryptor().update(ciphertext) 
    print(f"Recovered plaintext with padding: {recovered_plaintext_with_padding}")

    # Xóa phần đệm

    pkcs7_unpadder = padding.PKCS7(AES.block_size).unpadder()

    recovered_plaintext = pkcs7_unpadder.update(recovered_plaintext_with_padding) + pkcs7_unpadder.finalize() 
    print(f"Recovered plaintext: {recovered_plaintext}")

    assert (recovered_plaintext == plaintext)


    # Mã hóa ảnh mandel-bw.ppm

    # Đọc hình ảnh vào bộ nhớ

    with open("mandel-bw.ppm", "rb") as image:

        image_file = image.read()
        image_bytes = bytearray(image_file)
   
    # Giữ tiêu đề ppm

    header_size = 17
    image_header = image_bytes[:header_size]
    image_body = image_bytes [header_size:]

    # Đệm thân ảnh

    pkcs7_padder = padding.PKCS7(AES.block_size).padder() 
    padded_image_body = pkcs7_padder.update(image_body) + pkcs7_padder.finalize()

    # Mã hóa nội dung hình ảnh

    encrypted_image_body = aes_ecb_cipher.encryptor().update(padded_image_body)

    # Lắp ráp hình ảnh được mã hóa

    encrypted_image = image_header + encrypted_image_body[:len (image_body)]

    # Tạo và lưu hình ảnh được mã hóa đầy đủ

    with open("mandelbrot aes_ecb_encrypted.ppm", "wb") as image_encrypted: 
        image_encrypted.write(encrypted_image)





