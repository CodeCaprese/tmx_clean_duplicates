####################################################################################
# Author: Rene 
# Date: 01.08.2022
# Version: 0.1
#
# Description:
# Handles all the functions that are used in tmx cleanup and delete semi duplicates
#####################################################################################
import csv
from msvcrt import putch
import os
import time
import sys
import codecs # write xml in utf-8
from xml.dom.minidom import parse #xml parser

dir_path = r'./input/'
output_dir_path = r'./output/'
counter = 0
factor_cnt = 0
segments = [[], [], []] # 0 = tuids, 1 = segement, 2 = translation
lang_title_0 = ""
lang_title_1 = ""

def show_dots(factor):
    global factor_cnt
    factor_cnt += 1
    if factor_cnt % factor == 0: 
        print(".", end="")
        factor_cnt = 0
        time.sleep(0.01)
        sys.stdout.flush()

def print_status(process, count, total, modulo = 1):
    global counter
    counter += 1
    if(counter % modulo) == 0:
        counter=0
        print(' '*50, end='\r')
        if(process == "delete"):
            print("  " + str(count) + " out of " + str(total) + " deleted", end="\r")
        else:
            print("  " + str(count) + " out of " + str(total) + " checked", end="\r")
        time.sleep(0.03)
        sys.stdout.flush()

def quit_program():
    input("Press any key to close me.")
    quit()

def list_and_select_file(question, file_ext):
    exists = os.path.exists(dir_path)
    if not exists:
        print("Please provide an \"input\" folder. I can't work without.")
        quit_program()
    exists = os.path.exists(output_dir_path)
    if not exists:
        print("Please provide an \"output\" folder. I can't work without.")
        quit_program()

    res = []
    file_cntr = 1
    # Iterate directory
    for path in os.listdir(dir_path):
        # check if current path is a file
        if os.path.isfile(os.path.join(dir_path, path)):
            if(path != ".gitignore"):
                res.append(path)
                file_cntr += 1

    if file_cntr == 1:
        print ("Sorry, I couldn't find any files in the \"Input\" folder. Please add a file and try again.")
        quit_program()

    while True:
        try:
            print(question + " [enter the number]:")
            for f in range(len(res)): 
                print("[" + str(f+1) + "] " + res[f])
            file_number = int(input("No: "))
        except ValueError: 
            print("Sorry, I didn't understand that. Please try again.")
            #better try again... Return to the start of the loop
            continue
        else:
            if file_number < 1 or file_number >= file_cntr:
                print("Sorry, I couldn't find your selected file. Please select a different file")
                continue;
            split = res[(file_number-1)].split(".")
            if(split[1] != file_ext):
                print("Sorry, I can only handle " + file_ext.upper()  + " files.")
                continue;
            file_name = split[0]
            file_ext = split[1]
            break

    return [dir_path, file_name, file_ext]


def read_xml_file(file):
    
    global lang_title_0
    global lang_title_1

    try:
        tree = parse(file)
    except:
        print("I am really sorry to inform you that your selected TMX file is corrupt and I can't parse it.")
        print("I have to stop my work. Have a great day")
        quit_program()  
    
    lang_title_0 = tree.getElementsByTagName('tu')[0].getElementsByTagName("tuv")[0].getAttribute("xml:lang")
    lang_title_1 = tree.getElementsByTagName('tu')[0].getElementsByTagName("tuv")[1].getAttribute("xml:lang")        


    for node in tree.getElementsByTagName('tu'):
        segments[0].append(node.getAttribute("tuid"))
        tuv = node.getElementsByTagName("tuv")
        segments[1].append(tuv[0].getElementsByTagName("seg")[0].firstChild.nodeValue)
        segments[2].append(tuv[1].getElementsByTagName("seg")[0].firstChild.nodeValue)

        show_dots(100)
    
    segments.append(tree)
    return segments

