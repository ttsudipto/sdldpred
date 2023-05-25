from ..icd_util import get_all_pulmonary_diseases_mesh
from .ctd_util import filter_diseases_drug_disease_association
from .ctd_util import  filter_diseases_disease_drug_association
from .ctd_util import filter_drugs_drug_gene_association
from .ctd_util import read_drugs_ctd, read_diseases_ctd
from .ctd_util import get_pulmonary_drugs_ctd, read_pulmonary_drugs_ctd
from .ctd_util import get_pulmonary_diseases_ctd, read_pulmonary_diseases_ctd
from .ctd_util import get_pulmonary_genes_ctd, read_pulmonary_genes_ctd
from .ctd_util import read_pulmonary_drug_disease_association_ctd, read_pulmonary_disease_drug_association_ctd
from .ctd_util import read_pulmonary_drug_gene_association_ctd
from .ctd_util import get_pulmonary_disease_drug_association_matrix_ctd
from .ctd_util import get_pulmonary_drug_disease_association_matrix_ctd
from .ctd_util import get_pulmonary_drug_gene_association_matrix_ctd
from .ctd_parser import parse_drugs_ctd, parse_diseases_ctd, parse_genes_ctd
from .ctd_parser import parse_drug_disease_association_ctd
from .ctd_parser import parse_disease_drug_association_ctd
from .ctd_parser import parse_drug_gene_association_ctd
# from .ctd_parser import parse_pulmonary_drugs_ctd, parse_pulmonary_diseases_ctd


def print_map_counts(input_map, map_first=True):
    ss = set()
    for d, sm in input_map.items():
        for s in sm:
            ss.add(s)
    if map_first:
        print(len(input_map), len(ss))
    else:
        print(len(ss), len(input_map))
    return


# pulmonary_diseases = get_all_pulmonary_diseases_mesh()
# print(len(pulmonary_diseases))

#####################################################################
# Drug-disease association
#####################################################################

# drugs = parse_drugs_ctd(verbose=False)
# diseases = parse_diseases_ctd(verbose=False)
# print(len(diseases), len(drugs))
# drugs = read_drugs_ctd(verbose=False)
# diseases = read_diseases_ctd(verbose=False)
# print(len(diseases), len(drugs))


# drugDiseaseMap = parse_drug_disease_association_ctd()
# print_map_counts(drugDiseaseMap, map_first=False)
# pulmonaryDrugDiseaseMap = filter_diseases_drug_disease_association(drugDiseaseMap, pulmonary_diseases, verbose=False)
# print_map_counts(pulmonaryDrugDiseaseMap, map_first=False)

# diseaseDrugMap = parse_disease_drug_association_ctd()
# print_map_counts(diseaseDrugMap)
# pulmonaryDiseaseDrugMap = filter_diseases_disease_drug_association(diseaseDrugMap, pulmonary_diseases, verbose=False)
# print_map_counts(pulmonaryDiseaseDrugMap)


# get_pulmonary_drugs_ctd(pulmonaryDrugDiseaseMap)
# get_pulmonary_diseases_ctd(pulmonaryDiseaseDrugMap)
# pulmonary_drugs, disease_assoc_count = read_pulmonary_drugs_ctd(get_assoc_count=True)
# pulmonary_diseases, drug_assoc_count = read_pulmonary_diseases_ctd(get_assoc_count=True)
# print(len(pulmonary_drugs), len(disease_assoc_count), sum(disease_assoc_count.values()))
# print(len(pulmonary_diseases), len(drug_assoc_count), sum(drug_assoc_count.values()))

# drug_disease_association = read_pulmonary_drug_disease_association_ctd()
# print_map_counts(drug_disease_association, map_first=False)
# disease_drug_association = read_pulmonary_disease_drug_association_ctd()
# print_map_counts(disease_drug_association, map_first=True)

# get_pulmonary_disease_drug_association_matrix_ctd(save=False)
# get_pulmonary_drug_disease_association_matrix_ctd(save=False)

#####################################################################
# Drug-protein association
#####################################################################

# pulmonary_drugs = read_pulmonary_drugs_ctd()
# print(len(pulmonary_drugs))
# genes = parse_genes_ctd(verbose=True)
# print(len(genes))

# drugGeneMap = parse_drug_gene_association_ctd()
# print_map_counts(drugGeneMap, map_first=True)
# pulmonaryDrugGeneMap = filter_drugs_drug_gene_association(drugGeneMap, pulmonary_drugs, verbose=True)
# print_map_counts(pulmonaryDrugGeneMap, map_first=True)


# get_pulmonary_drugs_ctd(pulmonaryDrugGeneMap, target='gene')
# get_pulmonary_genes_ctd(pulmonaryDrugGeneMap)
# pulmonary_drugs, gene_assoc_count = read_pulmonary_drugs_ctd(target='gene', get_assoc_count=True)
# pulmonary_genes, drug_assoc_count = read_pulmonary_genes_ctd(get_assoc_count=True)
# print(len(pulmonary_drugs), len(gene_assoc_count), sum(gene_assoc_count.values()))
# print(len(pulmonary_genes), len(drug_assoc_count), sum(drug_assoc_count.values()))
#
# drug_gene_association = read_pulmonary_drug_gene_association_ctd()
# print_map_counts(drug_gene_association, map_first=True)

# get_pulmonary_drug_gene_association_matrix_ctd(save=False)
# get_pulmonary_drug_gene_association_matrix_ctd(save=True)

#####################################################################


# c = 0
# for d, s in drug_disease_association.items():
#     c += len(s)
# print(c)
# c=0
# for d, s in disease_drug_association.items():
#     c += len(s)
# print(c)


# freq1 = []
# for k,v in pulmonaryDrugDiseaseMap.items():
#     freq1.append(len(v))
# print(min(freq1), max(freq1), sum(freq1)/len(pulmonaryDrugDiseaseMap))
# freq2 = []
# for k,v in pulmonaryDiseaseDrugMap.items():
#     freq2.append(len(v))
# print(min(freq2), max(freq2), sum(freq2)/len(pulmonaryDiseaseDrugMap))

# print(list(reversed(sorted(pulmonaryDrugDiseaseMap, key=lambda x: len(pulmonaryDrugDiseaseMap[x]))))[:5])
# print(list(reversed(sorted(pulmonaryDiseaseDrugMap, key=lambda x: len(pulmonaryDiseaseDrugMap[x]))))[:5])
# print(len(pulmonaryDiseaseDrugMap['D008175']), len(pulmonaryDiseaseDrugMap['D009362']), len(pulmonaryDiseaseDrugMap['D001249']), len(pulmonaryDiseaseDrugMap['D029424']), len(pulmonaryDiseaseDrugMap['D006976']))
