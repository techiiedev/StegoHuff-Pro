import heapq
import os
import json
from collections import Counter
from PIL import Image

# --- HUFFMAN LOGIC ---
class Node:
    def __init__(self, char, freq):
        self.char, self.freq = char, freq
        self.left = self.right = None
    def __lt__(self, other): return self.freq < other.freq

def huffman_compress(text):
    if not text: return "", {}
    freq = Counter(text)
    heap = [Node(c, f) for c, f in freq.items()]
    heapq.heapify(heap)
    while len(heap) > 1:
        l, r = heapq.heappop(heap), heapq.heappop(heap)
        merged = Node(None, l.freq + r.freq)
        merged.left, merged.right = l, r
        heapq.heappush(heap, merged)
    
    codes = {}
    def build_codes(node, current):
        if not node: return
        if node.char: codes[node.char] = current
        build_codes(node.left, current + "0")
        build_codes(node.right, current + "1")
    
    build_codes(heap[0], "")
    return "".join(codes[c] for c in text), codes

def huffman_decompress(binary, codes):
    rev = {v: k for k, v in codes.items()}
    res, cur = "", ""
    for bit in binary:
        cur += bit
        if cur in rev:
            res += rev[cur]
            cur = ""
    return res

# --- STEGANOGRAPHY LOGIC ---
def encode_stego(img_path, binary_data, code_map, output_path):
    # We embed the code map as JSON strings before the message so we can decode it later
    map_json = json.dumps(code_map)
    map_bin = ''.join(format(ord(c), '08b') for c in map_json)
    # Format: [Map Length (32 bits)] + [Map Binary] + [Message Binary] + [Delimiter]
    final_data = format(len(map_bin), '032b') + map_bin + binary_data + '1111111111111110'
    
    img = Image.open(img_path).convert("RGB")
    pixels = list(img.getdata())
    new_pixels = []
    idx = 0
    
    for p in pixels:
        p = list(p)
        for i in range(3):
            if idx < len(final_data):
                p[i] = p[i] & ~1 | int(final_data[idx])
                idx += 1
        new_pixels.append(tuple(p))
    
    img.putdata(new_pixels)
    img.save(output_path, "PNG")

def decode_stego(img_path):
    img = Image.open(img_path).convert("RGB")
    binary = "".join(str(p[i] & 1) for p in img.getdata() for i in range(3))
    
    map_len = int(binary[:32], 2)
    map_bin = binary[32:32+map_len]
    map_json = "".join(chr(int(map_bin[i:i+8], 2)) for i in range(0, len(map_bin), 8))
    code_map = json.loads(map_json)
    
    remaining = binary[32+map_len:]
    msg_bin = remaining.split('1111111111111110')[0]
    return huffman_decompress(msg_bin, code_map)