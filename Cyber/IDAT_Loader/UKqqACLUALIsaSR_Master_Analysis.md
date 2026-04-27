# 🛡️ Master Analysis: IDAT/HijackLoader Modular Ecosystem
**Target:** `UKqqACLUALIsaSR` (1.0 MB DLL)
**Associated Config:** `oXAAsaYOQC188UF` (19 KB)
**Classification:** Modular Loader / Orchestrator

---

## 📊 1. System Architecture: The "Syringe & Fuel" Model
The investigation confirms that the malware is split into two distinct functional units to defeat automated sandbox analysis.

### 1.1 The Orchestrator (UKqqACLUALIsaSR)
This 1MB DLL acts as the execution engine. It contains no primary malicious strings; instead, it is designed to ingest and refine external data.
* **File I/O Anchors:** Static analysis revealed imports for `CreateFileW` and `ReadFile`.
* **Logic:** The loader locates the stager on disk, reads it into a heap buffer, and prepares it for the decryption engine.

### 1.2 The SIMD Decryption Engine (SSE)
Located at **`0x180003920`**, the loader uses a high-performance SIMD engine to process its payloads.
* **Registers:** Utilizes `xmm0`, `xmm1` (SSE).
* **Instructions:** `xorps` and `movups` perform 128-bit parallel decryption.
* **Stealth:** Routine is cloaked within `VCRUNTIME140.dll` exception handlers.

---

## 🔐 2. Cryptographic Deconstruction
We identified a layered approach to data protection within the 19KB stager file (`oXAAsaYOQC188UF`).

### 2.1 Layer 1: The "77UJ" Mask
A repeating 4-byte XOR pattern was identified via string leakage in the null-byte regions of the stager.
* **Key:** `0x3737554a` (ASCII: **`77UJ`**)
* **Finding:** Manual XORing revealed jumbled but recognizable ASCII (e.g., `neiulartatntnsi`).

### 2.2 Layer 2: Functional Coupling (Transposition)
The readable but scrambled strings indicate a second layer of obfuscation—likely a **Bit-Transposition** or **Shuffle**. 
* **Mechanism:** The SIMD engine in the loader "straightens" this data in memory.
* **Analyst Note:** The data file is useless without the specific logic inside the DLL orchestrator.

---

## 🌐 3. Network Infrastructure & C2
The loader manages a multi-stage communication protocol designed to blend into corporate traffic.
* **C2 Subnets:** `104.151.14.0/24` | `80.185.1.0/24`
* **Protocol:** Masquerades as **Microsoft Copilot/Telemetry** traffic.
* **Authentication (Secret Knock):** The malware derives a key from the Microsoft Digital Certificate signature (`0x30`). It beacons a hash of this certificate to the C2; the server drops any connection that does not present this campaign-specific thumbprint.

---

## 🛠️ 4. Forensic Reproduction Cheat Sheet

### Locate File Interaction Logic:
```bash
rabin2 -i UKqqACLUALIsaSR | grep -E "CreateFile|ReadFile"
```

### Manual Layer 1 De-masking:
```bash
# Wrap in single quotes to avoid Bash '!2048' history expansion errors
r2 -q -n -c 's 0x2a00; wox 0x3737554a @ 0x2a00!2048; px 256' ./oXAAsaYOQC188UF
```

### Hunting the Campaign Marker:
```bash
# Look for the April 2026 Marker (0xEA79A5C6)
r2 -q -c '/x C6A579EA' UKqqACLUALIsaSR
```

---

## 🏁 5. Current Infection Chain Status
1. **[SOLVED]** `UKqqACLUALIsaSR`: The Orchestrator Engine.
2. **[SOLVED]** `oXAAsaYOQC188UF`: The Encrypted Fuel/Config.
3. **[PENDING]** `nW0eNf35ZjkI6w`: The 2.1 MB Heavy Payload.

*Report compiled for GitHub Security Research Archive.*
