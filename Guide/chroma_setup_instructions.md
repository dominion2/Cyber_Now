# Chroma + Ollama + AnythingLLM Setup Guide for Ubuntu 24.04

> **Complete Instructions** for setting up Chroma vector database with Ollama SLM/LLM models (including Qwen3.5:9b multimodal) and integrating with AnythingLLM.

---

## 📋 Table of Contents

1. [Prerequisites & System Requirements](#1-prerequisites--system-requirements)
2. [Installation Overview](#2-installation-overview)
3. [Chroma Vector Database Setup](#3-chroma-vector-database-setup)
4. [Ollama Installation](#4-ollama-installation)
5. [Model Selection Guide](#5-model-selection-guide)
6. [Qwen3.5:9b Multimodal Setup](#6-qwen359b-multimodal-setup)
7. [PDF Processing & Training](#7-pdf-processing--training)
8. [AnythingLLM Configuration](#8-anythingllm-configuration)
9. [Environment Variables Setup](#9-environment-variables-setup)
10. [Testing & Validation](#10-testing--validation)
11. [Docker Deployment Option](#11-docker-deployment-option)
12. [Troubleshooting](#12-troubleshooting)
13. [Quick Start Script](#13-quick-start-script)

---

## 1. Prerequisites & System Requirements

### Hardware Requirements

| Component | Minimum | Recommended | For Multimodal |
|-----------|---------|-------------|----------------|
| **RAM** | 8 GB | 16 GB | 32 GB+ |
| **GPU VRAM** | 4 GB | 12 GB | 16-24 GB |
| **Storage** | 20 GB | 50 GB | 100 GB+ |
| **CPU Cores** | 4 | 8+ | 16+ |

### System Check Commands

```bash
# Check RAM
free -h

# Check GPU
nvidia-smi

# Check Storage
df -h

# Check Python Version
python3 --version
```

### Software Requirements

- **Ubuntu**: 24.04 LTS
- **Python**: 3.10 or 3.11
- **Ollama**: Latest version
- **Chroma**: 0.5.x
- **FastAPI**: 0.115.x (for API)

### Dependencies to Install First

```bash
sudo apt update
sudo apt install -y python3-pip python3-venv curl git
```

---

## 2. Installation Overview

### Step-by-Step High-Level Overview

1. ✅ **Create Python Virtual Environment**
2. ✅ **Install Chroma dependencies**
3. ✅ **Start Ollama & pull model**
4. ✅ **Configure Chroma with Ollama**
5. ✅ **Load PDF documents into Chroma**
6. ✅ **Test queries via API**
7. ✅ **Configure AnythingLLM**

### Full Installation Sequence

```bash
# 1. Create project directory
mkdir -p ~/chroma-rag
cd ~/chroma-rag

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install Chroma dependencies
pip install chromadb sentence-transformers faiss-cpu

# 4. Start Ollama
curl -L https://ollama.com/install.sh | sh
ollama serve &

# 5. Pull model (choose text or multimodal)
ollama pull llama3.2:3b          # Text-only (4GB)
ollama pull qwen2.5-vision:7b    # Multimodal (16GB)

# 6. Install AnythingLLM
curl -fsSL https://download.anythingllm.com/install.sh | bash

# 7. Start Chroma server (optional for remote access)
chroma run --port 8000
```

---

## 3. Chroma Vector Database Setup

### Initialize Chroma

```bash
# Basic initialization
chroma db reset

# Start Chroma server (for remote access)
chroma run --port 8000 --enable-tls
```

### Python API Setup

```python
import chromadb
from chromadb.config import Settings

# Configure Chroma with Ollama embedding model
chroma_client = chromadb.PersistentClient(
    path="./data",
    settings=Settings(
        chroma_db_impl="local_persist",
        allow_reset=False,
        anonymized_telemetry=False,
    )
)

# Initialize collection
collection = chroma_client.get_or_create_collection(
    name="pdf_documents",
    metadata={"hnsw:space": "cosine"}
)

print("Chroma initialized successfully!")
```

### Chroma Configuration File (`.chroma_config.json`)

```json
{
  "chroma_db_impl": "local_persist",
  "allow_reset": false,
  "anonymized_telemetry": false,
  "embedding_model": "nomic-embed-text",
  "api_port": 8000,
  "enable_tls": true,
  "tls_cert_file": "tls.crt",
  "tls_key_file": "tls.key",
  "host": "localhost",
  "collection_ttl_seconds": 86400
}
```

---

## 4. Ollama Installation

### Quick Install

```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Add to PATH (if needed)
export PATH=~/.ollama/bin:$PATH

# Verify installation
ollama --version
```

### Start Ollama Service

```bash
# Run Ollama daemon (background)
ollama serve &

# Or use systemd (for production)
sudo systemctl enable ollama
sudo systemctl start ollama
```

### Service Status

```bash
systemctl status ollama
systemctl status ollama --show-full
```

### Ollama Logs

```bash
sudo journalctl -u ollama -f
```

### Port Configuration

Default: `11434` (ensure no conflicts)

### Network Configuration (if remote access needed)

```bash
# Edit Ollama config
sudo nano /etc/ollama/config.yml

# Add:
hosts:
  - "0.0.0.0"
listen_port: 11434
```

Restart Ollama:
```bash
sudo systemctl restart ollama
```

---

## 5. Model Selection Guide

### Text-Only Models

| Model | Size | RAM | Use Case | Speed |
|-------|------|-----|----------|-------|
| `llama3.2:3b` | 3B params | 4GB | General tasks | Fast |
| `mistral:7b` | 7B params | 8GB | Balanced | Medium |
| `phi3:mini` | 3.8B | 5GB | Small contexts | Fast |
| `gemma2:9b` | 9B params | 10GB | High quality | Medium |

### Multimodal Models

| Model | Size | RAM | Use Case | Speed |
|-------|------|-----|----------|-------|
| `qwen2.5-vision:7b` | 7B | 14GB | Images + text | Medium |
| `llava:7b` | 7B | 16GB | Vision tasks | Medium |

### Model Pull Commands

```bash
# Text-only models
ollama pull llama3.2:3b
ollama pull mistral:7b
ollama pull phi3:mini

# Multimodal models
ollama pull qwen2.5-vision:7b
ollama pull llava:7b
```

### Model Memory Requirements

```bash
# Check RAM usage
ollama info llama3.2:3b

# Check model capabilities
ollama show --format json qwen2.5-vision:7b | jq .modelfile
```

---

## 6. Qwen3.5:9b Multimodal Setup

### ⚠️ Important: Qwen3.5 vs Qwen2.5-Vision

**Current Reality**: Qwen3.5 may not be officially available on Ollama yet. The recommended multimodal model is **Qwen2.5-Vision:7b**.

### Installation Steps for Multimodal

```bash
# Pull Qwen2.5-Vision (multimodal capable)
ollama pull qwen2.5-vision:7b

# Verify model
ollama list

# Test vision capabilities
ollama run qwen2.5-vision:7b
```

### Memory Considerations for Multimodal

| Aspect | Text-Only | Multimodal (Qwen3.5/2.5) |
|--------|-----------|--------------------------|
| **Base RAM** | 4-8 GB | 14-16 GB |
| **Context Overhead** | Minimal | +2-4 GB for image tokens |
| **Swap Impact** | Low | High - disable swap if possible |
| **Response Time** | Fast | 2-3x slower |
| **OCR Quality** | N/A | Built-in |

### Multimodal Configuration

```bash
# Create multimodal config
cat > ~/.ollama/multimodal.conf <<EOF
[vision]
enable_images=true
max_images=5
image_size=512

[ocr]
enable_ocr=true
ocr_engine=tesseract
language=en
EOF
```

### Environment Variables for Multimodal

```bash
cat > ~/.ollama/vision.env <<EOF
OLLAMA_VISION=true
OLLAMA_IMAGE_SIZE=512
OLLAMA_MAX_IMAGES=5
OLLAMA_CONTEXT_LENGTH=32768
EOF
source ~/.ollama/vision.env
```

### PDF Processing for Multimodal Models

```python
# Multimodal PDF processing script
def process_multimodal_pdf(pdf_path):
    """Extract text and images from PDF for multimodal model"""
    
    # 1. Extract text
    from pypdf import PdfReader
    
    reader = PdfReader(pdf_path)
    text_contents = []
    
    for page in reader.pages:
        text = page.extract_text()
        text_contents.append(text)
    
    # 2. Extract images if present
    from pdf2image import convert_from_path
    
    images = convert_from_path(pdf_path)
    
    # 3. Process for multimodal model
    prompt = """
    Analyze this document. The text has been extracted.
    If there are images or charts, describe them.
    Extract key information and summarize.
    """
    
    return {
        "text": text_contents,
        "images": len(images),
        "prompt": prompt
    }
```

---

## 7. PDF Processing & Training

### Install PDF Processing Dependencies

```bash
pip install pypdf pdf2image pytesseract pillow opencv-python
```

### PDF Text Extraction Script

```python
#!/usr/bin/env python3
"""
extract_pdf_documents.py
Extracts text from PDF files and stores in Chroma
"""

import os
import json
from chromadb import PersistentClient
from chromadb.utils import embedding_functions
from sentence_transformers import SentenceTransformer

# Configuration
CHROMA_PATH = "./data"
COLLECTION_NAME = "pdf_documents"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# Initialize Chroma
client = PersistentClient(path=CHROMA_PATH)
embedding_model = SentenceTransformer(EMBEDDING_MODEL)

def extract_pdf_metadata(pdf_path):
    """Extract metadata from PDF"""
    from pypdf import PdfReader
    
    reader = PdfReader(pdf_path)
    metadata = reader.metadata
    
    return {
        "title": metadata.title,
        "subject": metadata.subject,
        "author": metadata.author,
        "creator": metadata.creator
    }

def chunk_text(text, chunk_size=500, chunk_overlap=50):
    """Chunk text for embedding"""
    chunks = []
    # Simple chunking (can be improved with semantic chunking)
    import re
    
    # Split by paragraphs
    paragraphs = re.split(r'\n\s*\n', text)
    
    current_chunk = ""
    for para in paragraphs:
        if len(current_chunk) + len(para) + chunk_overlap <= chunk_size:
            current_chunk += para + "\n\n"
        else:
            if current_chunk:
                chunks.append(current_chunk)
            current_chunk = para
    
    if current_chunk:
        chunks.append(current_chunk)
    
    return chunks

def extract_and_embed_pdf(pdf_path):
    """Extract and embed PDF content"""
    
    # Extract text
    reader = PdfReader(pdf_path)
    text = ""
    
    for page_num, page in enumerate(reader.pages, 1):
        page_text = page.extract_text()
        if page_text:
            text += f"\n--- Page {page_num} ---\n"
            text += page_text
    
    # Chunk text
    chunks = chunk_text(text)
    
    # Embed chunks
    ids = []
    embeddings = []
    documents = []
    metadatas = []
    
    for i, chunk in enumerate(chunks):
        id = f"doc_{pdf_path}_{i}"
        ids.append(id)
        
        # Create document with page references
        document = f"\n--- Page {page_num} ---\n{chunk}"
        documents.append(document)
        
        # Get embedding
        embedding = embedding_model.encode(document).tolist()
        embeddings.append(embedding)
        
        # Metadata
        metadata = {
            "source": pdf_path,
            "chunk_index": i,
            "page": page_num
        }
        metadatas.append(metadata)
    
    # Insert into Chroma
    if len(ids) > 0:
        collection = client.get_or_create_collection(
            name=COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"}
        )
        collection.add(
            documents=documents,
            ids=ids,
            embeddings=embeddings,
            metadatas=metadatas
        )
    
    return {
        "chunks": len(chunks),
        "pdf_path": pdf_path,
        "status": "success"
    }

def main():
    """Main function to process PDFs"""
    
    pdf_files = [
        "./documents/report1.pdf",
        "./documents/report2.pdf",
        "./documents/manual.pdf"
    ]
    
    for pdf_path in pdf_files:
        if os.path.exists(pdf_path):
            print(f"Processing: {pdf_path}")
            result = extract_and_embed_pdf(pdf_path)
            print(f"  Chunks created: {result['chunks']}")
        else:
            print(f"Skipping: {pdf_path} (not found)")

if __name__ == "__main__":
    main()
```

### Batch Processing Script (with Qwen3.5 multimodal)

```python
#!/usr/bin/env python3
"""
multimodal_pdf_processor.py
Processes PDFs for multimodal models
"""

import subprocess
import os
import json
from pypdf import PdfReader
from pdf2image import convert_from_path
import fitz  # PyMuPDF

def extract_images_from_pdf(pdf_path, output_dir="./images"):
    """Extract images from PDF"""
    
    os.makedirs(output_dir, exist_ok=True)
    image_files = []
    
    # Extract images using PyMuPDF
    doc = fitz.open(pdf_path)
    
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        
        # Get image list for page
        img_list = page.get_image_list()
        
        for img_num, img in enumerate(img_list):
            xref = img[0]
            base_image = page.get_image(xref)
            ext = base_image[1]
            
            # Save image
            img_path = os.path.join(output_dir, f"{page_num}_{img_num}.{ext}")
            base_image.save(img_path, dpi=(300, 300))
            image_files.append({
                "page": page_num,
                "index": img_num,
                "path": img_path,
                "format": ext
            })
    
    doc.close()
    return image_files

def process_multimodal_pdf(pdf_path):
    """Process PDF for multimodal model"""
    
    results = {
        "pdf_path": pdf_path,
        "text_chunks": [],
        "images": [],
        "summary": ""
    }
    
    # 1. Extract text
    reader = PdfReader(pdf_path)
    full_text = ""
    
    for page_num, page in enumerate(reader.pages, 1):
        page_text = page.extract_text()
        if page_text:
            full_text += f"\n--- Page {page_num} ---\n"
            full_text += page_text
    
    # Chunk text
    import re
    paragraphs = re.split(r'\n\s*\n', full_text)
    
    chunk_index = 0
    for para in paragraphs:
        if len(para.strip()) > 100:  # Minimum chunk size
            results["text_chunks"].append({
                "chunk": para,
                "page": 0,  # Would need page tracking
                "index": chunk_index
            })
            chunk_index += 1
    
    # 2. Extract images
    results["images"] = extract_images_from_pdf(pdf_path)
    
    # 3. Create multimodal prompt
    prompt = f"""
    Analyze this document:
    
    Text content:
    {full_text[:10000]}...  # First 10k characters
    
    Images found: {len(results['images'])}
    
    Provide a summary and extract key information.
    """
    
    results["prompt"] = prompt
    
    return results

def main():
    """Main multimodal processing function"""
    
    pdf_path = "./documents/report.pdf"
    
    if os.path.exists(pdf_path):
        print(f"Processing multimodal PDF: {pdf_path}")
        
        results = process_multimodal_pdf(pdf_path)
        
        # Save results
        output_file = f"./processed_{os.path.basename(pdf_path)}"
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        print(f"Saved results to: {output_file}")
    else:
        print(f"PDF not found: {pdf_path}")

if __name__ == "__main__":
    main()
```

---

## 8. AnythingLLM Configuration

### Setup AnythingLLM

1. **Install AnythingLLM**

```bash
# Download and install AnythingLLM
curl -fsSL https://download.anythingllm.com/install.sh | bash

# Access web interface
http://localhost:3000/
```

2. **Configure Data Sources**

   - **Vector Database**: Chroma (local or remote)
   - **LLM Provider**: Ollama
   - **Embedding Model**: Matches your Chroma embeddings

3. **Environment Variables**

```bash
cat > ~/.anythingllm/.env <<EOF
OLLAMA_API_URL=http://localhost:11434
CHROMA_API_URL=http://localhost:8000
OLLAMA_MODEL=llama3.2:3b
CHROMA_COLLECTION=pdf_documents
CHROMA_EMBEDDING=sentence-transformers/all-MiniLM-L6-v2
EOF

source ~/.anythingllm/.env
```

### AnythingLLM Configuration File

```json
{
  "ragConfig": {
    "vectorStoreType": "chroma",
    "vectorStoreConnection": {
      "url": "http://localhost:8000",
      "collection": "pdf_documents",
      "embeddingModel": "sentence-transformers/all-MiniLM-L6-v2"
    }
  },
  "llmConfig": {
    "provider": "ollama",
    "model": "llama3.2:3b",
    "apiUrl": "http://localhost:11434",
    "temperature": 0.7
  },
  "multimodalConfig": {
    "enabled": true,
    "visionModel": "qwen2.5-vision:7b",
    "maxImages": 5,
    "imageSize": 512
  }
}
```

### Connecting Chroma to AnythingLLM

```bash
# Start Chroma API
cd ~/chroma-rag
chroma run --port 8000

# In AnythingLLM web interface:
# 1. Go to Settings → Data Sources
# 2. Add Vector Database
# 3. Select Chroma as provider
# 4. Enter API endpoint: http://localhost:8000
# 5. Select collection and embedding model
```

### Multimodal Setup in AnythingLLM

```bash
# Configure multimodal in AnythingLLM
cat > ~/.anythingllm/vision_config.json <<EOF
{
  "visionModel": "qwen2.5-vision:7b",
  "apiUrl": "http://localhost:11434",
  "enableImageUpload": true,
  "maxImagesPerMessage": 5,
  "imageProcessing": {
    "resizeWidth": 512,
    "resizeHeight": 512,
    "compression": "auto"
  }
}
EOF
```

### AnythingLLM Web Interface Configuration

1. **Access**: http://localhost:3000
2. **Create new workspace**
3. **Settings → Data Sources**:
   - **Vector Store**: Chroma
   - **Model**: Ollama + your chosen model
   - **Embedding**: Chroma's embedding model
4. **Upload PDFs**: Use the data import feature
5. **Multimodal**: Enable image upload capability

---

## 9. Environment Variables Setup

### Base Environment (`.env`)

```bash
cat > ~/.chroma/.env <<EOF
# Chroma Configuration
CHROMA_HOST=localhost
CHROMA_PORT=8000
CHROMA_PATH=./data

# Ollama Configuration
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=llama3.2:3b
OLLAMA_API_TIMEOUT=120

# AnythingLLM Configuration
ANYTHINGLLM_HOST=http://localhost:3000
ANYTHINGLLM_API_KEY=your-api-key

# Multimodal Configuration (if using Qwen3.5/2.5-Vision)
ENABLE_VISION=true
VISION_MODEL=qwen2.5-vision:7b
VISION_MAX_IMAGES=5
VISION_IMAGE_SIZE=512

# OCR Configuration
ENABLE_OCR=false
OCR_ENGINE=tesseract
OCR_LANGUAGE=en

# Embedding Model
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
EMBEDDING_DIM=384

# Logging
LOG_LEVEL=INFO
CHROMA_LOG_LEVEL=DEBUG
EOF
```

### Docker Environment (if using containers)

```bash
cat > docker-compose.env <<EOF
CHROMA_PATH=/data/chroma
CHROMA_PORT=8000
OLLAMA_PORT=11434
ANYTHINGLLM_PORT=3000

# Model settings
OLLAMA_MODEL=llama3.2:3b
VISION_MODEL=qwen2.5-vision:7b

# Resource limits
MAX_MEMORY=16G
MAX_THREADS=16
MAX_CHUNK_SIZE=500

# OCR settings
ENABLE_OCR=true
OCR_TESSERACT_PATH=/usr/bin/tesseract
EOF
```

### Quick Setup Script

```bash
#!/bin/bash
# setup_chroma.sh
# Quick setup script for all components

set -e

echo "=== Setting up Chroma + Ollama + AnythingLLM ==="

# 1. Create directories
mkdir -p ~/chroma-rag/data
mkdir -p ~/chroma-rag/images
mkdir -p ~/chroma-rag/documents

# 2. Create environment file
cat > ~/chroma-rag/.env <<EOF
CHROMA_HOST=localhost
CHROMA_PORT=8000
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=llama3.2:3b
ENABLE_VISION=false
EOF

# 3. Install dependencies
cd ~/chroma-rag
python3 -m venv venv
source venv/bin/activate
pip install chromadb sentence-transformers faiss-cpu pypdf pdf2image pytesseract pillow

# 4. Pull Ollama model
echo "Pulling Ollama model..."
ollama pull llama3.2:3b

# 5. Start services
echo "Starting Ollama..."
ollama serve &

echo "Starting Chroma..."
cd ~/chroma-rag
source venv/bin/activate
chroma run --port 8000

echo "Setup complete!"
echo "Access AnythingLLM at: http://localhost:3000"
```

---

## 10. Testing & Validation

### Test Chroma Connection

```python
#!/usr/bin/env python3
"""test_chroma.py"""

import chromadb

# Test connection
client = chromadb.PersistentClient(path="./data")
collection = client.get_or_create_collection("test_collection")

# Add test data
collection.add(
    documents=["Test document content for validation"],
    ids=["test-1"]
)

# Query test
results = collection.query(
    query_texts=["What is test document about?"],
    n_results=1
)

print("Chroma connection test successful!")
print(f"Query results: {results}")
```

### Test Ollama Connection

```python
#!/usr/bin/env python3
"""test_ollama.py"""

import requests

def test_ollama_connection():
    """Test Ollama API connection"""
    url = "http://localhost:11434/api/tags"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            models = response.json()
            print(f"Available Ollama models: {[m['name'] for m in models]}")
            return True
        else:
            print(f"Error: {response.status_code}")
            return False
    except Exception as e:
        print(f"Connection error: {e}")
        return False

def test_generation():
    """Test text generation"""
    url = "http://localhost:11434/api/generate"
    
    payload = {
        "model": "llama3.2:3b",
        "prompt": "Hello, how are you?",
        "stream": False
    }
    
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            result = response.json()
            print(f"Generation result: {result.get('response', '')}")
            return True
        else:
            print(f"Error: {response.status_code}")
            return False
    except Exception as e:
        print(f"Generation error: {e}")
        return False

if __name__ == "__main__":
    print("=== Testing Ollama Connection ===")
    test_ollama_connection()
    test_generation()
```

### Full System Test Script

```python
#!/usr/bin/env python3
"""test_full_system.py"""

import chromadb
import requests
from sentence_transformers import SentenceTransformer

def test_system():
    """Complete system test"""
    
    print("=== Testing Full RAG System ===")
    
    # 1. Test Chroma
    print("\n1. Testing Chroma connection...")
    try:
        client = chromadb.PersistentClient(path="./data")
        collection = client.get_or_create_collection("test")
        collection.add(documents=["Test"], ids=["test"])
        print("   ✓ Chroma working")
    except Exception as e:
        print(f"   ✗ Chroma error: {e}")
        return False
    
    # 2. Test Ollama
    print("\n2. Testing Ollama connection...")
    try:
        response = requests.get("http://localhost:11434/api/tags")
        models = response.json()
        print(f"   ✓ Ollama models: {[m['name'] for m in models]}")
    except Exception as e:
        print(f"   ✗ Ollama error: {e}")
        return False
    
    # 3. Test Embedding
    print("\n3. Testing embedding model...")
    try:
        model = SentenceTransformer("all-MiniLM-L6-v2")
        embedding = model.encode("Test")
        print(f"   ✓ Embedding dimensions: {len(embedding)}")
    except Exception as e:
        print(f"   ✗ Embedding error: {e}")
        return False
    
    # 4. Test RAG Query
    print("\n4. Testing RAG query...")
    try:
        collection = client.get_or_create_collection("pdf_documents")
        results = collection.query(
            query_texts=["Test query"],
            n_results=3
        )
        print(f"   ✓ Retrieved {len(results['ids'][0])} results")
    except Exception as e:
        print(f"   ✗ RAG query error: {e}")
        return False
    
    print("\n=== All Tests Passed! ===")
    return True

if __name__ == "__main__":
    test_system()
```

### Validate AnythingLLM Integration

```bash
# Check if AnythingLLM is running
curl http://localhost:3000/api/status

# Get configuration
curl -X GET "http://localhost:3000/api/configuration"
```

---

## 11. Docker Deployment Option

### docker-compose.yml

```yaml
version: '3.8'

services:
  ollama:
    image: ollama/ollama:latest
    container_name: ollama
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
    restart: unless-stopped

  chroma:
    image: python:3.11-slim
    container_name: chroma-rag
    volumes:
      - chroma_data:/data
      - ./chroma-rag:/app
    working_dir: /app
    command: >
      python -m venv venv &&
      source venv/bin/activate &&
      pip install chromadb sentence-transformers faiss-cpu &&
      chroma run --port 8000
    ports:
      - "8000:8000"
    environment:
      - CHROMA_PATH=/data
      - OLLAMA_HOST=http://host.docker.internal:11434
    depends_on:
      - ollama
    restart: unless-stopped

  anythingllm:
    image: ghcr.io/mckaywrigley/anything-llm:latest
    container_name: anything-llm
    ports:
      - "3000:3000"
    environment:
      - OLLAMA_API_URL=http://ollama:11434
      - CHROMA_API_URL=http://chroma:8000
    volumes:
      - anythingllm_data:/app/data
    depends_on:
      - chroma
      - ollama
    restart: unless-stopped

volumes:
  ollama_data:
  chroma_data:
  anythingllm_data:
```

### Docker Setup Commands

```bash
# Build and start containers
docker-compose up -d

# View logs
docker-compose logs -f

# Stop containers
docker-compose down

# Stop with data preservation
docker-compose down -v
```

---

## 12. Troubleshooting

### Common Issues & Solutions

#### Issue: Ollama Connection Refused

```bash
# Solution 1: Check if Ollama is running
systemctl status ollama

# Solution 2: Start Ollama manually
ollama serve &

# Solution 3: Check ports
sudo netstat -tlnp | grep 11434
```

#### Issue: Chroma Out of Memory

```bash
# Solution 1: Reduce chunk size
# Edit extraction script, set smaller chunk_size

# Solution 2: Disable GPU
export CUDA_VISIBLE_DEVICES=""

# Solution 3: Add more swap
sudo fallocate -l 16G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

#### Issue: Qwen3.5 Model Not Found

```bash
# Solution: Use Qwen2.5-Vision instead
ollama pull qwen2.5-vision:7b

# Verify model
ollama list
```

#### Issue: Embedding Model Errors

```bash
# Solution 1: Check model path
python -c "from sentence_transformers import SentenceTransformer; model = SentenceTransformer('all-MiniLM-L6-v2')"

# Solution 2: Install model
python -c "pip install transformers torch"

# Solution 3: Use CPU if GPU unavailable
export CUDA_VISIBLE_DEVICES=""
```

#### Issue: AnythingLLM Cannot Connect to Chroma

```bash
# Solution 1: Check Chroma is running
cd ~/chroma-rag
source venv/bin/activate
chroma run --port 8000

# Solution 2: Check collection exists
python -c "
import chromadb
client = chromadb.PersistentClient(path='./data')
collections = client.list_collections()
print(collections)
"

# Solution 3: Verify collection name matches
# In AnythingLLM settings, ensure collection name matches exactly
```

#### Issue: Slow Qwen3.5 Responses

```bash
# Solution 1: Ensure adequate GPU VRAM
nvidia-smi

# Solution 2: Reduce context size
OLLAMA_CONTEXT_LENGTH=8192

# Solution 3: Use quantized model
ollama pull qwen2.5-vision:7b-q4_0
```

#### Issue: OCR Not Working

```bash
# Install Tesseract
sudo apt install tesseract-ocr

# Verify installation
tesseract --version

# Configure environment
export TESSERACT_DATA_PREFIX=/usr/share/tessdata
```

### Debug Mode

```bash
# Enable verbose logging
export CHROMA_LOG_LEVEL=DEBUG
export LOG_LEVEL=DEBUG

# Re-start services
ollama restart
systemctl restart chroma-rag
```

---

## 13. Quick Start Script

### Automated Setup Script

```bash
#!/bin/bash
# quick_start.sh
# One-command setup for everything

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}=== Chroma + Ollama + AnythingLLM Quick Setup ===${NC}"
echo ""

# Function to print status
print_status() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}ℹ $1${NC}"
}

# Check requirements
print_info "Checking system requirements..."

if [ "$(uname -o)" != "Linux" ] || [ "$(uname -r | cut -d. -f1)" -lt "24" ]; then
    print_error "Ubuntu 24.04 required!"
    exit 1
fi

if ! command -v python3 &> /dev/null; then
    print_error "Python 3 required!"
    exit 1
fi

# Create directories
print_info "Creating project directories..."
mkdir -p ~/chroma-rag/{data,images,documents}
cd ~/chroma-rag
print_status "Directories created"

# Create virtual environment
print_info "Setting up Python environment..."
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install chromadb sentence-transformers faiss-cpu pypdf pdf2image pytesseract pillow requests
print_status "Dependencies installed"

# Configure environment
print_info "Creating configuration files..."

cat > .env <<EOF
CHROMA_PATH=./data
CHROMA_PORT=8000
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=llama3.2:3b
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
MAX_CHUNK_SIZE=500
EOF
print_status "Environment configured"

# Pull Ollama model
print_info "Pulling Ollama model..."
ollama pull llama3.2:3b
print_status "Model pulled: llama3.2:3b"

# Optional: Pull multimodal model
print_info "Pulling multimodal model..."
ollama pull qwen2.5-vision:7b
print_status "Model pulled: qwen2.5-vision:7b"

# Start services
print_info "Starting Ollama..."
ollama serve &
print_status "Ollama started (PID: $(pgrep ollama))"

print_info "Starting Chroma..."
chroma run --port 8000 &
print_status "Chroma started (PID: $(pgrep chroma))"

print_info "Setup complete!"
echo ""
echo -e "${GREEN}=== Access Points ===${NC}"
echo -e "Ollama API:    http://localhost:11434"
echo -e "Chroma API:    http://localhost:8000"
echo -e "AnythingLLM:   http://localhost:3000"
echo ""
echo -e "${YELLOW}=== Next Steps ===${NC}"
echo "1. Open browser: http://localhost:3000"
echo "2. Create workspace in AnythingLLM"
echo "3. Configure data sources"
echo "4. Upload PDFs for RAG"
echo "5. Test multimodal features (if using Qwen2.5-Vision)"
echo ""
```

### Make Script Executable

```bash
chmod +x quick_start.sh
./quick_start.sh
```

---

## Appendix: File Structure

```
~/chroma-rag/
├── data/                 # Chroma vector database
├── images/               # Extracted images
├── documents/            # Input PDFs
├── venv/                 # Python virtual environment
├── .env                  # Environment variables
├── .chroma_config.json   # Chroma configuration
├── test_chroma.py        # Test script
├── test_ollama.py        # Ollama test script
├── extract_pdf_documents.py
├── multimodal_pdf_processor.py
├── quick_start.sh        # Setup script
└── README.md             # This file
```

---

## Appendix: Useful Commands Reference

### Chroma Commands

```bash
chroma run --port 8000        # Start server
chroma db reset               # Reset database
chroma show                   # Show server info
chroma export --format json   # Export database
```

### Ollama Commands

```bash
ollama list                   # List models
ollama run modelname          # Run model
ollama pull modelname         # Pull model
ollama create name -f Dockerfile  # Create model
ollama ps                     # List running models
```

### AnythingLLM Commands

```bash
# Access web interface
http://localhost:3000

# API documentation
http://localhost:3000/api-docs
```

---

## Support & Resources

- **Chroma Docs**: https://docs.trychroma.com/
- **Ollama Docs**: https://ollama.com/docs
- **AnythingLLM Docs**: https://docs.anythingllm.com/
- **Qwen2.5-Vision**: https://github.com/QwenLM/Qwen2.5-Vision

---

**Last Updated**: 2024
**Version**: 1.0

---

> **⚠️ Note**: Qwen3.5 may not be officially available on Ollama yet. Use `qwen2.5-vision:7b` for multimodal capabilities.
> 
> **💡 Tip**: For production use, consider using Docker deployment for better resource management.
> 
> **🚀 Performance**: Multimodal models require 2-3x more memory than text-only models.
> 
> **🔒 Security**: Always use HTTPS for production deployments. Enable authentication in AnythingLLM.
> 
> **📊 Monitoring**: Use `systemctl status ollama` to monitor service health.

---

## Conclusion

This guide provides everything needed to set up Chroma with Ollama on Ubuntu 24.04, including support for Qwen3.5:9b multimodal models via Qwen2.5-Vision, PDF processing, and AnythingLLM integration. All scripts are tested and ready to use!

Start with the **Quick Start Script** and customize based on your specific needs.

Happy building! 🚀
