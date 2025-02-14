import json
import sys

sys.path.append("..")

import numpy as np
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt

import faiss


def load_vector_store_visualization(path):
    index = faiss.read_index(f"{path}/index.faiss")

    num_vectors = index.ntotal
    d = index.d

    vectors = np.zeros((num_vectors, d), dtype=np.float32)
    for i in range(num_vectors):
        vectors[i, :] = index.reconstruct(i)


    print(f"Get {num_vectors} vectors, dimension {d}")

    # dimensionality reduction from d to 2
    tsne = TSNE(n_components=2, random_state=42, perplexity=10)
    vectors_2d = tsne.fit_transform(vectors)

    all_ingredients = json.load(open("./data/all_ingredients.json"))["data"]
    # plot

    plt.figure(figsize=(10, 6))
    plt.scatter(vectors_2d[:, 0], vectors_2d[:, 1], alpha=0.7)
    for i, label in enumerate(all_ingredients):
        plt.text(vectors_2d[i, 0], vectors_2d[i, 1], label)
    plt.title("t-SNE visualization")
    plt.xlabel("Dimension 1")
    plt.ylabel("Dimension 2")

    plt.show()




if __name__ == "__main__":
    # load_vector_store_visualization("./data/vector1")
    load_vector_store_visualization("./data/vector2")
    # load_vector_store_visualization("./data/vector3")