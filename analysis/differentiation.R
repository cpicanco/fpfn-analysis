# Copyright (C) 2017 Rafael Picanço.
#
# The present file is distributed under the terms of the GNU General Public License (GPL v3.0).
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

norm_plot <- function(data, filen= '') {
	if (filen == '') {
		pdf('Figure.pdf', width= 4, height= 4)
	} else {
		png(sprintf("images/qqnorm_%s.png", filen), width= 400, height= 400)
	}

	qqnorm(data);
	qqline(data, col = 2)	
}

resid_plot <- function(X, Y, filen= '') {
	if (filen == '') {
		pdf('Figure.pdf', width= 4, height= 4)
	} else {
		png(sprintf("images/resid_%s.png", filen), width= 800, height= 800)
	}
	par(mfrow = c(2, 2))
	plot(lm(X ~ Y))
}

p_value_plot <- function(data, filen= -1, p_value=0.001, intra_subject=FALSE) {
	if (filen == -1) {
		pdf('Figure.pdf', width= 4, height= 4)
	} else {
		png(sprintf("images/p_values_%02d.png", filen), width= 400, height= 400)
	}

	# clean template
	if (intra_subject) {
        xlabel <- 'Subjects'
        xat <- seq(1, 12)
	} else {
		xlabel <- 'Trials'
		xat <- c(1, 13, 27)
	}

	plot(data, ylim= c(0.0, 1.0), xlim= c(1, length(data)), axes= FALSE, ann= FALSE, type= 'n')
	# connected white-black dots
 	# abline(h= 0.01, untf= FALSE, col= rgb(192,192,192,230, maxColorValue= 255))
	# lines(data, lty= 1, lwd= 1, type= 'l')

	for (i in 1:length(data)) {
		if (data[i] < p_value) {
			points(i, data[i], pch= 21, bg= 'black', cex= 0.8)
		} else {
			points(i, data[i], pch=21, bg='gray', cex=0.8)
		}
	}
	

	# y
	axis(2, at= c(0.0, 0.5, 1.0), tick= TRUE, las= 2, cex.axis= 0.8)

	# x
	axis(1, at= xat, tick= TRUE, las= 0, cex.axis= 0.8)

	title(
		#main= c("Mean Discriminative index"), 
		xlab= xlabel,
		ylab= 'p-value',
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

## https://www.r-bloggers.com/side-by-side-box-plots
## -with-patterns-from-data-sets-stacked-by-reshape2-and-melt-in-r/
boxplot_comparison <- function(positive, negative) {
	# compare one by one
	# for (i in 1:nrow(positive)) { 
	# 	positive_p <- as.numeric(positive[i, ])
	# 	negative_p <- as.numeric(negative[i, ])
	# 	custom_boxplot(positive_p, negative_p, i)
	# }

	# install.packages('reshape2')
	library(reshape2)

	# format data
	data <- positive[FALSE,]
	for (row in 1:nrow(positive)) {	
		p <- positive[row,]
		n <- negative[row,]
		data <- rbind(data, n, p)
	}
	rownames(data) <- NULL

	pnames <- c(
		'P1','P1',
		'P2','P2',
		'P3','P3',
		'P4','P4',
		'P5','P5',
		'P6','P6',
		'P7','P7',
		'P8','P8',
		'P9','P9',
		'P10','P10',
		'P11','P11',
		'P12','P12')

	pgroup <- c(replicate(12, c('FP', 'FN')))

	data$pnames <- pnames
	data$pgroup <- pgroup
	data <- melt(data, id = c('pnames', 'pgroup'))
	data <- data[, -3]
	data

	# plot data
	png('box_plots.png', width= 595, height= 400)
	par(mar=c(3.5, 2.3, 3.5, 0.0)) 
	ticks <- seq(1, 24, by= 1)
	
	is.even <- function(x) x %% 2 == 0
	a <- vector()
	for (i in ticks) {
		if (is.even(i)) {
			a <- c(a, i-0.9)
		} else {
			a <- c(a, i)
		}
	}

	boxplots <- boxplot(
		value~pgroup + pnames,
		 data= data,
		 at= ticks,
		 xaxt= 'n',
		 axes= FALSE,
		 ylim= c(.0, 1.),
		 boxwex=.5,
		 col= c('white', 'gray')
		 )

	# y
	axis(side= 2, at= c(0.0, 0.5, 1.0), tick= TRUE, las= 2)

	# x
	x_labels = c(
		'FP FN\nP1',
		'FP FN\nP2',
		'FP FN\nP3',
		'FP FN\nP4',
		'FP FN\nP5',
		'FP FN\nP6',
		'FP FN\nP7',
		'FP FN\nP8',
		'FP FN\nP9',
		'FP FN\nP10',
		'FP FN\nP11',
		'FP FN\nP12')
	ticks <- seq(1, 24, by= 2)
	axis(
		side= 1,
		at= ticks+0.5,
		labels = x_labels,
		line= 0.5,
		lwd= 0,
		las= 0,
		cex.axis= 0.9
		)
	title('Comparing button-pressing proportion across participants')

	# fp, fn between groups
	# pnames <- c('P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7', 'P8', 'P9', 'P10', 'P11', 'P12')
	# pnames <- c(pnames, pnames)
	# pgroup <- c(replicate(12, 'FP'), replicate(12, 'FN'))
	# data <- data.frame(rbind(as.matrix(negative), as.matrix(positive)))
	# data$pnames <- pnames
	# data$pgroup <- pgroup
	# data <- melt(data, id = c('pnames', 'pgroup'))
	# data <- data[, -3]

	# # plot

	# ticks_a = seq(1, 6.5, by= .5)
	# ticks_b = ticks_a+7

	# png('box_plots.png')
	# boxplots <- boxplot(
	# 	value~pnames + pgroup,
	# 	 data= data,
	# 	 at= c(ticks_a, ticks_b),
	# 	 xaxt= 'n',
	# 	 ylim= c(.0, 1.),
	# 	 xlim= range(0, max(ticks_b+1)),
	# 	 boxwex=.25
	# 	 # col= c(replicate(12, 'gray'), replicate(12, 'gray'))
	# 	 )

	# axis(
	# 	side= 1,
	# 	at= c(ticks_a[6], ticks_b[6]),
	# 	labels = c('X (FN)', 'Square (FP)'),
	# 	line= 0.5,
	# 	lwd= 0
	# 	)
	# title('Comparing button-pressing proportion across participants')
	dev.off()
}


# some alternative approachs:

# Eoin (https://stats.stackexchange.com/users/42952/eoin),
# How to compare difference between two time series?,
# URL (version: 2014-07-17): https://stats.stackexchange.com/q/108323
rank_test_per_col <- function(positive, negative, jittered= FALSE, algorithm= 'kruskal') {
	result <- vector()
	for (name in names(positive)) {
		if (jittered) {
			X <- jitter(positive[,name])
			Y <- jitter(negative[,name])
		} else {
			X <- positive[,name]
			Y <- negative[,name]
		}

		# norm_plot(X, name)
		# norm_plot(Y, name)
		# resid_plot(X, Y, name)

		if (algorithm == 'kruskal') {
			result = c(result, kruskal.test(list(X, Y))$p.value)
		}

		if (algorithm == 'wincox') {
			result = c(result, wincox.test(
				X, Y,
				alternative='greater',
				paired=TRUE)$p.value)			
		}

		if (algorithm == 'mann-whitney') {
			result = c(result, wincox.test(
				X, Y,
				alternative='greater',
				paired=FALSE)$p.value)			
		}

		if (result[length(result)]  > 1.0) {
			result[length(result)] <- 1.0
		}
	} 
	return(data.frame(t(result)))
}

rank_test_per_row <- function (positive, negative, jittered=FALSE, algorithm= 'friedman') {
	result <- vector()
	for (row in 1:nrow(positive)) {
		if (jittered) {
			X <- jitter(positive[row,])
			Y <- jitter(negative[row,])
		} else {
			X <- positive[row,]
			Y <- negative[row,]
		}

		if (algorithm == 'friedman') {
			result = c(result, friedman.test(matrix(c(X, Y), ncol=2))$p.value)
			result
		} 
	} 
	return(data.frame(t(result)))
}

# load data
positive <- read.table('9_intra_button_positive_relative_rate.txt', sep= ' ', na.strings= 'nan')
negative <- read.table('9_intra_button_negative_relative_rate.txt', sep= ' ', na.strings= 'nan')

# differentiation
# use_jitter <- FALSE
# if (use_jitter) {
# 	frame <- positive[FALSE,]
# 	for (i in seq(1,1000)) {
# 		frame <- rbind(frame, rank_test_per_col(positive, negative, use_jitter))
# 	}
# } else {
# 	frame <- rank_test_per_col(positive, negative)
# }
# p_value_plot(apply(frame, 2, mean), 1, p_value=0.005)

# plot means
# positive_means <- apply(positive, 2, mean, na.rm= TRUE)
# negative_means <- apply(negative, 2, mean, na.rm= TRUE)
# standard_plot(positive_means, negative_means,1)

boxplot_comparison(positive, negative)

# # differentiation intra-subject
# frame = rank_test_per_row(positive, negative)
# p_value_plot(as.numeric(frame[1,]), 1, p_value=0.001, intra_subject= TRUE)