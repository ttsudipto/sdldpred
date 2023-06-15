from typing import Dict, List, Tuple
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
from sklearn.metrics import calinski_harabasz_score
from sklearn.metrics import davies_bouldin_score
from sklearn.metrics.pairwise import euclidean_distances
from sklearn.model_selection import KFold
from sklearn.utils import shuffle
from sklearn.cluster import KMeans
from sklearn.cluster import BisectingKMeans
from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import DBSCAN
from sklearn.cluster import MeanShift
from sklearn.cluster import Birch
import numpy as np
import copy


class Model:

    def __init__(self, e_id: str, x: np.array, sample_names: List[str], k: int = 5, do_shuffle: bool = False) -> None:
        self.estimator_id = e_id
        self.sample_names = sample_names
        self.n_folds = k
        self.trained = False
        self.estimators = []
        self.total_estimator = None
        self.train_indices = []
        self.test_indices = []
        self.clusters = None
        if do_shuffle:
            self.data = shuffle(x, random_state=42)
        else:
            self.data = x
        self._split_cv_folds()
        self.dataScaler: StandardScaler | object = StandardScaler().fit(self.data)

    def is_trained(self) -> bool:
        return self.trained

    def create_estimator(self, params: Dict) \
            -> KMeans | BisectingKMeans | AgglomerativeClustering | DBSCAN | MeanShift | Birch:
        estimator = None
        if self.estimator_id == 'KMC':  # K-Means clustering
            estimator = KMeans(random_state=1, n_init='auto', max_iter=1000)
        elif self.estimator_id == 'BKM':  # Bisecting K-Means clustering
            estimator = BisectingKMeans(random_state=1, init='k-means++', n_init=1, max_iter=1000)
        elif self.estimator_id == "AGMC":  # Agglomerative clustering
            estimator = AgglomerativeClustering(compute_distances=True, compute_full_tree='auto')
        elif self.estimator_id == 'DBSCAN':  # DBSCAN
            estimator = DBSCAN(n_jobs=-1, algorithm='auto')
        elif self.estimator_id == 'MS':  # Mean-shift
            estimator = MeanShift(bin_seeding=False, min_bin_freq=1, cluster_all=True, n_jobs=-1, max_iter=10000)
        elif self.estimator_id == 'BIRCH':  # BIRCH
            estimator = Birch()
        else:
            raise ValueError('Error !!! Invalid name. Correct values = {KMC, AGMC, DBSCAN, MS, BIRCH} ... ')
        estimator.set_params(**params)
        return estimator

    def _split_cv_folds(self) -> None:
        if self.n_folds == 1:
            self.train_indices = [range(self.data.shape[0])]
            self.test_indices = [range(self.data.shape[0])]
        else:
            skf = KFold(n_splits=self.n_folds, shuffle=True, random_state=42)
            for train_index, test_index in skf.split(self.data):
                self.train_indices.append(train_index)
                self.test_indices.append(test_index)

    def _learn_without_cv(self, params: Dict, scale: bool = False) -> None:
        self.trained = False
        estimator = self.create_estimator(params)
        if scale:
            estimator.fit(self.dataScaler.transform(self.data))
        else:
            estimator.fit(self.data)
        self.total_estimator = copy.deepcopy(estimator)
        self.clusters = dict()
        for i in range(self.data.shape[0]):
            if self.total_estimator.labels_[i] in self.clusters:
                self.clusters[self.total_estimator.labels_[i]].append(i)
            else:
                self.clusters[self.total_estimator.labels_[i]] = [i]
        self.trained = True

    # def learn_k_fold(self, params: Dict, scale: bool = False):
    #     self.estimators = []
    #     for f in range(self.n_folds):
    #         estimator = self.create_estimator(params)
    #         if scale:
    #             estimator.fit(self.dataScaler.transform(self.data[self.train_indices[f]]))
    #         else:
    #             estimator.fit(self.data[self.train_indices[f]])
    #         self.estimators.append(copy.deepcopy(estimator))

    def learn(self, params: Dict, scale: bool = False) -> None:
        self._learn_without_cv(params, scale)
        # self.learn_k_fold(params, scale)

    def get_clusters(self) -> Tuple[List[List[int]], List[List[str]]]:
        if self.is_trained():
            clusters = [indices for indices in self.clusters.values()]
            named_clusters = [[self.sample_names[index] for index in indices] for indices in self.clusters.values()]
            return clusters, named_clusters

        raise RuntimeError('Error !!! Model not trained ...')

    def get_metrics(self, scale: bool = False) -> Tuple[float, float, float]:
        if self.is_trained():
            if scale:
                x = self.dataScaler.transform(self.data)
            else:
                x = self.data
            sil_score = silhouette_score(x, self.total_estimator.labels_)
            db_score = davies_bouldin_score(x, self.total_estimator.labels_)
            ch_score = calinski_harabasz_score(x, self.total_estimator.labels_)
            return sil_score, db_score, ch_score

        raise RuntimeError('Error !!! Model not trained ...')

    def _predict_blind_without_cv(self, b_data: np.array, scale: bool = False) \
            -> Tuple[np.array, List[List[str]], List[List[float]]]:
        if not self.is_trained():
            raise RuntimeError('Error !!! Model not trained ...')

        if scale:
            b_data = self.dataScaler.transform(b_data)
        y_pred = self.total_estimator.predict(b_data)
        neighbors_pred = [[self.sample_names[x] for x in self.clusters[y_pred[i]]] for i in range(y_pred.shape[0])]
        neighbors_dist = [
            [euclidean_distances(b_data, self.data[x, :] . reshape(1, -1))[0, 0] for x in self.clusters[y_pred[i]]]
            for i in range(y_pred.shape[0])
        ]

        return y_pred, neighbors_pred, neighbors_dist

    # def predict_one_fold(self, estimator, x_test: np.array, scale: bool = True):
    #     if scale:
    #         x_test = self.dataScaler.transform(x_test)
    #
    #     y_pred = estimator.predict(x_test)
    #
    #     # print(y_pred.shape)
    #     return y_pred

    def predict(self, b_data: np.array, scale: bool = False) -> Tuple[np.array, List[List[str]], List[List[float]]]:
        return self._predict_blind_without_cv(b_data, scale)
