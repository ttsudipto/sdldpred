library(ggplot2)
library(patchwork)

n_clusters_kmc <- rep(seq(10, 600, by=10), 3)
n_clusters_bkm <- rep(seq(20, 600, by=20), 3)
bandwidth_ms <- rep(seq(0.05, 2, by=0.05), 3)
n_clusters_birch <- rep(seq(20, 600, by=20), 3)

group_kmc <- c(rep("Cosine similarity", length(n_clusters_kmc)/3), rep("Pearson Correlation Coefficient", length(n_clusters_kmc)/3), rep("Jaccard similarity", length(n_clusters_kmc)/3))
group_bkm <- c(rep("Cosine similarity", length(n_clusters_bkm)/3), rep("Pearson Correlation Coefficient", length(n_clusters_bkm)/3), rep("Jaccard similarity", length(n_clusters_bkm)/3))
group_ms <- c(rep("Cosine similarity", length(bandwidth_ms)/3), rep("Pearson Correlation Coefficient", length(bandwidth_ms)/3), rep("Jaccard similarity", length(bandwidth_ms)/3))
group_birch<- c(rep("Cosine similarity", length(n_clusters_birch)/3), rep("Pearson Correlation Coefficient", length(n_clusters_birch)/3), rep("Jaccard similarity", length(n_clusters_birch)/3))

sil_coeff_kmc_cosine <- c(0.323, 0.38, 0.401, 0.419, 0.424, 0.453, 0.478, 0.501, 0.524, 0.55, 0.552, 0.546, 0.547, 0.552, 0.578, 0.581, 0.585, 0.588, 0.59, 0.596, 0.6, 0.601, 0.603, 0.605, 0.606, 0.609, 0.612, 0.615, 0.616, 0.617, 0.608, 0.606, 0.612, 0.612, 0.61, 0.612, 0.614, 0.616, 0.617, 0.623, 0.626, 0.631, 0.631, 0.632, 0.633, 0.639, 0.641, 0.641, 0.641, 0.64, 0.639, 0.638, 0.635, 0.634, 0.633, 0.63, 0.5, 0.575, 0.622, 0.599)
sil_coeff_bkm_cosine <- c(0.343, 0.364, 0.442, 0.473, 0.5, 0.521, 0.523, 0.544, 0.546, 0.561, 0.566, 0.574, 0.582, 0.59, 0.6, 0.604, 0.612, 0.613, 0.622, 0.628, 0.631, 0.64, 0.644, 0.647, 0.643, 0.643, 0.638, 0.631, 0.63, 0.63)
sil_coeff_ms_cosine <- c(0.63, 0.63, 0.63, 0.631, 0.631, 0.63, 0.627, 0.628, 0.609, 0.599, 0.583, 0.581, 0.571, 0.568, 0.564, 0.561, 0.56, 0.545, 0.533, 0.528, 0.53, 0.507, 0.49, 0.455, 0.423, 0.41, 0.41, 0.353, 0.377, 0.368, 0.278, 0.303, 0.31, 0.291, 0.294, 0.308, 0.297, 0.293, 0.287, 0.298)
sil_coeff_birch_cosine <- c(0.359, 0.412, 0.453, 0.478, 0.51, 0.515, 0.53, 0.537, 0.565, 0.572, 0.572, 0.586, 0.593, 0.593, 0.595, 0.614, 0.624, 0.627, 0.625, 0.63, 0.633, 0.631, 0.633, 0.639, 0.639, 0.636, 0.633, 0.631, 0.631, 0.631)

