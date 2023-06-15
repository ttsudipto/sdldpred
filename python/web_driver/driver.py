from ..ml.pickler import load_model_from_file
from ..ml.confidence import compute_confidence
from .io_wrapper import Input, Output, OutputEncoder
import numpy as np
import json
import sys


def parse_input(input_json: str) -> Input:
    json_dict = json.loads(input_json)
    input_wrapper = Input()
    params = input_wrapper.get_all_params()
    for p in params:
        if p in json_dict:
            input_wrapper.add_value(json_dict[p] / 10)
        else:
            input_wrapper.add_value(0.0)
    return input_wrapper


def predict_drugs(input_wrapper: Input) -> None:
    model = load_model_from_file(input_wrapper.get_estimator_id(), path_prefix='output/models/')
    y_pred, neighbors_pred, neighbors_dist = model.predict(input_wrapper.get_ndarray())
    neighbors = {neighbors_pred[0][i]: round(float(neighbors_dist[0][i]), 3) for i in range((len(neighbors_pred[0])))}
    output = Output(input_wrapper.get_estimator_id())
    output.add_association(input_wrapper.get_all_values())
    for drug, dist in sorted(neighbors.items(), key=lambda x: x[1]):
        data_index = model.sample_names.index(drug)
        association = list(np.round(model.data[data_index, :].astype(float), 3))
        confidence = round(compute_confidence(dist) * 100, 3)
        output.add_neighbor(drug, dist, confidence)
        output.add_association(association)
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
predict_drugs(inp)
