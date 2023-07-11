from pathlib import Path
import ctypes
import argparse
import sys


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
    return filename.exists() and str(filename).lower().endswith("d2s")

def insertChecksum(filename):
    checksum = getChecksum(filename)
    writeChecksum(filename, checksum)
    print(f"Generated new checksum: {checksum}")
    

def main():
    parser = argparse.ArgumentParser(
    prog="d2mapseed",
    description="Save or load map seeds for D2R."
    )
    
    parser.add_argument("filename", help="location of .d2s file that you wish to read/modify", type=str)
    parser.add_argument("-i", "--insert", help="insert a given map seed in .d2s file", type=str)
    parser.add_argument("-c", "--checksum", help="only insert valid checksum for .d2s file", action="store_true")
    parser.add_argument("-f", "--format", help="pick which format to use for the map seed")

    args = parser.parse_args()
    d2sfile = Path(args.filename)

    if not isValidFile(d2sfile):
        print(f"Path {args.filename} is not a valid .d2s file.")
        sys.exit()
    
    if args.insert:
        newSeed = args.insert
        if args.format == "dec":
            newSeed = str(int(newSeed).to_bytes(4, byteorder='big', signed = True).hex().upper())
        writeMapSeed(d2sfile, newSeed)
        print(f"Inserted seed: {args.insert}")
        insertChecksum(d2sfile)
    elif args.checksum:
        insertChecksum(d2sfile)
    else:
        mapSeed = getMapSeed(d2sfile)
        if args.format and args.format == "dec":
            mapSeed = int(mapSeed, 16)
        print(f"Map seed: {mapSeed}")

if __name__ == "__main__":
    main()
