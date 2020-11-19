# %%
import matplotlib.pyplot as plt
# %%
import numpy as np
# %%
x = np.linspace(0,10,10)
# %%
plt.ion()
from time import sleep 

fig,ax = plt.subplots(1,1)
line, = ax.plot([],[])

for i in range(len(x)):
    sleep(1)
    print(i)
    line.set_data(x[:i],np.sin(x[:i]))
    fig.draw_idle()