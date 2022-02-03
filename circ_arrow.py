import numpy as np
def circarrowdraw(ax,x0, y0, radius=1, aspect=1, direction=270, closingangle=-330,
                  arrowheadrelativesize=0.3, arrowheadopenangle=30, *args,**kwargs):
    """
    Circular arrow drawing. x0 and y0 are the anchor points.
    direction gives the angle of the circle center relative to the anchor
    in degrees. closingangle indicates how much of the circle is drawn
    in degrees with positive being counterclockwise and negative being
    clockwise. aspect is important to make the aspect of the arrow 
    fit the current figure.
    """

    xc = x0 + radius * np.cos(direction * np.pi / 180)
    yc = y0 + aspect * radius * np.sin(direction * np.pi / 180)

    headcorrectionangle = 5

    if closingangle < 0:
        step = -1
    else:
        step = 1
    x = [xc + radius * np.cos((ang + 180 + direction) * np.pi / 180)
         for ang in np.arange(0, closingangle, step)]
    y = [yc + aspect * radius * np.sin((ang + 180 + direction) * np.pi / 180)
         for ang in np.arange(0, closingangle, step)]

    ax.plot(x, y, *args,**kwargs)

    xlast = x[-1]
    ylast = y[-1]

    l = radius * arrowheadrelativesize

    headangle = (direction + closingangle + (90 - headcorrectionangle) *
                 np.sign(closingangle))

    x = [xlast +
         l * np.cos((headangle + arrowheadopenangle) * np.pi / 180),
         xlast,
         xlast +
         l * np.cos((headangle - arrowheadopenangle) * np.pi / 180)]
    y = [ylast +
         aspect * l * np.sin((headangle + arrowheadopenangle) * np.pi / 180),
         ylast,
         ylast +
         aspect * l * np.sin((headangle - arrowheadopenangle) * np.pi / 180)]

    ax.plot(x, y, *args,**kwargs)