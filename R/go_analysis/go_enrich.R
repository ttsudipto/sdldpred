library(clusterProfiler)
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

get_drug_cluster <- function(similarity, cluster_algo) {
  f_name <- paste0("output/gs/", similarity, "/optimal_clusters_", cluster_algo, ".tsv")
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

get_union_gene_set <- function(drugs, association, filter_genes = TRUE) {
  n_drugs <- length(drugs)
  genes = array()[-1]
  for (j in 1:n_drugs) {
    g <- get_gene_set(drugs[j], association)
    if(filter_genes) {
      if(length(g) < 1000)
        genes <- c(genes, g)
    } else
      genes <- c(genes, g)
  }
  genes <- unique(genes)
  return(genes)
}

get_gene_universe <- function (clusters, association) {
  gene_universe <- as.character(get_gene_id_map()$GeneID)
  return(gene_universe)
}

compute_GO_enrichment <- function(genes, ontology, gene_universe = NULL, p_adjust= "fdr") {
  ego <- enrichGO(gene = genes, OrgDb = "org.Hs.eg.db", ont = ontology,
                  pvalueCutoff = 0.01, pAdjustMethod = p_adjust,
                  qvalueCutoff = 0.05, universe = gene_universe, readable = TRUE)
  return(ego)
}

compute_cluster_enrichment <- function(association, similarity, cluster_algo, ontology, p_adjust="fdr", drop_level=2) {
  clusters <- get_drug_cluster(similarity, cluster_algo)
  gene_universe <- get_gene_universe(clusters, association)
  cluster_GO_enrich <- list()
  for (i in 1:length(clusters)) {
  # for (i in 25:25) {
    if (length(clusters[[i]]) > 1) {
      genes <- get_union_gene_set(clusters[[i]], association, filter_genes = FALSE)
      genes <- as.character(get_gene_id_map()[genes, "GeneID"])
      cat("Cluster ", i, "/", length(clusters), " => ", length(genes), " genes\n")
      ego <- compute_GO_enrichment(genes, ontology, gene_universe, p_adjust)
      if (!is.null(ego))
        for (j in 1:drop_level)
          ego <- dropGO(ego, level=j)
      cluster_GO_enrich[[i]] <- ego
    }
  }
  return(cluster_GO_enrich)
}

read_cluster_enrichment <- function(similarity, cluster_algo, ontology) {
  folder <- paste0("output/go_analysis/gene_union/", similarity, "/")
  f_name <- paste0(folder, "GOEnrichment_", cluster_algo, "_", tolower(ontology), ".rds")
  # f_name <- "foo.rds"
  cluster_similarity <- readRDS(f_name)
  return(cluster_similarity)
}

print_cluster_enrichment_metadata <- function(association, similarity, cluster_algo, ontology) {
  enrich_result <- read_cluster_enrichment(similarity, cluster_algo, ontology)
  clusters <- get_drug_cluster(similarity, cluster_algo)
  cat("Cluster\tNo_of_drugs\tNo_of_genes\tNo_of_enrichment_genes\tNo_of_bg_genes\tNo_of_enriched_GO_terms\tTop_GO_term\tTop_pvalue\n")
  for (i in 1:length(enrich_result)) {
  # for (i in 25:25) {
    if (is.null(enrich_result[[i]])) {
      enrich_gene_count <- bg_geneCcount <- enrich_GO_term_count <- top_pval <- 0
      min_GO_term <- ""
    } else {
      result <- enrich_result[[i]]@result
      cutoff <- enrich_result[[i]]@pvalueCutoff
      enrich_gene_count <- length(enrich_result[[i]]@gene)
      bg_gene_count <- length(enrich_result[[i]]@universe)
      enrich_GO_term_count <- length(result[result$p.adjust<cutoff,"p.adjust"])
      min_GO_term <- paste0(result[1,"Description"], " (", result[1, "ID"], ")")
      top_pval <- result[1, "p.adjust"]
    }
    cat(paste0(i, "\t", length(clusters[[i]]), "\t", length(get_union_gene_set(clusters[[i]], association, filter_genes = FALSE)), "\t",
               enrich_gene_count, "\t", bg_gene_count, "\t", enrich_GO_term_count, "\t", min_GO_term, "\t", top_pval, "\n"))
  }
}

# association <- read_drug_gene_association("input/CTD/pulmonary_drug_gene_association_matrix_ctd.tsv")
# all_genes <- as.character(get_gene_id_map()$GeneID)

# go_enrich_result <- compute_cluster_enrichment(association, similarity = "cosine", cluster_algo = "bkm", ontology = "MF")
# go_enrich_result <- compute_cluster_enrichment(association, similarity = "cosine", cluster_algo = "bkm", ontology = "BP")
# go_enrich_result <- compute_cluster_enrichment(association, similarity = "cosine", cluster_algo = "bkm", ontology = "CC")
# go_enrich_result <- compute_cluster_enrichment(association, similarity = "pearson", cluster_algo = "bkm", ontology = "MF")
# go_enrich_result <- compute_cluster_enrichment(association, similarity = "pearson", cluster_algo = "bkm", ontology = "BP")
# go_enrich_result <- compute_cluster_enrichment(association, similarity = "pearson", cluster_algo = "bkm", ontology = "CC")
# go_enrich_result <- compute_cluster_enrichment(association, similarity = "jaccard", cluster_algo = "ms", ontology = "MF")
# go_enrich_result <- compute_cluster_enrichment(association, similarity = "jaccard", cluster_algo = "ms", ontology = "BP")
# go_enrich_result <- compute_cluster_enrichment(association, similarity = "jaccard", cluster_algo = "ms", ontology = "CC")
# saveRDS(go_enrich_result, "foo.rds")

# go_enrich_result <- read_cluster_enrichment(similarity = "cosine", cluster_algo = "bkm", ontology = "MF")
# go_enrich_result <- read_cluster_enrichment(similarity = "cosine", cluster_algo = "bkm", ontology = "BP")
# go_enrich_result <- read_cluster_enrichment(similarity = "cosine", cluster_algo = "bkm", ontology = "CC")
# go_enrich_result <- read_cluster_enrichment(similarity = "pearson", cluster_algo = "bkm", ontology = "MF")
# go_enrich_result <- read_cluster_enrichment(similarity = "pearson", cluster_algo = "bkm", ontology = "BP")
# go_enrich_result <- read_cluster_enrichment(similarity = "pearson", cluster_algo = "bkm", ontology = "CC")
# go_enrich_result <- read_cluster_enrichment(similarity = "jaccard", cluster_algo = "ms", ontology = "MF")
# go_enrich_result <- read_cluster_enrichment(similarity = "jaccard", cluster_algo = "ms", ontology = "BP")
# go_enrich_result <- read_cluster_enrichment(similarity = "jaccard", cluster_algo = "ms", ontology = "CC")

# print_cluster_enrichment_metadata(association, similarity = "cosine", cluster_algo = "bkm", ontology = "MF")
# print_cluster_enrichment_metadata(association, similarity = "cosine", cluster_algo = "bkm", ontology = "BP")
# print_cluster_enrichment_metadata(association, similarity = "cosine", cluster_algo = "bkm", ontology = "CC")
# print_cluster_enrichment_metadata(association, similarity = "pearson", cluster_algo = "bkm", ontology = "MF")
# print_cluster_enrichment_metadata(association, similarity = "pearson", cluster_algo = "bkm", ontology = "BP")
# print_cluster_enrichment_metadata(association, similarity = "pearson", cluster_algo = "bkm", ontology = "CC")
# print_cluster_enrichment_metadata(association, similarity = "jaccard", cluster_algo = "ms", ontology = "MF")
# print_cluster_enrichment_metadata(association, similarity = "jaccard", cluster_algo = "ms", ontology = "BP")
# print_cluster_enrichment_metadata(association, similarity = "jaccard", cluster_algo = "ms", ontology = "CC")
