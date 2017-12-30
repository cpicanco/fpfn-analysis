# Copyright (C) 2017 Rafael Picanço.
#
# The present file is distributed under the terms of the GNU General Public License (GPL v3.0).
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

library('zoo')

load_gaze_file <- function(path, pattern='*2d_pr*', sep= '\t') {
	name = list.files(path, pattern=pattern)
	read.table(file.path(path, name), sep= sep, header=TRUE)
}


participant_path <- function(participant_number) {
	name <- sprintf('P%02d', participant_number)
	file.path(dirname(getwd()),'DATA',name)
}

load_numpy_file <- function(filename) {
	name <- file.path(getwd(), 'drawing', filename) 
	read.table(name, sep= ' ', header=TRUE)
}


standard_plot <- function(pdata, ndata, filen= -1) {
	if (filen == -1) {
		pdf('Figure.pdf', width= 4, height= 4)
	} else {
		png(sprintf("images/%02d.png", filen), width= 900, height= 400)
	}

	plot(pdata, ylim= c(.0,.4), type= 'n')


	# connected white-black dots
	lines(pdata, lty= 1, lwd= 1, type= 'l', col='black')
	lines(ndata, lty= 2, lwd= 1, type= 'l', col='red')

	# y
	# axis(2, at= c(0.0, 0.5, 1.0), tick= TRUE, las= 2, cex.axis= 0.8)

	# # x
	# axis(1, at= c(1, 13, 27), tick= TRUE, las= 0, cex.axis= 0.8)

	title(
		#main= c("Mean Discriminative index"), 
		xlab= 'Time',
		ylab= 'sd',
		cex.main= 1.2, cex.lab= 1.0, font.main= 1, font.lab= 1
	)
}
positive_frame <- load_numpy_file('positive9.txt')
negative_frame <- load_numpy_file('negative9.txt')

x <- rollapplyr(positive_frame[, 1], list(-(1000:1)), sd, fill=NA)
y <- rollapplyr(positive_frame[, 2], list(-(1000:1)), sd, fill=NA)

standard_plot(x, y, 1)