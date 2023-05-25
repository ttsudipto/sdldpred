import numpy as np

from .resource import read_association_data
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import Binarizer
from typing import Dict
import numpy


def print_drug_symptom_association_matrix(matrix: numpy.array,
                                          row_names: Dict[str, str],
                                          col_names: Dict[str, str]) -> None:
    print('\t'.join(['Symptom', '->'] + list(col_names.keys())))
    print('\t'.join(['Drug', 'DrugName'] + list(col_names.values())))
    row_names = list(row_names.items())
    for i in range(matrix.shape[0]):
        temp = [row_names[i][0], row_names[i][1]]
        for j in range(matrix.shape[1]):
            temp.append(str(matrix[i, j]))
        print('\t'.join(temp))


def trim_symptom_disease_association_matrix(matrix: numpy.array, cutoff: float = 100):
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            if matrix[i, j] > cutoff:
                matrix[i, j] = cutoff
            elif matrix[i, j] < 1:
                matrix[i, j] = 0
    matrix = matrix / cutoff
    return matrix


def get_drug_symptom_association_matrix(trim_matrix: bool = False, verbose: bool = False):
    hsdn_res = read_association_data('HSDN', verbose=False)
    ctd_res = read_association_data('CTD', verbose=False)

    symptoms = hsdn_res.get_row_ids()
    drugs = ctd_res.get_row_ids()
    hsdn_diseases = hsdn_res._read_headers()
    ctd_diseases = ctd_res._read_headers()
    common_diseases = set(hsdn_diseases).intersection(set(ctd_diseases))
    hsdn_common_indices = [i for i, x in enumerate(hsdn_diseases) if x in common_diseases]
    ctd_common_indices = [i for i, x in enumerate(ctd_diseases) if x in common_diseases]

    print(len(symptoms), len(drugs), len(hsdn_diseases), len(ctd_diseases), len(common_diseases))
    print(len(hsdn_common_indices), len(ctd_common_indices))
    print()

    if trim_matrix:
        hsdn_common_data = trim_symptom_disease_association_matrix(hsdn_res.data[:, hsdn_common_indices])
    else:
        hsdn_common_data = Binarizer().fit_transform(hsdn_res.data[:, hsdn_common_indices])
    ctd_common_data = ctd_res.data[:, ctd_common_indices]
    print(hsdn_common_data.shape, ctd_common_data.shape)
    print(numpy.count_nonzero(hsdn_common_data), numpy.size(hsdn_common_data) - numpy.count_nonzero(hsdn_common_data),
          numpy.size(hsdn_common_data))
    print()

    similarities = cosine_similarity(ctd_common_data, hsdn_common_data)
    # print(similarities.shape)

    if verbose:
        print_drug_symptom_association_matrix(similarities, drugs, symptoms)

    return similarities


similarity = get_drug_symptom_association_matrix(trim_matrix=True, verbose=False)
print(similarity.shape)
