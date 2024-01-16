from os import urandom
from Crypto.Cipher import AES

def encrypt_file(input_file, output_file, key):
    in_file = open(input_file, 'rb')
    encrypted_file = open(output_file, 'wb')

    cipher = AES.new(key, AES.MODE_CFB)
    encrypted_file.write(cipher.iv)

    bufferSize = 65536
    buffer = in_file.read(bufferSize)
    while len(buffer) > 0:
        ciphered_bytes = cipher.encrypt(buffer)
        encrypted_file.write(ciphered_bytes)
        buffer = in_file.read(bufferSize)

    # Close the input and output files
    in_file.close()
    encrypted_file.close()

def decrypt_file(input_file, output_file, key):
    in_file = open(input_file, 'rb')
    decrypted_file = open(output_file, 'wb')

    iv = in_file.read(16)

    cipher = AES.new(key, AES.MODE_CFB, iv=iv)

    bufferSize = 65536

    buffer = in_file.read(bufferSize)
    while len(buffer) > 0:
        decrypted_bytes = cipher.decrypt(buffer)
        decrypted_file.write(decrypted_bytes)
        buffer = in_file.read(bufferSize)

    # Close the input and output files
    in_file.close()
    decrypted_file.close()

def random_bytes(num_bytes):
    return urandom(num_bytes)

# generate a 32 bytes encryption key
#print(random_bytes(32))
