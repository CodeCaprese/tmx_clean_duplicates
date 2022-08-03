# TMX duplicates cleaner

## Short description

1. Use first the programm "tmx_cleanup.py" to find all duplicates in a given TMX files. Check the semi duplicates you want to delete.
2. Then use the second programm "delete_segments_by_tuids.py" to delete all the not necessary sgements via the ID in a given TMX File.

## Description

### tmx_cleanup.py

The program asks you which TMX file you want to edit. It has to be in the input folder.
It will delete all duplicates and create a txt file with found duplicates, a new TMx file without duplicates and CSV (Delimiter TAB) with all semi duplicates. The first duplicate found will not be deleted.
All of them are saved in the output folder.

Input TMX Format

- Encoding: UTF-8
- XML Version: 1.0
- TMX Version: 1.4

### delete_segments_by_tuids.py

The program asks you which TMX file you want to edit, then it will ask you for a TXT file, that contains all the IDs. This file has to be Tab sperated.
Both of them has to be in the input folder.
It will delete all segments if the ID is found from the imported by TXT file.
It will create a new TMX file like the inputed TMX file without the deleted segments.
if a row or the ID entry in the importet txt file is empty, the programm skips it.

Input CSV Format

- Encoding: UTF-8
- Delimiter: TAB (\t)
- Extension: .txt
- Header: ID    Lang_1 (e.g: en_US)    Lang_2 (e.g:de_DE)
- Rows: 9LASxy3fxC34qd91O80Qksps4    You are welcome.    Gern geschehen.

### Folder structure

- input (the programms looks in this folder for the input files to select)
- lib (programm helpful files, do not delete)
- output (all the generated files can be found here)

### Python version used while coding

- 3.9.6

## Note

- A semi duplicate is the same translation for different input strings.
- When importing the semi_duplicates.csv in Excel select the UTF-8 Encoding.
- To create the input file to import the IDs, click in Excel "Save as" and select the file type the "Text (tab delimited) (*.txt)".
