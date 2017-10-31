
from methods import ellipse

STIMULI = [
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
    def __init__(self, left_px, top_px, width_px=100, height_px=100):           
        self.left, self.top = normalize(left_px, top_px) 
        self.width, self.height = normalize(width_px, height_px)
        self.radius = [self.width/2, self.height/2]
        self.center = normalize(left_px+(width_px/2), top_px+(height_px/2))

    def Points(self, factor=1.):
        return ellipse(self.center, self.radius[0]*factor, self.radius[1]*factor)