# %%
# region: Celula 1

import matplotlib
matplotlib.use("Qt5Agg")
import matplotlib.pyplot as plt
import numpy as np

import matplotlib.style as mplstyle
mplstyle.use(['fast'])

x = np.linspace(5000,6000,1000)
y = np.sin(x/5)

# plt.ion()
i = 1
fff, ax = plt.subplots(2,7,sharey=True,tight_layout=True)
# ax = [ax]
for ex in ax.reshape((2*7,)):
    ex.plot(np.sin(i*x**i/5),x)
    i += 1
    ex.set_ylim([5300,5400])
    ex.invert_yaxis()

# endregion

# %%

def logscroll(event):
    # print(event)
    # print("====================================")
    ylim = ax[0,0].get_ylim()
    step = -5 if event.button == "up" else 5
    ax[0,0].set_ylim([ylim[0]+step,ylim[1]+step])
    fff.canvas.draw()
    print("teste")
    # print(ylim)
    # print("====================================")
    # print(type(event.button))
    # print("====================================")
    # for ex in ax:
    #     ex.set_ylim([ylim[0]+step,ylim[1]+step])
    #     fff.canvas.draw()

fff.canvas.mpl_connect("scroll_event",logscroll)
fff.canvas.draw()

plt.show()