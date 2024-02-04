#%%
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import networkx as nx

G = nx.dodecahedral_graph()
nx.draw(G)  # networkx draw()
plt.show()  # pyplot draw()