import time
from Bio import PDB
from Bio import SeqIO
import csv
from Bio.PDB.MMCIFParser import MMCIFParser
from Bio.PDB.MMCIFParser import FastMMCIFParser
# def get_length(structure):
#     for()


parser = MMCIFParser()
parser2 = FastMMCIFParser()
ts = time.time()
structure2 = parser2.get_structure('2ncy', "2ncy.cif")
print(structure2.get_id())
count = 0
for model in structure2:
    for chain in model:
        for res in chain:
            count += 1
    break

print(count)
ts2 = time.time()
print (ts2 - ts)
ts = time.time()
structure = parser.get_structure('2ncy','2ncy.cif')
ts2 = time.time()
print (ts2 - ts)
parser = PDB.MMCIFParser()
p53_1tup = parser.get_structure('P53', '1tup.cif')
#print(parser.__init__())
mmcif_dict = MMCIFParser("2ncy")
a = SeqIO.read('1tup.cif', mmcif_dict)
print(mmcif_dict['_entity_poly_seq.hetero'])
#def getLength(name, pdb)

