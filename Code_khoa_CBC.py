
import os

from cryptography.hazmat.primitives.ciphers import Cipher
from cryptography.hazmat.primitives.ciphers.algorithms import AES
from cryptography.hazmat.primitives.ciphers.modes import CBC 
from cryptography.hazmat.primitives import padding

if __name__ == "__main__":

    # Plaintext to be kept confidential

    plaintext = b'Fundamental Cryptography in Python' 
    print(f"Plaintext: {plaintext}")

    #256-bit AES key

    key = os.urandom(256 // 8)
    
    # Vectơ khởi tạo ngẫu nhiên 128 bit (iv) cần thiết cho chế độ hoạt động CBC

    iv = os.urandom(128 // 8)

    # Create AES CBC cipher

    aes_cbc_cipher = Cipher(AES(key), CBC(iv))

    # Encrypt

    ciphertext = aes_cbc_cipher.encryptor().update(plaintext) 
    print(f"Ciphertext: {ciphertext}")

    # Decrypt

    recovered_plaintext = aes_cbc_cipher.decryptor().update(ciphertext) 
    print(f"Recovered plaintext: {recovered_plaintext}")

    # Pad the plaintext

    pkcs7_padder = padding.PKCS7(AES.block_size).padder() 
    padded_plaintext = pkcs7_padder.update(plaintext) + pkcs7_padder.finalize()
    print(f"Padded plaintext: {padded_plaintext}")

    # Encrypt padded plaintext

    ciphertext=aes_cbc_cipher.encryptor().update(padded_plaintext)

    print(f"Ciphertext: {ciphertext}")

    # Decrypt to padded plaintext

    recovered_plaintext_with_padding = aes_cbc_cipher.decryptor().update(ciphertext) 
    print(f"Recovered plaintext with padding: {recovered_plaintext_with_padding}")

    # Remove padding

    pkcs7_unpadder = padding.PKCS7(AES.block_size).unpadder()

    recovered_plaintext = pkcs7_unpadder.update(recovered_plaintext_with_padding) + pkcs7_unpadder.finalize() 
    print(f"Recovered plaintext: {recovered_plaintext}")

    assert (recovered_plaintext == plaintext)


    #Encrypt mandel-bw.ppm

    #Read the image into memory

    with open("mandel-bw.ppm", "rb") as image:

        image_file = image.read()
        image_bytes = bytearray(image_file)
   
    #Keep ppm header

    header_size = 17
    image_header = image_bytes[:header_size]
    image_body = image_bytes [header_size:]

    # Pad the image body

    pkcs7_padder = padding.PKCS7(AES.block_size).padder() 
    padded_image_body = pkcs7_padder.update(image_body) + pkcs7_padder.finalize()

    #Encrypt the image body

    encrypted_image_body = aes_cbc_cipher.encryptor().update(padded_image_body)

    # Assemble encrypted image

    encrypted_image = image_header + encrypted_image_body[:len (image_body)]

    # Create and save the full encrypted image

    with open("mandelbrot aes_cbc_encrypted.ppm", "wb") as image_encrypted: 
        image_encrypted.write(encrypted_image)