def search_for_duplicates(tuids, segments, file_name):
    #vars
    found_tuids = []
    to_delete_tuids = []
    found = []
    index_to_unset = []

    f= open(output_dir_path + file_name + "_duplicated.txt","w+", encoding="utf-8")
    f.write ("Duplicated entries: \n")

    length = len(segments[0])
    for i in range((length)):
        temp_0 = segments[0][i]
        temp_1 = segments[1][i]

        if(tuids[(i)] not in found_tuids):
            for j in range(length):
                if((i != j) and ((segments[0][j] == temp_0) and (segments[1][j] == temp_1)) and (tuids[(j)] not in found_tuids)):
                    found.append(tuids[(j)])
                    index_to_unset.append(j)
            
            if found:
                found.append(tuids[(i)])
                for entry in found:
                    f.write("ID: " + entry + "\n")
                    found_tuids.append(entry)
                    if entry != tuids[(i)]:
                        to_delete_tuids.append(entry)

                f.write("from: " + temp_0 + " to: " + temp_1 + "\n")
                f.write("------------------------------------------------------ \n")
            found = []

        print_status("check", i, length, 99)

    print_status("check", (i+1), length)
    f.close()
    # we need to sort the entries reverse, becauese when deleting the entry, the next index to 
    # delete would move up the array and it is not the correct string to delete anymore
    index_to_unset.sort(reverse=True)
    for index in (index_to_unset):
        segments[0].pop(index)
        segments[1].pop(index)
        tuids.pop(index)

    return to_delete_tuids

def write_xml_file_wo_duplicates(tree, to_delete_tuids, file_name_wo_ext, semi = False):
    deleted_nodes = 0
    for node in tree.getElementsByTagName('tu'):
        tuid = node.getAttribute("tuid")    

        if tuid in to_delete_tuids:
            parent = node.parentNode
            parent.removeChild(node)
            print_status("delete", deleted_nodes, len(to_delete_tuids))
            deleted_nodes+=1

    if (semi):
        output = output_dir_path + file_name_wo_ext + "_wo_semi_duplicates.tmx"
    else:
        output = output_dir_path + file_name_wo_ext + "_wo_duplicates.tmx"

    with codecs.open(output, "w", "utf-8") as out:
        tree.writexml(out)

    print_status("delete", deleted_nodes, len(to_delete_tuids))

def find_and_write_semi_duplicates(tuids, segments, file_name_wo_ext):
    csv_col_tuids = []
    csv_col_lang_0 = []
    csv_col_lang_1 = []
    found_tuids = []
    length = len(segments[0])

    for i in range((length)):
        temp_0 = segments[0][i]
        temp_1 = segments[1][i]

        print_status("checked", i,length, 99)
        
        for j in range(length):
            if((i != j) and ((segments[0][j] == temp_0))):
                found_tuids.append(tuids[j])
                csv_col_tuids.append(tuids[j])
                csv_col_lang_0.append(segments[0][j])
                csv_col_lang_1.append(segments[1][j])

        for j in range(length):
            if((i != j) and ((segments[1][j] == temp_1))):
                found_tuids.append(tuids[j])
                csv_col_tuids.append(tuids[j])
                csv_col_lang_0.append(segments[0][j])
                csv_col_lang_1.append(segments[1][j])

    print_status("check", (i+1), length)
    print("\nI will now create a CSV file with these semi-duplicates.")

    with open(output_dir_path + file_name_wo_ext + '_semi_duplicates.csv', 'w', newline='', encoding='UTF8') as f:
        writer = csv.writer(f, delimiter = "\t")
        # write the header
        writer.writerow(['ID', lang_title_0, lang_title_1])

        for i in range(len(csv_col_tuids)):
            # write the data
            writer.writerow([csv_col_tuids[i], csv_col_lang_0[i], csv_col_lang_1[i]])

        # close the file
        f.close()

def get_tuids_to_delete(file_incl_path):
    tuids_to_delete = []
    
    with open(file_incl_path, newline='') as f:
        try:
            dialect = csv.Sniffer().sniff(f.read(), delimiters="\t")
            f.seek(0)
            reader = csv.reader(f, dialect)

            for row in reader:
                if(row[0] != "ID" and row[0] != "id" and row[0] != "" and row[0] != " " and row[0] != 'Column1'):
                    tuids_to_delete.append(row[0])
        except:
            print("TXT File uses wrong Delimiter. Please use TAB Delimiter")
            quit_program()

    return tuids_to_delete