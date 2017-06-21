# This measures performance specified parser over given extract of PDB database.
#
# Version 2.0
# It is compatible with Python 3.6
#
# Author: Monika Wiech

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

# set data dir and limit
root_dir = './'
data_dir = root_dir + 'data/'
grp_dir_limit = 100
str_dir_limit = 1000
grp_dir_count = 0

# define logging system
log_name = 'tester__%s'
err_ext = '.err'
log_ext = '.log'
out_ext = '.out'


# returns path to new log file which name is not taken in given directory
def get_log_file(dir_path, name_prefix, name_ext):
    file_name = dir_path + name_prefix + name_ext
    if os.path.exists(file_name):
        file_num = 1
        name_pattern = dir_path + name_prefix + '_%s' + name_ext
        while os.path.exists(name_pattern % file_num):
            file_num += 1
        file_name = name_pattern % file_num
    return file_name


# loop through all group dirs in data dir
for group_dir in glob.glob('%s/*/' % data_dir):
    if grp_dir_count == grp_dir_limit:
        break

    # create log file
    group_name = os.path.relpath(group_dir, data_dir)
    log_prefix = log_name % group_name

    err_file = get_log_file(root_dir, log_prefix, err_ext)
    out_file = get_log_file(root_dir, log_prefix, out_ext)
    log_file = get_log_file(root_dir, log_prefix, log_ext)

    # redirect output to out_file
    errors = open(err_file, 'w')
    output = open(out_file, 'w')
    logger = open(log_file, 'w')
    sys_err = sys.stderr
    sys_out = sys.stdout
    sys.stderr = output
    sys.stdout = output
    str_dir_count = 0
    str_count = 0

    # loop through all dirs in group dir
    for str_dir in glob.glob('%s/*/' % group_dir):
        if str_dir_count == str_dir_limit:
            break
        dir_parse_start = time.time()
        print('>> START_DIR:', str_dir, 'PARSER:', parser.__class__, file=errors)
        print('>> START_DIR:', str_dir, 'PARSER:', parser.__class__, file=output)
        print('>> START_DIR:', str_dir, 'PARSER:', parser.__class__, file=logger)

        # loop through all files in dir
        for gz_file_name in glob.glob('%s/*.gz' % str_dir):

            # extract all files
            with gzip.open(gz_file_name, 'rb') as in_file:
                cif_file_name = gz_file_name[:-3]
                with open(cif_file_name, 'wb') as out_file:
                    out_file.write(in_file.read())

                # process extracted file
                str_id = os.path.relpath(cif_file_name, str_dir)[:-4]
                print('> START_STR:', str_id, file=output)
                with open(cif_file_name) as cif_file:
                    try:
                        str_parse_start = time.time()
                        structure = parser.get_structure(str_id, cif_file)
                        str_parse_time = time.time() - str_parse_start

                        # calculate structure length
                        str_len = 0
                        for model in structure:
                            for chain in model:
                                for res in chain:
                                    str_len += 1
                            break

                        # log structure as processed
                        print('> STR_ID:', structure.get_id(), '|STR_LEN:', str(str_len), '|STR_TIME:', str_parse_time, file=logger)
                    except Exception as exc:
                        # log exception
                        print('> STR_ID:', str_id, '|STR_LEN: 0 |STR_TIME: 0', file=logger)
                        print('! STR_ID:', str_id, "|EXC_TYPE:", type(exc).__name__, '|EXC_MSG:', exc, file=errors)

                # remove processed file
                print('> FINISH_STR:', str_id, file=output)
                os.remove(cif_file_name)
            str_count += 1

        # log directory as processed
        dir_parse_time = time.time() - dir_parse_start
        print('>> FINISH_DIR:', str_dir, 'PARSER:', parser.__class__, '\n', file=errors)
        print('>> FINISH_DIR:', str_dir, 'PARSER:', parser.__class__, '\n', file=output)
        print('>> FINISH_DIR:', str_dir, 'PARSER:', parser.__class__, '|STR_COUNT:', str_count, '|DIR_TIME:',dir_parse_time, '\n', file=logger)
        str_dir_count += 1

    # restore output
    sys.stderr = sys_err
    sys.stdout = sys_out
    errors.close()
    output.close()
    logger.close()
    grp_dir_count += 1
