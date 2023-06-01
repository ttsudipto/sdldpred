library(GOSemSim)
# loadNamespace("Rcpp")

get_gene_id_map <- function() {
  f = "input/CTD/pulmonary_genes_ctd.tsv"
  gene_map <- read.csv(f, sep = "\t")
  rownames(gene_map) <- gene_map$GeneSymbol
  return(gene_map)
}

read_drug_gene_association <- function(f_name) {
  similarity <- read.csv(f_name, header=FALSE, sep="\t")
  c_names <- substr(similarity[1,], 0, 26)[3:dim(similarity)[2]]
  r_names <- substr(similarity[,2], 0, 26)[-1]
  similarity <- as.data.frame(lapply(similarity[-1, 3:dim(similarity)[2]],
                                     function(x) as.numeric(as.character(x))))
  rownames(similarity) <- r_names
  colnames(similarity) <- c_names
  return(similarity)
}

get_random_drug_cluster <- function(n, drugs) {
  set.seed(16) # measure = "Jiang"
  # set.seed(32) # measure = "Lin"
  f_name <- paste0("output/gs/optimal_clusters_bkm.tsv")
  clusters <- strsplit(read.csv(f_name, sep = "\t")$Drugs, ";")
  len <- 0
  for (i in 1:length(clusters))
    if(length(clusters[[i]]) > 1)
      len <- len + 1
  random_clusters <- list()
  for (i in 1:n) {
    random_indices <- sort(sample.int(length(drugs), round(1271/len)))
    random_clusters[[length(random_clusters) + 1]] <- drugs[random_indices]
  }
  # print(random_clusters)
  return(random_clusters)
}

get_drug_cluster <- function(cluster_algo) {
  f_name <- paste0("output/gs/optimal_clusters_", cluster_algo, ".tsv")
  clusters <- strsplit(read.csv(f_name, sep = "\t")$Drugs, ";")
  return(clusters)
}

get_gene_set <- function(drug, association) {
  g <- array()[-1]
  if (substr(drug,0,26) %in% rownames(association))
    g <- colnames(association)[which(association[substr(drug,0,26),]==1,)]
    # g <- colnames(association[substr(drug,0,26), association[substr(drug,0,26),]==1])
  return(g)
}

get_union_gene_set <- function(drugs, association) {
  n_drugs <- length(drugs)
  genes = array()[-1]
  for (j in 1:n_drugs) {
    g <- get_gene_set(drugs[j], association)
    if(length(g) < 1000)
      genes <- c(genes, g)
  }
  genes <- unique(genes)
  return(genes)
}

compute_semantic_similarity <- function(genes, ontology, measure="Jiang") {
  if (length(genes) > 1) {
    hsGO <- godata('org.Hs.eg.db', ont = ontology)
    sim <- GOSemSim::mgeneSim(genes, semData = hsGO, measure = measure,
                              drop = c("IEA", "ISS", "NAS", "ND", "IC"),
                              combine = "BMA", verbose = FALSE)
    sim <- sim[lower.tri(sim)]
  } else if (length(genes) == 1) {
    sim <- c(1)
  } else
    sim <- c(0)
  return(sim)
}

compute_cluster_similarity_gene_union <- function(association, cluster_algo, ontology, measure = "Jiang") {
  if(cluster_algo == "random")
    clusters <- get_random_drug_cluster(1, rownames(association))
  else
    clusters <- get_drug_cluster(cluster_algo)
  cluster_similarity <- list()
  for (i in 1:length(clusters)) {
  # for (i in 25:27) {
    if (length(clusters[[i]]) > 1) {
      genes <- get_union_gene_set(clusters[[i]], association)
      genes <- as.character(get_gene_id_map()[genes, "GeneID"])
      cat("Cluster ", i, "/", length(clusters), " => ", length(genes), " genes\n")
      sim <- compute_semantic_similarity(genes, ontology, measure)
      # sim <- c(0)
      cluster_similarity[[i]] <- as.vector(sim)
      # cat(min(cluster_similarity[[1]]), max(cluster_similarity[[1]]), mean(cluster_similarity[[1]]), median(cluster_similarity[[1]]), "\n")
    }
  }
  return(cluster_similarity)
}

