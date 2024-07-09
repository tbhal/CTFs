# Binary Heaven
- For this challenge we are given two files angel_A and angel_B.
- Starting with angel_A
```sh
file angel_A
angel_A: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=90a71dbbf2c94dc164a49328fb82f8fa914a9701, for GNU/Linux 3.2.0, not stripped
```
- Loading the file in r2 for analysis `r2 -A -d angel_A` or we can directly load the file and then use `aaa` option for analyzing the binary further.
```sh
afl ; for checking function present
0x5648a8cd5030    1      6 sym.imp.puts
0x5648a8cd5040    1      6 sym.imp.printf
0x5648a8cd5050    1      6 sym.imp.fgets
0x5648a8cd5060    1      6 sym.imp.ptrace
0x5648a8cd5070    1      6 sym.imp.exit
0x5648a8cd5080    1      6 sym.imp.__cxa_finalize
0x5648a8cd5090    1     42 entry0
0x5648a8cd7fe0    5   4130 reloc.__libc_start_main
0x5648a8cd50c0    4     34 sym.deregister_tm_clones
0x5648a8cd50f0    4     51 sym.register_tm_clones
0x5648a8cd5130    5     50 sym.__do_global_dtors_aux
0x5648a8cd5170    1      5 sym.frame_dummy
0x5648a8cd5000    3     23 sym._init
0x5648a8cd52c0    1      1 sym.__libc_csu_fini
0x5648a8cd52c4    1      9 sym._fini
0x5648a8cd5260    4     93 sym.__libc_csu_init
0x5648a8cd5175    8    225 main

pdf @sym.main (showing the content of the main function)
-------------------------snip---------------------------
0x5648a8cd51f3      eb48           jmp 0x5648a8cd523d
│      ┌──> 0x5648a8cd51f5      8b45fc         mov eax, dword [var_4h]
│      ╎│   0x5648a8cd51f8      4898           cdqe
│      ╎│   0x5648a8cd51fa      488d148500..   lea rdx, [rax*4]
│      ╎│   0x5648a8cd5202      488d05572e..   lea rax, obj.username   ; 0x5648a8cd8060 ; U"kym~humr"
│      ╎│   0x5648a8cd5209      8b1402         mov edx, dword [rdx + rax]
│      ╎│   0x5648a8cd520c      8b45fc         mov eax, dword [var_4h]
│      ╎│   0x5648a8cd520f      4898           cdqe
│      ╎│   0x5648a8cd5211      0fb64405f3     movzx eax, byte [rbp + rax - 0xd]
│      ╎│   0x5648a8cd5216      83f004         xor eax, 4
│      ╎│   0x5648a8cd5219      0fbec0         movsx eax, al
│      ╎│   0x5648a8cd521c      83c008         add eax, 8
│      ╎│   0x5648a8cd521f      39c2           cmp edx, eax
│     ┌───< 0x5648a8cd5221      7416           je 0x5648a8cd5239
│     │╎│   0x5648a8cd5223      488d3d560e..   lea rdi, str.e_31m_nThat_is_not_my_username_e_0m ; 0x5648a8cd6080
│     │╎│   0x5648a8cd522a      e801feffff     call sym.imp.puts       ; int puts(const char *s)
│     │╎│   0x5648a8cd522f      bf00000000     mov edi, 0
│     │╎│   0x5648a8cd5234      e837feffff     call sym.imp.exit       ; void exit(int status)
│     └───> 0x5648a8cd5239      8345fc01       add dword [var_4h], 1
-------------------------snip------------------------------
```
- In this code we can see that we have a loop which takes the value from a location (0x5648a8cd8060) and the xors with 4 and at end adds 8 to the digit
- Checking the content at that location
```sh
px @ 0x5648a8cd8060
- offset -      6061 6263 6465 6667 6869 6A6B 6C6D 6E6F  0123456789ABCDEF
0x5648a8cd8060  6b00 0000 7900 0000 6d00 0000 7e00 0000  k...y...m...~...
0x5648a8cd8070  6800 0000 7500 0000 6d00 0000 7200 0000  h...u...m...r...
```
- So these are the values that we have to take into consideration for getting our username this we'll do by a small python code
``` python
items = [0x6b, 0x79, 0x6d, 0x7e, 0x68, 0x75, 0x6d, 0x72]
username = ""
for item in items:
    username += chr((item - 8) ^ 4)
print(username)
```
- And with this we have our username
- Moving to angel_B as there is nothing more present in angel_A binary
```sh
file angel_B
angel_B: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), statically linked, Go BuildID=Xd_LgpWItJBNJmN63lQy/oWW_4FYae77KCrbbrcIX/2pmyS7gUszdXBsoOAYWo/PyEjnQ2VYI7PIdiOmGXg, not stripped
```
- Load the binary to r2 for analysis `r2 -A -d angel_B`, while checking the main function there was a very weird comment present there, it seemed like it's the password for our user so as to login to the machine
```
"GOg0esGrrr!IdeographicMedefaidrinNandinagariNew_Tai_LueOld_PersianOld_SogdianPau_Cin_HauSignWritingSoft_DottedWarang_CitiWhite_"
```
- The first part is the password for the server login.
