rule Win_IDAT_Ghostpulse_Campaign_2026 {
    meta:
        description = "Detects IDAT/Ghostpulse multi-stage loader and payloads from the April 2026 campaign"
        author = "Forensic Analyst"
        date = "2026-04-26"
        reference = "Internal Analysis of UKqqACLUALIsaSR"
        severity = "Critical"

    strings:
        // 1. The Stage 3 Synchronization Marker (Ghostpulse/IDAT)
        $idat_marker = { C6 A5 79 EA }

        // 2. Decoy Header Strings (Keyboard-mashed ASCII padding)
        $decoy_padding_1 = "ttcsseieesnnwrrl" ascii wide
        $decoy_padding_2 = "meletncnekattnoc" ascii wide
        
        // 3. The Stage 2 Config XOR Key (77UJ)
        $config_key = { 37 37 55 4a } 

        // 4. SIMD/SSE Decryption Engine Pattern
        // Looking for xorps (0F 57) and movups (0F 10) logic found in Loader
        $simd_routine = { 0F 10 ?? 0F 57 ?? 0F 11 ?? }

    condition:
        // Detect Stage 1 Orchestrator
        (uint16(0) == 0x5A4D and $simd_routine) or
        
        // Detect Stage 2 or Stage 3 Encrypted Components
        ($idat_marker and any of ($decoy_padding*)) or
        
        // General identification of the campaign config
        ($config_key and #config_key > 10)
}
