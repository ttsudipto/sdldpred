from typing import List

from .model import Model
import numpy as np


k_means_param_grid = {
    'init': ['k-means++', 'random'],
    'n_clusters': list(range(10, 601, 10))
}

bisecting_k_means_param_grid = {
    'bisecting_strategy': ['biggest_inertia'],
    'n_clusters': list(range(20, 601, 20))
}

agglomerative_grid = {
    'linkage': ['ward', 'single', 'complete', 'average'],
    'metric_single': ['euclidean', 'manhattan', 'cosine'],
    'metric_complete': ['euclidean', 'manhattan', 'cosine'],
    'metric_average': ['euclidean', 'manhattan', 'cosine'],
    'metric_ward': ['euclidean'],
    'n_clusters': list(range(10, 601, 10))
}

dbscan_grid = {
    'metric': ['euclidean', 'manhattan', 'cosine'],
    'min_samples': [3, 4, 5],
    'eps_euclidean': np.linspace(0.01, 2, 200).tolist(),
    'eps_manhattan': list(range(1, 30)),
    'eps_cosine': np.linspace(0.01, 1, 200).tolist(),
    # [0.1, 0.3, 0.5, 0.7, 0.9, 0.91, 0.93, 0.95, 0.97, 0.99, 1, 1.1, 1.3, 1.5, 1.7, 1.9, 2, 3, 4, 5, 6]
}

mean_shift_grid = {'bandwidth': np.linspace(0.05, 2, 40)}

birch_grid = {
    'threshold': np.linspace(0.1, 2, 20),
    'branching_factor': list(range(5, 16)),
    'n_clusters': list(range(20, 601, 20))
}

optimal_grids = {
    'KMC': {'init': 'k-means++', 'n_clusters': 470},
    'BKM': {'bisecting_strategy': 'biggest_inertia', 'n_clusters': 480},
    'MS': {'bandwidth': 0.25},
    'BIRCH': {'threshold': 0.1, 'branching_factor': 8, 'n_clusters': 480}
}


def print_param_grid(name: str) -> None:
    if name == 'KMC':
        grid = k_means_param_grid
    elif name == 'BKM':
        grid = bisecting_k_means_param_grid
    elif name == 'AGMC':
        grid = agglomerative_grid
    elif name == 'DBSCAN':
        grid = dbscan_grid
    elif name == 'MS':
        grid = mean_shift_grid
    elif name == 'BIRCH':
        grid = birch_grid
    else:
        raise ValueError('Error !!! Invalid name. Correct values = {KMC, BKM, AGMC, DBSCAN, MS, BIRCH} ... ')

    for k, v in grid.items():
        print((k + " = " + str(v)) .replace('[', '{') .replace(']', '}'))


def get_optimal_clusters(x, sample_names, estimator_id, scale=False, verbose=False):
    model = Model(e_id=estimator_id, x=x, sample_names=sample_names)
    param = optimal_grids[estimator_id]
    model.learn(param, scale)
    clusters = model.get_clusters()[1]
    if verbose:
        print('Cluster\tCluster size\tDrugs')
        for i, cluster in sorted(enumerate(clusters), key=lambda c: len(c[1]), reverse=True):
            print(str(i) + '\t' + str(len(cluster)) + '\t' + ';'.join(cluster))
    return clusters


def grid_search_k_means(x: np.array, sample_names: List[str], scale: bool = False, warning_ignore: bool = True) -> None:
    if warning_ignore:
        import warnings
        warnings.filterwarnings('ignore')
    print('init', 'n_clusters', 'Silhouette score', 'Davies-Bouldin score', 'Calinski-Harabasz score',
          'min(cluster_size)', 'max(cluster_size)', 'mean(cluster_size)', 'median(cluster_size)')
    model = Model(e_id='KMC', x=x, sample_names=sample_names)
    for init_method in k_means_param_grid['init']:
        for nc in k_means_param_grid['n_clusters']:
            param = {'init': init_method, 'n_clusters': nc}
            model.learn(param, scale)
            sil_score, db_score, ch_score = model.get_metrics(scale)
            max_cluster_size = np.max([len(c) for i, c in model.clusters.items() if i != -1])
            min_cluster_size = np.min([len(c) for i, c in model.clusters.items() if i != -1])
            mean_cluster_size = np.mean([len(c) for i, c in model.clusters.items() if i != -1])
            median_cluster_size = np.median([len(c) for i, c in model.clusters.items() if i != -1])
            print(init_method, nc, round(sil_score, 3), round(db_score, 3), round(ch_score, 3),
                  min_cluster_size, max_cluster_size, round(mean_cluster_size, 3), round(median_cluster_size, 3))
    print_param_grid('KMC')
    return


