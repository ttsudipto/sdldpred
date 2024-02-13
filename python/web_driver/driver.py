from typing import List
from ..ml.pickler import load_model_from_file
from ..ml.confidence import compute_confidence
from .io_wrapper import Input, Output, OutputEncoder, symptoms
from ..ctd.ctd_util import read_pulmonary_drug_disease_association_ctd, read_pulmonary_drugs_ctd, read_pulmonary_diseases_ctd
import numpy as np
import json
import sys


drugs = read_pulmonary_drugs_ctd()
diseases = read_pulmonary_diseases_ctd()
drug_disease_associations = read_pulmonary_drug_disease_association_ctd()


def parse_input(input_json: str) -> Input:
    json_dict = json.loads(input_json)
    input_wrapper = Input()
    params = input_wrapper.get_all_params()
    for p in params:
        if p in json_dict:
            input_wrapper.add_value(json_dict[p] / 10)
            input_wrapper.add_param(p)
        else:
            input_wrapper.add_value(0.0)
    return input_wrapper


def get_disease_associations(drug: str) -> List[str]:
    disease_associations = []
    drug_id = None
    for d_id, d_name in drugs.items():
        if d_name in drug:
            drug_id = d_id
    for disease in drug_disease_associations[drug_id].keys():
        link = '<a style="color:blue;" target="_blank" href = "https://ctdbase.org/detail.go?type=disease&acc=MESH%3A' + disease + '">' + diseases[disease] + '</a>'
        disease_associations.append(link)
    return disease_associations


def get_symptom_associations(drug_index: int, input_symptoms: List[str], data: np.array) -> List[str]:
    input_symptom_indices = [symptoms.index(input_symptom) for input_symptom in input_symptoms]
    symptom_associations = []
    for symptom_index in input_symptom_indices:
        if data[drug_index, symptom_index] > 0:
            symptom_associations.append(
                symptoms[symptom_index]
                # symptoms[symptom_index] + " - " + str(round(10 * data[drug_index, symptom_index], 2))
            )
    return symptom_associations


def predict_drugs(input_wrapper: Input, op_drug_count: int = 5) -> None:
    model = load_model_from_file(input_wrapper.get_estimator_id(), path_prefix='output/models/')
    y_pred, neighbors_pred, neighbors_dist = model.predict(input_wrapper.get_ndarray())
    neighbors = {neighbors_pred[0][i]: round(float(neighbors_dist[0][i]), 3) for i in range((len(neighbors_pred[0])))}
    output = Output(input_wrapper.get_estimator_id())
    # output.add_association(input_wrapper.get_all_values())
    for drug, dist in sorted(neighbors.items(), key=lambda x: x[1])[:op_drug_count]:
        drug_index = model.sample_names.index(drug)
        # symptom_association = list(np.round(model.data[drug_index, :].astype(float), 3))
        symptom_association = get_symptom_associations(drug_index, input_wrapper.get_input_params(), model.data)
        if len(symptom_association) > 0:
            disease_association = get_disease_associations(drug)
            confidence = round(compute_confidence(dist) * 100, 3)
            output.add_neighbor(drug, dist, confidence)
            output.add_symptom_association(symptom_association)
            output.add_disease_association(disease_association)
    print(json.dumps(output, cls=OutputEncoder))

    # from sklearn.metrics import euclidean_distances
    # from sklearn.metrics.pairwise import cosine_distances
    # print(y_pred)
    # print(neighbors_pred)
    # print(neighbors_dist)
    # distances = []
    # # print(input_wrapper.get_ndarray())
    # for i in range(model.data.shape[0]):
    #     distances.append( (model.sample_names[i],
    #                       euclidean_distances(input_wrapper.get_ndarray(), model.data[i, :].reshape(1, -1))[0, 0]) )
    # for d in sorted(distances, key=lambda x: x[1]):
    #     print(d)


inp = parse_input(sys.argv[1])
# params = inp.get_all_params()
# for i, x in enumerate(inp.get_all_values()):
#     print(str(i) + ' ' + params[i] + ' ' + str(x) + '<br/>')
predict_drugs(inp, op_drug_count=5)
