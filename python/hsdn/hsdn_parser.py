from typing import Dict, Tuple
from csv import DictReader


def parseIdentifierMap(entity: str, verbose: bool = False) -> Dict[str, str]:
    file_name = 'input/HSDN/Combined-Output.tsv'
    id_map = dict()
    
    if entity == 'Symptom':
        id_label = 'MeSH Symptom ID'
        name_label = 'MeSH Symptom Term'
    elif entity == 'Disease':
        id_label = 'MeSH Disease ID'
        name_label = 'MeSH Disease Term'
    else:
        raise ValueError('Error !!! Invalid entity parameter ...')
    
    csv_file = open(file_name, 'r')
    reader = DictReader(csv_file, delimiter='\t')
    for row in reader:
        if row[id_label] != '':
            if row[id_label] not in id_map:
                id_map[row[id_label]] = row[name_label]
            elif id_map[row[id_label]] != row[name_label] and verbose:
                print(row[id_label] + ' - ' + id_map[row[id_label]] + " != " + row[name_label])
    
    if verbose:
        print(id_label + '\t' + name_label)
        for k, v in sorted(id_map.items(), key=lambda x: x[1]):
            print(k + '\t' + v)
        print(len(id_map))
    
    return id_map


def parseDiseaseSymptomMap(verbose: bool = False) -> Dict[str, Dict[str, Tuple[float, int]]]:
    file_name = 'input/HSDN/Combined-Output.tsv'
    disease_symptom_map = dict()
    
    csv_file = open(file_name, 'r')
    reader = DictReader(csv_file, delimiter='\t')
    for row in reader:
        if row['MeSH Disease ID'] != '' and row['MeSH Symptom ID'] != '':
            if row['MeSH Disease ID'] not in disease_symptom_map:
                disease_symptom_map[row['MeSH Disease ID']] = {
                    row['MeSH Symptom ID']: (float(row['TFIDF score']), int(row['PubMed occurrence']))
                }
            else:
                disease_symptom_map[row['MeSH Disease ID']][row['MeSH Symptom ID']] = (
                    float(row['TFIDF score']), int(row['PubMed occurrence'])
                )
    
    if verbose:
        c = 1
        for disease, symptoms in disease_symptom_map.items():
            print(str(c) + '. ' + disease + ' :')
            for sid, attrs in sorted(symptoms.items()):
                print('\t----' + sid + ' - ' + str(attrs))
            c = c + 1
    
    return disease_symptom_map


def parseSymptomDiseaseMap(verbose: bool = False) -> Dict[str, Dict[str, Tuple[float, int]]]:
    file_name = 'input/HSDN/Combined-Output.tsv'
    symptom_disease_map = dict()
    
    csv_file = open(file_name, 'r')
    reader = DictReader(csv_file, delimiter='\t')
    for row in reader:
        if row['MeSH Symptom ID'] != '' and row['MeSH Disease ID'] != '':
            if row['MeSH Symptom ID'] not in symptom_disease_map:
                symptom_disease_map[row['MeSH Symptom ID']] = {
                    row['MeSH Disease ID']: (float(row['TFIDF score']), int(row['PubMed occurrence']))
                }
            else:
                symptom_disease_map[row['MeSH Symptom ID']][row['MeSH Disease ID']] = (
                    float(row['TFIDF score']), int(row['PubMed occurrence'])
                )
    
    if verbose:
        c = 1
        for symptom, diseases in symptom_disease_map.items():
            print(str(c) + '. ' + symptom + ' :')
            for did, attrs in sorted(diseases.items()):
                print('\t----' + did + ' - ' + str(attrs))
            c = c + 1
    
    return symptom_disease_map
