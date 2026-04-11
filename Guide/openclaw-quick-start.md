# 🚀 OpenClaw MCP Setup - Ubuntu 24.04 Quick Start Guide

**Target:** Ubuntu 24.04 Headless Server | **Tools:** AnythingLLM + Ollama | **Skills:** 48,000+ OpenClaw

---

## ✅ Prerequisites

| Item | Command |
|------|---------|
| Node.js 20+ | `curl -fsSL https://deb.nodesource.com/setup_20.x \| sudo -E bash - && sudo apt-get install -y nodejs npm` |
| Server Access | SSH from laptop to Ubuntu 24.04 server |
| Ollama | Already running on port 11434 |
| Network | Laptop and server on same network |

---

## 📦 Step 1: Install OpenClaw MCP Server

```bash
# On Ubuntu Server
git clone https://github.com/VoltAgent/openclaw.git
cd openclaw
npm install
npm run build
```

---

## 🔌 Step 2: Start MCP Server

```bash
# Allow external connections
nano openclaw/config/mcp-server.js
# Set: host: '0.0.0.0', allowCors: true

# Start server
nohup node openclaw/dist/server.mjs --host 0.0.0.0 --port 3000 > /var/log/openclaw.log 2>&1 &

# Verify running
curl http://localhost:3000/mcp-tools
```

---

## 🔒 Step 3: Firewall Configuration

```bash
sudo ufw allow 3000/tcp
sudo ufw allow 11434/tcp
sudo ufw status
```

---

## 🚀 Step 4: Configure AnythingLLM on Laptop

1. **Install MCP CLI**
   ```bash
   npm install -g @modelcontextprotocol/mcpc
   ```

2. **Connect to OpenClaw Server**
   ```bash
   mcpc connect http://<server-ip>:3000/mcp
   ```

3. **Configure in AnythingLLM**
   - Go to **Settings → Agents → Tools → MCP**
   - Add endpoint: `http://<server-ip>:3000/mcp`
   - Select tools (Git, Docker, File Manager, etc.)

---

## 📚 Step 5: Install Skills

```bash
# Recommended tools to add
npx @voltagent/clawhub install git-repo-tool
npx @voltagent/clawhub install docker-tool
npx @voltagent/clawhub install file-manager-tool
npx @voltagent/clawhub install http-tool
```

---

## 🛡️ Step 6: Production Setup (Optional)

Create systemd service file:

```bash
sudo nano /etc/systemd/openclaw.service

[Unit]
Description=OpenClaw MCP Server
After=network.target

[Service]
Type=simple
User=<your-username>
WorkingDirectory=/path/to/openclaw
ExecStart=/usr/bin/node openclaw/dist/server.mjs --host 0.0.0.0 --port 3000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable openclaw
sudo systemctl start openclaw
sudo journalctl -u openclaw -f
```

---

## ✅ Final Verification Checklist

- [ ] OpenClaw MCP server running on port 3000
- [ ] Firewall allows ports 3000 and 11434
- [ ] AnythingLLM can reach `http://<server-ip>:3000/mcp`
- [ ] MCP tools listed in AnythingLLM
- [ ] Agent can execute OpenClaw skills

---

## 📋 Quick Command Cheat Sheet

| Task | Command |
|------|---------|
| Start server | `nohup node openclaw/dist/server.mjs --host 0.0.0.0 --port 3000 &` |
| Stop server | `pkill -f openclaw` |
| Check logs | `tail -f /var/log/openclaw.log` |
| Test connection | `curl http://<server-ip>:3000/mcp-tools` |
| View MCP tools | `mcpc tools http://<server-ip>:3000` |

---

## 🆘 Troubleshooting

| Issue | Fix |
|-------|-----|
| Connection refused | Check server is running: `ps aux \| grep openclaw` |
| Tools not showing | Verify endpoint: `http://<server-ip>:3000/mcp` |
| CORS errors | Ensure `allowCors: true` in config |
| Ollama not responding | Check: `curl http://localhost:11434/api/tags` |

---

## 📖 Useful Links

- [OpenClaw GitHub](https://github.com/VoltAgent/openclaw)
- [ClawHub Marketplace](https://clawhub.ai/)
- [OpenClaw Skills](https://openclawskills.io/skills)
- [AnythingLLM Docs](https://docs.anythingllm.com/)

---

**⚠️ Note:** This guide assumes basic Linux knowledge. Review firewall and security settings before production use.

**Last Updated:** 2024 | **Version:** 1.0