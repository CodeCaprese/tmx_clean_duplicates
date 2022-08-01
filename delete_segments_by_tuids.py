####################################################################################
# Author: Rene 
# Date: 28.07.2022
# Version: 0.1
#
# Description:
# The program asks you which TMX file you want to edit. It has to be in the input 
# folder. Then it will ask you for a CSV file, that contains all the IDs. This file
# should be formatted like:
# ID,lang_1(e.g. en_EN), lang_2(e.g. de_DE)
# 1NP1Cs9h0YSjMbw0egcoLrhic, Hello my friend, Hallo mein Freund
# 
# The program will take the IDs from the CSV file and delete the corresponding nodes from the selected TMX file.
# It will output a new TMX file without the nodes. You cand find this file in
# the output folder.
#####################################################################################

import lib.file_handling as fh
tmx_file = fh.list_and_select_file("Please select a TMX file to edit", "tmx")
tmx_file_ext = tmx_file[2]
tmx_file_name = tmx_file[1]
tmx_file_w_path = tmx_file[0] + tmx_file[1] + "." + tmx_file[2]

txt_file = fh.list_and_select_file("Please select a TXT file that contains all the IDs to delete", "txt")
txt_file_ext = txt_file[2]
txt_file_name = txt_file[1]
txt_file_w_path = txt_file[0] + txt_file[1] + "." + txt_file[2]

### get first all tuids from txt input file 
tuids_to_delete = fh.get_tuids_to_delete(txt_file_w_path)

### start reading tmx file  
print("\nStarting to read file " + tmx_file_name + "." + txt_file_ext + ". This could take a while. Time to get a coffee/tea.")
segments = fh.read_xml_file(tmx_file_w_path)
tree = segments[3]
print("\nI will now delete the imported segments and create a new TMX file.")
fh.write_xml_file_wo_duplicates(tree, tuids_to_delete, tmx_file_name, semi=True)
print("\nThat was it! Have a great day.")
input("")