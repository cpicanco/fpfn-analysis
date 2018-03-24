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
	print(shapiro.test(data))
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
		xtitle <- 'friedman'
        xlabel <- 'Subjects'
        xat <- seq(1, 12)
	} else {
		xtitle <- 'rank test'
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
		main= xtitle, 
		xlab= xlabel,
		ylab= 'p-value',
		cex.main= 1.2, cex.lab= 1.0, font.main= 1, font.lab= 1
	)

	if (p_value <= 0.005) {
		s1 <- sprintf("p < %.03f", p_value)
		s2 <- sprintf("p >= %.03f", p_value)
	} else {
		s1 <- sprintf("p < %.02f", p_value)
		s2 <- sprintf("p >= %.02f", p_value)
	}
	legend(0.8, 1., legend=c(s1, s2),
       col=c("black", "gray"), pch=c(16, 16))
}

standard_plot <- function(pdata, ndata, filen= -1, ylim= c(0.0, 1.0)) {
	if (filen == -1) {
		pdf('Figure.pdf', width= 4, height= 4)
	} else {
		png(sprintf("images/%02d.png", filen), width= 400, height= 400)
	}

	# clean template
	plot(pdata, ylim= ylim, xlim= c(1,27), axes= FALSE, ann= FALSE, type= 'n')

	# connected white-black dots
	lines(ndata, lty= 2, lwd= 1, type= 'l')
	lines(pdata, lty= 1, lwd= 1, type= 'l')
	points(ndata, pch= 21, bg= 'white', cex= 0.8)
	points(pdata, pch= 21, bg= 'black', cex= 0.8)

	# # fit
	# x <- seq(1,27)
	# pmodel <- lm(pdata~poly(x,6,raw=TRUE))
	# nmodel <- lm(ndata~poly(x,5,raw=TRUE))
	# nmodel2 <- lm(ndata~poly(x,2,raw=TRUE))
	# print(anova(nmodel, nmodel2))

	# lines(x, predict(pmodel, data.frame(x= x)), col= 'black')
	# lines(x, predict(nmodel, data.frame(x= x)), col= 'gray')

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

custom_boxplot <- function(pdata, ndata, filen= -1) {
	if (filen == -1) {
		pdf('Figure.pdf', width= 4, height= 4)
	} else {
		png(sprintf("images/box_%02d.png", filen), width= 400, height= 400)
	}

	# template
	boxplot(pdata, ndata,
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

boxplot_comparison <- function(pdata, ndata) {
	# format data
	for (row in 1:nrow(pdata)) {	
		p <- pdata[row,]
		n <- ndata[row,]
		custom_boxplot(as.numeric(p), as.numeric(n), row)
	}

	pp1 <- as.numeric(pdata[1,])
	np1 <- as.numeric(ndata[1,])
	pp2 <- as.numeric(pdata[2,])
	np2 <- as.numeric(ndata[2,])
	pp3 <- as.numeric(pdata[3,])
	np3 <- as.numeric(ndata[3,])
	pp4 <- as.numeric(pdata[4,])
	np4 <- as.numeric(ndata[4,])
	pp5 <- as.numeric(pdata[5,])
	np5 <- as.numeric(ndata[5,])
	pp6 <- as.numeric(pdata[6,])
	np6 <- as.numeric(ndata[6,])
	pp7 <- as.numeric(pdata[7,])
	np7 <- as.numeric(ndata[7,])
	pp8 <- as.numeric(pdata[8,])
	np8 <- as.numeric(ndata[8,])
	pp9 <- as.numeric(pdata[9,])
	np9 <- as.numeric(ndata[9,])
	pp10 <- as.numeric(pdata[10,])
	np10 <- as.numeric(ndata[10,])
	pp11 <- as.numeric(pdata[11,])
	np11 <- as.numeric(ndata[11,])
	pp12 <- as.numeric(pdata[12,])
	np12 <- as.numeric(ndata[12,])

	# plot data
	png('box_plots.png', width= 595, height= 400)
	par(mar=c(3.5, 2.3, 3.5, 0.0)) 
	ticks <- seq(1, 24, by= 1)

	boxplots <- boxplot(
		pp1,np1,
		pp2,np2,
		pp3,np3,
		pp4,np4,
		pp5,np5,
		pp6,np6,
		pp7,np7,
		pp8,np8,
		pp9,np9,
		pp10,np10,
		pp11,np11,
		pp12,np12,		
		range= 0,
		xaxt= 'n',
		axes= FALSE,
		ylim= c(.0, 1.),
		boxwex=.5,
		col= c('white', 'gray'),
		frame.plot= FALSE
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
	dev.off()
}


# some alternative approachs:
# Eoin (https://stats.stackexchange.com/users/42952/eoin),
# How to compare difference between two time series?,
# URL (version: 2014-07-17): https://stats.stackexchange.com/q/108323
test_per_col <- function(positive, negative, jittered= FALSE, algorithm= 'kruskal') {
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

		if (algorithm == 'student') { # jittered results equivalent to single kruskal
			test <- t.test(X, Y, alternative='two.sided')
			result = c(result, test$p.value)
			# print(test)
		}

		if (result[length(result)]  > 1.0) {
			result[length(result)] <- 1.0
		}
	} 
	return(data.frame(t(result)))
}

rank_test_per_row <- function (positive, negative,
  jittered=FALSE, algorithm= 'friedman', output='pvalue') {
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
			test <- friedman.test(matrix(c(X, Y), ncol=2))
			print(test)
			if (output == 'pvalue') {
				result = c(result, test$p.value)
			}
			
			if (output == 'stats') {
				result = c(result, test$statistic)
			}	
		}
	} 
	return(data.frame(t(result)))
}

test_per_row <- function (positive, negative, experiment_name) {
	positive_result <- vector()
	negative_result <- vector()
	positive_mu <- vector()
	negative_mu <- vector()
	trials <- 1:27
	for (row in 1:nrow(positive)) {
		X <- as.numeric(positive[row,])
		Y <- as.numeric(negative[row,])

		# a participant from the feature positive group
		testp <- cor.test(X, trials, method='kendall')
		testp_mu <- mean(X)

		# a participant from the feature negative group
		testn <- cor.test(Y, trials, method='kendall')
		testn_mu <- mean(Y)

		# concatenate kendall estimates
		positive_result <- c(positive_result, unname(testp$estimate))
		negative_result <- c(negative_result, unname(testn$estimate))

		# concatenate averages
		positive_mu <- c(positive_mu, testp_mu)
		negative_mu <- c(negative_mu, testn_mu)
	}
	print(experiment_name)

	png(sprintf("images/%s_positive.png", experiment_name), width= 400, height= 400)
	plot(positive_result, ylim=c(-1, 1))
	title(sprintf("positive_%s", experiment_name))
	dev.off()

	png(sprintf("images/%s_negative.png", experiment_name), width= 400, height= 400)
	plot(negative_result, ylim=c(-1, 1))
	title(sprintf("negative_%s", experiment_name))
	dev.off()

	# participant's performances improved along time?
	print('Performance improvement')
	print(t.test(c(negative_result, positive_result), mu=0)$p.value)

	# participant's performances were different along time?
	print('Difference along time')
	print(t.test(negative_result, positive_result)$p.value)

	# participant's average performance was different?
	print('Average difference')
	print(t.test(negative_mu, positive_mu)$p.value)
	print('--------------------')
}

# load data
positive <- read.table('90_button_positive_relative_rate.txt', sep= ' ', na.strings= 'nan')
negative <- read.table('90_button_negative_relative_rate.txt', sep= ' ', na.strings= 'nan')
test_per_row(positive, negative, "90_button")

positive <- read.table('90_looking_positive_relative_rate.txt', sep= ' ', na.strings= 'nan')
negative <- read.table('90_looking_negative_relative_rate.txt', sep= ' ', na.strings= 'nan')
test_per_row(positive, negative, "90_looking")

positive <- read.table('90_latency_positive_relative_rate.txt', sep= ' ', na.strings= 'nan')
negative <- read.table('90_latency_negative_relative_rate.txt', sep= ' ', na.strings= 'nan')
test_per_row(positive, negative, "90_latency")

positive <- read.table('9_button_positive_relative_rate.txt', sep= ' ', na.strings= 'nan')
negative <- read.table('9_button_negative_relative_rate.txt', sep= ' ', na.strings= 'nan')
test_per_row(positive, negative, "9_button")

positive <- read.table('9_looking_positive_relative_rate.txt', sep= ' ', na.strings= 'nan')
negative <- read.table('9_looking_negative_relative_rate.txt', sep= ' ', na.strings= 'nan')
test_per_row(positive, negative, "9_looking")

positive <- read.table('9_latency_positive_relative_rate.txt', sep= ' ', na.strings= 'nan')
negative <- read.table('9_latency_negative_relative_rate.txt', sep= ' ', na.strings= 'nan')
test_per_row(positive, negative, "9_latency")

# differentiation
# use_jitter <- FALSE
# if (use_jitter) {
# 	frame <- positive[FALSE,]
# 	for (i in seq(1,1000)) {
# 		frame <- rbind(frame, test_per_col(positive, negative, use_jitter))
# 	}
# } else {
# 	frame <- test_per_col(positive, negative)
# }
# p_value_plot(apply(frame, 2, mean), 1, p_value=0.005)

# overall comparison
# data_positive <- as.vector(t(positive)) 
# data_negative <- as.vector(t(negative))
# resid_plot(data_positive, data_negative, 1)

# # sudo apt-get install libnlopt-dev
# # install.packages('car', dependencies = TRUE)
# library('car')
# data <- c(data_positive, data_negative)
# groups <- c(rep('posi', 270), rep('nega', 270))
# frame <- data.frame(data, groups)

# one should ensure homogeneity a priori
# we couldn't so here we are just checking 
# # Brown-Forsythe test for homogeneity of variance, assumes normally distributed data
# # leveneTest(data~groups, data=frame, center=median)

# # Levene's test
# # leveneTest(data~groups, data=frame, center=mean)

# # Fligner-Killeen test for homogeneity of variance, does not assumes distributed data
# fligner.test(data~groups, data=frame)

# t.test(data_positive, data_negative)

# # plot means
# positive_measure <- apply(positive, 2, mean)
# negative_measure <- apply(negative, 2, mean)

# norm_plot(positive_measure, 1)
# norm_plot(negative_measure, 2)
# standard_plot(positive_measure, negative_measure, 1)
# resid_plot(positive_measure, negative_measure, 5)
# # # differentiation intra-subject
# boxplot_comparison(positive, negative)
# frame = rank_test_per_row(positive, negative)
# p_value_plot(as.numeric(frame[1,]), 1, p_value=0.005, intra_subject= TRUE)