import os
import gc
import time
import chromadb
import ollama
from docling.document_converter import DocumentConverter

# 1. UNLEASH THE CORES
# With 128GB, we can handle multiple threads easily.
os.environ["DOCLING_NUM_THREADS"] = "8" 
os.environ["OMP_NUM_THREADS"] = "4"

# 2. LOCAL CONFIG
# Use PersistentClient for direct disk access (no network lag)
DB_PATH = os.path.expanduser("~/chroma_db")
client = chromadb.PersistentClient(path=DB_PATH)
collection = client.get_or_create_collection("datascience_study")

# Local Ollama connection
local_ollama = ollama.Client(host="http://localhost:11434")

# Update this to where you SCP'd the file
PDF_PATH = os.path.expanduser("~/Downloads/DataScience.pdf")

def main():
    print(f"--- Starting HIGH-SPEED Ingestion on Server ---")
    start_total = time.time()
    
    converter = DocumentConverter()
    
    # We can process larger batches now!
    BATCH_SIZE = 10 
    
    # Get total pages (Using a simple count for the loop)
    from pypdf import PdfReader
    total_pages = len(PdfReader(PDF_PATH).pages)

    for start in range(1, total_pages + 1, BATCH_SIZE):
        end = min(start + BATCH_SIZE - 1, total_pages)
        print(f"🚀 Processing Pages {start}-{end}...")

        try:
            # Conversion happens locally with 8 threads
            result = converter.convert(PDF_PATH, page_range=(start, end))
            doc = result.document
            all_items = list(doc.iterate_items())

            for i, (item, level) in enumerate(all_items):
                element_type = item.__class__.__name__
                content = ""

                if element_type == "TextItem":
                    content = item.text
                
                elif element_type in ["TableItem", "PictureItem"]:
                    # Context for Vision
                    context = " ".join([all_items[j][0].text for j in range(max(0, i-2), min(len(all_items), i+3)) 
                                      if hasattr(all_items[j][0], 'text')])
                    
                    # Local Vision call (Lightning fast compared to Wi-Fi)
                    response = local_ollama.chat(
                        model='qwen3.5:9b', 
                        messages=[{'role': 'user', 'content': f"Context: {context}\nSummarize this chart."}]
                    )
                    content = f"VISUAL: {response['message']['content']}"

                if content.strip():
                    collection.add(
                        documents=[content],
                        metadatas={"page": start, "source": "local_server"},
                        ids=[f"srv_p{start}_i{i}_{time.time()}"]
                    )

            # Manual RAM clear just in case, though 128GB is plenty
            del result
            gc.collect()

        except Exception as e:
            print(f"⚠️ Error on batch {start}: {e}")

    print(f"--- 🏁 FINISHED in {time.time() - start_total:.2f}s ---")

if __name__ == "__main__":
    main()
