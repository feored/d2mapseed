import ctypes
import argparse
import sys
from pathlib import Path

def getFileData(filename):
    fileData = []
    with open(filename, 'rb') as f:
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

def getChecksum(filename):
    checksum = calcChecksum(getFileData(filename))
    return checksum.to_bytes(4, byteorder='little', signed = True).hex().upper()

def writeChecksum(filename, checksum):
    with open(filename, 'r+b') as f:
        f.seek(12)
        f.write(bytes.fromhex(checksum))
        
def getMapSeed(filename):
    return getFileData(filename)[171:175].hex().upper()

def writeMapSeed(filename, seed):
    with open(filename, 'r+b') as f:
        f.seek(171)
        f.write(bytes.fromhex(seed))

def isValidFile(filename):
    return filename.lower().endswith("d2s")

def insertChecksum(filename):
    checksum = getChecksum(filename)
    writeChecksum(filename, checksum)
    print(f"Generated new checksum: {checksum}")
    

def main():
    parser = argparse.ArgumentParser(
    prog="d2mapseed",
    description="Save or load map seeds for D2R."
    )
    parser.add_argument("filename", help="location of .d2s file that you wish to read/modify",
                    type=str)
    
    parser.add_argument("-i", "--insert", help="insert a given map seed in .d2s file", type=str)
    parser.add_argument("-c", "--checksum", help="only insert valid checksum for .d2s file", action="store_true")

    args = parser.parse_args()

    if not isValidFile(args.filename):
        print(f"Path {args.filename} is not a valid .d2s file.")
        sys.exit()
    
    if args.insert:
        writeMapSeed(args.filename, args.insert)
        print(f"Inserted seed: {args.insert}")
        insertChecksum(args.filename)
    elif args.checksum:
        insertChecksum(args.filename)
    else:
        mapSeed = getMapSeed(args.filename)
        print(f"Map seed: {mapSeed}")

if __name__ == "__main__":
    main()
