# Version 0.9 (prototype)
#
# Author: Monika Wiech

import gzip
import time
from Bio.PDB.MMCIFParser import MMCIFParser
from Bio.PDB.MMCIFParser import FastMMCIFParser

parser = MMCIFParser()

file_dir = './mmCIF/00/'
str_id = '100d'
gz_file_name = file_dir + str_id + '.cif.gz'
cif_file_name = file_dir + str_id + '.cif'


total_start = time.time()

in_file = gzip.open(gz_file_name, 'rb')
out_file = open(cif_file_name, 'wb')
out_file.write(in_file.read())
in_file.close()
out_file.close()

file = open(cif_file_name)
parse_start = time.time()
structure = parser.get_structure(str_id, file)
parse_stop = time.time()
file.close()

total_stop = time.time()

print ('structure:', structure.get_id(), '\tparse time:', parse_stop - parse_start, '\ttotal time: ', total_stop - total_start)

