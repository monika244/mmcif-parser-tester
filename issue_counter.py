# This parses out files produced by tester.
#
# Warning entries for each structure are replaced
# with single entry with warning count.
#
# Version compatible with Python 2.7 and 3.6
#
# Author: Monika Wiech

import csv


def build_file_with_count(src_file, dest_file, file_delim):
    with open(src_file, 'r') as src:
        with open(dest_file, 'w') as dest:
            reader = csv.reader(src, delimiter=file_delim)
            str_id = ''
            count = 0
            for row in reader:
                if row[0] == str_id:
                    if len(row[1]) > 0:
                        count += 1
                else:
                    if len(str_id) > 0:
                        print(str_id + file_delim + str(count), file=dest)
                        if len(row[1]) > 0:
                            count = 1
                        else:
                            count = 0
                    str_id = row[0]


root_dir = './'
results_dir = root_dir + 'charts/'

file_name_fast = 'parseExc_FAST'
file_name_norm = 'parseExc_NORM'

count_sfx = '_c'
file_delim = ','
file_ext = '.csv'

file_path_fast = root_dir + results_dir + file_name_fast + file_ext
file_path_norm = root_dir + results_dir + file_name_norm + file_ext
fast_with_count = root_dir + results_dir + file_name_fast + count_sfx + file_ext
norm_with_count = root_dir + results_dir + file_name_norm + count_sfx + file_ext

build_file_with_count(file_path_fast, fast_with_count, file_delim)
build_file_with_count(file_path_norm, norm_with_count, file_delim)
