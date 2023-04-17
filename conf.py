from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import urllib.parse
import math
from cbc import byte_xor

def pad(data):
    numBlocks = math.ceil(len(data)/float(16))
    padValue = int(numBlocks * 16 - len(data)) # value determines -> 01, 02 02, 03 03 03, etc..

    if padValue == 0:
        return data + (16).to_bytes() * 16
    else:
        return data + (padValue).to_bytes() * padValue

#generate random key and iv (thats used in both submit and verify function)
key = get_random_bytes(16)
iv = get_random_bytes(16)
cipher = AES.new(key, AES.MODE_ECB)

def submit(input):
    newstring = 'userid=456;userdata='
    parsedinput = urllib.parse.quote(input)     #URL encode user input
    newstring += parsedinput
    print(newstring[24])
    newstring += ';session-id=31337'
    bytestring = bytes(newstring, 'utf-8')
    bytestring = pad(bytestring)
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

def verify(input):
    ciphertext = input[:16]
    decrypttext = cipher.decrypt(ciphertext)
    plaintext = byte_xor(iv, decrypttext)       #xor first decrypt text with iv to get first plaintext
    prevcipher = ciphertext                     #save ciphertext as prev cipher to xor following decrypt texts

    start = 16
    #Do CBC decrypt on rest of plaintext using prev ciphertext to xor deceypt texts to get plaintext
    for i in range((len(input) // 16) -1):
        ciphertext = input[start:start+16]
        decrypttext = cipher.decrypt(ciphertext)
        plaintext += byte_xor(prevcipher, decrypttext)
        prevcipher = ciphertext
        start += 16

    plaintext = str(plaintext)
    print(plaintext)
    if ";admin=true;" in plaintext:
        return True
    else:
        return False


#input that you can easily flip two bits to make ;admin=true;
cipherres = (submit("flipmadminetrue"))

#these two lines do A xor B xor C
changedchar = byte_xor((cipherres[8]).to_bytes(), bytes('m', 'utf-8'))
changedchar = byte_xor(changedchar, bytes(';', 'utf-8'))

secondchar = byte_xor((cipherres[14]).to_bytes(), bytes('e', 'utf-8'))
secondchar = byte_xor(secondchar, bytes('=', 'utf-8'))

#adds two flipped bits into previous cipher text
newciphertext = cipherres[:8]
newciphertext += changedchar
newciphertext += cipherres[9:14]
newciphertext += secondchar
newciphertext += cipherres[15:]

newplaintext = verify(newciphertext)
print(newplaintext)