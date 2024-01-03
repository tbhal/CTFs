# Protein-Cookies
- The taks is to login as a user and get the membership.

- In this challenge we are given a zip folder which contains all the files that are required to host and start a machine.

- There are multiple files so first going through them is important for understanding what is happening in the web.

## Understanding the code
- Some important files includes **routes.py**, **models.py** and **utils.py**.

- <ins>routes.py</ins>: Contains all the information that is required by the web to navigate around, we can also see from the code that the *flag.pdf* file that we need is accessible on `/program`.

- <ins>utils.py</ins>: Contians the logic that is used for site verification that is checking for login and view as guest functions.

- <ins>models.py</ins>: This is the most interesting code section present as we can see what does the class session and signature contains and performs. *verify_login* function calls *validate_login* function which calls *integrigty* function which itself calls the *create* function.
	> verify_login -> validate_login(session) -> integrity(signature) -> create(signature)
	- the create function uses sha512 for calculating the hexdigest.

- Now initially I had no idea what is the vulnerability here, being a crypto challenge I thought that it might have to do with some wrong usage of sha512, so started looking for weakness or attacks against sha512, then I came across **Hash Extension Attack**.

- After reading about the attack it made total sense why the code is written in such a way

## Hash Extension Attack

- I'll be going though the attack in brief but we these two articles are well written for understanding the attack - [Medium](https://slowmist.medium.com/the-hidden-risks-of-hash-functions-length-extension-attacks-and-server-side-security-158b131f374a), [SkullSecurity](https://www.skullsecurity.org/2012/everything-you-need-to-know-about-hash-length-extension-attacks).

- This attack exploits the fact given the hash(message) and the length of the hash then the attacker can calculate hash(message || padding || new-message).

- Example:
```
	let secret = "secret"
	let data = "data"
	let H = md5()
	let signature = hash(secret || data) = 6036708eba0d11f6ef52ad44e8b74d5b
	let append = "append"

	The server sends data and signature to the attacker.
	Knowing only data, H, and signature, the attacker's goal is to append append to data and generate a valid signature for the new data. And that's easy to do! Let's see how.
```
Taken from SkullSecurity

- This attack is possible due to the algorithm that is being used to construct these hashes which is **Merkle Damgard Construction**. What happens is the message is divided into multiple blocks and the hash value of each block is dependent on the hash of previous block as well.
- Means after we complete calculating hash till a certain length then we have a state from where we can start adding new blocks. But one thing that we have to keep check is the padding that we add.

- Good thing is the medium blog explains this attack in terms of web very well.

- Mechanism:
```
    1. Append a “1” bit at the end of the data;

    2. Add a certain number of “0” bits so that the length of the data mod 512 equals 448;

    3. Finally, append a 64-bit block indicating the length of the original data.
```
This is for sha-256

## Attack and Get the flag
- For our attack purpose we are going to use [hash extender](https://github.com/iagox86/hash_extender) tool.
- We can get the cookie by accessing the web, there are two portion in the cookies first section before a '.' is the part for the userId and isLoggedIn flag and the rest is the value.
	- tried changing the value from false to true and then sending it with the hash value but that didn't work.


- After reading about the attack we know that we need the hashed message and the length is known to us, we got hashed message from cookie and the secret length is 16, this we can see in models.py
```
cookie after decoding
username=guest&isLoggedIn=False.39b3eb0eb29affbef4cbc28c01021750691a13b34cfd3ea941897468c8d18c1bad8d27639d09161eae4a383a1a88f505659c0177b0f156655e3edf4b58eab742
The value that we want to append isLoggedIn=True
our hash value: 39b3eb0eb29affbef4cbc28c01021750691a13b34cfd3ea941897468c8d18c1bad8d27639d09161eae4a383a1a88f505659c0177b0f156655e3edf4b58eab742
secret length: 16
hash type: sha-512
```

- Command executed for executing hash_extender
```sh
./hash_extender -d "username=guest&isLoggedIn=False" -s "39b3eb0eb29affbef4cbc28c01021750691a13b34cfd3ea941897468c8d18c1bad8d27639d09161eae4a383a1a88f505659c0177b0f156655e3edf4b58eab742" -a "&isLoggedIn=True" -l 16 -f sha512
Type: sha512
Secret length: 16
New signature: cbdeb369d78c78fb128cc7b0a90a651d7122ff6d266f297822983a8c97848a13142751813a073b4c574be1c90ef8035d53eb78edb472f85570120f07bca51eb6
New string: 757365726e616d653d67756573742669734c6f67676564496e3d46616c73658000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001782669734c6f67676564496e3d54727565
```

- Now we have to club them together in a specific format that the web accepts, means first take the hex in new string convert it into bytes and then append that base64 encoded secret
`b64encode(data) + b"." + secret`

```python
>> from base64 import b64encode
>> data = bytes.fromhex('757365726e616d653d67756573742669734c6f67676564496e3d46616c73658000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001782669734c6f67676564496e3d54727565')
>> secret = b64encode('cbdeb369d78c78fb128cc7b0a90a651d7122ff6d266f297822983a8c97848a13142751813a073b4c574be1c90ef8035d53eb78edb472f85570120f07bca51eb6'.encode())
>> b64encode(data) + b"." + secret
b'dXNlcm5hbWU9Z3Vlc3QmaXNMb2dnZWRJbj1GYWxzZYAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABeCZpc0xvZ2dlZEluPVRydWU=.Y2JkZWIzNjlkNzhjNzhmYjEyOGNjN2IwYTkwYTY1MWQ3MTIyZmY2ZDI2NmYyOTc4MjI5ODNhOGM5Nzg0OGExMzE0Mjc1MTgxM2EwNzNiNGM1NzRiZTFjOTBlZjgwMzVkNTNlYjc4ZWRiNDcyZjg1NTcwMTIwZjA3YmNhNTFlYjY='
```

- Now we can use this cookie on the web and then navigate to the */program* section for getting the flag.

### Thank you for reading.
