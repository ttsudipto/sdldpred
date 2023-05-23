from typing import Dict
from csv import DictReader

# pulmonary_file = 'input/ICD/ICD_pulmonary.csv'
pulmonary_file = 'input/ICD/ICD_pulmonary_comorbidity.csv'


def get_all_pulmonary_diseases_icd11() -> Dict[str, str]:
    f = open(pulmonary_file, 'r')
    reader = DictReader(f, delimiter=',')
    icd11_map = dict()
    for row in reader:
        icd11_map[row['icd11Code']] = row['icd11Title']
    f.close()
    return icd11_map


def get_all_pulmonary_diseases_icd10() -> Dict[str, str]:
    f = open(pulmonary_file, 'r')
    reader = DictReader(f, delimiter=',')
    icd10_map = dict()
    for row in reader:
        icd10_map[row['icd10Code']] = row['icd10Title']
    f.close()
    return icd10_map


def get_icd11_TTD_aliases() -> Dict[str, str]:
    f = open(pulmonary_file, 'r')
    reader = DictReader(f, delimiter=',')
    icd_alias_map = dict()
    for row in reader:
        if row['icd11Code'] != '' and row['icd11TTDalias'] != '':
            icd_alias_map[row['icd11Code']] = row['icd11TTDalias']
    f.close()
    return icd_alias_map


def get_all_pulmonary_diseases_mesh() -> Dict[str, str]:
    f = open(pulmonary_file, 'r')
    reader = DictReader(f, delimiter=',')
    mesh_map = dict()
    for row in reader:
        if row['MeSHDiseaseID'] != '':
            mesh_map[row['MeSHDiseaseID']] = row['MeSHDiseaseTerm']
    f.close()
    return mesh_map


def get_TTD_pulmonary_diseases_icd11() -> Dict[str, str]:
    f = open(pulmonary_file, 'r')
    reader = DictReader(f, delimiter=',')
    icd11_map = dict()
    for row in reader:
        if row['TTDTitle'] != '':
            icd11_map[row['icd11Code']] = row['TTDTitle']
    f.close()
    return icd11_map


def get_TTD_pulmonary_diseases_mesh() -> Dict[str, str]:
    f = open(pulmonary_file, 'r')
    reader = DictReader(f, delimiter=',')
    mesh_map = dict()
    for row in reader:
        if row['TTDTitle'] != '':
            mesh_map[row['MeSHDiseaseID']] = row['TTDTitle']
    f.close()
    return mesh_map


def get_icd11_mesh_map() -> Dict[str, str]:
    f = open(pulmonary_file, 'r')
    reader = DictReader(f, delimiter=',')
    icd_mesh_map = dict()
    for row in reader:
        if row['icd11Code'] != '' and row['MeSHDiseaseID'] != '':
            icd_mesh_map[row['icd11Code']] = row['MeSHDiseaseID']
    f.close()
    return icd_mesh_map


def get_icd11_disease_group_map() -> Dict[str, str]:
    f = open('input/ICD/ICD_disease_groups.csv', 'r')
    reader = DictReader(f, delimiter=',')
    icd_group_map = dict()
    for row in reader:
        if row['icd11Code'] not in icd_group_map:
            icd_group_map[row['icd11Code']] = row['Category']
    f.close()
    return icd_group_map


def get_mesh_disease_group_map() -> Dict[str, str]:
    f = open('input/ICD/ICD_disease_groups.csv', 'r')
    reader = DictReader(f, delimiter=',')
    mesh_group_map = dict()
    for row in reader:
        if row['MeSHDiseaseID'] not in mesh_group_map:
            mesh_group_map[row['MeSHDiseaseID']] = row['Category']
    f.close()
    return mesh_group_map
