import sys
import numpy as np
import colorsys
import random


def get_colors(num_colors):
    colors = []
    for i in np.arange(0., 360., 360. / num_colors):
        hue = i/360.
        lightness = (30 + np.random.rand() * 30)/100.
        saturation = (50 + np.random.rand() * 50)/100.
        colors.append(colorsys.hls_to_rgb(hue, lightness, saturation))
    return colors

num_colors = int(sys.argv[1])
colors = get_colors(num_colors)
random.shuffle(colors)
for i in range(len(colors)):
    r, g, b = colors[i]
    print("set style line %d lc rgb '#%02x%02x%02x'" % (i+1, r*255, g*255, b*255))
