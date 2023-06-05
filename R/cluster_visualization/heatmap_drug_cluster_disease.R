library("pheatmap")
library("dplyr")

color <- rev(grDevices::hcl.colors(10, palette="Purples 3"))

get_cluster_annotations <- function(algo, n_clusters_cutoff = NA) {
  f_name <- paste0("output/gs/optimal_clusters_", algo, ".tsv")
  c <- strsplit(read.csv(f_name, sep = "\t")$Drugs, ";")
  cid <- 1
  drugs <- array()[-1]
  cluster_labels <- array()[-1]
  for (i in 1:length(c)) {
    for (j in 1:length(c[[i]])) {
      drugs <- c(drugs, substr(c[[i]][j], 0, 26))
      cluster_labels <- c(cluster_labels, cid)
    }
    cid <- cid + 1
  }
  clusters <- data.frame(Cluster = cluster_labels, row.names = drugs)
  if (!is.na(n_clusters_cutoff)) {
    for (i in 1:nrow(clusters))
      if (clusters[i, "Cluster"] > n_clusters_cutoff)
        clusters[i, "Cluster"] <- n_clusters_cutoff + 1
  }
  return(clusters)
}

merge_clusters <- function(clusters, c_label, algo, c_type = "str") {
  drugs <- rownames(clusters)
  c_temp = array()[-1]
  for (i in 1:nrow(c_label)) {
    if (c_type == "str")
      c_temp <- c(c_temp, toString(c_label[drugs[i], "Cluster"]))
    else
      c_temp <- c(c_temp, c_label[drugs[i], "Cluster"])
  }
  clusters$NewCluster <- c_temp
  colnames(clusters)[ncol(clusters)] <- algo
  # print(clusters)
  return(clusters)
}

read_disease_names <- function(f_name) {
  names <- read.csv(f_name, header = TRUE, sep="\t")
  rownames(names) <- names[, "DiseaseID"]
  return(names)
}

read_heatmap_data <- function(f_name) {
  similarity <- read.csv(f_name, header=FALSE, sep="\t")
  disease_names <- read_disease_names("input/CTD/pulmonary_diseases_ctd.tsv")
  c_ids <- substr(similarity[1,], 0, 26)[3:dim(similarity)[2]]
  r_names <- substr(similarity[,2], 0, 26)[-1]
  similarity <- as.data.frame(lapply(similarity[-1, 3:dim(similarity)[2]],
                                     function(x) as.numeric(as.character(x))))
  c_names <- array()
  for (i in 1:length(c_ids))
    c_names <- c(c_names, disease_names[c_ids[i], "DiseaseName"])
  rownames(similarity) <- r_names
  colnames(similarity) <- c_names[-1]
  return(similarity)
}

generate_ann_colors <- function(clusters) {
  color_discrete <- rep(c("maroon", "lightgreen"), 200)[1:length(unique(clusters[, 'BKM']))] 
  names(color_discrete) <- seq(1, length(unique(clusters[, "BKM"])))
  # color_discrete <- sample(grDevices::hcl.colors(n=length(unique(clusters[, "BKM"])), "Dark 3"))
  # names(color_discrete) <- unique(clusters[, "BKM"])
  ann_colors <- list(KMC=color_discrete, BKM=color_discrete, 
                     MS=color_discrete, BIRCH=color_discrete)
  return(ann_colors)
}

###############################################################################
#                               All clusters                                  #
###############################################################################

# clustered_drug_counts = data.frame(KMC=c(928), BKM=c(929), MS=c(818), BIRCH=c(913))
# cluster_count = data.frame(KMC=c(127), BKM=c(138), MS=c(96), BIRCH=c(122))
# # cluster_count = data.frame(KMC=c(470), BKM=c(480), MS=c(549), BIRCH=c(480))

# c_kmc <- get_cluster_annotations(algo = "kmc", n_clusters_cutoff = cluster_count[1,"KMC"])
# c_bkm <- get_cluster_annotations(algo = "bkm", n_clusters_cutoff = cluster_count[1,"BKM"])
# c_ms <- get_cluster_annotations(algo = "ms", n_clusters_cutoff = cluster_count[1,"MS"])
# c_birch <- get_cluster_annotations(algo = "birch", n_clusters_cutoff = cluster_count[1,"BIRCH"])
# clusters <- data.frame(row.names = sort(rownames(c_kmc)))
# clusters <- merge_clusters(clusters, c_kmc, "KMC")
# clusters <- merge_clusters(clusters, c_bkm, "BKM")
# clusters <- merge_clusters(clusters, c_ms, "MS")
# clusters <- merge_clusters(clusters, c_birch, "BIRCH")

# similarity <- read_heatmap_data("input/CTD/pulmonary_drug_disease_association_matrix_ctd.tsv")

# ann_colors <- generate_ann_colors(clusters)

# # svg(filename="drug_clustering_disease_all.svg", height=10, width=8)
# pheatmap(similarity[rownames(c_bkm),], color=color, border_color=NA,
#          annotation_row = clusters, annotation_colors = ann_colors,
#          fontsize=7, cluster_rows = FALSE, cluster_cols = TRUE,
#          show_colnames = TRUE, show_rownames = FALSE)
# # dev.off()

# # first 1:635 second 636:1271
# # svg(filename="drug_clustering_disease_1_635.svg", height=10, width=8)
# pheatmap(similarity[rownames(c_bkm)[1:635],], color=color, border_color="grey",
#          annotation_row = clusters, annotation_colors = ann_colors,
#          fontsize=7, cluster_rows = FALSE, cluster_cols = TRUE,
#          show_colnames = TRUE, show_rownames = FALSE)
# # dev.off()
# # svg(filename="drug_clustering_disease_636_1271.svg", height=10, width=8)
# pheatmap(similarity[rownames(c_bkm)[636:1271],], color=color, border_color="grey",
#          annotation_row = clusters, annotation_colors = ann_colors,
#          fontsize=7, cluster_rows = FALSE, cluster_cols = TRUE,
#          show_colnames = TRUE, show_rownames = FALSE)
# # dev.off()

###############################################################################
#                        Optimal cluster (size > 1)                           #
###############################################################################

# clustered_drug_counts = data.frame(KMC=c(928), BKM=c(929), MS=c(818), BIRCH=c(913))
# cluster_count = data.frame(KMC=c(127), BKM=c(138), MS=c(96), BIRCH=c(122))

# c_bkm <- get_cluster_annotations(algo = "bkm", n_clusters_cutoff = cluster_count[1,"BKM"])
# clusters <- data.frame(row.names = sort(rownames(c_bkm)))
# clusters <- merge_clusters(clusters, c_bkm, "BKM")

# similarity <- read_heatmap_data("input/CTD/pulmonary_drug_disease_association_matrix_ctd.tsv")

# ann_colors <- generate_ann_colors(clusters)

# # svg(filename="drug_clustering_disease_all.svg", height=10, width=8)
# pheatmap(similarity[rownames(c_bkm)[1:clustered_drug_counts[1,"BKM"]],], 
#          color=color, border_color=NA, annotation_colors = ann_colors,
#          annotation_row = clusters, fontsize=7, 
#          cluster_cols = FALSE, cluster_rows = FALSE,
#          show_colnames = TRUE, show_rownames = FALSE)
# # dev.off()