read_cluster_similarity <- function(cluster_algo, ontology, measure = "Jiang") {
  folder <- "output/go_analysis/gene_union/"
  f_name <- paste0(folder, "GOSemSim_", cluster_algo, "_", tolower(ontology), "_", tolower(measure), ".rds")
  cluster_similarity <- readRDS(f_name)
  return(cluster_similarity)
}

print_cluster_similarity <- function(cluster_similarity) {
  cat("Cluster\tPairwise_similarities\n")
  for (i in 1:length(cluster_similarity)) {
    cat(paste0(i, "\t", paste(cluster_similarity[[i]], collapse=";"), "\n"))
  }
}

print_cluster_similarity_metadata <- function(association, cluster_algo, ontology, measure = "Jiang") {
  cluster_similarity <- read_cluster_similarity(cluster_algo, ontology, measure)
  clusters <- get_drug_cluster(cluster_algo)
  cat("Cluster\tNo_of_drugs\tNo_of_genes\tNo_of_similarity_values\tMin_similarity\tMax_similarity\tMean_similarity\tMedian_similarity\n")
  for (i in 1:length(cluster_similarity)) {
    cat(paste0(i, "\t", length(clusters[[i]]), "\t", length(get_union_gene_set(clusters[[i]], association)), "\t", length(cluster_similarity[[i]]), "\t", min(cluster_similarity[[i]]), "\t", max(cluster_similarity[[i]]), "\t", mean(cluster_similarity[[i]]), "\t", median(cluster_similarity[[i]]), "\n"))
  }
}

read_cluster_similarity_metadata <- function(cluster_algo, ontology, measure = "Jiang") {
  folder <- "output/go_analysis/gene_union/"
  f_name <- paste0(folder, "GOSemSim_metadata_", cluster_algo, "_", tolower(ontology), "_", tolower(measure), ".tsv")
  cluster_similarity_metadata <- read.csv(f_name, sep = "\t")
  return(cluster_similarity_metadata)
}


# association <- read_drug_gene_association("input/CTD/pulmonary_drug_gene_association_matrix_ctd.tsv")
# all_genes <- as.character(get_gene_id_map()$GeneID)


# cluster_similarity <- compute_cluster_similarity_gene_union(association, cluster_algo = "kmc", ontology = "MF")
# cluster_similarity <- compute_cluster_similarity_gene_union(association, cluster_algo = "kmc", ontology = "BP")
# cluster_similarity <- compute_cluster_similarity_gene_union(association, cluster_algo = "kmc", ontology = "CC")
# cluster_similarity <- compute_cluster_similarity_gene_union(association, cluster_algo = "bkm", ontology = "MF")
# cluster_similarity <- compute_cluster_similarity_gene_union(association, cluster_algo = "bkm", ontology = "BP")
# cluster_similarity <- compute_cluster_similarity_gene_union(association, cluster_algo = "bkm", ontology = "CC")
# cluster_similarity <- compute_cluster_similarity_gene_union(association, cluster_algo = "ms", ontology = "MF")
# cluster_similarity <- compute_cluster_similarity_gene_union(association, cluster_algo = "ms", ontology = "BP")
# cluster_similarity <- compute_cluster_similarity_gene_union(association, cluster_algo = "ms", ontology = "CC")
# cluster_similarity <- compute_cluster_similarity_gene_union(association, cluster_algo = "birch", ontology = "MF")
# cluster_similarity <- compute_cluster_similarity_gene_union(association, cluster_algo = "birch", ontology = "BP")
# cluster_similarity <- compute_cluster_similarity_gene_union(association, cluster_algo = "birch", ontology = "CC")
# cluster_similarity <- compute_cluster_similarity_gene_union(association, cluster_algo = "random", ontology = "MF")
# cluster_similarity <- compute_cluster_similarity_gene_union(association, cluster_algo = "random", ontology = "BP")
# cluster_similarity <- compute_cluster_similarity_gene_union(association, cluster_algo = "random", ontology = "CC")
# print_cluster_similarity(cluster_similarity)
# saveRDS(cluster_similarity, "foo.rds")

