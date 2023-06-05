read_drug_drug_mcs_similarity <- function(f_name) {
  similarity <- read.csv(f_name, header=FALSE, sep="\t")
  c_names <- substr(similarity[2,], 0, 26)[3:dim(similarity)[2]]
  r_names <- substr(similarity[,2], 0, 26)[3:dim(similarity)[1]]
  similarity <- as.data.frame(lapply(similarity[3:dim(similarity)[1], 3:dim(similarity)[2]],
                                     function(x) as.numeric(as.character(x))))
  rownames(similarity) <- r_names
  colnames(similarity) <- c_names
  return(similarity)
}

get_random_drug_cluster <- function(n, drugs) {
  set.seed(19)
  f_name <- paste0("output/gs/optimal_clusters_bkm.tsv")
  clusters <- strsplit(read.csv(f_name, sep = "\t")$Drugs, ";")
  len <- 0
  for (i in 1:length(clusters))
    if(length(clusters[[i]]) > 1)
      len <- len + 1
  random_clusters <- list()
  for (i in 1:n) {
    random_indices <- sort(sample.int(length(drugs), 1271/len))
    random_clusters[[length(random_clusters) + 1]] <- drugs[random_indices]
  }
  return(random_clusters)
}

get_drug_cluster <- function(cluster_algo) {
  f_name <- paste0("output/gs/optimal_clusters_", cluster_algo, ".tsv")
  clusters <- strsplit(read.csv(f_name, sep = "\t")$Drugs, ";")
  return(clusters)
}

compute_cluster_similarity_mcs <- function(mcs_similarity, cluster_algo) {
  if(cluster_algo == "random")
    clusters <- get_random_drug_cluster(1, rownames(mcs_similarity))
  else
    clusters <- get_drug_cluster(cluster_algo)
  cluster_similarity <- list()
  for (i in 1:length(clusters)) {
  # for (i in 13:13) {
    drugs <- clusters[[i]]
    mcs_drugs <- array()[-1]
    for (j in 1:length(drugs))
      if (substr(drugs[j], 0, 26) %in% rownames(mcs_similarity)) #  && ((substr(drugs[j], 0, 26) %in% colnames(mcs_similarity))
        mcs_drugs <- c(mcs_drugs, substr(drugs[j], 0, 26))
    cat("Cluster ", i, "/", length(clusters), " => Found ", length(mcs_drugs), "/", length(drugs), " drugs\n")
    if (length(drugs) > 1) {
      # print(length(mcs_drugs))
      if (length(mcs_drugs) > 1) {
        sim <- array()[-1]
        for (j in 1 : (length(mcs_drugs)-1))
          for (k in (j+1) : length(mcs_drugs))
            sim <- c(sim, mcs_similarity[mcs_drugs[j], mcs_drugs[k]])
      } else if (length(mcs_drugs) == 1) {
        sim <- c(1)
      } else {
        sim <- c(0)
      }
      cluster_similarity[[i]] <- as.vector(sim)
    }
  }
  # cat(min(cluster_similarity[[1]]), max(cluster_similarity[[1]]), mean(cluster_similarity[[1]]), median(cluster_similarity[[1]]), "\n")
  return(cluster_similarity)
}

print_cluster_similarity <- function(cluster_similarity) {
  cat("Cluster\tPairwise_similarities\n")
  for (i in 1:length(cluster_similarity)) {
    cat(paste0(i, "\t", paste(cluster_similarity[[i]], collapse=";"), "\n"))
  }
}

read_cluster_similarity <- function(cluster_algo) {
  folder <- "output/mcs_analysis/"
  f_name <- paste0(folder, "MCSSim_", cluster_algo, "_overlap_coefficient.tsv")
  cluster_similarity <- type.convert(strsplit(read.csv(f_name, sep = "\t")$Pairwise_similarities, ";"), as.is=TRUE)
  return(cluster_similarity)
}

print_cluster_similarity_metadata <- function(association, cluster_algo) {
  cluster_similarity <- read_cluster_similarity(cluster_algo)
  clusters <- get_drug_cluster(cluster_algo)
  cat("Cluster\tNo_of_drugs\tNo_of_drugs_with_mcs\tNo_of_similarity_values\tMin_similarity\tMax_similarity\tMean_similarity\tMedian_similarity\n")
  for (i in 1:length(cluster_similarity)) {
    drugs <- clusters[[i]]
    mcs_drugs <- array()[-1]
    for (j in 1:length(drugs))
      if (substr(drugs[j], 0, 26) %in% rownames(mcs_similarity)) #  && ((substr(drugs[j], 0, 26) %in% colnames(mcs_similarity))
        mcs_drugs <- c(mcs_drugs, substr(drugs[j], 0, 26))
    cat(paste0(i, "\t", length(clusters[[i]]), "\t", length(mcs_drugs), "\t", length(cluster_similarity[[i]]), "\t", min(cluster_similarity[[i]]), "\t", max(cluster_similarity[[i]]), "\t", mean(cluster_similarity[[i]]), "\t", median(cluster_similarity[[i]]), "\n"))
  }
}

read_cluster_similarity_metadata <- function(cluster_algo) {
  folder <- "output/mcs_analysis/"
  f_name <- paste0(folder, "MCSSim_metadata_", cluster_algo, ".tsv")
  cluster_similarity_metadata <- read.csv(f_name, sep = "\t")
  return(cluster_similarity_metadata)
}

mcs_similarity <- read_drug_drug_mcs_similarity("input/PubChem/drug_drug_mcs_overlap_coefficient_matrix_pubchem.tsv")

# cluster_similarity <- compute_cluster_similarity_mcs(mcs_similarity, cluster_algo = "kmc")
# cluster_similarity <- compute_cluster_similarity_mcs(mcs_similarity, cluster_algo = "bkm")
# cluster_similarity <- compute_cluster_similarity_mcs(mcs_similarity, cluster_algo = "ms")
# cluster_similarity <- compute_cluster_similarity_mcs(mcs_similarity, cluster_algo = "birch")
# cluster_similarity <- compute_cluster_similarity_mcs(mcs_similarity, cluster_algo = "random")
# print_cluster_similarity(cluster_similarity)

# cluster_similarity <- read_cluster_similarity(cluster_algo = "kmc")
# cluster_similarity <- read_cluster_similarity(cluster_algo = "bkm")
# cluster_similarity <- read_cluster_similarity(cluster_algo = "ms")
# cluster_similarity <- read_cluster_similarity(cluster_algo = "birch")
cluster_similarity <- read_cluster_similarity(cluster_algo = "random")
print(cluster_similarity)

# print_cluster_similarity_metadata(association, cluster_algo = "kmc")
# print_cluster_similarity_metadata(association, cluster_algo = "bkm")
# print_cluster_similarity_metadata(association, cluster_algo = "ms")
# print_cluster_similarity_metadata(association, cluster_algo = "birch")

# cluster_similarity_metadata <- read_cluster_similarity_metadata(cluster_algo = "kmc")
# cluster_similarity_metadata <- read_cluster_similarity_metadata(cluster_algo = "bkm")
# cluster_similarity_metadata <- read_cluster_similarity_metadata(cluster_algo = "ms")
# cluster_similarity_metadata <- read_cluster_similarity_metadata(cluster_algo = "birch")
# print(cluster_similarity_metadata)
