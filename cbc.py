from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES

key = get_random_bytes(32)
print(key)
cipher = AES.new(key, AES.MODE_ECB)

with open("mustang.bmp", "rb") as f:
  clear = f.read()

print(len(clear))
print(len(clear)%128) 

clear_trimmed = clear[128:-(len(clear)%128)]

ciphertext = cipher.encrypt(clear_trimmed)


ciphertext = (clear[0:128] + ciphertext + clear[-(len(clear)%128):])
# print(ciphertext)
with open("ECB1_text.bmp", "wb") as f:
  f.write(ciphertext)
