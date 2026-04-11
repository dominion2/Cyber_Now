# 🚀 Ollama Docker Network Installation Guide

## 📋 Overview

Complete guide for installing Ollama in Docker with network-wide accessibility for AnythignLLM, including TurboQuant and Flash Attention configuration.

---

## 🔧 Installation Instructions by Platform

### 🐧 Linux Installation

#### Option 1: Without Docker (Systemd Service)

```bash
# 1. Install prerequisites
sudo apt update
sudo apt install -y docker.io docker-compose nvidia-docker2 nvidia-cuda-toolkit

# 2. Create Ollama service file
sudo tee /etc/systemd/system/ollama.service > /dev/null <<EOF
[Unit]
Description=Ollama Service
After=network-online.target

[Service]
Environment="OLLAMA_HOST=0.0.0.0"
Environment="OLLAMA_KV_CACHE_TYPE=tbq3"
Environment="OLLAMA_FLASH_ATTENTION=1"
ExecStart=/usr/local/bin/ollama serve
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# 3. Start and enable service
sudo systemctl daemon-reload
sudo systemctl start ollama
sudo systemctl enable ollama

# 4. Create data directory
sudo mkdir -p /data/ollama
sudo chown ollama:ollama /data/ollama
```

#### Option 2: With Docker (Linux)

```bash
# 1. Create directory structure
mkdir -p /etc/docker/overlay/ollama/config
mkdir -p /data/ollama

# 2. Create docker-compose.yml
cat > /etc/docker/overlay/ollama/ollama-compose.yml <<EOF
version: '3.8'

services:
  ollama:
    image: ollama/ollama:latest
    container_name: ollama
    network_mode: host
    ports:
      - "11434:11434"
    volumes:
      - /data/ollama:/root/.ollama
    environment:
      - OLLAMA_HOST=0.0.0.0
      - OLLAMA_KV_CACHE_TYPE=tbq3
      - OLLAMA_FLASH_ATTENTION=1
      - OLLAMA_PORT=11434
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
    restart: unless-stopped
EOF

# 3. Start service
sudo docker-compose -f /etc/docker/overlay/ollama/ollama-compose.yml up -d

# 4. Verify installation
docker-compose -f /etc/docker/overlay/ollama/ollama-compose.yml ps
```

### 🪟 Windows Installation

#### Option 1: Without Docker (WSL2 Required)

```powershell
# 1. Enable WSL2 and Docker
wsl --install
wsl --shutdown
wsl --set-default-version 2

# 2. Start Docker in WSL
docker run -d --gpus all -p 11434:11434 --name ollama ollama/ollama:latest

# 3. Pull models (inside WSL)
wsl -d docker-desktop ollama pull llama2:7b

# 4. Test connection
curl http://localhost:11434/api/health
```

#### Option 2: With Docker Desktop

```powershell
# 1. Install Docker Desktop (includes WSL2 backend)
# Download from: https://www.docker.com/products/docker-desktop

# 2. Start Docker Desktop
# Click the Docker Desktop icon in system tray
# Ensure "Wasm" and "GPU" options are enabled

# 3. Pull Ollama image
docker pull ollama/ollama:latest

# 4. Run Ollama with environment variables
docker run -d --gpus all -p 11434:11434 --name ollama `
  -e OLLAMA_HOST=0.0.0.0 `
  -e OLLAMA_KV_CACHE_TYPE=tbq3 `
  -e OLLAMA_FLASH_ATTENTION=1 `
  -v C:\ollama-data:/root/.ollama ollama/ollama:latest

# 5. Verify installation
docker ps
```

#### Option 3: Native Windows (Without WSL)

```powershell
# 1. Install Docker Toolbox (legacy) or use Windows Containers
# Note: GPU support requires WSL2

# 2. Alternative: Use Windows WSL2
wsl --install -d ollama-wsl

# 3. Run inside WSL
wsl bash <<EOF
sudo apt update
sudo apt install -y docker.io docker-compose
sudo mkdir -p /data/ollama
cat > /etc/docker/overlay/ollama/ollama-compose.yml <<YAML
version: '3.8'
services:
  ollama:
    image: ollama/ollama:latest
    network_mode: host
    ports:
      - "11434:11434"
    volumes:
      - /data/ollama:/root/.ollama
    environment:
      - OLLAMA_HOST=0.0.0.0
      - OLLAMA_KV_CACHE_TYPE=tbq3
      - OLLAMA_FLASH_ATTENTION=1
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
EOF

sudo docker-compose -f /etc/docker/overlay/ollama/ollama-compose.yml up -d
EOF
```

---

## ⚙️ Environment Variables Configuration

### Standard Environment Variables

