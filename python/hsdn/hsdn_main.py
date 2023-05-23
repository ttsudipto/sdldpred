from .hsdn_parser import parseDiseaseSymptomMap
from .hsdn_parser import parseSymptomDiseaseMap
from .hsdn_parser import parseIdentifierMap
from ..icd_util import get_all_pulmonary_diseases_mesh
from ..icd_util import get_TTD_pulmonary_diseases_mesh
from .hsdn_util import read_symptoms_hsdn, read_diseases_hsdn
from .hsdn_util import get_pulmonary_symptoms_hsdn, read_pulmonary_symptoms_hsdn
from .hsdn_util import get_pulmonary_diseases_hsdn, read_pulmonary_diseases_hsdn
from .hsdn_util import filter_diseases_from_disease_symptom_map
from .hsdn_util import filter_diseases_from_symptom_disease_map
from .hsdn_util import read_pulmonary_disease_symptom_association_hsdn
from .hsdn_util import read_pulmonary_symptom_disease_association_hsdn
from .hsdn_util import get_pulmonary_symptom_disease_matrix_hsdn
from .hsdn_util import get_pulmonary_disease_symptom_matrix_hsdn

pathPrefix = 'input/HSDN/'


def print_map_counts(input_map, map_first=True):
    ss = set()
    for d, sm in input_map.items():
        for s in sm.keys():
            ss.add(s)
    if map_first:
        print(len(input_map), len(ss))
    else:
        print(len(ss), len(input_map))


filterDiseases1 = get_all_pulmonary_diseases_mesh()

# symptomMap = parseIdentifierMap('Symptom', verbose=False)
# print(len(symptomMap))
# symptomMap = read_symptoms_hsdn(verbose=False)
# print(len(symptomMap))

# diseaseMap = parseIdentifierMap('Disease', verbose=False)
# print(len(diseaseMap))
# diseaseMap = read_diseases_hsdn(verbose=False)
# print(len(diseaseMap))

# diseaseSymptomMap = parseDiseaseSymptomMap(verbose=False)
# print_map_counts(diseaseSymptomMap, map_first=True)
# filteredDiseaseSymptomMap1 = filter_diseases_from_disease_symptom_map(diseaseSymptomMap, filterDiseases1, verbose=False)
# print_map_counts(filteredDiseaseSymptomMap1, map_first=True)

# symptomDiseaseMap = parseSymptomDiseaseMap(verbose=False)
# print_map_counts(symptomDiseaseMap, map_first=False)
# filteredSymptomDiseaseMap1 = filter_diseases_from_symptom_disease_map(symptomDiseaseMap, filterDiseases1, verbose=False)
# print_map_counts(filteredSymptomDiseaseMap1, map_first=False)


# get_pulmonary_diseases_hsdn(filteredDiseaseSymptomMap1)
# pulmonary_diseases, symptom_assoc_count = read_pulmonary_diseases_hsdn(get_assoc_count=True)
# print(len(pulmonary_diseases), len(symptom_assoc_count), sum(symptom_assoc_count.values()))

# get_pulmonary_symptoms_hsdn(filteredSymptomDiseaseMap1)
# pulmonary_symptoms, disease_assoc_count = read_pulmonary_symptoms_hsdn(get_assoc_count=True)
# print(len(pulmonary_symptoms), len(disease_assoc_count), sum(disease_assoc_count.values()))

# pulmonary_disease_symptom_association = read_pulmonary_disease_symptom_association_hsdn()
# print_map_counts(pulmonary_disease_symptom_association, map_first=True)
# pulmonary_symptom_disease_association = read_pulmonary_symptom_disease_association_hsdn()
# print_map_counts(pulmonary_symptom_disease_association, map_first=False)

# get_pulmonary_symptom_disease_matrix_hsdn(save=True)
# get_pulmonary_disease_symptom_matrix_hsdn(save=True)


# c = 0
# for d, s in filteredDiseaseSymptomMap1.items():
#     c += len(s)
# print(c)
# c=0
# for d, s in filteredDiseaseSymptomMap2.items():
#     c += len(s)
# print(c)
