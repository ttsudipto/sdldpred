from typing import List, Dict, Set
from csv import DictReader

pathPrefix = 'input/CTD/'


def convert_to_float(text: str):
    if len(text) > 0:
        return float(text)
    else:
        return 0.0


# ChemicalName	ChemicalID	CasRN	DiseaseName	DiseaseID	DirectEvidence	InferenceGeneSymbol	InferenceScore	OmimIDs	PubMedIDs
# ChemicalName	ChemicalID	CasRN	GeneSymbol	GeneID	GeneForms	Organism	OrganismID	Interaction	InteractionActions	PubMedIDs


def parse_drugs_ctd(verbose: bool = False) -> Dict[str, str]:
    f = open(pathPrefix + 'CTD_chemicals_diseases.tsv', 'r')
    reader = DictReader(f, delimiter='\t')
    if verbose:
        print('ChemicalName' + '\t' + 'ChemicalID' + '\t' + 'CasRN')
    unique_drugs = dict()
    for row in reader:
        if (row['CasRN'] != '') and (row['CasRN'] not in unique_drugs):
            if verbose:
                print(row['ChemicalName'] + '\t' + row['ChemicalID'] + '\t' + row['CasRN'])
            unique_drugs[row['CasRN']] = row['ChemicalName']
    f.close()
    return unique_drugs


def parse_diseases_ctd(verbose: bool = False) -> Dict[str, str]:
    f = open(pathPrefix + 'CTD_chemicals_diseases.tsv', 'r')
    reader = DictReader(f, delimiter='\t')
    if verbose:
        print('DiseaseName' + '\t' + 'DiseaseID')
    unique_diseases = dict()
    for row in reader:
        disease_elements = row['DiseaseID'].split(':')
        disease_id_label = disease_elements[0]
        disease_id = disease_elements[1]
        if disease_id not in unique_diseases and disease_id_label == 'MESH':
            if verbose:
                print(row['DiseaseName'] + '\t' + disease_id)
            unique_diseases[disease_id] = row['DiseaseName']
    f.close()
    return unique_diseases


def parse_genes_ctd(verbose: bool = False) -> Dict[str, str]:
    f = open(pathPrefix + 'CTD_chem_gene_ixns.tsv', 'r')
    reader = DictReader(f, delimiter='\t')
    if verbose:
        print('GeneSymbol' + '\t' + 'GeneID')
    unique_genes = dict()
    for row in reader:
        if row['GeneID'] not in unique_genes and row['GeneForms'] == 'protein' and row['Organism'] == 'Homo sapiens':
            unique_genes[row['GeneID']] = row['GeneSymbol']
    f.close()
    if verbose:
        for gid, symbol in sorted(unique_genes.items(), key=lambda x: x[1]):
            print(symbol + '\t' + gid)
    return unique_genes


def parse_pulmonary_drugs_ctd(pulmonary_diseases: List[str]) -> None:
    f = open(pathPrefix + 'CTD_chemicals_diseases.tsv', 'r')
    reader = DictReader(f, delimiter='\t')
    print('ChemicalName' + '\t' + 'ChemicalID' + '\t' + 'CasRN')
    unique_drugs = set()
    for row in reader:
        if (row['CasRN'] != '') and (row['CasRN'] not in unique_drugs):
            disease_elements = row['DiseaseID'].split(':')
            disease_id_label = disease_elements[0]
            disease_id = disease_elements[1]
            if disease_id in pulmonary_diseases:
                print(row['ChemicalName'] + '\t' + row['ChemicalID'] + '\t' + row['CasRN'])
                unique_drugs.add(row['CasRN'])
    f.close()


def parse_pulmonary_genes_ctd(pulmonary_drugs: List[str]) -> None:
    f = open(pathPrefix + 'CTD_chem_gene_ixns.tsv', 'r')
    reader = DictReader(f, delimiter='\t')
    print('GeneSymbol' + '\t' + 'GeneID')
    unique_genes = set()
    for row in reader:
        drug_id = row['ChemicalID']
        gene_id = row['GeneID']
        if (drug_id in pulmonary_drugs and
                gene_id not in unique_genes and row['GeneForms'] == 'protein' and row['Organism'] == 'Homo sapiens'):
            print(row['GeneSymbol'] + '\t' + row['GeneID'])
            unique_genes.add(gene_id)
    f.close()


def parse_drug_disease_association_ctd() -> Dict[str, Dict[str, float]]:
    f = open(pathPrefix + 'CTD_chemicals_diseases.tsv', 'r')
    reader = DictReader(f, delimiter='\t')
    drug_disease_map = dict()
    for row in reader:
        if row['CasRN'] != '' and row['DirectEvidence'] == 'therapeutic':
            disease_elements = row['DiseaseID'].split(':')
            disease_id_label = disease_elements[0]
            disease_id = disease_elements[1]
            # print(disease_id_label, disease_id)
            if disease_id_label == 'MESH':
                if row['CasRN'] in drug_disease_map:
                    drug_disease_map[row['CasRN']][disease_id] = convert_to_float(row['InferenceScore'])
                else:
                    associations = set()
                    associations.add(disease_id)
                    drug_disease_map[row['CasRN']] = {disease_id: convert_to_float(row['InferenceScore'])}
    f.close()
    return drug_disease_map


def parse_disease_drug_association_ctd() -> Dict[str, Dict[str, float]]:
    f = open(pathPrefix + 'CTD_chemicals_diseases.tsv', 'r')
    reader = DictReader(f, delimiter='\t')
    disease_drug_map = dict()
    for row in reader:
        if row['CasRN'] != '' and row['DirectEvidence'] == 'therapeutic':
            disease_elements = row['DiseaseID'].split(':')
            disease_id_label = disease_elements[0]
            disease_id = disease_elements[1]
            # print(disease_id_label, disease_id)
            if disease_id_label == 'MESH':
                if disease_id in disease_drug_map:
                    disease_drug_map[disease_id][row['CasRN']] = convert_to_float(row['InferenceScore'])
                else:
                    disease_drug_map[disease_id] = {row['CasRN']: convert_to_float(row['InferenceScore'])}
    f.close()
    return disease_drug_map


def parse_drug_gene_association_ctd() -> Dict[str, Set[str]]:
    f = open(pathPrefix + 'CTD_chem_gene_ixns.tsv', 'r')
    reader = DictReader(f, delimiter='\t')
    drug_gene_map = dict()
    for row in reader:
        if row['GeneForms'] == 'protein' and row['Organism'] == 'Homo sapiens':
            drug_id = row['ChemicalID']
            gene_id = row['GeneID']
            # print(disease_id_label, disease_id)
            if drug_id not in drug_gene_map:
                drug_gene_map[drug_id] = set()
            drug_gene_map[drug_id].add(gene_id)
    f.close()
    return drug_gene_map
