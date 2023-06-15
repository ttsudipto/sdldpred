from typing import List, Tuple
from .resource import DataResource, read_ml_data
from .model import Model
from .model_metadata import ModelMetadata
import numpy as np
import pickle
import joblib
import sys


optimal_grids = {
    'KMC': {'init': 'k-means++', 'n_clusters': 470},
    'BKM': {'bisecting_strategy': 'biggest_inertia', 'n_clusters': 480},
    'MS': {'bandwidth': 0.25},
    'BIRCH': {'threshold': 0.1, 'branching_factor': 8, 'n_clusters': 480}
}


def input_data() -> Tuple[DataResource, List[str]]:
    resource = read_ml_data(verbose=True)
    sample_names = list(resource.get_row_ids().values())
    return resource, sample_names


def dump_model_to_file(model: Model, path_prefix: str = '') -> None:
    f_name = path_prefix + model.estimator_id + '_estimator.joblib'
    md_f_name = path_prefix + model.estimator_id + '_metadata.pkl'
    old_rec_limit = sys.getrecursionlimit()
    sys.setrecursionlimit(0x1000)
    joblib.dump(model.total_estimator, f_name)
    sys.setrecursionlimit(old_rec_limit)
    md = ModelMetadata(model)
    metadata_file = open(md_f_name, 'wb')
    pickle.dump(md, metadata_file)
    metadata_file.close()


def load_model_from_file(estimator_id: str, path_prefix: str = '') -> Model:
    f_name = path_prefix + estimator_id + '_estimator.joblib'
    md_f_name = path_prefix + estimator_id + '_metadata.pkl'
    metadata_file = open(md_f_name, 'rb')  # load metadata
    md = pickle.load(metadata_file, encoding='latin1')
    metadata_file.close()
    model = md.get_model()  # `model` without estimators
    model.total_estimator = joblib.load(f_name)  # load total_estimator
    return model


def check_clustering_metrics(model: Model) -> None:
    n_clusters = len(model.get_clusters()[0])
    sil_score, db_score, ch_score = model.get_metrics(scale=False)
    max_cluster_size = np.max([len(c) for i, c in model.clusters.items() if i != -1])
    min_cluster_size = np.min([len(c) for i, c in model.clusters.items() if i != -1])
    mean_cluster_size = float(np.mean([len(c) for i, c in model.clusters.items() if i != -1]))
    median_cluster_size = float(np.median([len(c) for i, c in model.clusters.items() if i != -1]))
    print(model.estimator_id, n_clusters, round(sil_score, 3), round(db_score, 3), round(ch_score, 3),
          min_cluster_size, max_cluster_size, round(mean_cluster_size, 3), round(median_cluster_size, 3),
          optimal_grids[model.estimator_id])


def perform_clustering(estimator_id: str, data: np.array, sample_names: List[str], verbose: bool = True) -> Model:
    model = Model(estimator_id, data, sample_names)
    model.learn(optimal_grids[estimator_id], scale=False)
    if verbose:
        check_clustering_metrics(model)
    return model
