# Copyright (C) 2017 Rafael Picanço.
#
# The present file is distributed under the terms of the GNU General Public License (GPL v3.0).
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

p_value_plot <- function(means) {
	pdf("Figure.pdf", width = 4, height = 4)

	# clean template
	plot(means,ylim=c(0.0, 1.0), xlim= c(1,27), axes = FALSE, ann = FALSE, type = 'n')

	# connected white-black dots
 	abline(h = 0.01, untf = FALSE, col=rgb(192,192,192,230,maxColorValue = 255))
	lines(means, lty= 1, lwd= 1, type = 'l')
	points(means, pch= 21, bg= "black", cex= 0.8)

	# y
	axis(2, at=c(0.0, 0.5, 1.0), tick=TRUE, las=2, cex.axis=0.8)

	# x
	axis(1, at=c(1, 13, 27), tick = TRUE, las=0, cex.axis=0.8)

	title(
	  #main = c("Mean Discriminative index"), 
	  xlab = "Trials",
	  ylab = "mean p-value",
	  cex.main = 1.2, cex.lab = 1.0, font.main = 1, font.lab = 1
	)
}



standard_plot <- function(positive_means, negative_means) {
	pdf("Figure.pdf", width = 4, height = 4)

	# clean template
	plot(positive_means,ylim=c(0.0, 1.0), xlim= c(1,27), axes = FALSE, ann = FALSE, type = 'n')

	# connected white-black dots
	lines(negative_means, lty= 2, lwd= 1, type = 'l')
	lines(positive_means, lty= 1, lwd= 1, type = 'l')
	points(negative_means, pch= 21, bg= "white", cex= 0.8)
	points(positive_means, pch= 21, bg= "black", cex= 0.8)

	# y
	axis(2, at=c(0.0, 0.5, 1.0), tick=TRUE, las=2, cex.axis=0.8)

	# x
	axis(1, at=c(1, 13, 27), tick = TRUE, las=0, cex.axis=0.8)

	title(
	  #main = c("Mean Discriminative index"), 
	  xlab = "Trials",
	  ylab = "S+ button pressing proportion",
	  cex.main = 1.2, cex.lab = 1.0, font.main = 1, font.lab = 1
	)
}

jittered_wilcox_rank_sum_test <- function(positive, negative) {
	result <- vector()
	for (name in names(positive)) {
		result = c(result, wilcox.test(
			positive[,name],
			negative[,name],
			alternative="g",
			paired=FALSE)$p.value
		)
	}
	frame <- data.frame(t(result))
	return(frame)
}

# load our data
positive <- read.table('9_latency_positive_relative_rate.txt', sep = ' ', na.strings = 'nan')
negative <- read.table('9_latency_negative_relative_rate.txt', sep = ' ', na.strings = 'nan')


# frame <- positive[FALSE,]
# for (i in seq(1,10)) {
# 	frame <- rbind(frame, jittered_wilcox_rank_sum_test(positive, negative))
# }

p_value_plot(apply(jittered_wilcox_rank_sum_test(positive, negative), 2, mean, na.rm = TRUE))

# plot means
# positive_means <- apply(positive, 2, mean, na.rm = TRUE)
# negative_means <- apply(negative, 2, mean, na.rm = TRUE)
# standard_plot(positive_means, negative_means)