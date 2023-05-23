from typing import Dict, Tuple, Set
from csv import DictReader, DictWriter
from copy import deepcopy


def read_drugs_ctd(key: str = 'cas', verbose: bool = False) -> Dict[str, str]:
    f = open('input/CTD/drugs_ctd.tsv', 'r')
    reader = DictReader(f, delimiter='\t')
    drugs = dict()
    for row in reader:
        if key == 'cas':  # CAS
            drug_id = row['CasRN']
        else:  # MESH
            drug_id = row['ChemicalID']
        drugs[drug_id] = row['ChemicalName']
    f.close()
    if verbose:
        for k, v in drugs.items():
            print(k + '\t' + v)
        print(len(drugs))
    return drugs


def read_diseases_ctd(verbose: bool = False) -> Dict[str, str]:
    f = open('input/CTD/diseases_ctd.tsv', 'r')
    reader = DictReader(f, delimiter='\t')
    diseases = dict()
    for row in reader:
        diseases[row['DiseaseID']] = row['DiseaseName']
    f.close()
    if verbose:
        for k, v in diseases.items():
            print(k + '\t' + v)
        print(len(diseases))
    return diseases


def read_genes_ctd(verbose: bool = False) -> Dict[str, str]:
    f = open('input/CTD/genes_ctd.tsv', 'r')
    reader = DictReader(f, delimiter='\t')
    genes = dict()
    for row in reader:
        genes[row['GeneID']] = row['GeneSymbol']
    f.close()
    if verbose:
        for k, v in genes.items():
            print(k + '\t' + v)
        print(len(genes))
    return genes


def read_cas_mesh_drug_map_ctd(verbose: bool = False) -> Dict[str, str]:
    f = open('input/CTD/drugs_ctd.tsv', 'r')
    reader = DictReader(f, delimiter='\t')
    cas_mesh_map = dict()
    for row in reader:
        cas_mesh_map[row['CasRN']] = row['ChemicalID']
    f.close()
    if verbose:
        for k, v in cas_mesh_map.items():
            print(k + '\t' + v)
        print(len(cas_mesh_map))
    return cas_mesh_map


def read_mesh_cas_drug_map_ctd(verbose: bool = False) -> Dict[str, str]:
    f = open('input/CTD/drugs_ctd.tsv', 'r')
    reader = DictReader(f, delimiter='\t')
    mesh_cas_map = dict()
    for row in reader:
        mesh_cas_map[row['ChemicalID']] = row['CasRN']
    f.close()
    if verbose:
        for k, v in mesh_cas_map.items():
            print(k + '\t' + v)
        print(len(mesh_cas_map))
    return mesh_cas_map


def get_pulmonary_drugs_ctd(pulmonary_drug_disease_map: Dict[str, Dict[str, float]] | Dict[str, Set[str]],
                            target: str = 'disease') -> None:
    all_drugs = read_drugs_ctd(key='cas')
    cas_mesh_map = read_cas_mesh_drug_map_ctd()
    last_header = '# ' + target + ' associations'
    print('CasRN' + '\t' + 'ChemicalID' + '\t' + 'ChemicalName' + '\t' + last_header)
    for drug, diseases in pulmonary_drug_disease_map.items():
        print(drug + '\t' + cas_mesh_map[drug] + '\t' + all_drugs[drug] + '\t' + str(len(diseases)))


def read_pulmonary_drugs_ctd(key: str = 'cas', target: str = 'disease', get_assoc_count: bool = False,
                             verbose: bool = False) -> Tuple[Dict[str, str], Dict[str, int]] | Dict[str, str]:
    if target == 'disease':
        f = open('input/CTD/pulmonary_drugs_ctd.tsv', 'r')
    elif target == 'gene':
        f = open('input/CTD/pulmonary_drugs_dga_ctd.tsv', 'r')
    else:
        raise ValueError('Error !!! Invalid \'target\' parameter, must be {disease, gene} ...')

    reader = DictReader(f, delimiter='\t')
    drugs = dict()
    assoc_counts = dict()
    assoc_header = '# ' + target + ' associations'
    for row in reader:
        if key == 'cas':
            drugs[row['CasRN']] = row['ChemicalName']
            assoc_counts[row['CasRN']] = int(row[assoc_header])
        else:
            drugs[row['ChemicalID']] = row['ChemicalName']
            assoc_counts[row['ChemicalID']] = int(row[assoc_header])
    f.close()
    if verbose:
        for k, v in drugs.items():
            print(k + '\t' + v)
        print(len(drugs))
        if get_assoc_count:
            for k, v in assoc_counts.items():
                print(k + '\t' + v)
    if get_assoc_count:
        return drugs, assoc_counts
    else:
        return drugs


