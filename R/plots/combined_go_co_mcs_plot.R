library(ggplot2)
library(ggpubr)
library(patchwork)

plot_theme <- theme(plot.title=element_text(size=10),
                    panel.background=element_rect(fill="white"), 
                    # panel.grid.major.x=element_line(color="grey90"),
                    panel.border=element_rect(color="black", fill=NA),
                    axis.title.x=element_text(size=12), 
                    axis.title.y=element_text(size=10), 
                    axis.text=element_text(size=7, color="gray10",), 
                    axis.ticks.length=unit(3, "pt")
)

read_cluster_similarity_go_gene_union <- function(cluster_algo, ontology, measure = "Lin", cluster_cutoff = NA) {
  folder <- "output/go_analysis/gene_union/"
  f_name <- paste0(folder, "GOSemSim_", cluster_algo, "_", tolower(ontology), "_", tolower(measure), ".rds")
  cluster_similarity <- readRDS(f_name)
  if (!is.na(cluster_cutoff))
    cluster_similarity = cluster_similarity[1:cluster_cutoff]
  rf_name <- paste0(folder, "GOSemSim_random_", tolower(ontology), "_", tolower(measure), ".rds")
  random_cluster_similarity <- readRDS(rf_name)
  cluster_similarity[[length(cluster_similarity) + 1]] <- random_cluster_similarity[[1]]
  return(cluster_similarity)
}

read_cluster_similarity_co <- function(cluster_algo, ontology, measure = "Lin", cluster_cutoff = NA) {
  folder <- "output/co_analysis/"
  f_name <- paste0(folder, "COAnalysis_", cluster_algo, "_", ontology, "_", tolower(measure), ".tsv")
  cluster_similarity <- type.convert(strsplit(read.csv(f_name, sep = "\t")$Pairwise_similarities, ";"), as.is=TRUE)
  if (!is.na(cluster_cutoff))
    cluster_similarity = cluster_similarity[1:cluster_cutoff]
  rf_name <- paste0(folder, "COAnalysis_random_", ontology, "_", tolower(measure), ".tsv")
  random_cluster_similarity <- type.convert(strsplit(read.csv(rf_name, sep = "\t")$Pairwise_similarities, ";"), as.is=TRUE)
  cluster_similarity[[length(cluster_similarity) + 1]] <- random_cluster_similarity[[1]]
  return(cluster_similarity)
}

read_cluster_similarity_mcs <- function(cluster_algo, cluster_cutoff = NA) {
  folder <- "output/mcs_analysis/"
  f_name <- paste0(folder, "MCSSim_", cluster_algo, "_overlap_coefficient.tsv")
  cluster_similarity <- type.convert(strsplit(read.csv(f_name, sep = "\t")$Pairwise_similarities, ";"), as.is=TRUE)
  if (!is.na(cluster_cutoff))
    cluster_similarity = cluster_similarity[1:cluster_cutoff]
  rf_name <- paste0(folder, "MCSSim_random_overlap_coefficient.tsv")
  random_cluster_similarity <- type.convert(strsplit(read.csv(rf_name, sep = "\t")$Pairwise_similarities, ";"), as.is=TRUE)
  cluster_similarity[[length(cluster_similarity) + 1]] <- random_cluster_similarity[[1]]
  return(cluster_similarity)
}

convert_to_df <- function(cluster_similarity) {
  cluster <- array()[-1]
  similarity <- array()[-1]
  for (i in 1:length(cluster_similarity)) {
    # sc <- array()[-1]
    # for (j in 1:length(cluster_similarity[[i]]))
    #   if (cluster_similarity[[i]][j] < 0.1)
    #     sc <- c(sc, cluster_similarity[[i]][j])
    # similarity <- c(similarity, sc)
    # cluster <- c(cluster, rep(i, length(sc)))
    similarity <- c(similarity, cluster_similarity[[i]])
    cluster <- c(cluster, rep(i, length(cluster_similarity[[i]])))
  }
  cluster_similarity_df <- data.frame(Cluster = cluster, Similarity = similarity)
  return(cluster_similarity_df)
}

make_box_plot_go <- function(cluster_similarity_df, title="", ontology="") {
  cluster <- cluster_similarity_df$Cluster
  similarity <- cluster_similarity_df$Similarity
  avg <- median(cluster_similarity_df[(cluster_similarity_df$Cluster == max(cluster)), "Similarity"])
  ref <- length(unique(cluster))
  sig_labels <- list(cutpoints = c(0, 0.001, 0.01, 0.05, Inf), symbols = c("*\n*\n*", "*\n*", "*", ""))
  box_colors = c(rep("#ccccff", ref-1), "darkred")
  box_alpha = c(rep(0.3, ref-1), 0.6)
  plot <- ggplot(cluster_similarity_df, aes(x=as.factor(cluster), y=similarity)) +
    geom_boxplot(alpha=box_alpha, width=0.5, fill=box_colors) + 
    stat_compare_means(label.x = 6, label.y = 1.15, size=5) +
    stat_compare_means(method="wilcox", label = "p.signif", symnum.args = sig_labels, ref.group = ref, size = 9, lineheight = 0.4) +
    geom_hline(yintercept=avg, linetype="dashed", color="black") + 
    scale_y_continuous(breaks=seq(0,1,0.1)) +
    scale_x_discrete(labels=c(as.character(seq(1,length(unique(cluster))-1)), "R")) +
    xlab("Drug clusters") + ylab(paste0("Semantic similarity of GO ", ontology, " terms associated to gene targets of drugs")) + 
    ggtitle(label=title) +
    plot_theme + theme(legend.position="none")
  plot
  return(plot)
}

