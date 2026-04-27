# 🛡️ Analysis of IDAT/HijackLoader 2026 Variant: `UKqqACLUALIsaSR`

## 📊 Overview
This repository contains the technical deconstruction of an **IDAT/HijackLoader** variant identified in April 2026. The investigation leverages `radare2` to bypass multi-stage obfuscation, including environmental keying and SIMD-based encryption hidden within standard C++ exception handlers.

---

## 🛠️ Phase 1: Triage and Family Identification
Initial triage focused on identifying the binary's family using heuristic indicators and automated scanning.

### 1.1 Automated Detection (`hunt_idat.sh`)
The following custom bash script was utilized to automate the search for magic markers, steganographic chunks, and critical injection APIs across the target directory.

```bash
#!/bin/bash

# Define the target directory (defaults to current directory)
TARGET_DIR=${1:-.}

echo "--------------------------------------------------------"
echo "🔍 2026 IDAT/HijackLoader Multi-Stage Scanner"
echo "--------------------------------------------------------"

# Find all regular files, regardless of extension
find "$TARGET_DIR" -type f | while read -r file; do

    # 1. Check for PNG/IDAT Markers (Steganography)
    IDAT_CHECK=$(rabin2 -z "$file" 2>/dev/null | grep -iE "IDAT|IHDR")

    # 2. Check for Heaven's Gate (x86 -> x64 switch)
    HG_CHECK=$(r2 -q -c "/x EA........3300" "$file" 2>/dev/null | grep -v "not found")

    # 3. Check for April 2026 Specific Marker (0xEA79A5C6)
    MARKER_CHECK=$(r2 -q -c "/x C6A579EA" "$file" 2>/dev/null | grep -v "not found")

    # 4. Check for Critical Injection APIs
    API_CHECK=$(rabin2 -i "$file" 2>/dev/null | grep -iE "NtCreateSection|NtMapViewOfSection|InternetCheckConnectionW")

    # --- REPORTING ---
    if [[ -n "$IDAT_CHECK" || -n "$HG_CHECK" || -n "$MARKER_CHECK" || -n "$API_CHECK" ]]; then
        echo "[!] POTENTIAL LOADER DETECTED: $file"
        [[ -n "$IDAT_CHECK" ]]   && echo "  -> Found IDAT/PNG Chunks (Stego)"
        [[ -n "$HG_CHECK" ]]     && echo "  -> Found Heaven's Gate (32/64-bit switch)"
        [[ -n "$MARKER_CHECK" ]] && echo "  -> Found 2026 IDAT Marker (0xEA79A5C6)"
        [[ -n "$API_CHECK" ]]    && echo "  -> Found Suspect APIs: $(echo $API_CHECK | awk '{print $NF}' | tr '\n' ' ')"
        echo "--------------------------------------------------------"
    fi
done
echo "Done."
```

### 1.2 Contextual Analysis
* **Spoofing Target:** `CopilotFunnelTelemetry`
* **File Facade:** Microsoft `Telemetry.dll`
* **Logic:** The malware masquerades as an AI-assistant telemetry component to blend in with legitimate system traffic.

---

## 🔍 Phase 2: Behavioral Analysis with Radare2
Analysis targeted the identification of data gathering routines and the subsequent exfiltration pipeline.

### 2.1 Identifying the Data Source
* **Command:** `axt sym.imp.KERNEL32.dll_GetComputerNameW`
* **Logic:** Traced system identity gathering to find the entry point of the exfiltration logic. Identified the **Telemetry Dispatcher** at `0x18007e589`.

### 2.2 Reversing the Exfiltration Logic
The dispatcher finalizes a **264-byte (0x108)** buffer. Tracing control flow revealed an indirect jump to the primary encryption engine.
* **Engine Address:** `0x180003920`
* **Method:** Employs SIMD (SSE) instructions (`xorps`, `movups`) for 128-bit block XOR.
* **Evasion:** The routine is cloaked inside `VCRUNTIME140.dll` exception copy constructors (`___std_exception_copy`) to bypass behavioral EDR hooks.

---

## 🛡️ Phase 3: Breaking Indirect Addressing and Infrastructure Extraction
The final phase mapped the file overlay and identified the environmental keys used to unlock the C2 configuration.

### 3.1 Overlay Mapping
High-entropy data was located in the "slack space" immediately preceding the legitimate Microsoft Digital Signature.
* **Overlay Start:** `0x108000`
* **Signature Offset:** `0x108090`

### 3.2 Decrypting the C2 Configuration
The malware utilizes an indirect addressing table at `0x101200` containing relative offsets (Pointers) to protect against static IP extraction. The decryption key was derived from the first byte of the signature (`0x30` - ASN.1 Sequence Tag).

**Extracted Infrastructure:**
| Subnet | Ports | Role |
| :--- | :--- | :--- |
| `104.151.14.0/24` | 443, 19387 | Primary C2 VPS |
| `80.185.1.0/24` | 443 | Backup Command Node |
| `212.117.14.0/24` | 45499 | P2P Fallback / Proxy |

---

## 🏁 Conclusion and Detection Strategy
The IDAT/HijackLoader demonstrates high technical maturity. Effective detection requires:
1. **Network:** Monitor high-range ports (19000+) originating from signed Microsoft DLLs.
2. **Endpoint:** Flag usage of `VCRUNTIME140.dll` exceptions involving `XMM` register movements.
3. **File System:** Scan for non-PNG files containing `IDAT` chunks or the `0xEA79A5C6` marker.
