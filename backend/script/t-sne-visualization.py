import json
import sys

sys.path.append("../app")

import plotly.express as px
import numpy as np
import pandas as pd
from sklearn.manifold import TSNE

# from pinecone import Pinecone
# from configs.settings import setting
from configs.settings import settings
# import matplotlib.pyplot as plt
# import seaborn as sns

import faiss


def load_faiss_visualization(path):
    index = faiss.read_index(f"{path}/index.faiss")

    num_vectors = index.ntotal
    d = index.d

    vectors = np.zeros((num_vectors, d), dtype=np.float32)
    for i in range(num_vectors):
        vectors[i, :] = index.reconstruct(i)
    analyze_vector_and_show_chart(vectors, d, path)


def analyze_vector_and_show_chart(vectors, d, path):
    print(f"Get {len(vectors)} vectors, dimension {d}")

    # dimensionality reduction from d to 2
    tsne = TSNE(n_components=3, random_state=42, perplexity=10)
    vectors_3d = tsne.fit_transform(vectors)

    labels = json.load(open(f"{path}/all_drinks.json"))["data"]
    print(f"原始標籤數量: {len(labels)}")
    print(f"t-SNE 降維後的 shape: {vectors_3d.shape}")

    df = pd.DataFrame(vectors_3d, columns=["x", "y", "z"])
    df["label"] = labels
    fig = px.scatter_3d(
        df, x="x", y="y", z="z", color="label", title="t-SNE visualization"
    )

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


def load_pinecone_visualization(path):
    # pc = Pinecone(api_key=settings.PINECONE_API_KEY)
    # index = pc.Index("pinecone-index")

    # # 取得所有向量 ID（假設 Pinecone 存了 10,000 筆向量）
    # vector_ids = [ids for ids in index.list()]
    # # 批次獲取向量
    # vectors = []
    # labels = []
    # batch_size = 100  # 每次取 20 筆
    # vector_ids = vector_ids[0:batch_size]
    # for ids in vector_ids:
    #     response = index.fetch(ids)

    #     for key, value in response["vectors"].items():
    #         vectors.append(value["values"])  # 取得向量值
    #         labels.append(key)  # 取得向量的 ID 或標籤（可能是飲料名稱）

    # json.dump(vectors, open('../data/pinecone-data.json', 'w'))
    vectors = json.load(open("../data/pinecone-data.json", "r"))
    d = len(vectors[0])
    vectors = np.array(vectors)  # 轉成 numpy 格式
    analyze_vector_and_show_chart(vectors, d, path)


def load_vector_store_visualization(path):
    if settings.VECTOR_STORE_TYPE == "faiss":
        load_faiss_visualization(path)
    elif settings.VECTOR_STORE_TYPE == "pinecone":
        load_pinecone_visualization("../data/v1/vector2")


if __name__ == "__main__":
    # load_vector_store_visualization("../data/v1/vector1")
    load_vector_store_visualization("../data/v1/vector2")
    # load_vector_store_visualization("../data/v1/vector3")