| Variable | Value | Description |
|----------|-------|-------------|
| `OLLAMA_HOST` | `0.0.0.0` | Bind to all network interfaces |
| `OLLAMA_PORT` | `11434` | API server port |
| `OLLAMA_KV_CACHE_TYPE` | `tbq3` | Enable TurboQuant 3-bit KV cache |
| `OLLAMA_FLASH_ATTENTION` | `1` | Enable Flash Attention optimization |
| `OLLAMA_ORIGINS` | `*` | CORS allowed origins |

### Advanced Environment Variables

| Variable | Value | Description |
|----------|-------|-------------|
| `OLLAMA_NUM_GPU` | `12` | GPU memory allocation (GB) |
| `OLLAMA_NUM_PARALLEL` | `8` | Concurrent request limit |
| `OLLAMA_MAX_LOADED` | `1` | Models to keep in memory |
| `OLLAMA_MAX_QUEUE` | `512` | Request queue size |

---

## 🔌 Network Configuration

### Internal Network Setup

```bash
# 1. Create Docker network
docker network create ollama-network

# 2. Start with network alias
docker run -d `
  --name ollama `
  --network ollama-network `
  --network-alias ollama `
  -e OLLAMA_HOST=0.0.0.0 `
  -e OLLAMA_KV_CACHE_TYPE=tbq3 `
  -e OLLAMA_FLASH_ATTENTION=1 `
  -p 11434:11434 `
  ollama/ollama:latest
```

### Firewall Configuration

#### Linux (UFW)
```bash
# Allow connections from trusted IPs
sudo ufw allow from <trusted-ip> to any port 11434
sudo ufw reload

# Allow on public interface
sudo ufw allow 11434/tcp
```

#### Linux (Firewalld)
```bash
# Add port permanently
sudo firewall-cmd --permanent --add-port=11434/tcp
sudo firewall-cmd --reload
```

#### Windows
```powershell
# Using PowerShell
New-NetFirewallRule `
  -DisplayName "Ollama API" `
  -Direction Inbound `
  -LocalPort 11434 `
  -Protocol TCP `
  -Action Allow `
  -Enabled True
```

---

## 📦 Docker Compose Templates

### Basic Production Setup

```yaml
version: '3.8'

services:
  ollama:
    image: ollama/ollama:latest
    container_name: ollama
    network_mode: host
    ports:
      - "11434:11434"
    volumes:
      - ollama-data:/root/.ollama
    environment:
      - OLLAMA_HOST=0.0.0.0
      - OLLAMA_PORT=11434
      - OLLAMA_KV_CACHE_TYPE=tbq3
      - OLLAMA_FLASH_ATTENTION=1
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:11434/api/health"]
      interval: 30s
      timeout: 10s
      retries: 3

volumes:
  ollama-data:
    external: true
```

### Multi-Node Setup

```yaml
version: '3.8'

services:
  ollama-node1:
    image: ollama/ollama:latest
    container_name: ollama-node1
    network_mode: host
    ports:
      - "11434:11434"
    volumes:
      - ollama-data1:/root/.ollama
    environment:
      - OLLAMA_HOST=0.0.0.0
      - OLLAMA_KV_CACHE_TYPE=tbq3
      - OLLAMA_FLASH_ATTENTION=1
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
    restart: unless-stopped

  ollama-node2:
    image: ollama/ollama:latest
    container_name: ollama-node2
    network_mode: host
    ports:
      - "11435:11434"
    volumes:
      - ollama-data2:/root/.ollama
    environment:
      - OLLAMA_HOST=0.0.0.0
      - OLLAMA_KV_CACHE_TYPE=tbq3
      - OLLAMA_FLASH_ATTENTION=1
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
    restart: unless-stopped

volumes:
  ollama-data1:
  ollama-data2:
```

---

## 🔍 Verification Commands

### Service Status

```bash
# Linux (systemd)
sudo systemctl status ollama.service

# Docker
docker ps
docker-compose ps
```

### Health Check

```bash
# API health endpoint
curl http://localhost:11434/api/health

# Get system info
curl http://localhost:11434/api/version

# Check running models
curl http://localhost:11434/api/tags
```

### View Running Models

```bash
# List models
ollama list

# Pull model info
ollama show llama2:7b

# Delete model
ollama rm llama2:7b
```

### Check GPU Usage

```bash
# Linux
watch -n 1 nvidia-smi

# Docker logs
docker logs ollama -f
```

---

## 📝 Model Management

### Pull Models

```bash
# Small models
ollama pull llama2:7b
ollama pull mistral

# Medium models
ollama pull llama2:13b

# Large models (requires more VRAM)
ollama pull llama2:70b

# Custom versions
ollama pull llama2:7b-q4_0    # Quantized
ollama pull llama2:7b-turbo    # Turbo version
```

### Run Inference

