# Copyright (C) 2017 Rafael Picanço.
#
# The present file is distributed under the terms of the GNU General Public License (GPL v3.0).
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

p_value_plot <- function(means) {
	pdf('Figure.pdf', width = 4, height = 4)

	# clean template
	plot(means, ylim= c(0.0, 1.0), xlim= c(1,27), axes= FALSE, ann= FALSE, type= 'n')

	# connected white-black dots
 	abline(h= 0.01, untf= FALSE, col= rgb(192,192,192,230, maxColorValue= 255))
	lines(means, lty= 1, lwd= 1, type= 'l')

	for (i in 1:length(means)) {
		if (means[i] <= 0.01) {
			points(i, means[i], pch= 21, bg= 'black', cex= 0.8)
		} else {
			points(i, means[i], pch=21, bg='gray', cex=0.8)
		}
	}
	

	# y
	axis(2, at= c(0.0, 0.5, 1.0), tick= TRUE, las= 2, cex.axis= 0.8)

	# x
	axis(1, at= c(1, 13, 27), tick= TRUE, las= 0, cex.axis= 0.8)

	title(
		#main= c("Mean Discriminative index"), 
		xlab= 'Trials',
		ylab= 'mean p-value',
		cex.main= 1.2, cex.lab= 1.0, font.main= 1, font.lab= 1
	)
}

standard_plot <- function(positive_means, negative_means, filen= -1) {
	if (filen == -1) {
		pdf('Figure.pdf', width= 4, height= 4)
	} else {
		png(sprintf("images/%02d.png", filen), width= 400, height= 400)
	}

	# clean template
	plot(positive_means, ylim= c(0.0, 1.0), xlim= c(1,27), axes= FALSE, ann= FALSE, type= 'n')

	# connected white-black dots
	lines(negative_means, lty= 2, lwd= 1, type= 'l')
	lines(positive_means, lty= 1, lwd= 1, type= 'l')
	points(negative_means, pch= 21, bg= 'white', cex= 0.8)
	points(positive_means, pch= 21, bg= 'black', cex= 0.8)

	# y
	axis(2, at= c(0.0, 0.5, 1.0), tick= TRUE, las= 2, cex.axis= 0.8)

	# x
	axis(1, at= c(1, 13, 27), tick= TRUE, las= 0, cex.axis= 0.8)

	title(
		#main= c("Mean Discriminative index"), 
		xlab= 'Trials',
		ylab= 'S+ button pressing proportion',
		cex.main= 1.2, cex.lab= 1.0, font.main= 1, font.lab= 1
	)
}

custom_boxplot <- function(positive_means, negative_means, filen= -1) {
	if (filen == -1) {
		pdf('Figure.pdf', width= 4, height= 4)
	} else {
		png(sprintf("images/box_%02d.png", filen), width= 400, height= 400)
	}

	# template
	boxplot(positive_means, negative_means,
		names= c("fp", "fn"), range = 0,
		ylim= c(0.0, 1.0), axes= FALSE, ann= FALSE, frame.plot= FALSE)

	# y
	axis(2, at= c(0.0, 0.5, 1.0), tick= TRUE, las= 2, cex.axis= 0.8)

	# x
	axis(1, at= c(1, 2), labels= c("fp", "fn"), col= NA, col.ticks= 1)

	title(
		#main= c("Mean Discriminative index"), 
		xlab= 'Trials',
		ylab= 'S+ button pressing proportion',
		cex.main= 1.2, cex.lab= 1.0, font.main= 1, font.lab= 1
	)
}

wilcoxon_rank_sum_test <- function(positive, negative, jittered= FALSE) {
	result <- vector()
	for (name in names(positive)) {
		if (jittered) {
			X <- jitter(positive[,name])
			Y <- jitter(negative[,name])
		} else {
			X <- positive[,name]
			Y <- negative[,name]
		}
		result = c(result, wilcox.test(
			X,
			Y,
			alternative= 'greater',
			paired= FALSE)$p.value
		)
	}
	frame <- data.frame(t(result))
	return(frame)
}

# load our data
positive <- read.table('9_intra_button_positive_relative_rate.txt', sep= ' ', na.strings= 'nan')
negative <- read.table('9_intra_button_negative_relative_rate.txt', sep= ' ', na.strings= 'nan')

# differentiation
# use_jitter <- FALSE
# if (use_jitter) {
# 	frame <- positive[FALSE,]
# 	for (i in seq(1,1000)) {
# 		frame <- rbind(frame, wilcoxon_rank_sum_test(positive, negative, use_jitter))
# 	}
# } else {
# 	frame <- wilcoxon_rank_sum_test(positive, negative)
# }
# p_value_plot(apply(frame, 2, mean))

# plot means
# positive_means <- apply(positive, 2, mean, na.rm= TRUE)
# negative_means <- apply(negative, 2, mean, na.rm= TRUE)
# standard_plot(positive_means, negative_means)


# intra-subject, compare fp and fn trials
for (i in 1:nrow(positive)) {
	positive_p <- as.numeric(positive[i, ])
	negative_p <- as.numeric(negative[i, ])
	custom_boxplot(positive_p, negative_p, i)
}