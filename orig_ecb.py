from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES

key = get_random_bytes(32)
print(key)
cipher = AES.new(key, AES.MODE_ECB)

with open("mustang.bmp", "rb") as f:
  bitData = f.read()

print(len(bitData))
print(len(bitData)%128) 

bitData_trimmed = bitData[128:-(len(bitData)%128)]



cipherText = cipher.encrypt(bitData_trimmed)


cipherText = (bitData[0:128] + cipherText + bitData[-(len(bitData)%128):])
with open("ECB1_text.bmp", "wb") as f:
  f.write(cipherText)