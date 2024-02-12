from ..ml.resource import read_ml_data
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import BallTree
from statistics import mean
import numpy as np
import pandas as pd


# Modified from https://github.com/lachhebo/pyclustertend/blob/master/pyclustertend/hopkins.py
def hopkins(data_frame, sampling_size: int, random_state: int | None = None) -> float:
    """Assess the clusterability of a dataset. A score between 0 and 1, a score around 0.5 express
    no clusterability and a score tending to 0 express a high cluster tendency.

    Parameters
    ----------
    data_frame : numpy array
        The input dataset
    sampling_size : int
        The sampling size which is used to evaluate the number of DataFrame.
    random_state : int
        The integer seed used for random sampling and generating uniformly distributed sample.

    Returns
    ---------------------
    score : float
        The hopkins score of the dataset (between 0 and 1)
    """

    np.random.seed(random_state)

    if type(data_frame) == np.ndarray:
        data_frame = pd.DataFrame(data_frame)

    # Sample n observations from D : P
    if sampling_size > data_frame.shape[0]:
        raise Exception('The number of sample of sample is bigger than the shape of D')

    data_frame_sample = data_frame.sample(n=sampling_size, random_state=random_state)

    # Get the distance to their nearest neighbors in D : X
    tree = BallTree(data_frame, leaf_size=2)
    dist, _ = tree.query(data_frame_sample, k=2)
    data_frame_sample_distances_to_nearest_neighbours = dist[:, 1]

    # Randomly simulate n points with the same variation as in D : Q.
    max_data_frame = data_frame.max()
    min_data_frame = data_frame.min()

    uniformly_selected_values_0 = np.random.uniform(min_data_frame[0], max_data_frame[0], sampling_size)
    uniformly_selected_values_1 = np.random.uniform(min_data_frame[1], max_data_frame[1], sampling_size)

    uniformly_selected_observations = np.column_stack((uniformly_selected_values_0, uniformly_selected_values_1))
    if len(max_data_frame) >= 2:
        for i in range(2, len(max_data_frame)):
            uniformly_selected_values_i = np.random.uniform(min_data_frame[i], max_data_frame[i], sampling_size)
            to_stack = (uniformly_selected_observations, uniformly_selected_values_i)
            uniformly_selected_observations = np.column_stack(to_stack)

    uniformly_selected_observations_df = pd.DataFrame(uniformly_selected_observations)

    # Get the distance to their nearest neighbors in D : Y

    tree = BallTree(data_frame, leaf_size=2)
    dist, _ = tree.query(uniformly_selected_observations_df, k=1)
    uniformly_df_distances_to_nearest_neighbours = dist

    # return the hopkins score

    x = sum(data_frame_sample_distances_to_nearest_neighbours)
    y = sum(uniformly_df_distances_to_nearest_neighbours)

    if x + y == 0:
        raise Exception('The denominator of the hopkins statistics is null')

    np.random.seed(None)

    return x / (x + y)[0]


def compute_clustering_tendency(data: np.array, random_state: int | None = 0, verbose: bool = False) -> float:
    sampling_fractions = [0.08, 0.09, 0.1, 0.11, 0.12]
    h_statistic_values = []
    for sf in sampling_fractions:
        h_statistic_values.append(hopkins(data, sampling_size=int(sf * data.shape[0]),
                                          random_state=random_state))
    if verbose:
        print(h_statistic_values)
    return mean(h_statistic_values)


# res = read_ml_data(association_type='cosine', verbose=True)
# hopkins_statistic = compute_clustering_tendency(StandardScaler().fit_transform(res.data), verbose=True)
# print(hopkins_statistic)
#
# res = read_ml_data(association_type='pearson', verbose=True)
# hopkins_statistic = compute_clustering_tendency(StandardScaler().fit_transform(res.data), verbose=True)
# print(hopkins_statistic)
#
# res = read_ml_data(association_type='jaccard', verbose=True)
# hopkins_statistic = compute_clustering_tendency(StandardScaler().fit_transform(res.data), verbose=True)
# print(hopkins_statistic)
