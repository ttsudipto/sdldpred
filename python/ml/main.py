from .resource import read_ml_data
from .model import Model
from .grid_search import grid_search_k_means
from .grid_search import grid_search_bisecting_k_means
from .grid_search import grid_search_agglomerative_clustering
from .grid_search import grid_search_dbscan
from.grid_search import grid_search_mean_shift
from .grid_search import grid_search_birch
from .grid_search import get_optimal_clusters


res = read_ml_data(verbose=True)
samples = res.get_row_ids()
sample_ids = list(samples.keys())
sample_names = list(samples.values())

# grid_search_k_means(res.data, sample_names, scale=False)
# grid_search_bisecting_k_means(res.data, sample_names, scale=False)
# grid_search_agglomerative_clustering(res.data, sample_names, scale=False)
# grid_search_dbscan(res.data, sample_names, scale=False)
# grid_search_mean_shift(res.data, sample_names, scale=False)
# grid_search_birch(res.data, sample_names, scale=False)

# get_optimal_clusters(res.data, sample_names, 'KMC', scale=False, verbose=True)
# get_optimal_clusters(res.data, sample_names, 'BKM', scale=False, verbose=True)
# get_optimal_clusters(res.data, sample_names, 'AGMC', scale=False, verbose=True)
# get_optimal_clusters(res.data, sample_names, 'DBSCAN', scale=False, verbose=True)


# from sklearn.metrics import pairwise_distances
# import numpy as np
# de = pairwise_distances(res.data, metric='euclidean', n_jobs=-1)
# dm = pairwise_distances(res.data, metric='manhattan', n_jobs=-1)
# dc = pairwise_distances(res.data, metric='cosine', n_jobs=-1)
# print('Euclidean:', de.shape, np.min(de), np.max(de), np.mean(de), np.median(de))
# print('Manhattan:', dm.shape, np.min(dm), np.max(dm), np.mean(dm), np.median(dm))
# print('Cosine:', dc.shape, np.min(dc), np.max(dc), np.mean(dc), np.median(dc))

# model = Model('KMC', res.data, list(sample_names.values()))
# print(len(model.sample_names), model.data.shape)
# model.learn({})
# # print(model.total_estimator.labels_)
# # for k, v in model.clusters.items():
# #     print(k, '->', v)
# sil_score, ch_score, db_score = model.get_metrics()
# print(sil_score, ch_score, db_score)
# clusters, named_clusters = model.get_clusters()
# # for c in clusters:
# #     print(c)
# # for c in named_clusters:
# #     print(c)
