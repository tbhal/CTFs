# RSAisEasy
### Description
I think this is safe... Right?

#### Understanding of the challenge
This challenge gives us two file one is RSAisEasy.py and the other is output.txt
Output file contains four things n1, c1, c2, and (n1*E) + n2

Coming to the python file
RSA encryption algorithm is implemented
p, q and z are derived using getPrime function in Crypto library
then we calculate n1 and n2 using those primes

then we calculate the cipher texts
```
c1 = flag ^ e (mod n1)
c2 = flag ^ e (mod n2)
```
E which is generated using urandom method which is used to generate a string of size random bytes

```
t = n1*E + n2
lets rewrite this equation
t = p*q*E + q*z
  = q * (p*E + z)
```
1. Obtaining q from the know equations
Now we can see that **q** is the common factor between **t** and **n1**, so we can calculate **gcd of t and n1 to get q**

2. After getting q we can get p from n1 using `p = n1 / q`.

3. Calculate z from the known equations and variables
let's take the bracket portion as "a" in the above equation
```
a = p*E + z
t = a*q
a = t/q
```
Now that we have both a and p we can now calculate z using modulus operation
`a mod p = (E*p + z) mod p => E*p mod p + z mod p => z mod p => z`

4. Calculating the private key, for that first we need to calculate `phi(n) = (n-1)*(q-1)`
This is how to we calculate private key in the RSA algorithm
`d = e^-1 mod phi(n)`

5. Decryption is done using this method
`decrptText = cipherText ^ d (mod n)`

Thats how we get the flag for this challenge.

## **Thank You for Reading!**
