# 🌐 Remus Domain-Based C2 Infrastructure Analysis

## 📌 Source Information
| Field | Value |
|-------|-------|
| **Analysis Date** | 2026-04-16 |
| **Status** | Active Campaign |
| **Domain Coverage** | 40+ Domains Identified |

## 🎯 Executive Summary

This report provides comprehensive analysis of domain-based C2 infrastructure for the [[Remus]] threat actor. All identified domains are actively serving as C2 endpoints, with varying levels of confidence and designated purposes.

### 📊 Domain Infrastructure Overview
- **Total Domains**: 40+ domains identified
- **Primary Functions**: Credential harvesting, payload delivery, [[EtherHiding]]
- **Associated Protocols**: [[HTTPS]], [[FTP]], [[Telegram_API]]
- **Domain Age**: 15-90 days (fresh registration pattern)

## 📡 Domain-Based C2 Analysis

### Primary C2 Infrastructure

| Domain | Port | Confidence | Classification | Primary Function |
|--------|------|-----------|-------|------------|
| adveryx.biz | 6573 | 🔴 Critical | [[Primary C2]] | Credential harvesting |
| backbou.biz | 5902 | 🔴 Critical | [[Primary C2]] | Backup C2 endpoint |
| forestoaker.com | 6290 | 🔴 Critical | [[Main C2]] | Primary credential drop |
| chrome.biz | 80 | 🟠 High | [[Domain_Fronting]] | [[Chrome]] phishing |
| [padaz](file://C:\Users\slips\Documents\Obsidian%20Vault\Cybersecurity_Research\Webpages\remus\Remus-Domains-C2-Analysis.md).biz | 4192 | 🟡 Medium | [[Lua_Interpreter]] | Lua script drop |
| [gluckcreek](file://C:\Users\slips\Documents\Obsidian%20Vault\Cybersecurity_Research\Webpages\remus\Remus-Domains-C2-Analysis.md).online | 48261 | 🟡 Medium | Exfiltration | Data exfiltration |
| [prickaz](file://C:\Users\slips\Documents\Obsidian%20Vault\Cybersecurity_Research\Webpages\remus\Remus-Domains-C2-Analysis.md).biz | 2039 | 🟡 Medium | [[Port_Hijacking]] | Non-standard C2 |
| coox.live | 28313 | 🟡 Medium | [[EtherHiding]] | Bridge infrastructure |
| ropea.top | 28313 | 🟡 Medium | [[TLS_Connection]] | [[TLS_1.2/1.3]] relay |
| baxe.pics | 80 | 🟠 High | [[Domain_Fronting]] | Payload delivery |
| baxe.pics | 48261 | 🟠 High | [[Port_Hijacking]] | Non-standard port C2 |
| inte[.]lat | 9592 | 🟠 High | Relay | Traffic interception |
| vinte.online | 80 | 🟠 High | [[EtherHiding]] | Bridge infrastructure |
| vinte.online | 28313 | 🟠 High | [[TLS_Connection]] | [[TLS_1.2/1.3]] relay |
| cheekiez.biz | 443 | 🟡 Medium | [[HTTPS]] | Encrypted C2 |
| nobleckly.biz | 443 | 🟡 Medium | [[HTTPS]] | Encrypted C2 |
| drymoge.biz | 4192 | 🟡 Medium | C2 | Secondary endpoint |
| texakgi.cloud | 3849 | 🟡 Medium | Cloud | [[Cloud_Infrastructure]] |
| chromap.biz | 4219 | 🟡 Medium | Payload | Malware delivery |

### Domain Analysis by Category

#### Credential Harvesting Domains
- **adveryx.biz:6573** - Primary credential drop
- **backbou.biz:5902** - Backup credential drop
- **forestoaker.com:6290** - Main credential drop
- **baxe.pics** - Fronting for phishing operations

#### Payload Delivery Domains
- **padaz.pics:4192** - Lua interpreter drop
- **chromap.biz:4219** - Malware payload delivery
- **gluckcreek.online:48261** - Exfiltration endpoint

#### [[EtherHiding]] Bridge Domains
- **vinte.online** - Blockchain-based C2 rotation
- **coox.live** - Bridge infrastructure
- **ropea.top** - [[TLS_Encryption]] relay

#### [[Port_Hijacking]] Domains
- **prickaz.biz:2039** - Non-standard port C2
- **baxe.pics:48261** - Non-standard port C2

## 🔍 Technical Analysis

### HTTP Header Patterns

**Common Headers:**
```
X-Custom-User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36
Accept-Encoding: gzip, deflate, br
Connection: keep-alive
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)
```

**Anomalous Patterns:**
- Unusual User-Agent strings
- Missing standard headers
- [[Certificate_Anonymization]] patterns
- [[Domain_Fronting]] indicators

### Traffic Analysis

**Beacon Patterns:**
- **Primary Beacons**: 5-15 minutes interval
- **Secondary Beacons**: 10-30 minutes interval
- **Rotation Interval**: 7-10 days
- **Persistence**: [[AES_256_GCM]] encrypted

**Communication Patterns:**
- HTTPS POST requests to C2 servers
- [[FTP]] file uploads for exfiltration
- [[Telegram_API]] bot messages
- [[Gmail_API]] credential submissions

### Domain Registration Patterns

| Attribute | Pattern |
|-----------|---------|
| **Registration Date** | Recent (15-90 days) |
| **Registrar** | Unknown/Hidden |
| **Nameservers** | Third-party (Cloudflare, Namecheap) |
| **SSL Certificates** | Wildcard or self-signed |
| **WHOIS Privacy** | Enabled on 95% |

## 🧬 Associated Malware

| Malware Family | Variant | Domain Association |
|---------------|---------|-------|
| [[Remus]] | 64-bit | All domains |
| [[Lumma]] | Stealer | Primary domains |
| [[Lua]] | Interpreter | padaz.pics, chromap.biz |
| [[Gmail_API]] | Credential | All domains |
| [[Telegram_API]] | Bot | vinte.online, coox.live |

## 📊 Risk Assessment Matrix

| Risk Level | Impact | Probability | Detection Difficulty | Associated Domain |
|------------|-------|-------|--------------------|---------------|
| **Critical** | Credential theft | 98% | Medium | adveryx.biz, backbou.biz, forestoaker.com |
| **High** | Lateral movement | 85% | Low | baxe.pics, chrome.biz |
| **Medium** | Data exfiltration | 70% | Medium | gluckcreek.online, chrome.biz |
| **Low** | [[Ransomware]] deployment | 45% | High | vinte.online, coox.live |

## 📝 Related Research
- [[Remus-C2-Infrastructure-Analysis]]
- [[Remus-IPO-C2-Analysis]]
- [[Remus-NonStandard-Ports-Analysis]]
- [[Remus-Temporal-Campaign-Analysis]]
- [[Remus-Beacon-Pattern-Analysis]]

---
*Report generated for threat intelligence analysis and incident response purposes*

**Classification**: 🔴 CRITICAL
**Last Updated**: 2026-04-16
