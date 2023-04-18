import math
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES

# Uses PKCS7 to add padding 
def pad(data):
    numBlocks = math.ceil(len(data)/float(16))
    padValue = int(numBlocks * 16 - len(data)) # value determines -> 01, 02 02, 03 03 03, etc..

    if padValue == 0:
        return data + (16).to_bytes() * 16
    else:
        return data + (padValue).to_bytes() * padValue


key = get_random_bytes(16)
cipher = AES.new(key, AES.MODE_ECB)

with open("mustang.bmp", "rb") as f:
  bitData = f.read()

#save header of bmp file (128 works on my mac)
header = bitData[0:128]
rest = bitData[128:]
cipherText = bytes()




start = 16
bitData = pad(rest)
for i in range((len(rest) // 16) - 1):
  # encrypt 128 blocks, and add them together
  cipherText += cipher.encrypt(rest[start:start+16])
  start += 16

#pad the final block if it isnt long enough
if start < len(rest):
  cipherText += cipher.encrypt(pad(rest[start:start+16]))

#add header back on
cipherText = header + cipherText

with open("ECB__encoded_image.bmp", "wb") as f:
  f.write(cipherText)

