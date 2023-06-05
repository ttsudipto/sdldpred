library("fmcsR")

structure_file <- "input/PubChem/pulmonary_drugs_structure_pubchem.sdf"
id_file <- "input/PubChem/pulmonary_drugs_pubchem.tsv"

read_drug_identifiers <- function(file_name) {
  drug_identifiers <- read.csv(file_name, sep="\t")
  drug_identifiers <- drug_identifiers[drug_identifiers$PubChemCID != "NULL",]
  return(drug_identifiers)
}

get_mesh_name_map <- function(identifiers) {
  mesh_name_map <- data.frame(ChemicalName=identifiers$ChemicalName, row.names = identifiers$ChemicalID)
  return(mesh_name_map)
}

print_matrix <- function(m) {
  for(i in 1:nrow(m)){
    for (j in 1: ncol(m))
      cat(m[i,j], "\t")
    cat ("\n")
  }
}

read_structure_data <- function(file_name, identifiers) {
  sdfset <- read.SDFset("input/PubChem/pulmonary_drugs_structure_pubchem.sdf")
  valid <- validSDF(sdfset)
  sdfset <- sdfset[valid]
  for(i in 1:length(sdfset)) {
    cid(sdfset)[[i]] <- identifiers[identifiers$PubChemCID==header(sdfset)[[i]][[1]], "ChemicalID"][1]
    # substr(identifiers[identifiers$PubChemCID==header(sdfset)[[i]][[1]], "ChemicalName"][1], 0, 26),
  }
  return(sdfset)
}

compare_fmcs <- function(sdfset, mesh_name_map, coefficient_type) {
  ids <- cid(sdfset)
  n_drugs <- length(sdfset)
  cat("ChemicalID1\tChemicalName1\tChemicalID2\tChemicalName2\tFPSimilarity\n")
  for (i in 1:(n_drugs-1)) {
    for (j in (i+1):n_drugs) {
      sim <- fmcs(sdfset[[i]], sdfset[[j]])@stats[coefficient_type]
      cat(paste0(ids[[i]], "\t", mesh_name_map[ids[[i]],1], "\t", ids[[j]], "\t", mesh_name_map[ids[[j]],1], "\t", sim, "\n"))
    }
  }
}

compare_fmcs_matrix <- function(sdfset, mesh_name_map, coefficient_type) {
  ids <- cid(sdfset)
  n_drugs <- length(sdfset)
  m <- matrix(nrow = n_drugs+2, ncol = (n_drugs+2))
  cat("ChemicalID\t->")
  for (i in 1:n_drugs)
    cat(paste0("\t", ids[[i]]))
  cat("\n\\|/\tChemicalName")
  for (i in 1:n_drugs)
    cat(paste0("\t", mesh_name_map[ids[[i]], 1]))
  cat("\n")
  for (i in 1:n_drugs) {
    sim_batch <- fmcsBatch(sdfset[[i]], sdfset, timeout = 10000, numParallel = 20)
    cat(paste0(ids[[i]], "\t", mesh_name_map[ids[[i]], 1]))
    for (j in 1:n_drugs)
      cat(paste0("\t", sim_batch[ids[[j]], coefficient_type]))
    cat("\n")
  }
  return(m)
}


drug_identifiers <- read_drug_identifiers(id_file)
mesh_name_map <- get_mesh_name_map(drug_identifiers)
sdfset <- read_structure_data(structure_file, drug_identifiers)
n_drugs <- length(sdfset)
# print(n_drugs)
# print(cid(sdfset))

# compare_fmcs(sdfset, mesh_name_map, "Tanimoto_Coefficient")
# compare_fmcs(sdfset, mesh_name_map, "Overlap_Coefficient")

# m <- compare_fmcs_matrix(sdfset, mesh_name_map, "Tanimoto_Coefficient")
# m <- compare_fmcs_matrix(sdfset, mesh_name_map, "Overlap_Coefficient")
