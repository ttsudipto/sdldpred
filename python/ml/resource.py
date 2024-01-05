from typing import Type, List, Dict
from sys import maxsize
import numpy as np
import csv

np.set_printoptions(threshold=maxsize)

path_prefix = 'input/'


# def get_ip_data_file_name(dataset):
#     return 'genomics_input_' + dataset + '.tsv'


# def get_ip_target_file_name(dataset):
#     return 'genomics_input_labels_' + dataset + '.tsv'


class DataResource:

    def __init__(self, dataset_name: str) -> None:
        self.d_type = DataResource._get_dtype(dataset_name)
        self.file_name = DataResource._get_file_name(dataset_name)
        self.data = None
        self.headers = None

    @staticmethod
    def _get_file_name(dataset_name: str) -> str:
        if dataset_name == 'CTD':
            return path_prefix + dataset_name + '/pulmonary_drug_disease_association_matrix_ctd.tsv'
        elif dataset_name == 'HSDN':
            return path_prefix + dataset_name + '/pulmonary_symptom_disease_association_matrix_hsdn.tsv'
        elif dataset_name == 'ML_cosine' or dataset_name == 'ML_pearson':
            return path_prefix + dataset_name[:2] + '/similarity_' + dataset_name[3:] + '_trimmed.tsv'
        elif dataset_name == 'ML_jaccard':
            return path_prefix + 'ML/similarity_jaccard.tsv'
        else:
            raise ValueError(
                'Error !!! Invalid dataset name. Correct values = {CTD, HSDN, ML_cosine, ML_pearson, ML_jaccard} ... '
            )

    @staticmethod
    def _get_dtype(dataset_name: str) -> Type:
        if dataset_name == 'CTD':
            return np.int32
        elif dataset_name == 'HSDN':
            return np.float32
        elif dataset_name == 'ML_cosine' or dataset_name == 'ML_pearson' or dataset_name == 'ML_jaccard':
            return np.float32
        else:
            raise ValueError(
                'Error !!! Invalid dataset name. Correct values = {CTD, HSDN, ML_cosine, ML_pearson, ML_jaccard} ... '
            )

    def _read_headers(self, offset: int, delimiter: str = '\t') -> List[str]:
        csvfile = open(self.file_name, 'r')
        reader = csv.DictReader(csvfile, delimiter=delimiter)
        headers = reader.fieldnames[offset:]
        csvfile.close()
        return headers

    def get_row_ids(self, return_type: str, header_lines: int, delimiter: str = '\t') -> List[str] | Dict[str, str]:
        if header_lines not in (1, 2):
            raise ValueError('Error !!! Invalid header lines. Must be 1 or 2 ...')
        csvfile = open(self.file_name, 'r')
        reader = csv.reader(csvfile, delimiter=delimiter)
        for i in range(header_lines):
            next(reader)
        if return_type == 'dict':
            rows = {row[0]: row[1] for row in reader}
        elif return_type == 'list':
            rows = [row[0] for row in reader]
        else:
            raise ValueError('Error !!! Invalid return type. Correct values = {dict, list}')
        csvfile.close()
        return rows

    def read_data_from_csv(self, col_start: int, col_end: int, header_lines: int, delimiter: str = '\t') -> None:
        self.headers = self._read_headers(col_start, delimiter)
        csvfile = open(self.file_name, 'r')
        self.data = np.genfromtxt(csvfile,
                                  delimiter=delimiter,
                                  skip_header=header_lines,
                                  usecols=range(col_start, col_end),
                                  dtype=self.d_type)
        csvfile.close()


class AssociationDataResource(DataResource):

    col_offset = 2
    delimiter = '\t'
    header_lines = 1

    def __init__(self, dataset_name: str) -> None:
        if dataset_name not in ('HSDN', 'CTD'):
            raise ValueError('Error !!! Invalid dataset name. Correct values = {CTD, HSDN} ... ')
        super().__init__(dataset_name)

    def _read_headers(self) -> List[str]:
        headers = super()._read_headers(AssociationDataResource.col_offset, AssociationDataResource.delimiter)
        return headers

    def get_row_ids(self) -> Dict[str, str]:
        rows = super().get_row_ids('dict', 1, AssociationDataResource.delimiter)
        return rows

    def read_data_from_csv(self) -> None:
        self.headers = self._read_headers()
        csvfile = open(self.file_name, 'r')
        self.data = np.genfromtxt(csvfile,
                                  delimiter=AssociationDataResource.delimiter,
                                  skip_header=AssociationDataResource.header_lines,
                                  usecols=range(2, len(self.headers) + 2),
                                  dtype=self.d_type)
        csvfile.close()


class MLDataResource(DataResource):

    col_offset = 2
    delimiter = '\t'
    header_lines = 2

    def __init__(self, association_type: str = 'cosine') -> None:
        if association_type not in ('cosine', 'pearson', 'jaccard'):
            raise ValueError('Error !!! Invalid association_type. Correct values = {cosine, pearson, jaccard}')
        super().__init__(dataset_name='ML_' + association_type)

    def _read_headers(self) -> List[str]:
        headers = super()._read_headers(MLDataResource.col_offset, MLDataResource.delimiter)
        return headers

    def get_row_ids(self) -> Dict[str, str]:
        rows = super().get_row_ids('dict', MLDataResource.header_lines, MLDataResource.delimiter)
        return rows

    def read_data_from_csv(self) -> None:
        self.headers = self._read_headers()
        csvfile = open(self.file_name, 'r')
        self.data = np.genfromtxt(csvfile,
                                  delimiter=MLDataResource.delimiter,
                                  skip_header=MLDataResource.header_lines,
                                  usecols=range(2, len(self.headers) + 2),
                                  dtype=self.d_type)
        csvfile.close()


def print_data_summary(res: DataResource) -> None:
    print('Data')
    print(res.data.shape)
    print(res.data[0, :10])
    print(res.data[-1, :10])
    print(res.data[0, -10:])
    print(res.data[-1, -10:])
    print()


def read_association_data(dataset_name: str, verbose: bool = False) -> DataResource:
    res = AssociationDataResource(dataset_name)
    res.read_data_from_csv()
    if verbose:
        print_data_summary(res)
    return res


def read_ml_data(association_type: str = 'cosine', verbose: bool = False) -> DataResource:
    res = MLDataResource(association_type=association_type)
    res.read_data_from_csv()
    if verbose:
        print_data_summary(res)
    return res