def get_pulmonary_diseases_ctd(pulmonary_disease_drug_map: Dict[str, Dict[str, float]]) -> None:
    all_diseases = read_diseases_ctd()
    print('DiseaseID' + '\t' + 'DiseaseName' + '\t' + '# drug associations')
    for disease, drugs in pulmonary_disease_drug_map.items():
        print(disease + '\t' + all_diseases[disease] + '\t' + str(len(drugs)))


def read_pulmonary_diseases_ctd(get_assoc_count: bool = False,
                                verbose: bool = False) -> Tuple[Dict[str, str], Dict[str, int]] | Dict[str, str]:
    f = open('input/CTD/pulmonary_diseases_ctd.tsv', 'r')
    reader = DictReader(f, delimiter='\t')
    diseases = dict()
    assoc_counts = dict()
    for row in reader:
        diseases[row['DiseaseID']] = row['DiseaseName']
        assoc_counts[row['DiseaseID']] = int(row['# drug associations'])
    f.close()
    if verbose:
        for k, v in diseases.items():
            print(k + '\t' + v)
        print(len(diseases))
        if get_assoc_count:
            for k, v in assoc_counts.items():
                print(k + '\t' + v)
    if get_assoc_count:
        return diseases, assoc_counts
    else:
        return diseases


def get_pulmonary_genes_ctd(pulmonary_drug_gene_map: Dict[str, Set[str]]) -> None:
    all_genes = read_genes_ctd()
    print('GeneID' + '\t' + 'GeneSymbol' + '\t' + '# drug associations')
    pulmonary_genes = dict()
    for drug, genes in pulmonary_drug_gene_map.items():
        for gene in genes:
            if gene not in pulmonary_genes:
                pulmonary_genes[gene] = 1
            else:
                pulmonary_genes[gene] += 1
    for gene, assoc_count in sorted(pulmonary_genes.items(), key=lambda x: all_genes[x[0].lower()]):
        print(gene + '\t' + all_genes[gene] + '\t' + str(assoc_count))


def read_pulmonary_genes_ctd(get_assoc_count: bool = False,
                                verbose: bool = False) -> Tuple[Dict[str, str], Dict[str, int]] | Dict[str, str]:
    f = open('input/CTD/pulmonary_genes_ctd.tsv', 'r')
    reader = DictReader(f, delimiter='\t')
    genes = dict()
    assoc_counts = dict()
    for row in reader:
        genes[row['GeneID']] = row['GeneSymbol']
        assoc_counts[row['GeneID']] = int(row['# drug associations'])
    f.close()
    if verbose:
        for k, v in genes.items():
            print(k + '\t' + v)
        print(len(genes))
        if get_assoc_count:
            for k, v in assoc_counts.items():
                print(k + '\t' + v)
    if get_assoc_count:
        return genes, assoc_counts
    else:
        return genes


def read_pulmonary_disease_drug_association_ctd(verbose: bool = False) -> Dict[str, Dict[str, float]]:
    f = open('input/CTD/pulmonary_drug_disease_association_ctd.tsv', 'r')
    reader = DictReader(f, delimiter='\t')
    disease_drug_map = dict()
    for row in reader:
        if row['DiseaseID'] in disease_drug_map:
            disease_drug_map[row['DiseaseID']][row['CasRN']] = float(row['Score'])
        else:
            disease_drug_map[row['DiseaseID']] = {row['CasRN']: float(row['Score'])}

    if verbose:
        c = 1
        for disease, drugs in disease_drug_map.items():
            print(str(c) + '. ' + disease + ' :')
            for dis_id, attrs in sorted(drugs.items()):
                print('\t----' + dis_id + ' - ' + str(attrs))
            c = c + 1

    return disease_drug_map


