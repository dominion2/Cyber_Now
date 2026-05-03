import sys
import os
import numpy as np
from collections import Counter
from scipy.stats import kurtosis

class StreamSentinel:
    def __init__(self):
        # PHYSICAL LAWS: SPECIES PROFILES
        self.ideal_text = self._build_dist({32: 0.18, 101: 0.12, 116: 0.09, 97: 0.08, 111: 0.07})
        self.ideal_bin = self._build_dist({0: 0.35, 255: 0.08, 144: 0.04, 32: 0.04})
        
    def _build_dist(self, anchors):
        dist = np.zeros(256) + 1e-9
        for b, f in anchors.items(): dist[b] = f
        return dist / dist.sum()

    def find_long_rhythm(self, data, max_len=512):
        """Scans for long rhythmic pulses (like your 256-byte theory)."""
        iocs = []
        for length in range(1, max_len + 1):
            slice_data = data[::length]
            if len(slice_data) < 2: 
                iocs.append(0); continue
            counts = Counter(slice_data)
            ioc = sum(f * (f - 1) for f in counts.values()) / (len(slice_data) * (len(slice_data) - 1))
            iocs.append(ioc)
        
        # We look for the first significant spike above the noise floor
        avg_ioc = np.mean(iocs)
        for length, ioc in enumerate(iocs, 1):
            if ioc > avg_ioc * 1.45: return length
        return 1

    def solve_unbiased_alignment(self, slice_data):
        """Heavy Chi-Squared Alignment for low-density slices."""
        best_byte, min_chisq = 0, float('inf')
        n = len(slice_data)
        for k in range(256):
            counts = Counter([b ^ k for b in slice_data])
            observed = np.array([counts[i]/n for i in range(256)])
            score = min(np.sum(((observed - self.ideal_text)**2) / self.ideal_text),
                        np.sum(((observed - self.ideal_bin)**2) / self.ideal_bin))
            if score < min_chisq:
                min_chisq, best_byte = score, k
        return best_byte

    def autopsy_stream(self, file_list):
        """
        The Stream Engine: Joins multiple packets/files to 
        overcome the 256-byte statistical thinning.
        """
        print(f"🕵️ STREAM INVESTIGATION: Aggregating {len(file_list)} forensic samples...")
        
        full_stream = b""
        for f_path in file_list:
            with open(f_path, "rb") as f:
                full_stream += f.read()

        total_bytes = len(full_stream)
        print(f"📊 Total DNA Secured: {total_bytes} bytes.")

        # 1. Detect Rhythm
        L = self.find_long_rhythm(full_stream)
        print(f"📏 RHYTHM DETECTED: {L}-byte Mask")
        
        density = total_bytes / L
        print(f"📡 STATISTICAL DENSITY: {density:.1f} samples per mask-bin.")
        
        if density < 30:
            print("⚠️ WARNING: Density too low for 98.5% precision. Results may 'drift'.")

        # 2. Extract 256-byte Mask
        mask = [self.solve_unbiased_alignment(full_stream[i::L]) for i in range(L)]
        
        # 3. Output the verdict
        mask_hex = ' '.join([f"0x{b:02x}" for b in mask])
        print(f"🔑 EXTRACTED MASTER MASK: {mask_hex[:80]}...")
        
        # 4. Decrypt first 500 bytes of the stream for preview
        reality = bytes([full_stream[i] ^ mask[i % L] for i in range(min(total_bytes, 1000))])
        
        print("\n" + "="*60 + "\n📜 CORE REALITY PREVIEW:\n" + "="*60)
        print(reality.decode('ascii', errors='replace'))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("❌ Usage: python XOR_Stream.py file1.dat file2.dat file3.dat ...")
        sys.exit(1)

    # All arguments after the script name are treated as packet/file samples
    targets = sys.argv[1:]
    
    sentinel = StreamSentinel()
    sentinel.autopsy_stream(targets)
