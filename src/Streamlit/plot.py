"""
This file implements the function to generate embedding graph.
"""
import numpy as np
from matplotlib import pyplot as plt
from sklearn.manifold import TSNE

def plot_embeddings_graph(embeddings):
    embeddings_array = np.array(embeddings)  # Convert to NumPy array
    tsne = TSNE(random_state=1, n_iter=15000, metric="cosine", n_components=3, perplexity=30)
    embs = tsne.fit_transform(embeddings_array)

    FS = (10, 8)
    fig = plt.figure(figsize=FS)
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(embs[:, 0], embs[:, 1], embs[:, 2], alpha=.1)

    return fig

