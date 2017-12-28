# Copyright (C) 2017 Rafael Picanço.
#
# The present file is distributed under the terms of the GNU General Public License (GPL v3.0).
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

load_gaze_file <- function(path, pattern='*3d_pr*') {
	name = list.files(path, pattern=pattern)
	read.table(file.path(path, name), sep= '\t', header=TRUE)
}


participant_path <- function(participant_number) {
	name <- sprintf('P%02d', participant_number)
	file.path(dirname(getwd()),'DATA',name)
}

frame <- load_gaze_file(participant_path(1))

var(frame[, 'x_norm'], frame[, 'y_norm']) 