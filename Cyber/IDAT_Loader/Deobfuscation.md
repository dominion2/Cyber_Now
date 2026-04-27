import os

# Define the master consolidated report content
master_report_md = """# 🛡️ Master Analysis Report: IDAT/HijackLoader Orchestrator
**Target Binary:** `UKqqACLUALIsaSR` (1.0 MB DLL)
**Associated Components:** `oXAAsaYOQC188UF` (19 KB Config)
**Date of Analysis:** April 26, 2026
**Classification:** Advanced Modular Loader / Stage 1 Orchestrator

---

## 📊 1. Overview
`UKqqACLUALIsaSR` is a sophisticated multi-stage loader identified in the April 2026 campaign. It functions as the "Engine" of the infection, responsible for environmental validation, component ingestion, and fileless execution of secondary stages.

## ⚙️ 2. Core Technical Architecture
The loader utilizes a "Syringe and Fuel" model, where the main DLL contains the logic but relies on external, encrypted files for configuration and payloads.

### 2.1 File Ingestion (The Syringe)
Static analysis of the Import Address Table (IAT) confirms its reliance on Windows File APIs to interact with local components:
* **`CreateFileW`**: Opens handles to hidden files like `oXAAsaYOQC188UF`.
* **`ReadFile`**: Ingests encrypted blobs into memory buffers for processing.

### 2.2 The SIMD Decryption Engine
The decryption routine (located at `0x180003920`) is a high-performance SIMD engine:
* **Architecture**: Uses x64 SSE/SIMD registers (`xmm0`, `xmm1`).
* **Instructions**: Employs `xorps` and `movups` for parallel 128-bit block processing.
* **Stealth**: The code is strategically placed within `VCRUNTIME140.dll` exception handling functions to evade heuristic detection of custom cryptography.

---

## 🔐 3. Cryptographic Layer Analysis
Our manual deconstruction revealed a two-layer protection mechanism on the associated stager files.

### 3.1 Layer 1: The "77UJ" Mask
We identified a repeating 4-byte XOR pattern used to hide strings from static scanners.
* **Key**: `0x3737554a` (ASCII: **`77UJ`**)
* **Result**: Applying this key to `oXAAsaYOQC188UF` reveals partially readable but jumbled ASCII (e.g., `neiulartatntnsi`).

### 3.2 Layer 2: Environmental Keying
The loader binds its execution to a specific digital signature.
* **Source**: The first byte of the Microsoft Digital Signature (`0x30` - ASN.1 Sequence tag).
* **Function**: This byte serves as a secondary seed for the SIMD engine. If the signature is removed, the "fuel" cannot be properly refined into executable code.

---

## 🌐 4. Network & Infrastructure (C2)
The loader manages communications through a "Secret Knock" protocol.
* **Beacon Subnets**: `104.151.14.0/24` and `80.185.1.0/24`.
* **Authentication**: The malware beacons its own certificate hash to the C2. The server refuses connections from clients that do not provide this specific "Microsoft/Redmond" signature metadata.
* **Camouflage**: Exfiltration is disguised as **Copilot/Telemetry** traffic over Port 443.

---

## 🛠️ 5. Forensic Reproduction Guide (Radare2)

### 5.1 Identifying File I/O
```bash
rabin2 -i UKqqACLUALIsaSR | grep -E \"CreateFile|ReadFile\"