make_box_plot_co <- function(cluster_similarity_df, ontology="", title="") {
  cluster <- cluster_similarity_df$Cluster
  similarity <- cluster_similarity_df$Similarity
  avg <- median(cluster_similarity_df[(cluster_similarity_df$Cluster == max(cluster)), "Similarity"])
  ref <- length(unique(cluster))
  sig_labels <- list(cutpoints = c(0, 0.001, 0.01, 0.05, Inf), symbols = c("*\n*\n*", "*\n*", "*", ""))
  box_colors = c(rep("#ccccff", ref-1), "darkred")
  box_alpha = c(rep(0.3, ref-1), 0.6)
  plot <- ggplot(cluster_similarity_df, aes(x=as.factor(cluster), y=similarity)) +
    geom_boxplot(alpha=box_alpha, width=0.5, fill=box_colors) + 
    stat_compare_means(label.x = 6, label.y = 1.15, size=5) +
    stat_compare_means(method="wilcox", label = "p.signif", symnum.args = sig_labels, ref.group = ref, size = 9, lineheight = 0.4) +
    geom_hline(yintercept=avg, linetype="dashed", color="black") + 
    scale_y_continuous(breaks=seq(0,1,0.1)) +
    scale_x_discrete(labels=c(as.character(seq(1,length(unique(cluster))-1)), "R")) +
    xlab("Drug clusters") + ylab(paste0("Semantic similarity of CO '", ontology, "' terms associated to drugs")) + 
    ggtitle(label = title) + 
    plot_theme + theme(legend.position="none")
  plot
  return(plot)
}

make_box_plot_mcs <- function(cluster_similarity_df, title="") {
  cluster <- cluster_similarity_df$Cluster
  similarity <- cluster_similarity_df$Similarity
  avg <- median(cluster_similarity_df[(cluster_similarity_df$Cluster == max(cluster)), "Similarity"])
  ref <- length(unique(cluster))
  sig_labels <- list(cutpoints = c(0, 0.001, 0.01, 0.05, Inf), symbols = c("*\n*\n*", "*\n*", "*", ""))
  box_colors = c(rep("#ccccff", ref-1), "darkred")
  box_alpha = c(rep(0.3, ref-1), 0.6)
  plot <- ggplot(cluster_similarity_df, aes(x=as.factor(cluster), y=similarity)) +
    geom_boxplot(alpha=box_alpha, width=0.5, fill=box_colors) + 
    stat_compare_means(label.x = 6, label.y = 1.15, size=5) +
    stat_compare_means(method="wilcox", label = "p.signif", symnum.args = sig_labels, ref.group = ref, size = 9, lineheight = 0.4) +
    geom_hline(yintercept=avg, linetype="dashed", color="black") + 
    scale_y_continuous(breaks=seq(0,1,0.1)) +
    scale_x_discrete(labels=c(as.character(seq(1,length(unique(cluster))-1)), "R")) +
    xlab("Drug clusters") + ylab("Maximum common substructure overlap coefficient") + 
    ggtitle(label = title) + 
    plot_theme + theme(legend.position="none")
  return(plot)
}

cluster_similarity_go <- read_cluster_similarity_go_gene_union(cluster_algo = "bkm", ontology = "MF", cluster_cutoff = 80)
cluster_similarity_df_go <- convert_to_df(cluster_similarity_go)
plot_go <- make_box_plot_go(cluster_similarity_df_go, title="(a)", ontology="MF")
# plot_go

cluster_similarity_co <- read_cluster_similarity_co(cluster_algo = "bkm", ontology = "role", measure = "lin", cluster_cutoff = 80)
cluster_similarity_df_co <- convert_to_df(cluster_similarity_co)
plot_co <- make_box_plot_co(cluster_similarity_df_co, title="(b)", ontology="role")
# plot_co

cluster_similarity_mcs <- read_cluster_similarity_mcs(cluster_algo = "bkm", cluster_cutoff = 80)
cluster_similarity_df_mcs <- convert_to_df(cluster_similarity_mcs)
plot_mcs <- make_box_plot_mcs(cluster_similarity_df_mcs,  title="(c)")
# plot_mcs

# # svg(filename="foo.svg", height=18, width=12)
# plot_go / plot_co / plot_mcs
# # dev.off()