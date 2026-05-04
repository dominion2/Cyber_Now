import os
import zlib
import numpy as np
import pandas as pd
from scapy.all import PcapReader, IP, TCP, UDP
from scipy.stats import kurtosis
from collections import Counter

class ForensicDataSentry:
    def __init__(self, pcap_path):
        # Normalize path and handle quotes
        self.pcap_path = os.path.normpath(pcap_path.strip().replace('"', ''))
        self.flow_last_ts = {}  
        self.bytes_since_null = {}  
        self.packet_count = 0
        self.results = []

    def get_stats(self, payload):
        """
        Calculates mathematical markers for the 'Muscle' (payload).
        Returns: modal, kurtosis, state, compression_ratio
        """
        # THE SAFETY FLOOR: Mirroring Wireshark State 'C' logic
        if not payload or len(payload) < 4:
            return 0, 0.0000, 'C', 0.0000
        
        byte_arr = np.frombuffer(payload, dtype=np.uint8)
        
        # 1. MODAL: Find the most frequent byte
        modal = Counter(byte_arr).most_common(1)[0][0]
        
        # 2. KURTOSIS: Fisher's Excess Kurtosis (Normal = 0.0)
        k_val = float(kurtosis(byte_arr))
        
        # 3. COMPRESSION RATIO (Entropy Proxy)
        comp_len = len(zlib.compress(payload))
        comp_ratio = comp_len / len(payload)
        
        # 4. STATE ENGINE: X = Extreme (Encrypted/Obfuscated), B = Benign
        # Mirroring the Lua threshold (Entropy > 7.0 roughly equals CompR ~1.0)
        state = 'X' if comp_ratio > 0.90 else 'B'
        
        return modal, k_val, state, comp_ratio

    def run_audit(self):
        if not os.path.exists(self.pcap_path):
            print(f"❌ Path Error: {self.pcap_path} not found.")
            return

        print(f"\n📊 HIGH-PRECISION AUDIT: {os.path.basename(self.pcap_path)}")
        print("-" * 160)
        header = (f"{'Epoch Time':<16} | {'Destination':<15} | {'Port':<5} | "
                  f"{'Modal':<6} | {'Kurt':<9} | {'State':<5} | {'CompR':<9} | "
                  f"{'Rhythm':<10} | {'Buffer Gap'}")
        print(header)
        print("-" * 160)
        
        try:
            with PcapReader(self.pcap_path) as reader:
                for pkt in reader:
                    self.packet_count += 1
                    
                    if IP in pkt:
                        # 1. PROTOCOL AGNOSTIC EXTRACTION (Fixes 'Layer not found' error)
                        src, dst = pkt[IP].src, pkt[IP].dst
                        ts = float(pkt.time)
                        
                        # Extract Destination Port and Payload (The Muscle)
                        if TCP in pkt:
                            dport = pkt[TCP].dport
                            payload = bytes(pkt[TCP].payload)
                        elif UDP in pkt:
                            dport = pkt[UDP].dport
                            payload = bytes(pkt[UDP].payload)
                        else:
                            dport = 0
                            payload = b""

                        

                        # 2. CALCULATE BINARY MARKERS
                        modal, kurt, state, compr = self.get_stats(payload)
                        
                        # 3. SYNCED RHYTHM: IP-to-IP Key (Matches Lua V32)
                        flow_key = (src, dst)
                        rhythm = ts - self.flow_last_ts.get(flow_key, ts - 0.0001)
                        self.flow_last_ts[flow_key] = ts

                        # 4. BUFFER GAP TRACKING
                        if flow_key not in self.bytes_since_null:
                            self.bytes_since_null[flow_key] = 0
                        
                        gap_val = 0
                        gap_str = ""
                        if state == 'X' and modal == 0:
                            gap_val = self.bytes_since_null[flow_key]
                            gap_str = f"{gap_val:,} bytes"
                            self.bytes_since_null[flow_key] = 0 
                        else:
                            self.bytes_since_null[flow_key] += len(payload)

                        # 5. FORMATTING & PRECISION
                        modal_hex = f"0x{modal:02X}"
                        
                        

                        # Terminal Output
                        print(f"{ts:<16.6f} | {dst:<15} | {dport:<5} | "
                              f"{modal_hex:<6} | {kurt:<9.4f} | {state:<5} | {compr:<9.4f} | "
                              f"{rhythm:<10.4f}s | {gap_str}")

                        # Store results for CSV
                        self.results.append({
                            'Epoch': ts,
                            'Destination': dst,
                            'Source': src,
                            'Port': dport,
                            'ModalHex': modal_hex,
                            'Kurt': round(kurt, 4),
                            'State': state,
                            'CompR': round(compr, 4),
                            'Rhythm': round(rhythm, 4),
                            'BufferGap': gap_val
                        })
            
            # Save to Disk
            df = pd.DataFrame(self.results)
            df.to_csv("high_precision_audit.csv", index=False)
            print("-" * 160)
            print(f"✅ Audit Complete ({self.packet_count} pkts). Saved to 'high_precision_audit.csv'")

        except Exception as e:
            print(f"\n❌ Forensic Error: {e}")

if __name__ == "__main__":
    path = input("Enter PCAP path: ").strip()
    ForensicDataSentry(path).run_audit()
