from .model import Model
from copy import deepcopy


class ModelMetadata:
    def __init__(self, model: Model) -> None:
        self.estimator_id = model.estimator_id
        self.sample_names = model.sample_names
        self.n_folds = model.n_folds
        self.trained = model.trained
        # self.estimators = []
        # self.total_estimator = None
        self.train_indices = model.train_indices
        self.test_indices = model.test_indices
        self.clusters = model.clusters
        self.data = model.data
        self.dataScaler = model.dataScaler

    def get_model(self) -> Model:
        model = Model(self.estimator_id, deepcopy(self.data), deepcopy(self.sample_names),
                      k=self.n_folds, do_shuffle=False)
        model.trained = self.trained
        model.train_indices = deepcopy(self.train_indices)
        model.test_indices = deepcopy(self.test_indices)
        model.clusters = deepcopy(self.clusters)
        model.dataScaler = deepcopy(self.dataScaler)
        return model