sil_coeff_kmc_pearson <- c(0.313, 0.342, 0.393, 0.413, 0.444, 0.463, 0.496, 0.498, 0.521, 0.533, 0.533, 0.549, 0.557, 0.558, 0.563, 0.568, 0.572, 0.576, 0.578, 0.582, 0.585, 0.588, 0.591, 0.597, 0.6, 0.603, 0.606, 0.608, 0.61, 0.612, 0.613, 0.612, 0.615, 0.616, 0.617, 0.618, 0.62, 0.623, 0.627, 0.624, 0.622, 0.625, 0.626, 0.628, 0.628, 0.629, 0.631, 0.633, 0.632, 0.633, 0.638, 0.64, 0.639, 0.637, 0.633, 0.629, 0.5, 0.571, 0.485, 0.504)
sil_coeff_bkm_pearson <- c(0.3, 0.37, 0.412, 0.44, 0.468, 0.497, 0.516, 0.531, 0.552, 0.559, 0.566, 0.572, 0.58, 0.587, 0.591, 0.596, 0.602, 0.612, 0.615, 0.622, 0.627, 0.635, 0.638, 0.641, 0.641, 0.641, 0.636, 0.63, 0.63, 0.63)
sil_coeff_ms_pearson <- c(0.63, 0.63, 0.63, 0.63, 0.631, 0.631, 0.63, 0.628, 0.623, 0.598, 0.59, 0.583, 0.576, 0.566, 0.567, 0.561, 0.554, 0.553, 0.541, 0.531, 0.525, 0.508, 0.492, 0.489, 0.458, 0.415, 0.366, 0.356, 0.358, 0.388, 0.379, 0.343, 0.299, 0.3, 0.296, 0.282, 0.284, 0.281, 0.287, 0.272)
sil_coeff_birch_pearson <- c(0.336, 0.388, 0.444, 0.48, 0.493, 0.5, 0.519, 0.526, 0.536, 0.543, 0.553, 0.57, 0.586, 0.59, 0.59, 0.599, 0.602, 0.615, 0.62, 0.624, 0.624, 0.622, 0.623, 0.629, 0.631, 0.64, 0.636, 0.63, 0.629, 0.629)

