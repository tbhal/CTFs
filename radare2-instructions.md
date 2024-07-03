# Radare2 commands

### General Commands
- shift + v -> This is used for seeing multiple views that are present, when we are inside the views we can use `p` to switch between multiple views. For going back to the previous view we use `shift + v`.
- navigation keys -> While in views we can use the navigation keys **up and down** to change the seek address.
- jumping to function: When our seek is at a point where a program is being called we can press `enter` to jump to that program. When we want to go back we press `u`.
- shift + (:colon) : We use this command to enter stuff for analysis like afl.
- afl -> Shows function list, Full form is **Access Function List**.When we don't get any output from this that means we haven't analyzed the binary yet. After the analysis is done then we can continue with this command. We can use `afll` for a more verbose version.
- aaa -> Analyzing the binary.
- s main -> Stands for seek main, that is we go to the main function.
- q -> To quit and go back to the original screen.

## Cross-reference
Checking where all does this function has been called in the code, for doing so we first `place our seek on the function and press enter` and after this we press "colon" and then type command `axt`. This will list out all the places where this function has been called. `axt' is for cross-reference to and `axf` is cross-reference from.

### Show import, exports, symbols, sections and strings
- i -> The infomration module, for checking all the operation that we can do we enter `i?` and this lists out the operations.
- ii -> Info about imports.
- iE -> Info about exports.
- iS -> Info about sections.
- is -> Info about symbols.
- iz -> Get all strings from data section.
- izz -> Get all strings from the binary.

### Getting General information about a binary using rabin2 and rafind2
The syntax is: **rabin2 <tag> <binary_we_want_to_analyze>**. See man page for more info.
- I -> Show binary info.
- H -> Show header fields.
- M -> Start address of main.
- z -> Dumps string from data section.
- zz -> Dumps string from the binary.

rafind2 is used for finding byte pattern in file.
The syntax is: **rafind2 <tag> <term_to_search> <binary_we_want_to_search_in>**.
- s -> Gives the address of the term we searched.
- S -> Wide string search

### Parse a header
- nn -> To load header structures(rbin) and applies to files.
- pf. -> Shows the pf headers available.
- pf.elf_header @ elf_header -> what happening over here is we are parsing the *pf.elf_header* structure at mempry address given by *elf_header* in the binary.

### Patching a binary
- w -> Open the binary in write mode `r2 -w ./binary`.
- aaa -> Analyze the binary.
- Check functions list and then seek to the required function.
- Allign seek to the instruction that we are trying to patch then press `shift + a`now we can enter our assembly code.
- Press `enter` we'll be asked if we want to confirm changes, press `y` to confirm.
- And we are done patching the binary.
- We can also use the write command that is `w` we can use 'w?` for more information on this command.

### Debugging binaries
- d -> To load the binary in debugging mode `r2 -d ./binary`
- e stack.size 256 -> Increasing the stack response size to 256 bytes
- F7/dsp -> Step into.
- F8 -> Step over.
- db -> Put a breakpoint `db function_name`
- dc -> Get to the function or in general *continue* command.
- do -> Reopen and reattach the program.
- dsf -> Step out.
- dsb -> Step back.

### Graph View Navigation and Writing comments
- VV : For going to grpah view.
- Navigating to connected functions we use some values that r2 gives while we see loop, like gf, gj etc we just type these and it directly jumps to that block of code.
- P or p -> For different type of views we can use `P or p`.
- x -> For cross-reference no need of typing axt.
- semi-colon(;) -> For entering a comment.

