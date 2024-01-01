# Secure Signing

- In the challenge we are given one python script which tells us how the signing algorithm is working.

## Understanding the code

- There are two choices that we get when interacting with the code, Sign our Message and verify our message.
- The algo written uses combination of xor and sha256 digest.
- One major thing that we should note about the xor function is how it's tackling the length of the two inputs that are being given to it, right how the xor operation would happen when the length of the inputs are not same.
- The xor function is using a `zip` which is ensures that both iterables are of same length
```python
if len(a) < len(b):
	b = b[:len(a)]
if len(a) > len(b):
	a = a[:len(b)]
```
- Ok so now we know how the variable length is being handled, now how to get the flag, where is the vulnerability.

## Understanding the attack

- The script is vulnerable due the **Identity Element** property of xor operation that is `a xor 0 = a`.
- So what we can do is pass variable length of `b"\x00"` and check the resultnat hash if it's correct or not, first checking if this approach works or not.
- We know that our flag starts from HTB{, so what we can do for POC is pass this part of the flag to the server get the hash and check if our attack actually works that is initally we'll pass `b"\x00" * 1` for comparison with 'H' then `b"\x00" * 2` for comparison with 'HT' and then `b"\x00" * 3` for 'HTB'.

```python
from pwn import xor, connect
from hashlib import sha256

host, port = "replace-with-your-connection".split(":")
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
```
```sh
[+] Opening connection to 188.166.175.58 on port 30307: Done
Test H: True
Test HT: True
Test HTB: True
[*] Closed connection to 188.166.175.58 port 30307
```

## Solution
- We see that our POC works means the Identity Element xor operation is our cue to attack, after this the main thing is how we compare.
- We are going to write a brute force solution which contains comapres all the elements present under strings.printable.
- Solution will start with only one letter flag: "HTB{", whenever we pass the `b"\x00"` it will always be of length flag and the moment we hit a match we will add that value in the flag and add one in counter
- The bruteforce method will run until we reach the end of the flag, this will be indicated when we reach "}" as that's the usual structure of the flag.

```python
from pwn import string, connect
from hashlib import sha256

host, port = "188.166.175.58:30307".split(":")
ins = connect(host, port)
flag = "HTB{"
counter = 4

progress_report = ins.progress(flag)


def brute(flag_part):
	# nonlocal counter
	ins.sendlineafter(b">", b"1")   # sending message in bytes
	ins.sendlineafter(b":", b"\x00" * (len(flag_part) + 1))
	hash_val = ins.recvuntil(b"\n").strip().split()[-1].decode()

	for char in string.printable:
		# test the hash value of flag + char aginst the main hash obtained above
		hash_char = sha256((flag_part + char).encode()).hexdigest()
		if hash_char == hash_val:
			# counter += 1
			return flag + char
			break

	return flag_part

# the flag always closes on }
while "}" not in flag:
	flag = brute(flag)
	progress_report.status(flag)

ins.close()
```

> This takes some time due to the brute force approach and amount of comparisons being done.

### Credit
I would like to Thank Pyp, he helped me in solving this challenge, logic and code wise. He is a great Cryptographer, Programmer, Pro-Hacker, he has his blogs as well, interested can check them out [here](https://pyp-s-blog.web.app/)