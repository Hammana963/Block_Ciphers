import math
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES

# Uses PKCS7 to add padding 
def pad(data):
    numBlocks = math.ceil(len(data)/float(128))
    padValue = int(numBlocks * 128 - len(data)) # value determines -> 01, 02 02, 03 03 03, etc..

    if padValue == 0:
        return data + (128).to_bytes() * 128
    else:
        return data + (padValue).to_bytes() * padValue

key = get_random_bytes(32)
cipher = AES.new(key, AES.MODE_ECB)

with open("mustang.bmp", "rb") as f:
  bitData = f.read()

#save header of bmp file (128 works on my mac)
header = bitData[0:128]
cipherText = bytes()

start = 128

for i in range((len(bitData) // 128) - 1):
  # encrypt 128 blocks, and add them together
  cipherText += cipher.encrypt(bitData[start:start+128])
  start += 128

#pad the final block if it isnt long enough
if start < len(bitData):
  cipherText += cipher.encrypt(pad(bitData[start:start+128]))

#add header back on
cipherText = header + cipherText

with open("ECB_text.bmp", "wb") as f:
  f.write(cipherText)

