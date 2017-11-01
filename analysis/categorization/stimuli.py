import sys
sys.path.append('../../analysis')
from methods import load_ini_data
from methods import ellipse

STIMULI_COORDENATES = [
    (874, 334),
    (808, 517),
    (639, 614),
    (448, 580),
    (323, 431),
    (323, 237),
    (448, 88 ),
    (639, 54 ),
    (808, 151)]

def normalize(x_px, y_px,screen=(1280, 768)):
    return x_px/screen[0], y_px/screen[1]

class Circle(object):
    """Circle"""
    def __init__(self, left_px, top_px, width_px=100, height_px=100, do_normalize=True): 
        if do_normalize:          
            self.left, self.top = normalize(left_px, top_px) 
            self.width, self.height = normalize(width_px, height_px)
            self.radius = [self.width/2, self.height/2]
            self.center = normalize(left_px+(width_px/2), top_px+(height_px/2))
        else:
            self.left, self.top = left_px, top_px 
            self.width, self.height = width_px, height_px
            self.radius = self.width/2, self.height/2
            self.center = left_px+(width_px/2), top_px+(height_px/2)

    def points(self, factor=1.):
        return ellipse(self.center, self.radius[0]*factor, self.radius[1]*factor)

def circular_grid():
    return [Circle(x, y, do_normalize=False) for (x, y) in STIMULI_COORDENATES]  

  
def debug_window():
    from graphics import GraphWin

    win = GraphWin('Floor', 1280, 768)
    win.setBackground("black")

    for circle in circular_grid():
        for [x, y] in circle.points():
            win.plotPixel(x, y, "white")

    win.getKey()
    win.close()

if __name__ == '__main__':
    debug_window()