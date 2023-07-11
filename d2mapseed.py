import ctypes
from pathlib import Path

def getFileData(fileName):
    fileData = []
    with open(fileName, 'rb') as f:
        fileData = f.read()
    return fileData

def calcChecksum(data):
    checksum = 0
    for i in range(len(data)):
        ch = data[i]
        if (i >= 12 and i < 16):
            ch = 0
        checksum = ctypes.c_int32((checksum << 1) + ch + ctypes.c_int32(checksum < 0).value).value
    return checksum

def getChecksum(fileName):
    checksum = calcChecksum(getFileData(fileName))
    return checksum.to_bytes(4, byteorder='little', signed = True).hex()

def writeChecksum(fileName, checksum):
    with open(fileName, 'r+b') as f:
        f.seek(12)
        f.write(bytes.fromhex(checksum))
        
def getMapSeed(fileName):
    return getFileData(fileName)[171:175].hex()

def insertMapSeed(fileName, seed):
    with open(fileName, 'r+b') as f:
        f.seek(171)
        f.write(bytes.fromhex(seed))