def read_pulmonary_drug_disease_association_ctd(verbose: bool = False) -> Dict[str, Dict[str, float]]:
    f = open('input/CTD/pulmonary_drug_disease_association_ctd.tsv', 'r')
    reader = DictReader(f, delimiter='\t')
    drug_disease_map = dict()
    for row in reader:
        if row['CasRN'] in drug_disease_map:
            drug_disease_map[row['CasRN']][row['DiseaseID']] = float(row['Score'])
        else:
            drug_disease_map[row['CasRN']] = {row['DiseaseID']: float(row['Score'])}

    if verbose:
        c = 1
        for drug, diseases in drug_disease_map.items():
            print(str(c) + '. ' + drug + ' :')
            for dr_id, attrs in sorted(diseases.items()):
                print('\t----' + dr_id + ' - ' + str(attrs))
            c = c + 1

    return drug_disease_map


def read_pulmonary_drug_gene_association_ctd(verbose: bool = False) -> Dict[str, Set[str]]:
    f = open('input/CTD/pulmonary_drug_gene_association_ctd.tsv', 'r')
    reader = DictReader(f, delimiter='\t')
    drug_gene_map = dict()
    for row in reader:
        if row['CasRN'] not in drug_gene_map:
            drug_gene_map[row['CasRN']] = set()
        drug_gene_map[row['CasRN']].add(row['GeneID'])

    if verbose:
        c = 1
        for drug, genes in drug_gene_map.items():
            print(str(c) + '. ' + drug + ' :')
            for gene in sorted(genes):
                print('\t----' + gene)
            c = c + 1

    return drug_gene_map


def get_pulmonary_disease_drug_association_matrix_ctd(save: bool = False) -> None:
    pulmonary_diseases = read_pulmonary_diseases_ctd()
    headers = ['Disease', 'DiseaseName'] + list(sorted(read_pulmonary_drugs_ctd().keys()))
    pulmonary_disease_drug_map = read_pulmonary_disease_drug_association_ctd()
    f = writer = None
    if save:
        f = open('input/CTD/pulmonary_disease_drug_association_matrix_ctd.tsv', 'w')
        writer = DictWriter(f, delimiter='\t', fieldnames=headers, restval=0)
        writer.writeheader()
    else:
        print(headers)
    for disease, drugs in sorted(pulmonary_disease_drug_map.items(), key=lambda x: pulmonary_diseases[x[0]]):
        row = {'Disease': disease, 'DiseaseName': pulmonary_diseases[disease]}
        for drug in drugs.keys():
            row[drug] = 1
        if save:
            writer.writerow(row)
        else:
            print(row)
    if save:
        f.close()


def get_pulmonary_drug_disease_association_matrix_ctd(save: bool = False) -> None:
    pulmonary_drugs = read_pulmonary_drugs_ctd()
    headers = ['Drug', 'DrugName'] + list(sorted(read_pulmonary_diseases_ctd().keys()))
    pulmonary_drug_disease_map = read_pulmonary_drug_disease_association_ctd()
    f = writer = None
    if save:
        f = open('input/CTD/pulmonary_drug_disease_association_matrix_ctd.tsv', 'w')
        writer = DictWriter(f, delimiter='\t', fieldnames=headers, restval=0)
        writer.writeheader()
    else:
        print(headers)
    for drug, diseases in sorted(pulmonary_drug_disease_map.items(), key=lambda x: pulmonary_drugs[x[0]]):
        row = {'Drug': drug, 'DrugName': pulmonary_drugs[drug]}
        for disease in diseases.keys():
            row[disease] = 1
        if save:
            writer.writerow(row)
        else:
            print(row)
    if save:
        f.close()


def get_pulmonary_drug_gene_association_matrix_ctd(save: bool = False) -> None:
    pulmonary_drugs = read_pulmonary_drugs_ctd()
    pulmonary_genes = read_pulmonary_genes_ctd()
    headers = ['Drug', 'DrugName'] + list(sorted(read_pulmonary_genes_ctd().values()))
    pulmonary_drug_gene_map = read_pulmonary_drug_gene_association_ctd()
    f = writer = None
    if save:
        f = open('input/CTD/pulmonary_drug_gene_association_matrix_ctd.tsv', 'w')
        # f = open('foo.tsv', 'w')
        writer = DictWriter(f, delimiter='\t', fieldnames=headers, restval=0)
        writer.writeheader()
    else:
        print(headers)
    for drug, genes in pulmonary_drug_gene_map.items():
        row = {'Drug': drug, 'DrugName': pulmonary_drugs[drug]}
        for gene in genes:
            row[pulmonary_genes[gene]] = 1
        if save:
            writer.writerow(row)
        else:
            print(row)
    if save:
        f.close()


