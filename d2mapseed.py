from pathlib import Path
import ctypes
import argparse
import sys

OFFSET_CHECKSUM_START   = 12
OFFSET_CHECKSUM_END     = 16
OFFSET_MAP_SEED_START   = 171
OFFSET_MAP_SEED_END     = 175

D2S_FILE_SIGNATURE      = b'\x55\xAA\x55\xAA'


def getFileData(filename):
    fileData = []
    with open(filename, 'rb') as f:
        fileData = f.read()
    return fileData

def calcChecksum(data):
    checksum = 0
    for i in range(len(data)):
        ch = data[i]
        if (i >= OFFSET_CHECKSUM_START and i < OFFSET_CHECKSUM_END):
            ch = 0
        checksum = ctypes.c_int32((checksum << 1) + ch + ctypes.c_int32(checksum < 0).value).value
    return checksum

def getChecksum(filename):
    checksum = calcChecksum(getFileData(filename))
    return checksum.to_bytes(4, byteorder='little', signed = True).hex().upper()

def writeChecksum(filename, checksum):
    with open(filename, 'r+b') as f:
        f.seek(OFFSET_CHECKSUM_START)
        f.write(bytes.fromhex(checksum))
        
def getMapSeed(filename):
    return getFileData(filename)[OFFSET_MAP_SEED_START:OFFSET_MAP_SEED_END].hex().upper()

def writeMapSeed(filename, seed):
    with open(filename, 'r+b') as f:
        f.seek(OFFSET_MAP_SEED_START)
        f.write(bytes.fromhex(seed))

def isValidFile(filename):
    if not filename.exists():
        return False
    if not str(filename).lower().endswith("d2s"):
        return False
    with open(filename, 'rb') as f:
        signature = f.read(4)
        if signature != D2S_FILE_SIGNATURE:
            return False
    return True

def insertChecksum(filename):
    checksum = getChecksum(filename)
    writeChecksum(filename, checksum)
    return checksum
    
    

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
        sys.exit(f"Path {args.filename} is not a valid .d2s file.")
        
    if args.insert:
        newSeed = args.insert
        if args.format and args.format == "dec":
            if not newSeed.isnumeric():
                sys.exit("Input seed is invalid (must contain only numbers).")
            newSeed = str(int(newSeed).to_bytes(4, byteorder='big', signed = True).hex().upper())
        if len(newSeed) != 8 or not newSeed.isalnum():
            sys.exit("Input seed is invalid.")
        writeMapSeed(d2sfile, newSeed)
        print(f"Inserted seed: {args.insert}")
        insertChecksum(d2sfile)
    elif args.checksum:
        newChecksum = insertChecksum(d2sfile)
        print(f"Generated new checksum: {newChecksum}")
    else:
        mapSeed = getMapSeed(d2sfile)
        if args.format and args.format == "dec":
            mapSeed = int(mapSeed, 16)
        print(f"Map seed: {mapSeed}")

if __name__ == "__main__":
    main()
