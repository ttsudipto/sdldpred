from .resource import read_association_data
from scipy.stats import pearsonr
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import jaccard_score
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


def print_drug_symptom_association_edge_list(matrix: numpy.array,
                                             row_names: Dict[str, str],
                                             col_names: Dict[str, str]) -> None:
    row_names_list = list(row_names.items())
    col_names_list = list(col_names.items())
    print('\t'.join(['CasRN', 'DrugName', 'SymptomID', 'SymptomName', 'Association']))
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            if matrix[i, j] > 0:
                print(
                    '\t'.join(
                        [
                            row_names_list[i][0],
                            row_names_list[i][1],
                            col_names_list[j][0],
                            col_names_list[j][1],
                            str(matrix[i, j])
                        ]
                    )
                )


def trim_symptom_disease_association_matrix(matrix: numpy.array, cutoff: float = 100) -> numpy.array:
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            if matrix[i, j] > cutoff:
                matrix[i, j] = cutoff
            elif matrix[i, j] < 1:
                matrix[i, j] = 0
    matrix = matrix / cutoff
    return matrix


def get_drug_symptom_association_matrix(trim_matrix: bool = False, association_metric: str = 'cosine',
                                        verbose: str = None) -> numpy.array:
    hsdn_res = read_association_data('HSDN', verbose=False)
    ctd_res = read_association_data('CTD', verbose=False)

    symptoms = hsdn_res.get_row_ids()
    drugs = ctd_res.get_row_ids()
    hsdn_diseases = hsdn_res._read_headers()
    ctd_diseases = ctd_res._read_headers()
    common_diseases = set(hsdn_diseases).intersection(set(ctd_diseases))
    hsdn_common_indices = [i for i, x in enumerate(hsdn_diseases) if x in common_diseases]
    ctd_common_indices = [i for i, x in enumerate(ctd_diseases) if x in common_diseases]

    # print(len(symptoms), len(drugs), len(hsdn_diseases), len(ctd_diseases), len(common_diseases))
    # print(len(hsdn_common_indices), len(ctd_common_indices))
    # print()

    if trim_matrix:
        hsdn_common_data = trim_symptom_disease_association_matrix(hsdn_res.data[:, hsdn_common_indices])
    else:
        hsdn_common_data = Binarizer().fit_transform(hsdn_res.data[:, hsdn_common_indices])

    ctd_common_data = ctd_res.data[:, ctd_common_indices]

    # print(hsdn_common_data.shape, ctd_common_data.shape)
    # print(numpy.count_nonzero(hsdn_common_data), numpy.size(hsdn_common_data) - numpy.count_nonzero(hsdn_common_data),
    #       numpy.size(hsdn_common_data))
    # print()

    if association_metric == 'cosine':
        similarities = cosine_similarity(ctd_common_data, hsdn_common_data)
    elif association_metric == 'pearson':
        similarities = numpy.zeros((ctd_common_data.shape[0], hsdn_common_data.shape[0]), dtype=numpy.float32)
        for drug in range(ctd_common_data.shape[0]):
            for symptom in range(hsdn_common_data.shape[0]):
                similarities[drug, symptom] = pearsonr(ctd_common_data[drug, :], hsdn_common_data[symptom, :])[0]
        similarities = numpy.nan_to_num(similarities)
    elif association_metric == 'jaccard':
        similarities = numpy.zeros((ctd_common_data.shape[0], hsdn_common_data.shape[0]), dtype=numpy.float32)
        if trim_matrix:  # force binarization of symptom-disease associations for jaccard similarity
            hsdn_common_data = Binarizer().fit_transform(hsdn_common_data)
        for drug in range(ctd_common_data.shape[0]):
            for symptom in range(hsdn_common_data.shape[0]):
                similarities[drug, symptom] = jaccard_score(ctd_common_data[drug, :], hsdn_common_data[symptom, :])
        similarities = numpy.nan_to_num(similarities)
    else:
        raise ValueError('Error !!! Invalid association_metric. Correct values = {cosine, pearson, jaccard} ... ')

    if verbose == 'matrix':
        print_drug_symptom_association_matrix(similarities, drugs, symptoms)
    elif verbose == 'edge_list':
        print_drug_symptom_association_edge_list(similarities, drugs, symptoms)

    return similarities


# similarity = get_drug_symptom_association_matrix(trim_matrix=True, association_metric='cosine', verbose=None)
# print(similarity.shape)
# similarity = get_drug_symptom_association_matrix(trim_matrix=True, association_metric='pearson', verbose=None)
# print(similarity.shape)
# similarity = get_drug_symptom_association_matrix(association_metric='jaccard', verbose=None)
# print(similarity.shape)

# similarity = get_drug_symptom_association_matrix(trim_matrix=True, association_metric='cosine', verbose='matrix')
# similarity = get_drug_symptom_association_matrix(trim_matrix=True, association_metric='pearson', verbose='matrix')
# similarity = get_drug_symptom_association_matrix(association_metric='jaccard', verbose='matrix')

# similarity = get_drug_symptom_association_matrix(trim_matrix=True, association_metric='cosine', verbose='edge_list')
# similarity = get_drug_symptom_association_matrix(trim_matrix=True, association_metric='pearson', verbose='edge_list')
# similarity = get_drug_symptom_association_matrix(association_metric='jaccard', verbose='edge_list')
