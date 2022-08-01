# TMX duplicates Cleaner

## Short Description

The first programm "tmx_cleanup.py" will find all duplicates in a given TMX file and output a cleaned TMX Files and a TAB seperated CSV with all semi duplicates.
So you can work out which translations are not necessary anymore.
Save all the not nexessary IDs in a TAB seperated txt file (Excel is helpful) and use the second programm "delete_segments_by_tuids.py".
Select the TMX file that has to be cleaned from the semi duplicates. Select the TXT file with all the IDs that should be deleted.
As Output you get a new TMX file without the semi duplicates.

### tmx_cleanup.py

It will delete all duplicates, write out a txt file with found duplicates and a new TMx file, without duplicates. One (the first found) of duplicates will not be deleted.
It also create a CSV file (Delimiter TAB) with all found semi duplicates.

Input TMX Format

- Encoding: UTF-8
- XML Version: 1.0
- TMX Version: 1.4

### delete_segments_by_tuids.py

It will delete all nodes (imported by TXT file) where the ID is found in the imported List.
It will create a new TMX File without all imported IDs.

Input CSV Format

- Encoding: UTF-8
- Delimiter: TAB (\t)
- Extension: .txt
- Header: ID    Lang_1 (e.g: en_US)    Lang_2 (e.g:de_DE)
- Rows: 9LASxy3fxC34qd91O80Qksps4    You are welcome.    Gern geschehen.

## Folder Structure

- input (the programms will search this folder for the input files)
- lib (programm helpful files)
- output (all the generated files will copied here)

### Python Version tested

- 3.9.6

## Note

When importing the semi_duplicates.csv in Excel select the UTF-8 Encoding.
When saving the file as TAB seperated TXT File (for input), then "Save as" the file and select as file type the .txt file with TAB seperated.
