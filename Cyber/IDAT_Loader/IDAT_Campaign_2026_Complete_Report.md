🛡️ Campaign Analysis Report: IDAT/HijackLoader Ecosystem
Campaign Date: April 2026
Threat Actor Profile: Sophisticated / Evasive (Multi-Stage Loading)
Total Components Analyzed: 3

📊 1. Executive Summary
This campaign utilizes a modular "Refinery" model to deliver a high-entropy payload to a victim machine. The attack is split into three distinct files: an Orchestrator (DLL), a Configuration Blob, and an Encrypted Cargo. This separation ensures that no single file triggers traditional heuristic alarms.

⚙️ 2. Component Analysis
2.1 Stage 1: The Orchestrator (UKqqACLUALIsaSR)
Role: The Execution Engine.

Technical Profile: 1.0 MB x64 DLL.

Key Functionality:

Environmental Binding: Uses the first byte of its own Digital Signature (0x30) as a cryptographic seed.

Vectorized Decryption: Implements a high-performance SIMD/SSE engine at 0x180003920 using xorps and movups instructions to process 128-bit data blocks.

Persistence: Masquerades as a legitimate component of the VC++ Runtime environment.

2.2 Stage 2: The Config Fuel (oXAAsaYOQC188UF)
Role: Campaign Directions & C2 Config.

Technical Profile: 19 KB Data file.

Obfuscation Discovery Logic:

Initial Triage: file identified as raw data; binwalk showed high entropy.

The Mask: Identified a 4-byte repeating pattern (77UJ / 0x3737554a) leaked through original null-byte padding regions.

Decryption: XORing with 77UJ revealed jumbled ASCII (neiulartatntnsi), proving a secondary bit-transposition layer.

2.3 Stage 3: The Heavy Payload (nW0eNf35ZjkI6w)
Role: Final Malicious Cargo (Likely LummaC2/Stealer).

Technical Profile: 2.1 MB Data file.

Detection Markers:

Synchronization: Identified the Ghostpulse/IDAT marker C6 A5 79 EA at offset 0x4056.

Dynamic Encryption: Uses a unique session key starting at 0x405a (78 83 76 8a), confirming it is compartmentalized from the Stage 2 key.

Payload Features: Contains a massive encrypted string table (detected at 0x37e4) for API and C2 concealment.

🌐 3. Infrastructure & IOCs
C2 Subnets: 104.151.14.0/24, 80.185.1.0/24.

Traffic Profile: Exfiltration disguised as Port 443 Copilot/Telemetry traffic.

Authentication: "Secret Knock" thumbprint requirement; C2 validates client's digital certificate hash before responding.

🛠️ 4. Forensic Reproduction Toolkit (Radare2)
Locate Campaign Marker:
Bash
r2 -q -c "/x C6A579EA" ./nW0eNf35ZjkI6w
Unmask Config Layer 1:
Bash
r2 -q -n -c 's 0x2a00; wox 0x3737554a @ 0x2a00!2048; px 256' ./oXAAsaYOQC188UF
Analyze SIMD Entry Point:
Bash
r2 -q -c "pdf @ 0x180003920" UKqqACLUALIsaSR
🏁 5. Conclusion
The 2026 IDAT campaign represents a high level of technical maturity, specifically focusing on Functional Coupling (making files useless without each other) and Environmental Keying (binding execution to the digital signature). Defensive teams should focus on monitoring the SIMD-based decryption routines in memory rather than disk-based signatures.

Final Consolidated Report for GitHub Security Research Archive.
