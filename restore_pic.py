import os
from encrypt import decrypt_file

encrypt_key = b'\x8d5\x89\xbb\xe1\x1c\xed\x9f\x92HQ~kF \xd2\xea\x19\x9b\xaa\x03\x10\xbaM\xe0\x14R\xfb\x01\xc5\x9f\xc6'

image_dir = "./data"

for f in os.listdir(image_dir):

    if f.endswith(".jpg"):
        decrypt_file(image_dir + "/" + f, image_dir + '/rs_' + f, encrypt_key)

