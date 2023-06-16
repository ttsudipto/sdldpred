from typing import List, Tuple
from sklearn.metrics.pairwise import euclidean_distances
from scipy.stats import gaussian_kde
from scipy.integrate import simps
from csv import DictReader
from .model import Model
from .pickler import load_model_from_file
import numpy as np


def compute_drug_distances(model: Model, verbose: bool = False) -> List[float]:
    distances = []
    for i in range(model.data.shape[0] - 1):
        for j in range(i + 1, model.data.shape[0]):
            dist = euclidean_distances(model.data[i, :].reshape(1, -1), model.data[j, :].reshape(1, -1))
            distances.append(float(dist[0, 0]))
    if verbose:
        print('Distance')
        for d in sorted(distances):
            print(d)
    return distances


def compute_cluster_distances(model: Model) -> List[float]:
    cluster_centers = model.total_estimator.cluster_centers_
    distances = []
    for i in range(cluster_centers.shape[0] - 1):
        for j in range(i + 1, cluster_centers.shape[0]):
            dist = euclidean_distances(cluster_centers[i, :].reshape(1, -1), cluster_centers[j, :]. reshape(1, -1))
            distances.append(float(dist[0, 0]))
    return distances


def load_drug_distances() -> List[float]:
    f = open('output/density/distances.tsv', 'r')
    reader = DictReader(f, delimiter='\t')
    distances = []
    for row in reader:
        distances.append(float(row['Distance']))
    return distances


def print_distances(distances: List[float]) -> None:
    for d in distances:
        print(d)


def print_gaussian(distances: List[float]) -> Tuple:
    density = gaussian_kde(distances)
    min_distance = 0
    max_distance = float(
        euclidean_distances(np.ones((1, 305), dtype=np.float32), np.zeros((1, 305), dtype=np.float32))[0, 0]
    )
    x_values = np.linspace(min_distance, max_distance, int(np.max(distances) * 1000))
    density.covariance_factor = lambda: 0.25
    density._compute_covariance()
    densities = density(x_values)
    print('Distance' + '\t' + 'Density')
    for i in range(len(x_values)):
        print(str(round(x_values[i], 4)) + '\t' + str(round(densities[i], 4)))
    return x_values, densities


def print_histogram(distances):
    min_distance = 0
    max_distance = float(
        euclidean_distances(np.ones((1, 305), dtype=np.float32), np.zeros((1, 305), dtype=np.float32))[0, 0]
    )
    hist, xs = np.histogram(distances, bins='scott', range=(min_distance, max_distance))
    print('Distance\tFrequency')
    for i in range(len(hist)):
        print(str(round(xs[i], 4)) + '\t' + str(hist[i]))


def load_density() -> np.array:
    filename = 'output/density/density.tsv'
    csvfile = open(filename)
    density = np.genfromtxt(csvfile, delimiter='\t', skip_header=1)
    csvfile.close()
    return density


def compute_confidence(distance: float) -> float:
    density = load_density()
    masked_data = np.ma.masked_where((density[:, 0] < distance), density[:, 0])
    score_index = np.argmin(masked_data)
    # print(masked_data)
    # print(score_index)
    # print(density[score_index:, 0])
    # print(density[score_index:, 1])
    return simps(density[score_index:, 1], density[score_index:, 0])


# m = load_model_from_file('KMC', path_prefix='output/models/')
# m = load_model_from_file('BKM', path_prefix='output/models/')
# m = load_model_from_file('MS', path_prefix='output/models/')
# m = load_model_from_file('BIRCH', path_prefix='output/models/')

# drug_distances = compute_drug_distances(m, verbose=False)
# drug_distances = load_drug_distances()
# print(len(drug_distances))
# print(np.min(drug_distances), np.max(drug_distances), np.mean(drug_distances), np.median(drug_distances))

# xs, dens = print_gaussian(drug_distances)
# density = load_density()
# # print(density)

# print_histogram(drug_distances)

# for i in range(density.shape[0]):
#     print(str(density[i, 0]) + '\t' + str(round(compute_confidence(density[i, 0]), 4)))
# confidence = compute_confidence(0)
# print(confidence)

# cluster_distances = compute_cluster_distances(m)
# print(len(cluster_distances))
# print(np.min(cluster_distances), np.max(cluster_distances), np.mean(cluster_distances), np.median(cluster_distances))
