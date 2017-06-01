import gzip
import glob
import os
import sys
import time

# select parser class
# from Bio.PDB.MMCIFParser import MMCIFParser
from Bio.PDB.MMCIFParser import FastMMCIFParser
# parser = MMCIFParser()
parser = FastMMCIFParser()

# create log file
log_file_pattern = './tester%s.log'
log_file_num = 0
while os.path.exists(log_file_pattern % log_file_num):
    log_file_num += 1

# redirect output to log file
sys.stdout = open(log_file_pattern % log_file_num, 'w')


root_data_dir = './mmCIF/'
dir_count = 0
str_count = 0
limit = 4

total_parse_start = time.time()

print('parser:', parser.__class__, '\nSTART')
# loop through all dirs in root data dir
for data_dir in glob.glob('%s/*/' % root_data_dir):
    if dir_count == limit:
        break

    dir_parse_start = time.time()
    print('\nstarting', data_dir, '\n')

    # extract all files
    for gz_file_name in glob.glob('%s/*.gz' % data_dir):
        with gzip.open(gz_file_name, 'rb') as in_file:
            cif_file_name = gz_file_name[:-3]
            with open(cif_file_name, 'wb') as out_file:
                out_file.write(in_file.read())
            # process extracted file
            with open(cif_file_name) as cif_file:
                str_id = cif_file_name[len(data_dir):-4]
                str_parse_start = time.time()
                structure = parser.get_structure(str_id, cif_file)
                str_parse_stop = time.time()

                str_len = 0
                for model in structure:
                    for chain in model:
                        for res in chain:
                            str_len += 1
                    break

                print('structure:', structure.get_id(), '\tlength:', str(str_len), '\ttime:',
                      str_parse_stop - str_parse_start)
            # remove processed file
            os.remove(cif_file_name)
        str_count += 1

    dir_parse_stop = time.time()
    print('\nfinished', data_dir, '\ttime:', dir_parse_stop - dir_parse_start)
    dir_count += 1

total_parse_stop = time.time()
print('\nFINISH\ndir_count:\t ' + str(dir_count) + '\nstr_count:\t' + str(str_count) + '\ntotal_time:\t', total_parse_stop - total_parse_start)