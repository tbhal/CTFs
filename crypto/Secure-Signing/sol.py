from pwn import string, connect
from hashlib import sha256

host, port = "188.166.175.58:30307".split(":")
ins = connect(host, port)
flag = "HTB{"
counter = 4

progress_report = ins.progress(flag)


def brute(flag_part):
	ins.sendlineafter(b">", b"1")   # sending message in bytes
	ins.sendlineafter(b":", b"\x00" * (counter + 1))
	hash_val = ins.recvuntil(b"\n").strip().split()[-1].decode()

	for char in string.printable:
		# test the hash value of flag + char aginst the main hash obtained above
		hash_char = sha256((flag_part + char).encode()).hexdigest()
		if hash_char == hash_val:
			return flag + char
			break

	return flag_part

# the flag always closes on }
while "}" not in flag:
	flag = brute(flag)
	progress_report.status(flag)

ins.close()