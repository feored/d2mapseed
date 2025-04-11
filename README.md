
# D2R Map Seed Tool

**Warning: Always back up your files before you start!**

This tool reads the map seed from a .d2s single-player file or writes a map seed in hex format into a .d2s file (as well as a valid new checksum).

Find a map with a good LK or Durance of Hate layout and save it for later use.

Alternatively, this script can also be useful for testing if you are modifying your .d2s files manually with a hex editor, as it can insert a new valid file size value and checksum in the header.

### Usage

#### Get map seed
    python d2mapseed.py "C:\Users\You\Saved Games\Diablo II Resurrected\Example.d2s"
    08939C62

Combined with --format dec to get it in decimal format:

    python d2mapseed.py "C:\Users\You\Saved Games\Diablo II Resurrected\Example.d2s" --format dec
    143891554

#### Insert map seed
    python d2mapseed.py --insert 08939C62 "C:\Users\You\Saved Games\Diablo II Resurrected\OtherExample.d2s" 

If your map seed is in decimal format (ex: 348294647), combine with --format option:

    python d2mapseed.py --insert 348294647 --format dec "C:\Users\You\Saved Games\Diablo II Resurrected\OtherExample.d2s" 

#### Repair file

Instead of writing a new map seed, you can generate a new checksum with the --checksum flag, and overwrite the size flag with a current value with --size:

    python d2mapseed.py "C:\Users\You\Saved Games\Diablo II Resurrected\Example.d2s"  --checksum --size
(Can be useful if you've been editing things manually and your save file seems broken.)





### Notes

* Tested on D2R and D2LoD v1.14d, won't work for <1.10

* Requires Python 3, no dependencies

* You can run the program and get a map seed while the game is running, but inserting a new seed will only work if the game is not running.

* Thanks to [krisives](https://github.com/krisives/d2s-format), [nokka](https://github.com/nokka/d2s) and others for information on the d2s file header and checksum algorithm.
 