def grid_search_bisecting_k_means(x: np.array, sample_names: List[str], scale: bool = False) -> None:
    print('bisecting_strategy', 'n_clusters', 'Silhouette score', 'Davies-Bouldin score', 'Calinski-Harabasz score',
          'min(cluster_size)', 'max(cluster_size)', 'mean(cluster_size)', 'median(cluster_size)')
    model = Model(e_id='BKM', x=x, sample_names=sample_names)
    for bs in bisecting_k_means_param_grid['bisecting_strategy']:
        for nc in bisecting_k_means_param_grid['n_clusters']:
            param = {'bisecting_strategy': bs, 'n_clusters': nc}
            model.learn(param, scale)
            sil_score, db_score, ch_score = model.get_metrics(scale)
            max_cluster_size = np.max([len(c) for i, c in model.clusters.items() if i != -1])
            min_cluster_size = np.min([len(c) for i, c in model.clusters.items() if i != -1])
            mean_cluster_size = np.mean([len(c) for i, c in model.clusters.items() if i != -1])
            median_cluster_size = np.median([len(c) for i, c in model.clusters.items() if i != -1])
            print(bs, nc, round(sil_score, 3), round(db_score, 3), round(ch_score, 3),
                  min_cluster_size, max_cluster_size, round(mean_cluster_size, 3), round(median_cluster_size, 3))
    print_param_grid('BKM')
    return


def grid_search_agglomerative_clustering(x: np.array, sample_names: List[str], scale: bool = False) -> None:
    print('linkage', 'metric', 'n_clusters', 'Silhouette score', 'Davies-Bouldin score', 'Calinski-Harabasz score',
          'min(cluster_size)', 'max(cluster_size)', 'mean(cluster_size)', 'median(cluster_size)')
    model = Model(e_id='AGMC', x=x, sample_names=sample_names)
    for ln in agglomerative_grid['linkage']:
        for m in agglomerative_grid['metric_' + ln]:
            for nc in agglomerative_grid['n_clusters']:
                param = {'compute_distances': False, 'linkage': ln, 'metric': m, 'n_clusters': nc}
                model.learn(param, scale)
                sil_score, db_score, ch_score = model.get_metrics(scale)
                max_cluster_size = np.max([len(c) for i, c in model.clusters.items() if i != -1])
                min_cluster_size = np.min([len(c) for i, c in model.clusters.items() if i != -1])
                mean_cluster_size = np.mean([len(c) for i, c in model.clusters.items() if i != -1])
                median_cluster_size = np.median([len(c) for i, c in model.clusters.items() if i != -1])
                print(ln, m, nc, round(sil_score, 3), round(db_score, 3), round(ch_score, 3),
                      min_cluster_size, max_cluster_size, round(mean_cluster_size, 3), round(median_cluster_size, 3))
    print_param_grid('AGMC')
    return


def grid_search_dbscan(x: np.array, sample_names: List[str], scale: bool = False) -> None:
    print('metric', 'min_samples', 'eps', 'Silhouette score', 'Davies-Bouldin score', 'Calinski-Harabasz score',
          'n_clusters', 'Clustered sample size', 'Noisy sample size',
          'min(cluster_size)', 'max(cluster_size)', 'mean(cluster_size)', 'median(cluster_size)')
    model = Model(e_id='DBSCAN', x=x, sample_names=sample_names)
    for m in dbscan_grid['metric']:
        for ms in dbscan_grid['min_samples']:
            for eps in dbscan_grid['eps_' + m]:
                param = {'metric': m, 'min_samples': ms, 'eps': eps}
                model.learn(param, scale)
                try:
                    sil_score, db_score, ch_score = model.get_metrics(scale)
                except ValueError:
                    sil_score = db_score = ch_score = 0
                n_clusters = len(model.clusters)
                max_cluster_size = np.max([len(c) for i, c in model.clusters.items() if i != -1])
                min_cluster_size = np.min([len(c) for i, c in model.clusters.items() if i != -1])
                mean_cluster_size = np.mean([len(c) for i, c in model.clusters.items() if i != -1])
                median_cluster_size = np.median([len(c) for i, c in model.clusters.items() if i != -1])
                noisy_sample_size = 0
                if -1 in model.clusters:
                    n_clusters -= 1
                    noisy_sample_size = len(model.clusters[-1])
                clustered_sample_size = x.shape[0] - noisy_sample_size
                print(m, ms, round(eps, 3), round(sil_score, 3), round(db_score, 3), round(ch_score, 3),
                      n_clusters, clustered_sample_size, noisy_sample_size,
                      min_cluster_size, max_cluster_size, round(mean_cluster_size, 3), round(median_cluster_size, 3))
    print_param_grid('DBSCAN')
    return


