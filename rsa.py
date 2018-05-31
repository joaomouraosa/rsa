#!/usr/bin/env python2
import random

def keygen(b):
    p = getPrimeNumber(b)
    q = getPrimeNumber(b)
    n = p*q
    m = (p-1)*(q-1)
    e = getCoprime(m)
    d = getModInverse(e, m)
    return (n,p,q,e,d)

def cipher(msg,n,e):
    blockSize = getBlockSize(n,0)-1
    blocks=splitInBlocks(msg,blockSize)
    
    blocksBase10 = map(lambda block :
                        int(''.join(map(str, block)),2)
                       ,blocks)
    
    cipherBlocks = map(lambda block :
                       cipherBlock(block,e,n)                      
                       ,blocksBase10)

    cipherMessage = []
    for block in cipherBlocks:        
        cipherMessage +=addZeros(convertToListBits(block), blockSize+1)
        
    return cipherMessage
    
def decipher(msg,n,d):
    lengthMsg  = len(msg)
    blockSize  = getBlockSize(n,0)
    k=0    
    blocks=[]
    
    for i in range(0,lengthMsg/blockSize):
        blocks.append(msg[k:k+blockSize])
        k+=blockSize
   
    blocksBase10 = map(lambda block :
                    int(''.join(map(str, block)),2)
                    ,blocks)
    
    cipherBlocks = map(lambda block :
                    cipherBlock(block,d,n)                      
                    ,blocksBase10)

    lim = cipherBlocks.pop(0)

    cipherMessage = []
    for block in cipherBlocks:        
        cipherMessage +=addZeros(convertToListBits(block), blockSize-1)

    return (cipherMessage[0:-lim])


def splitInBlocks(msg,blockSize):
    nBlocks = len(msg)/blockSize+1
    blocks=[]    
    header = convertToListBits(len(msg))
    k=0
    padding=0
    for i in range(0,nBlocks):
        if (i==nBlocks-1):
            padding= k+blockSize-len(msg)
            if (padding<0):
                padding=0

            blocks.append(msg[k:] + [random.randint(0,1) for x in range(padding)])
        else:
            blocks.append(msg[k:k+blockSize])
        k+=blockSize
    blocks[:0] = [addZeros(convertToListBits(padding), blockSize)]
    
    return blocks
 
def getCoprime(m):
    def gcd(arg1, arg2):
        while (arg2>0):
            tmp = arg1
            arg1= arg2
            arg2= tmp%arg2        
        return arg1

    while(True):
        e = random.randint(2,m)
        if (gcd(m,e)==1):
            return e
    return -1

def getBlockSize(n,exp):
    while(True):
        if ((2**(exp))>n):
            return exp
        else:
            exp+=1

def cipherBlock(a,b,n):
    val= 1
    while (b>0):
        if ((b%2)==1):
            val= (val*a)%n
        a = (a*a)%n
        b = b//2
    return val
    
def addZeros(lst, blockSize):
    n = blockSize-len(lst)
    return [0 for x in range(0,n)] + lst

def convertToListBits(n):
    text=list("{0:b}".format(n))
    val= list(map(lambda x: (ord(x)-48), text))
    return val

def getModInverse(arg1, arg2):
    a, d = 1,1
    b, c = 0,0
    n = arg2
    
    while (arg2 != 0):
        quo  = arg1//arg2
        tmp  = arg1
        arg1 = arg2
        arg2 = tmp % arg2
        tmpA = a
        tmpC = c
        a = b
        b = tmpA-quo*b
        c = d
        d = tmpC-quo*d
            
    if (arg1==1):
        return (a%n)

def getPrimeNumber(bits):
    lowerBound = 2**(bits/2)
    upperBound = 2**(bits/2+1)

    while(True):        
        n = random.randint(lowerBound,upperBound)
        if (fermatTest(n) and millerRabinTest(n)):
            return n
    return -1

def fermatTest(n):
    if (n==2):
	return True
    if ((n&1)==0):
	return False
    return (pow(2, n-1, n)==1)

def millerRabinTest(n):
    it=40
    r=0
    s=n-1

    while ((s%2)==0):
        r+= 1
        s= s//2
    
    for i in range(0,it):
        a = random.randint(2,n-1)
        x = pow(a,s,n)
        if (not((x==1) or (x==n-1))):
            j=0
            for j in range(0,r-1):
                x = pow(x,2,n)
                if (x==n-1):
                    break
            if (j==r-1):
                return False
    return True
