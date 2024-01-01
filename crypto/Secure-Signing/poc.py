from pwn import xor, connect
from hashlib import sha256

host, port = "188.166.175.58:30307".split(":")
ins = connect(host, port)
flag = b"HTB{"

# Part 1 for H
h_part = flag[:1]
ins.sendlineafter(b">", b"1")   # sending message in bytes
ins.sendlineafter(b":", b"\x00" * 1)
hash1 = ins.recvuntil(b"\n").strip().split()[-1].decode()
print(f"Test H: {hash1 == sha256(h_part).hexdigest()}")

# Part 1 for HT
ht_part = flag[:2]
ins.sendlineafter(b">", b"1")   # sending message in bytes
ins.sendlineafter(b":", b"\x00" * 2)
hash2 = ins.recvuntil(b"\n").strip().split()[-1].decode()
print(f"Test HT: {hash2 == sha256(ht_part).hexdigest()}")

# Part 1 for HTB
htb_part = flag[:3]
ins.sendlineafter(b">", b"1")   # sending message in bytes
ins.sendlineafter(b":", b"\x00" * 3)
hash3 = ins.recvuntil(b"\n").strip().split()[-1].decode()
print(f"Test HTB: {hash3 == sha256(htb_part).hexdigest()}")

ins.close()