```bash
# Chat interface
ollama run llama2:7b "Your question here"

# API usage (Python)
import requests
response = requests.post(
    "http://localhost:11434/api/generate",
    json={
        "model": "llama2",
        "prompt": "Hello!"
    }
)
print(response.text)
```

---

## 🔐 Security Configuration

### Enable Authentication

```bash
# Basic Auth (Linux)
sudo apt install apache2-utils
htpasswd -c /etc/ollama/.htpasswd username

# Docker Compose with Auth
environment:
  - OLLAMA_HOST=0.0.0.0
  - OLLAMA_AUTH_USER=username
  - OLLAMA_AUTH_PASSWORD=secret
```

### CORS Configuration

```bash
# Enable CORS in Ollama
OLLAMA_ORIGINS=https://anything-llm.example.com,https://your-app.com

# Test CORS
curl -X POST `
  -H "Origin: https://your-app.com" `
  -H "Content-Type: application/json" `
  http://localhost:11434/api/generate `
  -d '{"prompt": "Hello"}'
```

---

## 🛠️ Troubleshooting

### Common Issues

#### Issue: Ollama won't start
```bash
# Check logs
docker logs ollama

# Check GPU support
nvidia-smi

# Restart service
sudo systemctl restart ollama.service
```

#### Issue: Cannot connect from network
```bash
# Check firewall
sudo ufw status

# Verify host binding
curl http://localhost:11434/api/health

# Check network configuration
docker network inspect ollama-network
```

#### Issue: Out of memory
```bash
# Stop all running models
ollama ps
ollama rm $(ollama ps -q)

# Or increase VRAM allocation
OLLAMA_NUM_GPU=16
```

---

## 📊 Performance Tuning

### Flash Attention Configuration

```bash
# Enable Flash Attention
Environment="OLLAMA_FLASH_ATTENTION=1"

# This improves throughput by enabling flash attention
# Reduces memory usage during attention computation
```

### TurboQuant Configuration

```bash
# Enable TurboQuant KV cache
Environment="OLLAMA_KV_CACHE_TYPE=tbq3"

# tbq3 activates 3-bit TurboQuant KV cache
# Provides better performance on consumer GPUs
```

### Environment Variables Reference

```bash
# Core Variables
OLLAMA_HOST=0.0.0.0              # Listen on all interfaces
OLLAMA_PORT=11434                # Default API port
OLLAMA_ORIGINS=                  # CORS whitelist

# Performance Variables
OLLAMA_KV_CACHE_TYPE=tbq3        # TurboQuant cache
OLLAMA_FLASH_ATTENTION=1         # Enable Flash Attention
OLLAMA_NUM_GPU=12                # GPU memory (for large models)
OLLAMA_NUM_PARALLEL=8            # Concurrent requests

# Model-Specific Variables
OLLAMA_MAX_LOADED=1              # Models to keep in memory
OLLAMA_MAX_QUEUE=512             # Request queue size
OLLAMA_MAX_LOADED_SEQUENCES=1
```

---

## 📚 Quick Reference

### Essential Commands

| Command | Description |
|---------|-------------|
| `ollama list` | List all installed models |
| `ollama run <model> "prompt"` | Run inference |
| `ollama pull <model>` | Pull a model |
| `ollama rm <model>` | Remove a model |
| `ollama show <model>` | Show model info |
| `ollama ps` | List running sessions |
| `docker logs <container>` | View logs |
| `docker ps` | List containers |
| `docker-compose up -d` | Start services |
| `docker-compose down` | Stop services |

### Health Checks

```bash
# Quick health check
curl http://localhost:11434/api/health

# Get version info
curl http://localhost:11434/api/version

# List loaded models
curl http://localhost:11434/api/tags
```

### Backup Strategy

```bash
# Backup model data
tar -czf ollama-backup-$(date +%Y%m%d).tar.gz /data/ollama

# Restore from backup
tar -xzf ollama-backup-YYYYMMDD.tar.gz -C /
```

---

## ✅ Summary Checklist

- [ ] Install Docker and GPU drivers
- [ ] Configure Ollama with environment variables
- [ ] Enable TurboQuant and Flash Attention
- [ ] Set up network accessibility
- [ ] Configure firewall rules
- [ ] Test connectivity from AnythignLLM
- [ ] Pull desired models
- [ ] Verify health endpoint
- [ ] Set up monitoring
- [ ] Create backup strategy

---

## 📖 Additional Resources

- [Ollama Official Docs](https://github.com/ollama/ollama)
- [Ollama Hub](https://ollama.ai/library)
- [Flash Attention GitHub](https://github.com/Dao-AILab/flash-attention)
- [TurboQuant Documentation](https://github.com/turboprecision/turboquant)

---

**Created**: $(date)  
**Last Updated**: $(date)  
**Version**: 1.0