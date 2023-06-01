from .chebi_util import get_pulmonary_drugs_pubchem
from .chebi_util import get_pulmonary_drugs_chebi
from .chebi_util import read_pulmonary_drugs_chebi
from .owl_converter import convert_owl
from csv import DictReader


# get_pulmonary_drugs_pubchem()

# get_pulmonary_drugs_chebi()
# drugs = read_pulmonary_drugs_chebi(key='id', verbose=False)
# drugs = read_pulmonary_drugs_chebi(key='name', verbose=False)
# print(len(drugs))


# f = open('input/ChEBI/pulmonary_drugs_chebi.tsv', 'r')
# reader = DictReader(f, delimiter='\t')
# chebi_drugs = dict()
# for row in reader:
#     if row['ChEBIID'] != '':
#         chebi_drugs[row['ChEBIID']] = row['ChemicalName']
# f.close()
# for k, v in chebi_drugs.items():
#     print(k + ' -> ' + v)
# print(len(chebi_drugs))

# convert_owl(chebi_drugs)
