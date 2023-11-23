from pwn import *
import binascii
import math

r = remote('mercury.picoctf.net', 28517)
r.recvlines(4)

r.recvuntil(b'n: ')
n = int(r.recvline().strip())

r.recvuntil(b'e: ')
e = int(r.recvline().strip())

r.recvuntil(b'ciphertext: ')
cipher = int(r.recvline().strip())

payload = cipher * pow(3, e, n)

r.sendlineafter(b'Give me ciphertext to decrypt: ', str(payload))
r.recvuntil(b'Here you go: ')
combined_plain = int(r.recvline().strip())

pt_hex = hex(combined_plain // 3)[2:]
pt_bytes = bytes.fromhex(pt_hex)
print("Flag: ", pt_bytes.decode())

r.close()