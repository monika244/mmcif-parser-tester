import time
import csv
from Bio.PDB.MMCIFParser import MMCIFParser
from Bio.PDB.MMCIFParser import FastMMCIFParser
parser = MMCIFParser()
parser2 = FastMMCIFParser()
ts = time.time()
structure2 = parser2.get_structure('2ncy',"2ncy.cif")
print(structure2.get_id())

ts2 = time.time()
print (ts2 - ts)


ts = time.time()
structure = parser.get_structure('2ncy', '2ncy.cif')
print(structure.__len__())
ts2 = time.time()
print (ts2 - ts)
from __future__ import print_function
from Bio import PDB
parser = PDB.MMCIFParser()
p53_1tup = parser.get_structure('P53', '1tup.cif')
def describe_model(name, pdb):
    print()
    for model in p53_1tup:
        for chain in model:
            print('%s - Chain: %s. Number of residues: %d.Numberofatoms: % d.' %name, chain.id, len(chain),len(list(chain.get_atoms())))
describe_model('1TUP', p53_1tup)