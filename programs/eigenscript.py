import os
import chromadb
import numpy as np
from sklearn.decomposition import PCA

# --- 1. SET UP LOCAL ACCESS ---
DB_PATH = os.path.expanduser("~/chroma_db")

def run_local_audit():
    print(f"📡 Connecting to local database at {DB_PATH}...")

    # Use PersistentClient to talk directly to the SSD
    client = chromadb.PersistentClient(path=DB_PATH)

    try:
        # Get your Data Science collection
        collection = client.get_collection("datascience_study")

        # 2. EXTRACT DATA
        # We need embeddings for the math and documents for the context
        data = collection.get(include=['embeddings', 'metadatas', 'documents'])

        # THE FIX: We use len() to check if the list is empty.
        # Python handles the 'truth' of an integer (0 vs >0) without ambiguity.
        if data['embeddings'] is None or len(data['embeddings']) == 0:
            print("❌ No embeddings found. Check if the ingestion script is finished or writing to this path.")
            return

        embeddings = np.array(data['embeddings'])
        documents = data['documents']

        # 3. PCA MATH (The Eigen-Audit)
        # We ensure n_components doesn't exceed our actual data points
        n_comp = min(5, len(embeddings))
        pca = PCA(n_components=n_comp)
        pca.fit(embeddings)

        # 4. REPORT RESULTS
        print(f"\n" + "="*50)
        print(f"📊 EIGEN-AUDIT RESULTS (n={len(embeddings)} chunks)")
        print(f"Captured {np.sum(pca.explained_variance_ratio_)*100:.2f}% of total document variance.")
        print("="*50)

        # Variance breakdown per component (The "Eigenvalues")
        for i, ratio in enumerate(pca.explained_variance_ratio_):
            print(f"PC{i+1}: {ratio*100:.2f}% (Information Weight)")

        # 5. SEMANTIC CENTER (PC1)
        # We transform the data to find the points that align most with the main axis
        projections = pca.transform(embeddings)[:, 0]
        top_indices = np.argsort(projections)[-3:]

        print("\n" + "-"*50)
        print("🧠 ABSOLUTE CORE THEMES (PC1 SAMPLES)")
        print("-"*50)
        for idx in top_indices:
            page_info = data['metadatas'][idx].get('page', 'Unknown')
            print(f" [Page {page_info}] -> {documents[idx][:160]}...")
            print("-" * 20)

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    run_local_audit()