# cluster_similarity <- read_cluster_similarity(cluster_algo = "kmc", ontology = "MF")
# cluster_similarity <- read_cluster_similarity(cluster_algo = "kmc", ontology = "BP")
# cluster_similarity <- read_cluster_similarity(cluster_algo = "kmc", ontology = "CC")
# cluster_similarity <- read_cluster_similarity(cluster_algo = "bkm", ontology = "MF")
# cluster_similarity <- read_cluster_similarity(cluster_algo = "bkm", ontology = "BP")
# cluster_similarity <- read_cluster_similarity(cluster_algo = "bkm", ontology = "CC")
# cluster_similarity <- read_cluster_similarity(cluster_algo = "ms", ontology = "MF")
# cluster_similarity <- read_cluster_similarity(cluster_algo = "ms", ontology = "BP")
# cluster_similarity <- read_cluster_similarity(cluster_algo = "ms", ontology = "CC")
# cluster_similarity <- read_cluster_similarity(cluster_algo = "birch", ontology = "MF")
# cluster_similarity <- read_cluster_similarity(cluster_algo = "birch", ontology = "BP")
# cluster_similarity <- read_cluster_similarity(cluster_algo = "birch", ontology = "CC")
# cluster_similarity <- read_cluster_similarity(cluster_algo = "random", ontology = "MF")
# cluster_similarity <- read_cluster_similarity(cluster_algo = "random", ontology = "BP")
# cluster_similarity <- read_cluster_similarity(cluster_algo = "random", ontology = "CC")
# print(cluster_similarity)

# print_cluster_similarity_metadata(association, cluster_algo = "kmc", ontology = "MF")
# print_cluster_similarity_metadata(association, cluster_algo = "kmc", ontology = "BP")
# print_cluster_similarity_metadata(association, cluster_algo = "kmc", ontology = "CC")
# print_cluster_similarity_metadata(association, cluster_algo = "bkm", ontology = "MF")
# print_cluster_similarity_metadata(association, cluster_algo = "bkm", ontology = "BP")
# print_cluster_similarity_metadata(association, cluster_algo = "bkm", ontology = "CC")
# print_cluster_similarity_metadata(association, cluster_algo = "ms", ontology = "MF")
# print_cluster_similarity_metadata(association, cluster_algo = "ms", ontology = "BP")
# print_cluster_similarity_metadata(association, cluster_algo = "ms", ontology = "CC")
# print_cluster_similarity_metadata(association, cluster_algo = "birch", ontology = "MF")
# print_cluster_similarity_metadata(association, cluster_algo = "birch", ontology = "BP")
# print_cluster_similarity_metadata(association, cluster_algo = "birch", ontology = "CC")


# cluster_similarity_metadata <- read_cluster_similarity_metadata(cluster_algo = "kmc", ontology = "MF")
# cluster_similarity_metadata <- read_cluster_similarity_metadata(cluster_algo = "kmc", ontology = "BP")
# cluster_similarity_metadata <- read_cluster_similarity_metadata(cluster_algo = "kmc", ontology = "CC")
# cluster_similarity_metadata <- read_cluster_similarity_metadata(cluster_algo = "bkm", ontology = "MF")
# cluster_similarity_metadata <- read_cluster_similarity_metadata(cluster_algo = "bkm", ontology = "BP")
# cluster_similarity_metadata <- read_cluster_similarity_metadata(cluster_algo = "bkm", ontology = "CC")
# cluster_similarity_metadata <- read_cluster_similarity_metadata(cluster_algo = "ms", ontology = "MF")
# cluster_similarity_metadata <- read_cluster_similarity_metadata(cluster_algo = "ms", ontology = "BP")
# cluster_similarity_metadata <- read_cluster_similarity_metadata(cluster_algo = "ms", ontology = "CC")
# cluster_similarity_metadata <- read_cluster_similarity_metadata(cluster_algo = "birch", ontology = "MF")
# cluster_similarity_metadata <- read_cluster_similarity_metadata(cluster_algo = "birch", ontology = "BP")
# cluster_similarity_metadata <- read_cluster_similarity_metadata(cluster_algo = "birch", ontology = "CC")
# print(cluster_similarity_metadata)
