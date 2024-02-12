from typing import Dict, List
from csv import DictReader, field_size_limit
from sys import maxsize
from statistics import mean, median
import ssmpy
import random
from ..chebi.chebi_util import read_pulmonary_drugs_chebi


field_size_limit(maxsize)
ont = 'role'
# ont = 'entity'
# ont = 'all'


def create_ontology_db(input_owl_file: str, output_db_file: str) -> None:
    ssmpy.create_semantic_base('input/ChEBI/' + input_owl_file, output_db_file,
                               'http://purl.obolibrary.org/obo/', 'http://www.w3.org/2000/01/rdf-schema#subClassOf', '')
    return


def set_ontology_db(ontology: str) -> None:
    if ontology == 'role':
        ssmpy.semantic_base('input/ChEBI/chebi_lite_role.db')
    elif ontology == 'entity':
        ssmpy.semantic_base('input/ChEBI/chebi_lite_entity.db')
    elif ontology == 'all':
        ssmpy.semantic_base('input/ChEBI/chebi.db')
    else:
        raise ValueError('Error !!! Invalid ontology. Correct values = {\'role\', \'entity\', \'all\'} ...')
    ssmpy.ssm.mica = True
    ssmpy.ssm.intrinsic = True


def has_ssmpy_id(drug: str) -> bool:
    return ssmpy.get_id('CHEBI_' + drug) != -1


def get_drug_clusters(similarity: str, cluster_algo: str) -> Dict[str, List[str]]:
    f = open('output/gs/' + similarity + '/optimal_clusters_' + cluster_algo + '.tsv', 'r')
    reader = DictReader(f, delimiter='\t')
    clusters = dict()
    for row in reader:
        drugs = row['Drugs'].split(';')
        clusters[row['Cluster']] = drugs
    return clusters


