####################################################################################
# Author: Rene 
# Date: 27.07.2022
# Version: 0.1
#
# Description:
# The program asks you which TMX file you want to edit. It has to be in the input 
# folder. 
# It will find all true duplicates in the TMX file and delete them.
# As output you get a new TMX file without the duplicates and a TXT file with all 
# duplicates. Both are saved in the output folder.
# Afterwards it will search for all semi-duplicates and create a CSV file with 
# the ID    lang_0 (e.g. en_US)     lang_1 (de_DE). It is tab delimited. 
# This file is also saved in the output folder.
#####################################################################################
import lib.file_handling as fh

#globals
path_to_file = "" # used to read the file in xml
used_file = "" # used in print statement
lang_type_0 = "" # used to set csv header
lang_type_1 = "" # used to set csv header

tuids = [] # all found tuids, store them in an array
segments = [[],[]] # store the segments and translations here

selected_file = fh.list_and_select_file("Please select a file to clean up", "tmx")

path_to_file = selected_file[0] + selected_file[1] + "." + selected_file[2] # complete filename including folder structure
used_file = selected_file[1] + "." + selected_file[2] # only filename with extension

print("Start to read file " + used_file + ". This could take a while. Time to get a cup of coffee/tea.")
temp = fh.read_xml_file(path_to_file)
tuids = temp[0] # all tuids found in xml file
segments[0] = temp[1] # language segments
segments[1] = temp[2] # translation segments
tree = temp[3] # tree of xml file

print("\nI will now search for duplicates.")

to_delete_tuids = fh.search_for_duplicates(tuids, segments, selected_file[1])

# delete duplicates and set arrays for semi duplicate searching
print("\nI will now delete all duplicates.")
fh.write_xml_file_wo_duplicates(tree,to_delete_tuids,selected_file[1])

print("\nI will now check for semi-duplicates. This can take a while. Time for another coffee/tea.")

# find all semi-duplicates and write CSV file
fh.find_and_write_semi_duplicates(tuids, segments, selected_file[1])

print("\nThanks for waiting. You can find the tab delimited TXT file (" + selected_file[1] + "_semi_duplicates.csv) in the output folder.")
print("That was it! Have a great day.")
input("")