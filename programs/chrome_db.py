import os
import gc
import sys
import time
import chromadb
import ollama
from pypdf import PdfReader
from docling.document_converter import DocumentConverter

# 1. OPTIMIZATION (Unleashing the 14700K)
os.environ["DOCLING_NUM_THREADS"] = "20"
DB_PATH = os.path.expanduser("~/chroma_db")
PDF_PATH = os.path.expanduser("~/Downloads/training_data/DataScience.pdf")

# 2. CONNECT
try:
    client = chromadb.PersistentClient(path=DB_PATH)
    collection = client.get_or_create_collection("datascience_study")
    local_ollama = ollama.Client(host="http://localhost:11434")
except Exception as e:
    print(f"❌ Connection Error: {e}")
    sys.exit(1)

def get_last_processed_page():
    """Checks ChromaDB for the highest page number currently indexed."""
    try:
        results = collection.get(include=['metadatas'])
        if not results['metadatas']:
            return 0
        pages = [m.get('page', 0) for m in results['metadatas']]
        return max(pages)
    except Exception as e:
        print(f"  Could not find existing progress: {e}")
        return 0

def main():
    last_page = get_last_processed_page()
    reader = PdfReader(PDF_PATH)
    total_pages = len(reader.pages)
        if last_page >= total_pages:
        print(f"✅ Ingestion already complete! (Page {last_page}/{total_pages})")
        return

    print(f"--- 🔄 RESUMING FROM PAGE {last_page + 1} of {total_pages} ---")

    converter = DocumentConverter()
    BATCH_SIZE = 10

    try:
        # MAIN PROCESSING LOOP
        for start in range(last_page + 1, total_pages + 1, BATCH_SIZE):
            end = min(start + BATCH_SIZE - 1, total_pages)
            print(f"🚀 Processing Batch: {start}-{end}...")

            result = converter.convert(PDF_PATH, page_range=(start, end))
            doc = result.document
            all_items = list(doc.iterate_items())

            for i, (item, level) in enumerate(all_items):
                element_type = item.__class__.__name__
                content = ""

                if hasattr(item, "text") and element_type == "TextItem":
                    content = item.text

                elif element_type in ["TableItem", "PictureItem"]:
                    # --- THE VISION STATUS MESSAGE IS BACK ---
                    print(f"   [Vision] 👁️  Analyzing {element_type} on Page {start} with Qwen 3.5...")

                    # Context/Vision logic
                    context = " ".join([
                        all_items[j][0].text for j in range(max(0, i-2), min(len(all_items), i+3))
                        if hasattr(all_items[j][0], 'text')
                    ])

                    response = local_ollama.chat(
                        model='qwen3.5:9b',
                        messages=[{'role': 'user', 'content': f"Context: {context}\nSummarize this chart."}]
                    )
                    content = f"VISUAL: {response['message']['content']}"

                if content.strip():
                    collection.add(
                        documents=[content],
                        metadatas={"page": start, "source": "local_server"},
                        ids=[f"p{start}_i{i}_{time.time()}"]
                    )

            # Cleanup batch
            del result
            gc.collect()
            print(f"✅ Batch {start}-{end} Saved to ChromaDB.")

    except KeyboardInterrupt:
        # --- THE GRACEFUL EXIT ---
        print("\n\n🛑 STOP SIGNAL RECEIVED (CTRL+C)")
        print(f"💾 Progress saved up to Page {start-1}. You can resume later.")
        print("👋 Exiting gracefully...")
        sys.exit(0)

    except Exception as e:
        print(f"  Unexpected Error: {e}")
        sys.exit(1)

    print("--- 🏁 ALL 511 PAGES INDEXED ---")

if __name__ == "__main__":
    main()

                        