def get_random_drug_cluster(n: int, similarity: str, cluster_algo: str, drugs: List[str]) -> Dict[str, List[str]]:
    # random.seed(11)  # ont = 'role'
    # random.seed(2)  # ont = 'entity'
    s = 2 if ont == 'entity' else 11
    random.seed(s)
    clusters = get_drug_clusters(similarity, cluster_algo)
    nc = 0
    for d in clusters.values():
        if len(d) > 1:
            nc += 1
    random_clusters = dict()
    chebi_map = read_pulmonary_drugs_chebi(key='name')
    chebi_drugs = [d for d in drugs if (d in chebi_map and has_ssmpy_id(chebi_map[d]))]
    for i in range(n):
        random_indices = random.sample(range(len(chebi_drugs)), 1271//nc)
        random_clusters[str(i+1)] = [chebi_drugs[index] for index in random_indices]
        print(random_indices)
        print(random_clusters['1'])
    return random_clusters


def compute_semantic_similarity(drugs: List[str], measure: str = 'jiang') -> List[float]:
    similarity = list()
    for i in range(len(drugs) - 1):
        for j in range(i+1, len(drugs)):
            e1 = ssmpy.get_id('CHEBI_' + drugs[i])
            e2 = ssmpy.get_id('CHEBI_' + drugs[j])
            # print(drugs[i], drugs[j], e1, e2)
            if measure == 'jiang':
                sim = ssmpy.ssm_jiang_conrath(e1, e2)
            elif measure == 'lin':
                sim = ssmpy.ssm_lin(e1, e2)
            elif measure == 'resnik':
                sim = ssmpy.ssm_resnik(e1, e2)
            else:
                raise ValueError('Error !!! Invalid key. Correct values = {\'jiang\', \'lin\', \'resnik\'} ...')
            similarity.append(round(sim, 3))
    return similarity


def compute_cluster_similarity(similarity: str, cluster_algo: str, measure: str = 'jiang') -> Dict[str, List[float]]:
    chebi_map = read_pulmonary_drugs_chebi(key='name')
    if cluster_algo[0:6] == 'random':
        clusters = get_random_drug_cluster(1, similarity, cluster_algo[7:], list(chebi_map.keys()))
    else:
        clusters = get_drug_clusters(similarity, cluster_algo)
    cluster_similarity = dict()
    i = 1
    for cluster, drugs in clusters.items():
        # if len(drugs) > 5 or len(drugs) < 5:
        #     continue
        chebi_drugs = [chebi_map[d] for d in drugs if (d in chebi_map and has_ssmpy_id(chebi_map[d]))]
        print("Cluster " + cluster + " (" + str(i) + "/" + str(len(clusters)) + ") => Found " +
              str(len(chebi_drugs)) + "/" + str(len(drugs)) + " drugs ")
        if len(drugs) > 1:
            if len(chebi_drugs) > 1:
                similarity = compute_semantic_similarity(chebi_drugs, measure)
                cluster_similarity[cluster] = similarity
            elif len(chebi_drugs) == 1:
                cluster_similarity[cluster] = [1.0]
            else:
                cluster_similarity[cluster] = [0.0]
        i = i + 1
    return cluster_similarity


def print_cluster_similarity(cluster_similarity: Dict[str, List[float]]) -> None:
    print('Cluster_label\tCluster\tPairwise_similarities')
    i = 1
    for cluster, similarities in cluster_similarity.items():
        print(cluster + '\t' + str(i) + '\t' + ';'.join([str(s) for s in similarities]))
        i = i + 1
    return


def read_cluster_similarity(similarity: str, cluster_algo: str, ontology: str, measure: str = 'jiang',
                            verbose: bool = False) -> Dict[str, List[float]]:
    f = open('output/co_analysis/' +
             similarity + '/COAnalysis_' + cluster_algo + '_' + ontology + '_' + measure + '.tsv')
    reader = DictReader(f, delimiter='\t')
    cluster_similarity = dict()
    for row in reader:
        similarities = row['Pairwise_similarities'].split(';')
        cluster_similarity[row['Cluster']] = [float(s) for s in similarities]
    if verbose:
        for cluster, similarities in cluster_similarity.items():
            print(cluster + ' => ' + str(len(similarities)))
    return cluster_similarity


def print_cluster_similarity_metadata(similarity: str, cluster_algo: str, ontology: str,
                                      measure: str = 'jiang') -> None:
    clusters = get_drug_clusters(similarity, cluster_algo)
    f = open('output/co_analysis/' +
             similarity + '/COAnalysis_' + cluster_algo + '_' + ontology + '_' + measure + '.tsv')
    reader = DictReader(f, delimiter='\t')
    print('Cluster\tNo_of_drugs\tNo_of_similarity_values\t'
          'Min_similarity\tMax_similarity\tMean_similarity\tMedian_similarity')
    for row in reader:
        similarities = [float(s) for s in row['Pairwise_similarities'].split(';')]
        print(row['Cluster'] + '\t' + str(len(clusters[row['Cluster']])) + '\t' + str(len(similarities)) + '\t' +
              str(min(similarities)) + '\t' + str(max(similarities)) + '\t' +
              str(mean(similarities)) + '\t' + str(median(similarities)))
    return


# create_ontology_db('chebi_lite_entity.owl', 'chebi_lite_entity.db')
# create_ontology_db('chebi_lite_role.owl', 'chebi_lite_role.db')
# create_ontology_db('chebi.owl', 'chebi.db')

# set_ontology_db(ont)

# cs = compute_cluster_similarity(similarity='cosine', cluster_algo='bkm', measure='lin')
# cs = compute_cluster_similarity(similarity='cosine', cluster_algo='random_bkm', measure='lin')
# cs = compute_cluster_similarity(similarity='pearson', cluster_algo='bkm', measure='lin')
# cs = compute_cluster_similarity(similarity='pearson', cluster_algo='random_bkm', measure='lin')
# cs = compute_cluster_similarity(similarity='jaccard', cluster_algo='ms', measure='lin')
# cs = compute_cluster_similarity(similarity='jaccard', cluster_algo='random_ms', measure='lin')
# print_cluster_similarity(cs)
# print(min(cs['1']), max(cs['1']), mean(cs['1']), median(cs['1']))

# cs = read_cluster_similarity(similarity="cosine", cluster_algo='bkm', ontology=ont, measure='lin', verbose=False)
# cs = read_cluster_similarity(similarity="cosine", cluster_algo='random', ontology=ont, measure='lin', verbose=False)
# cs = read_cluster_similarity(similarity="pearson", cluster_algo='bkm', ontology=ont, measure='lin', verbose=False)
# cs = read_cluster_similarity(similarity="pearson", cluster_algo='random', ontology=ont, measure='lin', verbose=False)
# cs = read_cluster_similarity(similarity="jaccard", cluster_algo='ms', ontology=ont, measure='lin', verbose=False)
# cs = read_cluster_similarity(similarity="jaccard", cluster_algo='random', ontology=ont, measure='lin', verbose=False)
# print(len(cs))

# print_cluster_similarity_metadata(similarity="cosine", cluster_algo='bkm', ontology=ont, measure='lin')
# print_cluster_similarity_metadata(similarity="pearson", cluster_algo='bkm', ontology=ont, measure='lin')
# print_cluster_similarity_metadata(similarity="jaccard", cluster_algo='ms', ontology=ont, measure='lin')


# e_id1 = ssmpy.get_id('CHEBI_2376')
# e_id2 = ssmpy.get_id('CHEBI_68327')
# print(ssmpy.ssm_jiang_conrath(e_id1, e_id2))
# print(ssmpy.ssm_lin(e_id1, e_id2))
# print(ssmpy.common_ancestors(e_id1, e_id2))
# print()
# import numpy
# print(ssmpy.information_content(e_id1))
# print(ssmpy.information_content(e_id2))
# print(ssmpy.shared_ic(e_id1, e_id2))
# print(1/(ssmpy.information_content(e_id1) + ssmpy.information_content(e_id2) - (2 * ssmpy.shared_ic(e_id1, e_id2)) + 1))
# print(1 - numpy.min([1, ssmpy.information_content(e_id1) + ssmpy.information_content(e_id2) - (2 * ssmpy.shared_ic(e_id1, e_id2))]))

# query = "pragma table_info(transitive)"
# print(ssmpy.run_query(query, tuple()).fetchall())
