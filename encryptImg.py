# -*- coding: utf-8 -*-
"""
Created on Fri Sep 14 21:15:20 2018

@author: beniz
"""

import cv2
import math
import bitarray as bta

def imageLoader(path):
    img = cv2.imread(path)
    return img

def imageSize(img):
    size = img.shape
    return size

def setBit(num, bit, index = 0):
    mask = 1 << index
    num &= ~mask
    if(bit == 1):
        num |= mask
    return num

def getBit(num, index = 0):
    mask = 1 << index
    bit = num & mask
    return bit

def stringLen(strBitArry, maxLen):
    '''
     the function returns the amount of bits in the string
     and a list that contain the binary representation of
     the bits amount
     '''
    strLen = len(strBitArry)
    if(strLen > int(math.pow(2,maxLen) - 1)):
        return 1
    binLenStr = bin(strLen)[2:]
    binLen = []
    for i in binLenStr:
        binLen.append(int(i))
    while(len(binLen) < maxLen):
        # padding with zeros
        binLen.insert(0,0)
    return binLen, strLen

def readLen(img, row, col, maxLen):
    bitList = []
    i, j, k = 0, 0, 0
    while (len(bitList) < maxLen):
        bitList.append(getBit(img[i,j,k]))
        if(k < 2):
            k += 1
        else:
            k = 0
            if(j < (col - 2)):
                j += 1
            else:
                j = 0
                if(i < (row - 2)):
                    i += 1
                else:
                    return 0
    strLen = 0
    for bit in bitList:
        strLen = (strLen << 1) | bit
    return strLen, i, j, k

def maxMessageLen(row, col, strLen, maxLen):
    totalNumOfBits = row * col * 3
    numOfBitsForData = totalNumOfBits - (maxLen + 3)
    if (strLen > numOfBitsForData):
        return 1
    return 0
    

def readStr(img, row, col, strLen, i, j, k):
    bitList = []
    while (len(bitList) < strLen):
        bitList.append(getBit(img[i,j,k]))
        if(k < 2):
            k += 1
        else:
            k = 0
            if(j < (col - 1)):
                j += 1
            else:
                j = 0
                if(i < (row - 1)):
                    i += 1
                else:
                    return 0
    message = bta.bitarray(bitList).tobytes().decode('utf-8')
    return message 

def setLen(img, row, col, strLen):
    i, j, k = 0, 0, 0
    for bit in strLen:
        img[i,j,k] = setBit(img[i,j,k], bit)
        if(k < 2):
            k += 1
        else:
            k = 0
            if(j < (col - 1)):
                j += 1
            else:
                j = 0
                if(i < (row - 1)):
                    i += 1
                else:
                    return 1
    return i, j, k

def setStr(img, row, col, strBitArry, i, j, k):
        for bit in strBitArry:
            img[i,j,k] = setBit(img[i,j,k], bit)
            if(k < 2):
                k += 1
            else:
                k = 0
                if(j < (col - 1)):
                    j += 1
                else:
                    j = 0
                    if(i < (row - 1)):
                        i += 1
                    else:
                        print("i= ", i, "row= ", row, "k= ", k)
                        return 1
        return 0
    
def setMessage(path, message, newName, maxLen = 16):
    '''
    Hide a message in the image.
    The length of the message is limited to (2^maxLen-1).
    The method creates a new image and doesn't change the given one.
    '''
    error = 0
    img = imageLoader(path)
    imgSize = imageSize(img)
    row = imgSize[0]
    col = imgSize[1]
    strBitArry = bta.bitarray()
    strBitArry.frombytes(message.encode('utf-8'))
    strLen = stringLen(strBitArry, maxLen)
    if(strLen == 1):
        print("maxLen is too small")
    error = maxMessageLen(row, col, strLen[1], maxLen)
    if(error == 1):
        print("maxLen Error")
        return  
    i, j, k = setLen(img, row, col, strLen[0])
    error = setStr(img, row, col, strBitArry, i, j, k)
    cv2.imwrite(newName + '.png',img)
    if(error == 1):
        print("setStr Error")
    
def getMessage(path, maxLen = 16):
    '''
    Get the hidden message from the given image.
    The maxLen argument must be the same one used with
    the setMessage method.
    '''
    img = imageLoader(path)
    imgSize = imageSize(img)
    row = imgSize[0]
    col = imgSize[1]
    strLen, i, j, k = readLen(img, row, col, maxLen)
    message = readStr(img, row, col, strLen, i, j, k)
    return message
    
    
    
    




    
        
        
            
    
    


    
    
    