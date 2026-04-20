import os
import random
import numpy as np
import pandas as pd
from tqdm import tqdm
import glob
import re
from sklearn.preprocessing import normalize
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt
from PIL import Image

import tensorflow as tf

#Root folder where the img/ is locatd
IMAGE_ROOT = r"C:\Users\Wanna\Desktop\Fashion FYP\img"




EMBEDDINGS_DIR = r"C:\Users\Wanna\Desktop\Fashion FYP\embeddings"



def load_embeddings(): 
    global all_embeddings, all_image_paths, path_to_embedding_index

    embedding_files = glob.glob(os.path.join(EMBEDDINGS_DIR, "embeddings_batch_*.npy"))

    #Extract batch numbers
    batch_pattern = re.compile(r"embeddings_batch_(\d+)\.npy")

    batches = {}

    for file in embedding_files:
        match = batch_pattern.search(os.path.basename(file))
        if match:
            batch_num = int(match.group(1))
            batches[batch_num] = file

    #Step 2: Load in correct numeric order
    all_embeddings = []
    all_image_paths = []

    for batch_num in sorted(batches.keys()):
        emb_file = batches[batch_num]
        path_file = os.path.join(
            EMBEDDINGS_DIR,
            f"image_paths_batch_{batch_num:02d}.npy"
        )

        if not os.path.exists(path_file):
            raise FileNotFoundError(f"Missing path file for batch {batch_num}")

        emb = np.load(emb_file)
        paths = np.load(path_file)

        if len(emb) != len(paths):
            raise ValueError(f"Mismatch in batch {batch_num}: embeddings vs paths length")

        all_embeddings.append(emb)
        all_image_paths.append(paths)

    #Step 3: Concatenate
    all_embeddings = np.vstack(all_embeddings)
    all_image_paths = np.concatenate(all_image_paths)

    print("Total embeddings:", all_embeddings.shape)
    print("Total image paths:", all_image_paths.shape)


    print("Lookup dictionary built.")


    all_embeddings = all_embeddings.astype(np.float32)
    all_embeddings = all_embeddings / np.linalg.norm(all_embeddings, axis=1, keepdims=True)


    path_to_embedding_index = {
        path: idx for idx, path in enumerate(all_image_paths)
    }

    print("Embeddings loaded. ")

CURATED_PATH = r"C:\Users\Wanna\Desktop\Fashion FYP\notebooks\curated_annotations.csv"
curated_df = pd.read_csv(CURATED_PATH)


def show_image(img_path, title=None):
    plt.figure(figsize=(3, 3))
    img = Image.open(os.path.join(IMAGE_ROOT, img_path))
    plt.imshow(img)
    if title:
        plt.title(title)
    plt.axis("off")
    plt.show()


def query_by_image_path_results(query_path, top_k=5):

    if query_path not in path_to_embedding_index:
        return []

    query_idx = path_to_embedding_index[query_path]

    query_embedding = all_embeddings[query_idx]

    similarities = np.dot(all_embeddings, query_embedding)

    top_indices = similarities.argsort()[::-1][1:top_k+1]

    return [all_image_paths[idx] for idx in top_indices]


def query_by_annotation(gender=None, Weather=None, Context=None, top_k=3, n_queries=3):

    filtered_df = curated_df.copy()

    if gender:
        filtered_df = filtered_df[filtered_df["gender"] == gender]

    if Weather:
        filtered_df = filtered_df[filtered_df["Weather"] == Weather]

    if Context:
        filtered_df = filtered_df[filtered_df["Context"] == Context]

    if filtered_df.empty:
        print("No matching items.")
        return

    candidate_paths = filtered_df["image_path"].tolist()

    if len(candidate_paths) < n_queries:
        print("Not enough images to sample multiple queries.")
        n_queries = len(candidate_paths)


    selected_queries = random.sample(candidate_paths, n_queries)

    results ={}

    print(f"\nShowing {n_queries} random queries for:")
    print(f"Gender={gender}, Weather={Weather}, Context={Context}\n")

    for query_path in selected_queries:
        
        results[query_path] = query_by_image_path_results(query_path, top_k=top_k)
    
    return results


load_embeddings()