def grid_search_mean_shift(x: np.array, sample_names: List[str], scale: bool = False) -> None:
    print('bandwidth', 'Silhouette score', 'Davies-Bouldin score', 'Calinski-Harabasz score',
          'n_clusters', 'min(cluster_size)', 'max(cluster_size)', 'mean(cluster_size)', 'median(cluster_size)')
    model = Model(e_id='MS', x=x, sample_names=sample_names)
    for bw in mean_shift_grid['bandwidth']:
        param = {'bandwidth': bw}
        model.learn(param, scale)
        # print(model.total_estimator.labels_)
        try:
            sil_score, db_score, ch_score = model.get_metrics(scale)
        except ValueError:
            sil_score = db_score = ch_score = 0
        n_clusters = len(model.clusters)
        max_cluster_size = np.max([len(c) for i, c in model.clusters.items() if i != -1])
        min_cluster_size = np.min([len(c) for i, c in model.clusters.items() if i != -1])
        mean_cluster_size = np.mean([len(c) for i, c in model.clusters.items() if i != -1])
        median_cluster_size = np.median([len(c) for i, c in model.clusters.items() if i != -1])
        print(round(bw, 3), round(sil_score, 3), round(db_score, 3), round(ch_score, 3), n_clusters,
              min_cluster_size, max_cluster_size, round(mean_cluster_size, 3), round(median_cluster_size, 3))
    print_param_grid('MS')
    return


def grid_search_birch(x: np.array, sample_names: List[str], scale: bool = False) -> None:
    print('threshold', 'branching_factor', 'n_clusters', 'Silhouette score', 'Davies-Bouldin score', 'Calinski-Harabasz score',
          'min(cluster_size)', 'max(cluster_size)', 'mean(cluster_size)', 'median(cluster_size)')
    model = Model(e_id='BIRCH', x=x, sample_names=sample_names)
    for t in birch_grid['threshold']:
        for bf in birch_grid['branching_factor']:
            for nc in birch_grid['n_clusters']:
                param = {'threshold': t, 'branching_factor': bf, 'n_clusters': nc}
                import warnings
                warnings.filterwarnings('ignore')
                model.learn(param, scale)
                sil_score, db_score, ch_score = model.get_metrics(scale)
                max_cluster_size = np.max([len(c) for i, c in model.clusters.items() if i != -1])
                min_cluster_size = np.min([len(c) for i, c in model.clusters.items() if i != -1])
                mean_cluster_size = np.mean([len(c) for i, c in model.clusters.items() if i != -1])
                median_cluster_size = np.median([len(c) for i, c in model.clusters.items() if i != -1])
                print(round(t, 1), bf, nc, round(sil_score, 3), round(db_score, 3), round(ch_score, 3),
                      min_cluster_size, max_cluster_size, round(mean_cluster_size, 3), round(median_cluster_size, 3))
    print_param_grid('BIRCH')
    return


def get_optimal_performance(e_id: str, x: np.array, sample_names: List[str], scale: bool = False) -> None:
    # print('estimator_id', 'n_clusters', 'Silhouette score', 'Davies-Bouldin score',
    #       'Calinski-Harabasz score',
    #       'min(cluster_size)', 'max(cluster_size)', 'mean(cluster_size)', 'median(cluster_size)', 'params')
    model = Model(e_id, x, sample_names)
    model.learn(optimal_grids[e_id], scale=False)
    n_clusters = len(model.get_clusters()[0])
    sil_score, db_score, ch_score = model.get_metrics(scale=False)
    max_cluster_size = np.max([len(c) for i, c in model.clusters.items() if i != -1])
    min_cluster_size = np.min([len(c) for i, c in model.clusters.items() if i != -1])
    mean_cluster_size = float(np.mean([len(c) for i, c in model.clusters.items() if i != -1]))
    median_cluster_size = float(np.median([len(c) for i, c in model.clusters.items() if i != -1]))
    print(e_id, n_clusters, round(sil_score, 3), round(db_score, 3), round(ch_score, 3), min_cluster_size,
          max_cluster_size, round(mean_cluster_size, 3), round(median_cluster_size, 3), optimal_grids[e_id])
