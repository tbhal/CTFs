# The Needle

### Description
As a part of our SDLC process, we've got our firmware ready for security testing. Can you help us by performing a security assessment?

### Procedure
* First checking the type of file we have
code: `file firmware.bin`
`firmware.bin: Linux kernel ARM boot executable zImage (big-endian)`
* Analyzing the file using binwalk
code: `binwalk -e firmware.bin`
* There are multiple files that are present in the extracted folder.
* When we try to connect with the the spawn machine using netcat we can see a login page comes up command: `nc <ip> <port>`
```��������
hwtheneedle-539595-694dd87777-5h74v login:
```
* It automatically times out after 60 seconds.
* As we have a login menu, we can try and look for some credentials or some files related to login, for this purpose we can use grep and look for every file and see if we can find something realted with login
`grep -rn "./" -e login`
What this command means is search in the current directory recursively and look expresseion which matches with "login".
```
-r : recursive
-n : line number
-e : patterns
```

`telnetd -l "/usr/sbin/login" -u Device_Admin:$sign	-i $lf &` This confirms that the user is **Device_Admin**

* Now that we have username we'll look for password, I ran the same command as above just replaced login with password to look for password but didn't get any result

* Then I looked properly I was missing something, in the above result that I have mentioned we can see that after adding user we are providing a file whose name is sign, so lets look for that.
`find ./ -name sign`
```
./squashfs-root/etc/config/sign
./sign
```
* Both files have same content which is **qS6-X/n]u>fVfAt!**

* Now that we have both username and password we can login and see what do we have at the machine
* We are able to login, and we can get the flag using `cat flag.txt`

## Thank you for reading
