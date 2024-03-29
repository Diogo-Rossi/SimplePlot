# File: ScrollTest.py
# coding: ASCII
"""
Interatively zoom plots together, but permit them to scroll independently.
"""
from matplotlib import pyplot
import sys

def _get_limits( ax ):
    """ Return X and Y limits for the passed axis as [[xlow,xhigh],[ylow,yhigh]]
    """
    return [list(ax.get_xlim()), list(ax.get_ylim())]

def _set_limits( ax, lims ):
    """ Set X and Y limits for the passed axis
    """
    ax.set_xlim(*(lims[0]))
    ax.set_ylim(*(lims[1]))
    return

def pre_zoom( fig ):
    """ Initialize history used by the re_zoom() event handler.
        Call this after plots are configured and before pyplot.show().
    """
    global oxy
    oxy = [_get_limits(ax) for ax in fig.axes]
    # :TODO: Intercept the toolbar Home, Back and Forward buttons.
    return

def re_zoom(event):
    """ Pyplot event handler to zoom all plots together, but permit them to
        scroll independently.  Created to support eyeball correlation.
        Use with 'motion_notify_event' and 'button_release_event'.
    """
    global oxy
    for ax in event.canvas.figure.axes:
        navmode = ax.get_navigate_mode()
        if navmode is not None:
            break
    scrolling = (event.button == 1) and (navmode == "PAN")
    if scrolling:                   # Update history (independent of event type)
        oxy = [_get_limits(ax) for ax in event.canvas.figure.axes]
        return
    if event.name != 'button_release_event':    # Nothing to do!
        return
    # We have a non-scroll 'button_release_event': Were we zooming?
    zooming = (navmode == "ZOOM") or ((event.button == 3) and (navmode == "PAN"))
    if not zooming:                 # Nothing to do!
        oxy = [_get_limits(ax) for ax in event.canvas.figure.axes]  # To be safe
        return
    # We were zooming, but did anything change?  Check for zoom activity.
    changed = None
    zoom = [[0.0,0.0],[0.0,0.0]]    # Zoom from each end of axis (2 values per axis)
    for i, ax in enumerate(event.canvas.figure.axes): # Get the axes
        # Find the plot that changed
        nxy = _get_limits(ax)
        if (oxy[i] != nxy):         # This plot has changed
            changed = i
            # Calculate zoom factors
            for j in [0,1]:         # Iterate over x and y for each axis
                # Indexing: nxy[x/y axis][lo/hi limit]
                #           oxy[plot #][x/y axis][lo/hi limit]
                width = oxy[i][j][1] - oxy[i][j][0]
                # Determine new axis scale factors in a way that correctly
                # handles simultaneous zoom + scroll: Zoom from each end.
                zoom[j] = [(nxy[j][0] - oxy[i][j][0]) / width,  # lo-end zoom
                           (oxy[i][j][1] - nxy[j][1]) / width]  # hi-end zoom
            break                   # No need to look at other axes
    if changed is not None:
        for i, ax in enumerate(event.canvas.figure.axes): # change the scale
            if i == changed:
                continue
            for j in [0,1]:
                width = oxy[i][j][1] - oxy[i][j][0]
                nxy[j] = [oxy[i][j][0] + (width*zoom[j][0]),
                          oxy[i][j][1] - (width*zoom[j][1])]
            _set_limits(ax, nxy)
        event.canvas.draw()         # re-draw the canvas (if required)
        pre_zoom(event.canvas.figure)   # Update history
    return
# End re_zoom()

def main(argv):
    """ Test/demo code for re_zoom() event handler.
    """
    import numpy
    x = numpy.linspace(0,100,1000)      # Create test data
    y = numpy.sin(x)*(1+x)

    fig = pyplot.figure()               # Create plot
    ax1 = pyplot.subplot(211)
    ax1.plot(x,y)
    ax2 = pyplot.subplot(212)
    ax2.plot(x,y)

    pre_zoom( fig )                     # Prepare plot event handler
    pyplot.connect('motion_notify_event', re_zoom)  # for right-click pan/zoom
    pyplot.connect('button_release_event',re_zoom)  # for rectangle-select zoom

    pyplot.show()                       # Show plot and interact with user
# End main()

if __name__ == "__main__":
    # Script is being executed from the command line (not imported)
    main(sys.argv)

# End of file ScrollTest.py