
# D2R Map Seed Tool

## Warning: Always back up your files before you start!

This tool can read the map seed from a .d2s single-player file or load a map seed in hex format into a .d2s file (as well as a valid new checksum).

Find a map with a good LK or Durance of Hate layout and save it for later use. 

## Usage

#### Get map seed:
    python d2mapseed.py "C:\Users\You\Saved Games\Diablo II Resurrected\Example.d2s"

Result:

    Map seed: 08939C62

#### Insert map seed:
    python d2mapseed.py --insert 08939C62 "C:\Users\You\Saved Games\Diablo II Resurrected\OtherExample.d2s" 

#### Only generate new checksum:
    python d2mapseed.py "C:\Users\You\Saved Games\Diablo II Resurrected\Example.d2s"  --c 
(Can be useful if you've been editing things manually and your save file seems broken.)





### Notes

* Only tested with D2R.

* Requires Python 3, no dependencies

* You can run the program and get a map seed while the game is running, but inserting a new seed will only work if the game is not running.

* Thanks to [krisives](https://github.com/krisives/d2s-format), [nokka](https://github.com/nokka/d2s) and others for information on the d2s file header and checksum algorithm.
 