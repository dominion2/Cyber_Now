# 🛡️ In-Depth IDAT/HijackLoader 2026 Deconstruction & Methodology

> A comprehensive, step-by-step technical roadmap detailing the command-line methodology used to deconstruct the 2026 IDAT/HijackLoader variant (`UKqqACLUALIsaSR`). This document explicitly connects radare2/rabin2 commands to the logical progression of the analysis.

## 📝 Table of Contents
1. [Phase 1: Triage and Family Identification](#-phase-1-triage-and-family-identification)
2. [Phase 2: Behavioral Analysis & Bypassing Obfuscation](#-phase-2-behavioral-analysis--bypassing-obfuscation)
3. [Phase 3: Breaking Indirect Addressing and Extraction](#-phase-3-breaking-indirect-addressing-and-extraction)
4. [Detection Strategy](#-detection-strategy)

---

## 🚀 Phase 1: Triage and Family Identification
**Goal:** Identify the binary's family using heuristic indicators and automated scanning without executing the payload.

### The Methodology & Commands
To determine what we were dealing with, we needed to hunt for known signatures of the 2026 IDAT variants. Instead of manual string searches, we built `hunt_idat.sh` using the radare2 tool suite to automate the triage across the file system.

1.  **Checking for Steganography (`rabin2 -z`):**
    * *Command:* `rabin2 -z "$file" | grep -iE "IDAT|IHDR"`
    * *Why:* `rabin2 -z` dumps all strings from the binary's data sections. We piped this to `grep` to look for "IDAT" or "IHDR". These are standard PNG chunk headers. Their presence in a PE (Portable Executable) file strongly suggests the loader is hiding its next-stage payload inside a fake or embedded PNG image, a classic HijackLoader technique.
2.  **Hexadecimal Signature Hunting (`r2 -c "/x"`):**
    * *Command:* `r2 -q -c "/x C6A579EA" "$file"`
    * *Why:* The `-q` flag runs radare2 quietly (no prompt), and `-c` executes a command. `/x` searches the binary for specific hex byte arrays. `C6A579EA` is a known magic marker used by this specific 2026 variant to denote the beginning of the encrypted payload.
3.  **API Import Triage (`rabin2 -i`):**
    * *Command:* `rabin2 -i "$file" | grep -iE "NtCreateSection|NtMapViewOfSection"`
    * *Why:* `rabin2 -i` lists the imported APIs. Seeing these specific NTDLL functions indicates the malware intends to perform Process Hollowing or MapView injection to execute its payload in memory.

### The Automation Script
```bash
#!/bin/bash
# 2026 IDAT/HijackLoader Multi-Stage Scanner
find "$TARGET_DIR" -type f | while read -r file; do
    IDAT_CHECK=$(rabin2 -z "$file" 2>/dev/null | grep -iE "IDAT|IHDR")
    HG_CHECK=$(r2 -q -c "/x EA........3300" "$file" 2>/dev/null | grep -v "not found")
    MARKER_CHECK=$(r2 -q -c "/x C6A579EA" "$file" 2>/dev/null | grep -v "not found")
    API_CHECK=$(rabin2 -i "$file" 2>/dev/null | grep -iE "NtCreateSection|NtMapViewOfSection|InternetCheckConnectionW")

    if [[ -n "$IDAT_CHECK" || -n "$HG_CHECK" || -n "$MARKER_CHECK" || -n "$API_CHECK" ]]; then
        echo "[!] POTENTIAL LOADER DETECTED: $file"
    fi
done
```

---

## 🧠 Phase 2: Behavioral Analysis & Bypassing Obfuscation
**Goal:** Trace data gathering routines and reverse the exfiltration pipeline by tracking the execution flow in radare2.

### Step 2.1: Identifying the Data Source
* **The Problem:** The malware was highly obfuscated, making it hard to find the main execution loop.
* **The Command:** `axt sym.imp.KERNEL32.dll_GetComputerNameW`
* **The Methodology:** We knew the malware had to profile the victim machine before phoning home. In radare2, `axt` (find code/data references to this address) allows us to work backward. By asking r2 "which functions call the API used to get the computer name?", we instantly bypassed the junk code and landed directly at the **Telemetry Dispatcher** at `0x18007e589`. We then used `s 0x18007e589` to seek to that address and `pdf` (print disassemble function) to map out the dispatcher's logic.

### Step 2.2: Reversing the Exfiltration Logic & SIMD Obfuscation
* **The Problem:** While tracing the dispatcher, standard XOR decryption loops were missing. Instead, execution kept jumping into standard C++ runtime libraries (`VCRUNTIME140.dll`).
* **The Methodology:** * By stepping through the execution (`ds` in radare2 debugging mode) into the `___std_exception_copy` constructor, we noticed unusual register usage. 
    * Using the `dr` (display registers) command, the 128-bit `XMM` registers were suddenly populated with high-entropy data.
    * Disassembling the exception handler revealed `xorps` and `movups` (SIMD instructions). The malware author intentionally cloaked their decryption routine inside an exception handler because EDRs (Endpoint Detection and Response) rarely hook these standard C++ functions due to performance overhead.

---

## 🛠️ Phase 3: Breaking Indirect Addressing and Extraction
**Goal:** Map the file overlay, identify environmental keys, and extract the C2 configuration from memory.

### Step 3.1: Overlay Mapping & Environmental Keying
* **The Problem:** The SIMD decryption routine required a dynamic seed.
* **The Command:** `rabin2 -O` (to check for overlays) and `iS` (list sections).
* **The Methodology:** Standard PE sections (like `.text`, `.data`) end at a specific offset. `rabin2 -O` revealed a massive chunk of data appended to the end of the file starting at `0x108000`—the "slack space." Exploring this space with `px 256 @ 0x108000` (print 256 hex bytes) showed high-entropy data followed by the Microsoft Digital Signature at `0x108090`. We observed the code reading the first byte of this signature (`0x30`, the ASN.1 SEQUENCE marker) and loading it into the SIMD decryption loop as the master key.

### Step 3.2: Uncovering the Indirect Addressing Table
* **The Problem:** Standard string dumps (`iz`) showed no IP addresses or domains.
* **The Command:** `pxw 32 @ 0x00101200`
* **The Methodology:** By tracing the memory registers post-decryption, we noticed the malware populating a table at `0x101200`. Running `px` (print hex) just showed garbage bytes. However, running `pxw 32` (print 32 hex words/DWORDs) revealed a repeating pattern of 4-byte structures. The malware was storing IPs not as strings (e.g., "104.151.14.0"), but as raw 32-bit integers.

### Step 3.3: Execution & IOC Generation (`findIP.py`)
To automate the extraction of these C2 nodes from the `pxw` output, we wrote the Python utility below. It uses `struct.pack("<I", val)` to natively translate the memory structures (little-endian integers) back into the 4-byte octets required for IPv4 routing. It identifies high-range networking ports by checking for specific Big-Endian marker bytes (`0xBB`, `0xB8`).

```python
import struct

# Data from radare2 'pxw 32 @ 0x00101200' output
raw_data = [
    0x000e9768, 0x0001b950, 0x0001bb4b, 0x000e904c,
    0x00101210, 0x0001bb50, 0x0001bbb1, 0x000e75d4
]

def decrypt_idat_table(data_list):
    print(f"{'Index':<6} | {'Original Hex':<12} | {'Decoded IP/Port Candidate'}")
    print("-" * 50)

    for i, val in enumerate(data_list):
        # Unpack as 4 bytes for IP analysis
        bytes_val = struct.pack("<I", val & 0xFFFFFFFF)

        # Check if it looks like a port (e.g., 443 is 0x01BB)
        if 0xBB in bytes_val or 0xB8 in bytes_val:
            decoded = f"PORT: {struct.unpack('>H', bytes_val[0:2])[0]}"
        else:
            decoded = f"IP: {'.'.join(map(str, bytes_val))}"

        print(f"{i:<6} | {hex(val):<12} | {decoded}")

decrypt_idat_table(raw_data)
```

**Extraction Output:**
```text
Index  | Original Hex | Decoded IP/Port Candidate
--------------------------------------------------
0      | 0xe9768      | IP: 104.151.14.0
1      | 0x1b950      | IP: 80.185.1.0
2      | 0x1bb4b      | PORT: 19387
3      | 0xe904c      | IP: 76.144.14.0
4      | 0x101210     | IP: 16.18.16.0
5      | 0x1bb50      | PORT: 20667
6      | 0x1bbb1      | PORT: 45499
7      | 0xe75d4      | IP: 212.117.14.0
```

---

## 🏁 Detection Strategy
- [ ] **Network:** Monitor high-range ports (19000-21000) and port 45499.
- [ ] **Endpoint:** Flag `VCRUNTIME140.dll` exceptions that utilize `XMM` registers for non-standard data processing.
- [ ] **File System:** Scan for the `0xEA79A5C6` marker within `Telemetry.dll` facades.
