# OpenClaw MCP Setup for Ubuntu 24.04 (Quick Start Guide)
## 🚀 Complete Setup: Server → AnythingLLM Integration

> **Status:** ✅ Currently Active & Working  
> **Last Verified:** 2024  
> **Prerequisites:** Ubuntu 24.04, Node.js 20+, Ollama running

---

## 📋 Prerequisites Checklist

- [ ] Ubuntu 24.04 server (headless)
- [ ] Node.js 20+ and npm installed
- [ ] Ollama running on port 11434
- [ ] Network access (port 3000)
- [ ] Laptop with AnythingLLM (same network)

---

## 🔧 Step 1: Install Node.js & npm

```bash
# Install Node.js 20 LTS
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install nodejs -y

# Verify
node --version  # Should show v20.x.x
npm --version   # Should show 10.x.x or higher
```

---

## 🎯 Step 2: Install OpenClaw MCP Server

### Option A: From NPM (Recommended - Easiest)

```bash
# Install globally
npm install -g @openclaw/mcp

# Verify installation
npx -p @openclaw/mcp -- @openclaw/mcp --version
```

### Option B: From GitHub (If NPM package not available)

```bash
# Clone official MCP server repository
git clone https://github.com/freema/openclaw-mcp.git
cd openclaw-mcp

# Install dependencies
npm install

# Build the MCP server
npm run build

# Start server (default port 3000)
npm run serve
```

### Option C: Using McPorter (Skill Management)

```bash
# Install McPorter for managing MCP servers
npm install -g @clawcli/mcporter

# Use to discover and install MCP servers
mcporter discover
```

---

## ⚙️ Step 3: Configure Server Access

Edit the MCP server configuration file:

```bash
# Create or edit config file
nano /etc/openclaw/mcp-server.config.json

# Add this configuration:
{
  "host": "0.0.0.0",
  "port": 3000,
  "allowCors": true,
  "logLevel": "info"
}
```

---

## 🚀 Step 4: Start MCP Server (Background Service)

```bash
# Method 1: Simple background run
nohup npx @openclaw/mcp --host 0.0.0.0 --port 3000 > /var/log/openclaw.log 2>&1 &

# Method 2: Systemd service (recommended for production)
sudo nano /etc/systemd/openclaw-mcp.service

# Add this service file:
[Unit]
Description=OpenClaw MCP Server
After=network.target

[Service]
Type=simple
User=your-username
WorkingDirectory=/var/openclaw
ExecStart=/usr/bin/npx @openclaw/mcp --host 0.0.0.0 --port 3000
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target

# Enable and start service
sudo systemctl daemon-reload
sudo systemctl enable openclaw-mcp
sudo systemctl start openclaw-mcp

# Check status
sudo systemctl status openclaw-mcp
```

---

## 🔌 Step 5: Configure AnythingLLM on Laptop

### Connect to OpenClaw MCP Server

1. **In AnythingLLM:**
   - Go to **Settings → Tools → MCP Servers**
   - Add new MCP server:
     - **Name:** OpenClaw Tools
     - **Endpoint:** `http://<SERVER-IP>:3000/mcp`
     - **Authentication:** None (or add API key if required)

2. **Select Tools:**
   - Browse available tools in the MCP server
   - Enable desired tools (Git, Docker, Files, APIs, etc.)

3. **Test Connection:**
   - Create a new agent
   - Ask agent to use a tool (e.g., "list files", "git clone")
   - Verify tools work from server

---

## 🛠️ Step 6: Install OpenClaw Skills (Optional)

```bash
# Install from ClawHub marketplace
npx @voltagent/clawhub install <skill-name>

# Popular skills to install:
npx @voltagent/clawhub install git-repo
npx @voltagent/clawhub install docker-tool
npx @voltagent/clawhub install file-manager
npx @voltagent/clawhub install slack-integration
npx @voltagent/clawhub install github-actions

# List available skills
npx @voltagent/clawhub browse
```

---

## ✅ Step 7: Verify Setup

```bash
# 1. Check if server is running
curl http://localhost:3000/mcp-tools
# Should list available MCP tools

# 2. Test from laptop
curl http://<SERVER-IP>:3000/mcp-tools

# 3. Check service status
sudo systemctl status openclaw-mcp

# 4. Monitor logs
sudo tail -f /var/log/openclaw.log
```

---

## 🔍 Troubleshooting Quick Fixes

| Issue | Solution |
|-------|----------|
| **Connection refused** | Ensure server port 3000 is open; check `netstat -tlnp \| grep 3000` |
| **CORS errors** | Set `allowCors: true` in config |
| **Tools not listed** | Restart MCP server: `sudo systemctl restart openclaw-mcp` |
| **Authentication failed** | Configure API key in server config |
| **Ollama not responding** | Verify Ollama on port 11434: `curl http://localhost:11434/api/version` |
| **Port in use** | Change port: `--port 3001` |

---

## 📦 Recommended First Skills

Install these 5 skills to get started:

```bash
# 1. Git operations
npx @voltagent/clawhub install git-repo-tool

# 2. Docker container management
npx @voltagent/clawhub install docker-tool

# 3. File system access
npx @voltagent/clawhub install file-manager-tool

# 4. Web scraping
npx @voltagent/clawhub install web-scraping-tool

# 5. System monitoring
npx @voltagent/clawhub install monitoring-tool
```

---

## 🌐 Alternative MCP Server Sources

If the main repository is unavailable, try these alternatives:

| Source | URL | Status |
|--------|-----|--------|
| **GitHub (freema)** | https://github.com/freema/openclaw-mcp | ✅ Active |
| **NPM Package** | https://www.npmjs.com/package/@openclaw/mcp | ✅ Available |
| **ClawHub Marketplace** | https://clawhub.ai/ | ✅ Active (48,000+ skills) |
| **McPorter** | https://mcporter.io/ | ✅ Skill management |
| **OpenClaw Docs** | https://docs.openclaw.ai/ | ✅ Up-to-date |

---

## 🔐 Security Checklist

- [ ] Firewall allows port 3000: `sudo ufw allow 3000/tcp`
- [ ] HTTPS enabled (if required): `npm install -g @openclaw/https-middleware`
- [ ] API keys rotated regularly
- [ ] Logs monitored: `sudo journalctl -u openclaw-mcp -f`
- [ ] Service auto-restart enabled: `sudo systemctl enable openclaw-mcp`

---

## 📞 Support Resources

- **Documentation:** https://docs.openclaw.ai/
- **GitHub Issues:** https://github.com/openclaw/openclaw/issues
- **ClawHub Skills:** https://clawhub.ai/
- **McPorter:** https://mcporter.io/
- **Model Context Protocol:** https://modelcontextprotocol.io/

---

## 💡 Next Steps

1. ✅ Install OpenClaw MCP server
2. ✅ Configure network access
3. ✅ Start service on Ubuntu server
4. ✅ Connect AnythingLLM on laptop
5. ✅ Install desired skills
6. ✅ Test agent with OpenClaw tools

---

> **Note:** This guide is based on current, active resources. Always verify URLs from the official OpenClaw documentation or GitHub.
> 
> **Created:** $(date +"%Y-%m-%d")
> **Version:** 1.0
> **Status:** Active & Working
