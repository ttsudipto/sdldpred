library(ggplot2)
library(patchwork)

plot_theme <- theme(plot.title=element_text(size=10),
                    panel.background=element_rect(fill="white"), 
                    panel.border=element_rect(color="black", fill=NA),
                    axis.title=element_text(size=12), 
                    axis.text=element_text(size=7, color="gray10",), 
                    axis.ticks.length=unit(3, "pt")
)
grid_plot_theme <- theme(plot.title=element_text(size=10),
                    panel.background=element_rect(fill="white"), 
                    panel.grid.major=element_line(color="grey90"),
                    panel.border=element_rect(color="black", fill=NA),
                    axis.title=element_text(size=12), 
                    axis.text=element_text(size=7, color="gray10",), 
                    axis.ticks.length=unit(3, "pt")
)

read_distances <- function() {
  distances = read.csv("output/density/distances.tsv", sep="\t")
  return(distances)
}

read_density <- function() {
  density <- read.csv("output/density/density.tsv", sep="\t")
  return(density)
}

read_confidences <- function() {
  confidences = read.csv("output/density/confidences.tsv", sep="\t")
  for(i in 1:nrow(confidences))
    confidences[i, "Confidence"] = confidences[i, "Confidence"] * 100
  return(confidences)
}

make_distance_hist_plot <- function(distances) {
  plot <- ggplot(distances, aes(x=`Distance`)) +
    geom_histogram(breaks = seq(0, 6.3, 0.05), fill="slategrey", color="black", alpha=0.1) +
    scale_x_continuous(breaks = seq(0, 6.3, 0.5)) +
    xlab("Pairwise euclidean distances between drugs") + ylab("Frequency") + 
    ggtitle(label="(a)") +
    plot_theme + theme(legend.position="none")
  return(plot)
}

make_density_plot <- function(density) {
  plot <- ggplot(density, aes(x=`Distance`, y=`Density`)) +
    geom_line(color="darkblue", linewidth=0.5) +
    geom_hline(yintercept=0, color="black", linewidth=0.2) +
    scale_x_continuous(breaks = seq(0, 6.3, 0.5)) +
    xlab("Pairwise euclidean distances between drugs") + ylab("Probability") + 
    ggtitle(label="(b)") +
    plot_theme + theme(legend.position="none")
  return(plot)
}

make_predicted_distance_plot <- function(density, dist) {
  shaded_density <- density[density$Distance >= dist,]
  shaded_density <- rbind(c(dist,0), subset(density, density$Distance >= dist), c(3,0))
  plot <- ggplot(density, aes(x=`Distance`, y=`Density`)) +
    geom_line(color="darkblue", linewidth=0.5) +
    geom_segment(aes(x=dist, y=0, xend=dist, yend=`Density`), linetype="dashed", linewidth=0.5) +
    geom_hline(yintercept=0, color="black", linewidth=0.2) +
    geom_point(aes(x=dist, y=0), color="darkred", size=4) +
    geom_polygon(data=shaded_density, aes(x=`Distance`, y=`Density`), fill="purple", alpha=0.1, linetype=0) +
    scale_x_continuous(breaks = seq(0, 6.3, 0.5)) +
    xlab("Pairwise euclidean distances between drugs") + ylab("Probability") + 
    ggtitle(label="(a)") +
    plot_theme + theme(legend.position="none")
  return(plot)
}

make_confidence_plot <- function(confidences) {
  confidence_90 <- approx(confidences$Confidence, confidences$Distance, xout=90)$y
  plot <- ggplot(confidences, aes(x=`Distance`, y=`Confidence`)) +
    geom_line(color="black", linewidth=0.5) +
    geom_segment(aes(x=0, y=90, xend=confidence_90, yend=90), linetype="dashed", linewidth=0.5) +
    geom_segment(aes(x=confidence_90, y=0, xend=confidence_90, yend=90), linetype="dashed", linewidth=0.5) +
    geom_point(aes(x=confidence_90, y=90), color="black", size=2) +
    geom_hline(yintercept=0, color="black", linewidth=0.2) +
    annotate("text", label="(1.63, 90)", x=2.5, y=90) +
    scale_x_continuous(breaks = seq(0, 6.3, 0.5)) +
    xlab("Predicted euclidean distance") + ylab("Confidence score (%)") + 
    ggtitle(label="(b)") +
    grid_plot_theme + theme(legend.position="none")
  return(plot)
}

distances <- read_distances()
density <- read_density()
density <- density[density$Distance < 6.3,]
confidences <- read_confidences()
confidences <- confidences[confidences$Distance < 6.3,]

hist_plot <- make_distance_hist_plot(distances)
# hist_plot

density_plot <- make_density_plot(density)
# density_plot

predicted_distance_plot <- make_predicted_distance_plot(density, 1.5)
# # svg("predicted_distance_plot.svg", width=6, height=4)
# predicted_distance_plot
# # dev.off()

confidence_plot <- make_confidence_plot(confidences)
# # svg("confidences_plot.svg", width=4, height=4)
# confidence_plot
# # dev.off()

# # svg("combined_hist_density_plot.svg", width=6, height=10)
# hist_plot / density_plot / predicted_distance_plot
# # dev.off()

# # svg("combined_density_confidence_plot.svg", width=6, height=8)
# predicted_distance_plot / confidence_plot
# # dev.off()

# # svg("combined_hist_density_confidence_plot.svg", width=6, height=12)
# hist_plot / density_plot / predicted_distance_plot / confidence_plot
# # dev.off()
