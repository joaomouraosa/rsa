# rsa
Module implementing RSA to cipher/decipher a list of bits in ECB mode.

## keygen(b)
- returns the b length public and private key pairs.

## cipher(msg, n , e)
- ciphers msg with the public key.

## decipher(msg, n, d)
- deciphers msg with the private key.

