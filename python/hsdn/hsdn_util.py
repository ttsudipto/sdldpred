from csv import DictReader, DictWriter
from typing import Dict, List, Tuple
from copy import deepcopy


def read_symptoms_hsdn(verbose: bool = False) -> Dict[str, str]:
    f = open('input/HSDN/symptoms_hsdn.tsv', 'r')
    reader = DictReader(f, delimiter='\t')
    symptoms = dict()
    for row in reader:
        symptoms[row['MeSH Symptom ID']] = row['MeSH Symptom Term']
    f.close()
    if verbose:
        for k, v in symptoms.items():
            print(k + '\t' + v)
        print(len(symptoms))
    return symptoms


def read_diseases_hsdn(verbose: bool = False) -> Dict[str, str]:
    f = open('input/HSDN/diseases_hsdn.tsv', 'r')
    reader = DictReader(f, delimiter='\t')
    diseases = dict()
    for row in reader:
        diseases[row['MeSH Disease ID']] = row['MeSH Disease Term']
    f.close()
    if verbose:
        for k, v in diseases.items():
            print(k + '\t' + v)
        print(len(diseases))
    return diseases


def get_pulmonary_symptoms_hsdn(pulmonary_symptom_disease_map: Dict[str, Dict[str, Tuple[float, int]]]) -> None:
    all_symptoms = read_symptoms_hsdn()
    print('MeSH Symptom ID' + '\t' + 'MeSH Symptom Term' + '\t' + '# disease associations')
    for symptom, diseases in sorted(pulmonary_symptom_disease_map.items(), key=lambda x: all_symptoms[x[0]]):
        print(symptom + '\t' + all_symptoms[symptom] + '\t' + str(len(diseases)))


def read_pulmonary_symptoms_hsdn(get_assoc_count: bool = False,
                                 verbose: bool = False) -> Tuple[Dict[str, str], Dict[str, int]] | Dict[str, str]:
    f = open('input/HSDN/pulmonary_symptoms_hsdn.tsv', 'r')
    reader = DictReader(f, delimiter='\t')
    symptoms = dict()
    assoc_counts = dict()
    for row in reader:
        symptoms[row['MeSH Symptom ID']] = row['MeSH Symptom Term']
        assoc_counts[row['MeSH Symptom ID']] = int(row['# disease associations'])
    f.close()
    if verbose:
        for k, v in symptoms.items():
            print(k + '\t' + v)
        print(len(symptoms))
        if get_assoc_count:
            for k, v in assoc_counts.items():
                print(k + '\t' + v)
    if get_assoc_count:
        return symptoms, assoc_counts
    else:
        return symptoms


def get_pulmonary_diseases_hsdn(pulmonary_disease_symptom_map: Dict[str, Dict[str, Tuple[float, int]]]) -> None:
    all_diseases = read_diseases_hsdn()
    print('MeSH Disease ID' + '\t' + 'MeSH Disease Term' + '\t' + '# symptom associations')
    for disease, symptoms in sorted(pulmonary_disease_symptom_map.items(), key=lambda x: all_diseases[x[0]]):
        print(disease + '\t' + all_diseases[disease] + '\t' + str(len(symptoms)))


def read_pulmonary_diseases_hsdn(get_assoc_count: bool = False,
                                 verbose: bool = False) -> Tuple[Dict[str, str], Dict[str, int]] | Dict[str, str]:
    f = open('input/HSDN/pulmonary_diseases_hsdn.tsv', 'r')
    reader = DictReader(f, delimiter='\t')
    diseases = dict()
    assoc_counts = dict()
    for row in reader:
        diseases[row['MeSH Disease ID']] = row['MeSH Disease Term']
        assoc_counts[row['MeSH Disease ID']] = int(row['# symptom associations'])
    f.close()
    if verbose:
        for k, v in diseases.items():
            print(k + '\t' + v)
        print(len(diseases))
        if get_assoc_count:
            for k, v in assoc_counts.items():
                print(k + '\t' + v)
    if get_assoc_count:
        return diseases, assoc_counts
    else:
        return diseases


def read_pulmonary_disease_symptom_association_hsdn(verbose: bool = False) -> Dict[str, Dict[str, Tuple[float, int]]]:
    f = open('input/HSDN/pulmonary_disease_symptom_association_hsdn.tsv', 'r')
    reader = DictReader(f, delimiter='\t')
    disease_symptom_map = dict()
    for row in reader:
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


def read_pulmonary_symptom_disease_association_hsdn(verbose: bool = False) -> Dict[str, Dict[str, Tuple[float, int]]]:
    f = open('input/HSDN/pulmonary_symptom_disease_association_hsdn.tsv', 'r')
    reader = DictReader(f, delimiter='\t')
    symptom_disease_map = dict()
    for row in reader:
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


