import json
import sys

sys.path.append("..")

import plotly.express as px
import numpy as np
import pandas as pd
from sklearn.manifold import TSNE
# import matplotlib.pyplot as plt
# import seaborn as sns

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
    tsne = TSNE(n_components=3, random_state=42, perplexity=10)
    vectors_3d = tsne.fit_transform(vectors)

    labels = json.load(open(f"{path}/all_drinks.json"))["data"]
    print(f"原始標籤數量: {len(labels)}")  
    print(f"t-SNE 降維後的 shape: {vectors_3d.shape}")


    df = pd.DataFrame(vectors_3d, columns=["x", "y", "z"])
    df["label"] = labels
    fig = px.scatter_3d(df, x="x", y="y", z="z", color="label", title="t-SNE visualization")

    fig.show()

    # color
    # palette = sns.color_palette("husl", len(all_ingredients))
    # label_to_color = {label: palette[i] for i, label in enumerate(all_ingredients)}

    # # draw 3d t-sne

    # fig = plt.figure(figsize=(10, 7))
    # ax = fig.add_subplot(111, projection='3d')
    
    # for i, label in enumerate(all_ingredients):
    #     x, y, z = vectors_3d[i, 0], vectors_3d[i, 1], vectors_3d[i, 2]
    #     ax.scatter(x, y, z, color=label_to_color[label], label=label if label not in label_to_color else "")
    
    # # 
    # handles = [plt.Line2D([], [0], marker='o', color='w', label=label, markerfacecolor=label_to_color[label], markersize=8) for label in all_ingredients]
    # ax.legend(handles, all_ingredients, title="Ingredient", bbox_to_anchor=(1.05, 1), loc="upper left")

    # ax.set_title("3D t-SNE visualization of FAISS vectors")
    # ax.set_xlabel("t-SNE Dimension 1")
    # ax.set_ylabel("t-SNE Dimension 2")
    # ax.set_zlabel("t-SNE Dimension 3")
    # plt.show()

    # draw 2d
    # plt.figure(figsize=(10, 6))
    # plt.scatter(vectors_2d[:, 0], vectors_2d[:, 1], alpha=0.7)
    # for i, label in enumerate(all_ingredients):
    #     plt.text(vectors_2d[i, 0], vectors_2d[i, 1], label)
    # plt.title("t-SNE visualization")
    # plt.xlabel("Dimension 1")
    # plt.ylabel("Dimension 2")

    # plt.show()




if __name__ == "__main__":
    # load_vector_store_visualization("./data/vector1")
    # load_vector_store_visualization("./data/vector2")
    load_vector_store_visualization("./data/vector3")