def filter_diseases_disease_drug_association(disease_drug_map: Dict[str, Dict[str, float]], disease_ids: Dict[str, str],
                                             verbose: bool = False) -> Dict[str, Dict[str, float]]:
    filtered_map = dict()
    for disease, drugs in disease_drug_map.items():
        if disease in disease_ids:
            filtered_map[disease] = deepcopy(drugs)
    if verbose:
        pulmonary_drugs = read_pulmonary_drugs_ctd()
        pulmonary_diseases = read_pulmonary_diseases_ctd()
        c = 1
        print('DiseaseID' + '\t' + 'DiseaseName' + '\t' + 'CasRN' + '\t' + 'ChemicalName' + '\t' + 'Score')
        for disease, drugs in sorted(filtered_map.items(), key=lambda x: pulmonary_diseases[x[0]].lower()):
            # print(str(c) + '. ' + disease + ' : ' + str(len(drugs)))
            for drug, score in sorted(drugs.items(), key=lambda x: pulmonary_drugs[x[0]].lower()):
                print(disease + '\t' + pulmonary_diseases[disease] + '\t' + drug + '\t' + pulmonary_drugs[drug] +
                      '\t' + str(score))
            c = c + 1
    return filtered_map


def filter_diseases_drug_disease_association(drug_disease_map: Dict[str, Dict[str, float]], disease_ids: Dict[str, str],
                                             verbose: bool = False) -> Dict[str, Dict[str, float]]:
    filtered_map = dict()
    for drug, diseases in drug_disease_map.items():
        filter_association = dict()
        for disease, score in diseases.items():
            if disease in disease_ids:
                filter_association[disease] = score
        if len(filter_association) > 0:
            filtered_map[drug] = filter_association
    if verbose:
        pulmonary_drugs = read_pulmonary_drugs_ctd()
        pulmonary_diseases = read_pulmonary_diseases_ctd()
        c = 1
        print('CasRN' + '\t' + 'ChemicalName' + '\t' + 'DiseaseID' + '\t' + 'DiseaseName' + '\t' + 'Score')
        for drug, diseases in sorted(filtered_map.items(), key=lambda x: pulmonary_drugs[x[0]].lower()):
            # print(str(c) + '. ' + drug + ' : ' + str(len(diseases)))
            for disease, score in sorted(diseases.items(), key=lambda x: pulmonary_diseases[x[0]].lower()):
                print(drug + '\t' + pulmonary_drugs[drug] + '\t' + disease + '\t' + pulmonary_diseases[disease] +
                      '\t' + str(score))
            c = c + 1
    return filtered_map


def filter_drugs_drug_gene_association(drug_gene_map: Dict[str, Set[str]], drug_ids: Dict[str, str],
                                             verbose: bool = False) -> Dict[str, Set[str]]:
    filtered_map = dict()
    mesh_cas_map = read_mesh_cas_drug_map_ctd()
    for drug, genes in drug_gene_map.items():
        if drug in mesh_cas_map and mesh_cas_map[drug] in drug_ids:
            filtered_map[mesh_cas_map[drug]] = deepcopy(genes)
    if verbose:
        pulmonary_drugs = read_pulmonary_drugs_ctd()
        pulmonary_genes = read_pulmonary_genes_ctd()
        cas_mesh_map = read_cas_mesh_drug_map_ctd()
        c = 1
        print('CasRN' + '\t' + 'ChemicalID' + '\t' + 'ChemicalName' + '\t' + 'GeneID' + '\t' + 'GeneSymbol')
        for drug, genes in sorted(filtered_map.items(), key=lambda x: pulmonary_drugs[x[0]].lower()):
            # print(str(c) + '. ' + drug + ' : ' + str(len(genes)))
            for gene in sorted(genes, key=lambda x: pulmonary_genes[x].lower()):
                print(drug + '\t' + cas_mesh_map[drug] + '\t' + pulmonary_drugs[drug] + '\t' + gene +
                      '\t' + pulmonary_genes[gene])
            c = c + 1
    return filtered_map
