# 🕵️‍♂️ Pre-Disassembly Triage Workflow: IDAT/HijackLoader 2026

## 📖 Overview
Before diving into low-level assembly with debuggers or advanced reverse engineering frameworks like Radare2, it is critical to perform static analysis and triage. This phase establishes the malware's footprint, uncovers Indicators of Compromise (IOCs), and dictates the entire direction of the investigation.

Below is the complete, step-by-step workflow used to analyze the IDAT/HijackLoader 2026 variant (UKqqACLUALIsaSR), including the rationale for each tool.

---

## 🛠️ Step-by-Step Triage Methodology

### 1. File Type Identification (`file`)
Malware authors frequently spoof file extensions (e.g., naming an executable `.txt` or `.png`).
* **Command Used:** `file *`
* **Why we used it:** To read the "magic bytes" at the start of each file, revealing how the OS actually interprets them. 
* **Discovery:** Revealed that the Stage 2 Config Fuel (`oXAAsaYOQC188UF`) was raw data, while other components were standard PE32+ Windows DLLs.

### 2. Entropy & Embedded Data Scanning (`binwalk`)
High entropy indicates packing, encryption, or compression.
* **Command Used:** `binwalk -E <filename>` and `binwalk <filename>`
* **Why we used it:** To check for high-entropy sections and hidden components appended to the files.
* **Discovery:** Confirmed the Stage 2 payload was heavily obfuscated/encrypted and hinted at the steganographic nature of the loader.

### 3. Automated Marker Hunting (`hunt_idat.sh`)
Once hidden data is suspected, we must hunt for specific architectural markers.
* **Tools Used:** `find`, `grep`, `xxd`/`hexdump` (via custom Bash script)
* **Why we used it:** To specifically hunt for steganographic PNG chunk headers (`IDAT`) and the magic marker `0xEA79A5C6` used by the malware to locate its payload.
* **Discovery:** Allowed us to rapidly separate legitimate files from malicious loaders across the entire directory.

### 4. String & Plain-Text Extraction (`strings` / `rabin2 -z`)
Malware often leaves accidental plain-text indicators or artifacts.
* **Command Used:** `strings <filename>` or `rabin2 -z <filename>`
* **Why we used it:** To dump human-readable ASCII and Unicode characters before decompilation.
* **Discovery:** Uncovered the repeated `77UJ` pattern in padding regions, which we later used to partially decrypt the configuration file (revealing `neiulartatntnsi`).

### 5. PE Header Parsing (EAT/IAT) (`winedump` / `objdump`)
Understanding what legitimate Windows APIs a binary claims to use provides insight into its capabilities.
* **Command Used:** `winedump -j export <filename>` / `winedump -j import <filename>`
* **Why we used it:** To dump the Export and Import Address Tables (EAT/IAT).
* **Discovery:** Found imports like `InternetCheckConnectionW`, giving an immediate clue that the malware performs internet connectivity checks for sandbox evasion.

### 6. Certificate & Signature Extraction (`osslsigncode` & `openssl`)
The malware masqueraded as a legitimate Microsoft Visual C++ component.
* **Command Used:** `osslsigncode extract-signature <file> <out.p7b>` followed by `openssl pkcs7 -print_certs ...`
* **Why we used it:** To extract the PKCS#7 digital signature and parse its certificate to see if it was forged or stolen.
* **Discovery:** Led to the discovery of "Environmental Binding"—the malware used the first byte of the signature (ASN.1 Sequence Tag `0x30`) as the cryptographic seed to decrypt its configuration.

### 7. High-Level Decompilation & Flow Override (`Ghidra`)
Before reading raw assembly, high-level pseudocode helps map the general logic flow.
* **Tool Used:** Ghidra (GUI and Decompiler)
* **Why we used it:** To analyze the `InternetCheckConnectionW` sandbox evasion loop. 
* **Discovery & Action:** The malware used indirect jumps (`JMP qword ptr`) to break decompilers, resulting in a *"Could not recover jumptable"* error. We manually applied a **"Flow Override"** in Ghidra, changing the indirect jump to a `CALL`. This forced the decompiler to successfully generate clean C-like pseudocode.

---
*Document generated as part of the Cyber_Now / IDAT_Loader analysis series.*