def get_pulmonary_symptom_disease_matrix_hsdn(save: bool = False) -> None:
    pulmonary_symptoms = read_pulmonary_symptoms_hsdn()
    headers = ['Symptom', 'SymptomName'] + list(sorted(read_pulmonary_diseases_hsdn().keys()))
    pulmonary_symptom_disease_map = read_pulmonary_symptom_disease_association_hsdn()
    f = writer = None
    if save:
        f = open('input/HSDN/pulmonary_symptom_disease_association_matrix_hsdn.tsv', 'w')
        writer = DictWriter(f, delimiter='\t', fieldnames=headers, restval=0)
        writer.writeheader()
    else:
        print(headers)
    for symptom, diseases in pulmonary_symptom_disease_map.items():
        row = {'Symptom': symptom, 'SymptomName': pulmonary_symptoms[symptom]}
        for disease, score in diseases.items():
            row[disease] = score[0]
        if save:
            writer.writerow(row)
        else:
            print(row)
    if save:
        f.close()


def get_pulmonary_disease_symptom_matrix_hsdn(save: bool = False) -> None:
    pulmonary_diseases = read_pulmonary_diseases_hsdn()
    headers = ['Disease', 'DiseaseName'] + list(sorted(read_pulmonary_symptoms_hsdn().keys()))
    pulmonary_disease_symptom_map = read_pulmonary_disease_symptom_association_hsdn()
    f = writer = None
    if save:
        f = open('input/HSDN/pulmonary_disease_symptom_association_matrix_hsdn.tsv', 'w')
        writer = DictWriter(f, delimiter='\t', fieldnames=headers, restval=0)
        writer.writeheader()
    else:
        print(headers)
    for disease, symptoms in pulmonary_disease_symptom_map.items():
        row = {'Disease': disease, 'DiseaseName': pulmonary_diseases[disease]}
        for symptom, score in symptoms.items():
            row[symptom] = score[0]
        if save:
            writer.writerow(row)
        else:
            print(row)
    if save:
        f.close()


def filter_diseases_from_disease_symptom_map(
        disease_symptom_map: Dict[str, Dict[str, Tuple[float, int]]],
        disease_ids: Dict[str, str],
        verbose: bool = False) -> Dict[str, Dict[str, Tuple[float, int]]]:

    filtered_map = dict()
    for disease, symptoms in disease_symptom_map.items():
        if disease in disease_ids:
            filtered_map[disease] = deepcopy(symptoms)
    if verbose:
        pulmonary_symptoms = read_pulmonary_symptoms_hsdn()
        pulmonary_diseases = read_pulmonary_diseases_hsdn()
        c = 1
        print('MeSH Disease ID' + '\t' + 'MeSH Disease Term' + '\t' + 'MeSH Symptom ID' + '\t' + 'MeSH Symptom Term' +
              '\t' + 'TFIDF score' + '\t' + 'PubMed occurrence')
        for disease, symptoms in sorted(filtered_map.items(), key=lambda x: pulmonary_diseases[x[0]]):
            # print(str(c) + '. ' + disease + ' : ' + str(len(symptoms)))
            for symptom, scores in sorted(symptoms.items(), key=lambda x: pulmonary_symptoms[x[0]]):
                print(disease + '\t' + pulmonary_diseases[disease] + '\t' + symptom + '\t' + pulmonary_symptoms[symptom]
                      + '\t' + str(scores[0]) + '\t' + str(scores[1]))
            c = c + 1

    return filtered_map


def filter_diseases_from_symptom_disease_map(
        symptom_disease_map: Dict[str, Dict[str, Tuple[float, int]]],
        disease_ids: Dict[str, str],
        verbose: bool = False) -> Dict[str, Dict[str, Tuple[float, int]]]:

    filtered_map = dict()
    for symptom, diseases in symptom_disease_map.items():
        diseases_new = dict()
        for disease, v in diseases.items():
            if disease in disease_ids:
                diseases_new[disease] = v
        if len(diseases_new) > 0:
            filtered_map[symptom] = diseases_new
    if verbose:
        pulmonary_symptoms = read_pulmonary_symptoms_hsdn()
        pulmonary_diseases = read_pulmonary_diseases_hsdn()
        c = 1
        print('MeSH Symptom ID' + '\t' + 'MeSH Symptom Term' + '\t' + 'MeSH Disease ID' + '\t' + 'MeSH Disease Term' +
              '\t' + 'TFIDF score' + '\t' + 'PubMed occurrence')
        for symptom, diseases in sorted(filtered_map.items(), key=lambda x: pulmonary_symptoms[x[0]]):
            # print(str(c) + '. ' + symptom + ' : ' + str(len(diseases)))
            for disease, scores in sorted(diseases.items(), key=lambda x: pulmonary_diseases[x[0]]):
                print(symptom + '\t' + pulmonary_symptoms[symptom] + '\t' + disease + '\t' + pulmonary_diseases[disease]
                      + '\t' + str(scores[0]) + '\t' + str(scores[1]))
            c = c + 1

    return filtered_map