sil_coeff_kmc_jaccard <- c(0.311, 0.337, 0.379, 0.412, 0.447, 0.444, 0.464, 0.461, 0.488, 0.503, 0.514, 0.513, 0.512, 0.517, 0.527, 0.529, 0.533, 0.536, 0.537, 0.545, 0.547, 0.553, 0.552, 0.552, 0.557, 0.561, 0.563, 0.565, 0.574, 0.577, 0.578, 0.578, 0.583, 0.588, 0.587, 0.589, 0.595, 0.595, 0.6, 0.601, 0.607, 0.609, 0.612, 0.612, 0.612, 0.614, 0.614, 0.615, 0.619, 0.624, 0.627, 0.629, 0.629, 0.629, 0.63, 0.63, 0.507, 0.492, 0.532, 0.492)
sil_coeff_bkm_jaccard <- c(0.297, 0.369, 0.421, 0.451, 0.462, 0.489, 0.503, 0.52, 0.536, 0.544, 0.551, 0.557, 0.565, 0.567, 0.573, 0.58, 0.587, 0.59, 0.596, 0.603, 0.603, 0.615, 0.621, 0.625, 0.626, 0.629, 0.63, 0.629, 0.63, 0.63)
sil_coeff_ms_jaccard <- c(0.63, 0.63, 0.622, 0.596, 0.579, 0.552, 0.509, 0.498, 0.468, 0.428, 0.377, 0.334, 0.328, 0.342, 0.331, 0.345, 0.183, 0.206, 0.197, 0.183, 0.224, 0.223, 0.223, 0.351, 0.351, 0.351, 0.351, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
sil_coeff_birch_jaccard <- c(0.322, 0.368, 0.439, 0.461, 0.481, 0.496, 0.509, 0.544, 0.543, 0.549, 0.55, 0.553, 0.554, 0.549, 0.553, 0.556, 0.566, 0.568, 0.571, 0.572, 0.579, 0.586, 0.595, 0.599, 0.604, 0.618, 0.625, 0.625, 0.625, 0.625)

sc_kmc <- c(sil_coeff_kmc_cosine, sil_coeff_kmc_pearson, sil_coeff_kmc_jaccard)
sc_bkm <- c(sil_coeff_bkm_cosine, sil_coeff_bkm_pearson, sil_coeff_bkm_jaccard)
sc_ms <- c(sil_coeff_ms_cosine, sil_coeff_ms_pearson, sil_coeff_ms_jaccard)
sc_birch <- c(sil_coeff_birch_cosine, sil_coeff_birch_pearson, sil_coeff_birch_jaccard)

data_kmc <- data.frame("n_clusters"=n_clusters_kmc, "SC"=sc_kmc, "Group"=group_kmc)
data_bkm <- data.frame("n_clusters"=n_clusters_bkm, "SC"=sc_bkm, "Group"=group_bkm)
data_ms <- data.frame("n_clusters"=bandwidth_ms, "SC"=sc_ms, "Group"=group_ms)
data_birch <- data.frame("n_clusters"=n_clusters_birch, "SC"=sc_birch, "Group"=group_birch)

plot_theme <- theme(plot.title=element_text(size=10),
                    panel.background=element_rect(fill="white"), 
                    panel.grid=element_line(color="grey90"),
                    panel.grid.minor=element_blank(),
                    panel.border=element_rect(color="black", fill=NA),
                    axis.title=element_text(size=9), 
                    axis.text=element_text(size=9, color="gray10",), 
                    axis.ticks.length=unit(7, "pt")
)
legend_theme <- theme(legend.title=element_blank(),
                      legend.text=element_text(size=10),
                      legend.spacing.y=unit(7, "pt"),
                      # legend.background=element_rect(fill="gray95"),
                      legend.direction="horizontal",
                      legend.position="bottom",
                      legend.key.width = unit(50, "pt")
)

plot_kmc <- ggplot(data_kmc, mapping=aes(x=n_clusters_kmc, y=sc_kmc, group=group_kmc)) +
  geom_line(aes(group=group_kmc, color=group_kmc)) +
  xlab("Number of clusters") + ylab("Silhouette Coefficient") +
  ggtitle(paste0("(a) K-means")) +
  # scale_color_manual(values = c("red", "blue", "black")) +
  scale_x_continuous(breaks=seq(0, 600, by=100)) +
  scale_y_continuous(breaks=seq(0.25, 0.7, by=0.05)) +
  coord_cartesian(ylim = c(0.25, 0.7)) +
  plot_theme + theme(legend.position="none") 
  # legend_theme
# plot_kmc

plot_bkm <- ggplot(data_bkm, mapping=aes(x=n_clusters_bkm, y=sc_bkm, group=group_bkm)) +
  geom_line(aes(group=group_bkm, color=group_bkm)) +
  xlab("Number of clusters") + ylab("Silhouette Coefficient") +
  ggtitle(paste0("(b) Bisecting K-means")) +
  scale_x_continuous(breaks=seq(0, 600, by=100)) +
  scale_y_continuous(breaks=seq(0.25, 0.7, by=0.05)) +
  coord_cartesian(ylim = c(0.25, 0.7)) +
  plot_theme + theme(legend.position="none") 
  # legend_theme
# plot_bkm

plot_ms <- ggplot(data_ms, mapping=aes(x=bandwidth_ms, y=sc_ms, group=group_ms)) +
  geom_line(aes(group=group_ms, color=group_ms)) +
  xlab("Bandwidth") + ylab("Silhouette Coefficient") +
  ggtitle(paste0("(c) Mean Shift")) +
  scale_x_continuous(breaks=seq(0, 2, by=0.2)) +
  scale_y_continuous(breaks=seq(0, 0.7, by=0.1)) +
  coord_cartesian(ylim = c(0, 0.7)) +
  plot_theme + theme(legend.position="none") 
  # legend_theme
# plot_ms

plot_birch <- ggplot(data_birch, mapping=aes(x=n_clusters_birch, y=sc_birch, group=group_birch)) +
  geom_line(aes(group=group_birch, color=group_birch)) +
  xlab("Number of clusters") + ylab("Silhouette Coefficient") +
  ggtitle(paste0("(d) Balanced Iterative Reducing and Clustering using Hierarchies")) +
  scale_x_continuous(breaks=seq(0, 600, by=100)) +
  scale_y_continuous(breaks=seq(0.25, 0.7, by=0.05)) +
  coord_cartesian(ylim = c(0.25, 0.7)) +
  plot_theme + theme(legend.position="none") 
  # legend_theme
# plot_birch

design <- "
  12
  34
  55
"
# # svg(filename=paste0("output/plots/sc_variation.svg"), height=8, width=10)
# plot_kmc + plot_bkm + plot_ms + plot_birch + legend_theme + guide_area() + plot_layout(design = design, guides="collect", nrow=3, heights=c(3,3,1))
# # dev.off()

# (plot_kmc | plot_bkm) / (plot_ms + plot_birch) 


