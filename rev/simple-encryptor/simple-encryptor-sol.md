# Simple-Encryptor

1. We are given two files with this challenge, encrypt and flag.enc, a little description about the files using the `file` command
```
encrypt: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=0bddc0a794eca6f6e2e9dac0b6190b62f07c4c75, for GNU/Linux 3.2.0, not stripped

flag.enc: data
```

2. Next we used Ghidra to decompile the program, for having a better understanding of what we are dealing with.

3. The code had weird naming convention, so the first task now was to convert it something that we can understand.

~~~ 
undefined8 main(void)

{
  int random1;
  time_t tVar1;
  long in_FS_OFFSET;
  uint seed;
  uint random2;
  long i;
  FILE *flag_file;
  size_t flag_size;
  void *flag;
  FILE *encrypted_flag_file;
  long fs;
  
  fs = *(long *)(in_FS_OFFSET + 0x28);
  flag_file = fopen("flag","rb");
  fseek(flag_file,0,2);
  flag_size = ftell(flag_file);
  fseek(flag_file,0,0);
  flag = malloc(flag_size);
  fread(flag,flag_size,1,flag_file);
  fclose(flag_file);
  tVar1 = time((time_t *)0x0);
  seed = (uint)tVar1;
  srand(seed);
  for (i = 0; i < (long)flag_size; i = i + 1) {
    random1 = rand();
    *(byte *)((long)flag + i) = *(byte *)((long)flag + i) ^ (byte)random1;
    random2 = rand();
    random2 = random2 & 7;
    *(byte *)((long)flag + i) =
         *(byte *)((long)flag + i) << (sbyte)random2 |
         *(byte *)((long)flag + i) >> 8 - (sbyte)random2;
  }
  encrypted_flag_file = fopen("flag.enc","wb");
  fwrite(&seed,1,4,encrypted_flag_file);
  fwrite(flag,1,flag_size,encrypted_flag_file);
  fclose(encrypted_flag_file);
  if (fs != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return 0;
}
~~~

4. There are 4 phases of this code
    - First reading the flag file
    - Initializing the srand value
    - Encrypting the value in the flag file
    - storing the result in the **flag.enc** file

5. The tough part in reversing this code is having that srand that the code generated using the **seed** value, but good for us that while storing the result into the flag file we can see srand vlaue being stored in the first 4 bytes
> fwrite(&seed,1,4,encrypted_flag_file);

6. Now starting with the encryption logic, the simplified logic from the above code is
```
random1 = rand()
flag = flag ^ random1
random2 = rand()
flag = flag << random2 | flag >> (8 - random2)
```

7. The reversed version of this will look like
```
random1 = rand()
random2 = rand()
encFlag = encFlag >> random2 | encFlag << (8 - random2)
flag = encFlag ^ random1
```

8. Run the sol file using gcc for getting the flag.

### Thank you for reading.
