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


def submit(input):
    bytestring = pad(input)
    ciphertext = bytes()

    xoredtext = byte_xor(iv, bytestring[:128])  #first xor with iv
    encrypttext = cipher.encrypt(xoredtext)     #encrypt text
    #changing the data of the cipher block before target plaintext block
    ciphertext += encrypttext                   #add encrypted text to cipher text
    start = 16
    #Do CBC encrypt on rest of plaintext using prev encrypt text to xor plaintext
    for i in range((len(bytestring) // 16)-1):
        xoredtext = byte_xor(encrypttext, bytestring[start:start+16])   
        encrypttext = cipher.encrypt(xoredtext)                         
        start += 16
        ciphertext += encrypttext
    return ciphertext    

# XOR function for bytes
def byte_xor(var, key):
    return bytes(a ^ b for a, b in zip(var, key))
    
key = get_random_bytes(16)
iv = get_random_bytes(16)

cipher = AES.new(key, AES.MODE_ECB)

with open("mustang.bmp", "rb") as f:
  bitData = f.read()

#save header of bmp file (128 works on my mac)
header = bitData[0:128]
rest = bitData[128:]


#add header back on
cipherText = header + submit(rest)

with open("CBC_encoded_image.bmp", "wb") as f:
  f.write(cipherText)