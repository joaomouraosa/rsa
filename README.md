# rsa
Module implementing RSA to cipher/decipher a list of bits in ECB mode.

# keygen(b)
- returns a public key with b bits. 

# cipher(msg, n , e)
- ciphers msg with the public key (n, e).

# decipher(msg, n, d)
- deciphers msg with the private key (n, d).

