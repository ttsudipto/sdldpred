from typing import Dict, List
from csv import DictReader

path_prefix = 'input/ChEBI/'


def get_pulmonary_drugs_pubchem() -> None:
    mf = open(path_prefix + 'mesh_pubchem_map.csv', 'r')
    map_reader = DictReader(mf, delimiter=',')
    mesh_cid_map = dict()
    mesh_sid_map = dict()
    for row in map_reader:
        mesh_cid_map[row['sidextid']] = row['cid']
        mesh_sid_map[row['sidextid']] = row['sid']
    mf.close()
    f = open('input/CTD/pulmonary_drugs_ctd.tsv', 'r')
    reader = DictReader(f, delimiter='\t')
    print('PubChemSID' + '\t' + 'PubChemCID' + '\t' + 'CasRN' + '\t' + 'ChemicalID' + '\t' + 'ChemicalName')
    for row in reader:
        mesh = row['ChemicalID']
        print(mesh_sid_map[mesh] + '\t' + mesh_cid_map[mesh]
              + '\t' + row['CasRN'] + '\t' + mesh + '\t' + row['ChemicalName'])


def get_pulmonary_drugs_chebi() -> None:
    mf = open(path_prefix + 'pubchem_chebi_map.csv', 'r')
    map_reader = DictReader(mf, delimiter=',')
    pubchem_chebi_map = dict()
    for row in map_reader:
        if row['cid'] != 'NULL':
            pubchem_chebi_map[row['cid']] = row['sidextid'][6:]
    mf.close()
    f = open(path_prefix + 'pulmonary_drugs_pubchem.tsv', 'r')
    reader = DictReader(f, delimiter='\t')
    print('PubChemSID' + '\t' + 'PubChemCID' + '\t' + 'CasRN' + '\t' + 'ChemicalID' + '\t'
          + 'ChemicalName' + '\t' + 'ChEBIID')
    for row in reader:
        chebi_id = ''
        if row['PubChemCID'] in pubchem_chebi_map:
            chebi_id = pubchem_chebi_map[row['PubChemCID']]
        print(row['PubChemSID'] + '\t' + row['PubChemCID'] + '\t' + row['CasRN'] + '\t' + row['ChemicalID'] + '\t'
              + row['ChemicalName'] + '\t' + chebi_id)


def read_pulmonary_drugs_chebi(key: str = 'id', verbose: bool = False) -> Dict[str, str]:
    if key == 'id':
        key_column = 'ChemicalID'
    elif key == 'name':
        key_column = 'ChemicalName'
    else:
        raise ValueError('Error !!! Invalid key. Correct values = {\'id\', \'name\'} ...')
    f = open(path_prefix + 'pulmonary_drugs_chebi.tsv', 'r')
    reader = DictReader(f, delimiter='\t')
    drugs = dict()
    for row in reader:
        if row['ChEBIID'] != '':
            drugs[row[key_column]] = row['ChEBIID']
    if verbose:
        for k, v in drugs.items():
            print(k + ' => ' + v)
    return drugs
