import sys
import os
import numpy as np
from collections import Counter
from scipy.stats import kurtosis

class RecursiveForensicSentinel:
    def __init__(self):
        # --- PHYSICAL LAWS: SPECIES PROFILES ---
        
        # Profile A: Human Language (ETAOIN + Space)
        self.ideal_text = np.zeros(256) + 1e-9
        text_anchors = {32: 0.17, 101: 0.12, 116: 0.09, 97: 0.08, 111: 0.07, 105: 0.07, 110: 0.06, 115: 0.06}
        for b, f in text_anchors.items(): self.ideal_text[b] = f
        self.ideal_text /= self.ideal_text.sum()

        # Profile B: Machine Code (Nulls + Headers + NOPs)
        self.ideal_binary = np.zeros(256) + 1e-9
        binary_anchors = {0: 0.30, 255: 0.05, 32: 0.05, 144: 0.03, 72: 0.02, 85: 0.02}
        for b, f in binary_anchors.items(): self.ideal_binary[b] = f
        self.ideal_binary /= self.ideal_binary.sum()

        # Heuristic Constants
        self.printable_range = range(32, 127)
        self.whitespace = [10, 13, 9]

    def get_printable_ratio(self, data):
        """Measures how close the buffer is to 'ASCII Reality'."""
        if not data: return 0
        printable = sum(1 for b in data if b in self.printable_range or b in self.whitespace)
        return printable / len(data)

    def find_fundamental_rhythm(self, data, max_len=64):
        """
        Detects key length using Index of Coincidence.
        Filters out harmonics to find the fundamental frequency.
        """
        iocs = []
        for length in range(1, max_len + 1):
            slice_data = data[::length]
            if len(slice_data) < 2: 
                iocs.append(0); continue
            counts = Counter(slice_data)
            n = len(slice_data)
            ioc = sum(f * (f - 1) for f in counts.values()) / (n * (n - 1))
            iocs.append(ioc)
        
        # Fundamental Law: We look for the FIRST peak that is 40% above the average
        avg_ioc = np.mean(iocs)
        for length, ioc in enumerate(iocs, 1):
            if ioc > avg_ioc * 1.4:
                return length
        return 1

    def align_slice_unbiased(self, slice_data):
        """
        Extracts a single mask byte by testing against 
        ALL physical species profiles (Chi-Squared).
        """
        best_byte, min_chisq = 0, float('inf')
        n = len(slice_data)

        for candidate_key in range(256):
            decrypted = [b ^ candidate_key for b in slice_data]
            counts = Counter(decrypted)
            observed = np.array([counts[i]/n for i in range(256)])
            
            # Distance from Physical Laws
            dist_text = np.sum(((observed - self.ideal_text)**2) / self.ideal_text)
            dist_bin = np.sum(((observed - self.ideal_binary)**2) / self.ideal_binary)
            
            current_min = min(dist_text, dist_bin)
            if current_min < min_chisq:
                min_chisq, best_byte = current_min, candidate_key
        return best_byte

    def solve_layer(self, data):
        """Identifies and extracts one layer of XOR masking."""
        L = self.find_fundamental_rhythm(data)
        mask = [self.align_slice_unbiased(data[i::L]) for i in range(L)]
        return mask, L

    def peel_layers(self, data, max_layers=5, current_layer=1):
        """
        The Recursive Sentinel: Continues peeling until ASCII 
        Reality is found or max depth is reached.
        """
        ratio = self.get_printable_ratio(data)
        k_val = kurtosis(list(data))
        
        print(f"\n--- [ ANALYSIS LAYER {current_layer} ] ---")
        print(f"📊 Current State: Printable Ratio: {ratio:.1%}, Kurtosis: {k_val:.2f}")

        # STOP CONDITION: If we have reached readable ASCII text
        if ratio > 0.88:
            print(f"✨ REALITY SECURED: Final Reconstruction follows.")
            return data

        if current_layer > max_layers:
            print("🚫 EXHAUSTED: Maximum layer depth reached. Fantasy is too deep.")
            return data

        # CRACKING: Perform unbiased extraction for this layer
        mask, L = self.solve_layer(data)
        print(f"📏 Detected Rhythm: {L}-byte Mask")
        print(f"🔑 Extracted Key: {' '.join([hex(b) for b in mask])}")
        
        # APPLYING: Create the input for the next recursive step
        unmasked_buffer = bytes([data[i] ^ mask[i % L] for i in range(len(data))])

        # RECURSE: Dive into the next potential layer
        return self.peel_layers(unmasked_buffer, max_layers, current_layer + 1)

# --- EXECUTION ENTRY POINT ---
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ Usage: python XOR_Heavy.py <malicious_file.dat>")
        sys.exit(1)

    target_file = sys.argv[1]
    if not os.path.exists(target_file):
        print(f"❌ Error: {target_file} not found.")
        sys.exit(1)

    with open(target_file, "rb") as f:
        raw_data = f.read()

    print(f"🕵️ Heavy Sentinel deploying on {len(raw_data)} bytes of data.")
    
    sentinel = RecursiveForensicSentinel()
    final_reality = sentinel.peel_layers(raw_data)

    print("\n" + "="*60)
    print("📜 FINAL FORENSIC RECONSTRUCTION:")
    print("="*60)
    
    try:
        # Final Species Check for Display
        if sentinel.get_printable_ratio(final_reality) > 0.5:
            print(final_reality.decode('ascii', errors='replace'))
        else:
            # If still binary (shellcode), show hex dump
            for i in range(0, min(len(final_reality), 512), 16):
                chunk = final_reality[i:i+16]
                print(f"{i:08x}  {chunk.hex(' ', 1)}  |{chunk.decode('ascii', errors='ignore')}|")
    except:
        print(final_reality.hex(' ', 16))
