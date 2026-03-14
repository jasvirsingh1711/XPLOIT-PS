#!/usr/bin/env python3
"""
Patch the chal binary to bypass authentication
"""

import shutil
import struct

# Read the original binary
with open('/mnt/d/xploit/chal', 'rb') as f:
    binary = bytearray(f.read())

# The authentication check happens at 0x198c-0x1991
# It compares eax with 0x3e7 (999)
# cmp $0x3e7,%eax  => 3d e7 03 00 00
# jne 19b3         => 75 20 (jne = jump if not equal)

# We want to change it to always jump to the success path
# We can patch the jne instruction to be an unconditional jmp
# or change the comparison value

# Let's find the actual byte offset
# The instruction at 0x198c is: cmp $0x3e7,%eax
# In the file, we need to find this pattern

# Search for the pattern: 3d e7 03 00 00 75 20
pattern = bytes([0x3d, 0xe7, 0x03, 0x00, 0x00, 0x75, 0x20])
position = binary.find(pattern)

if position != -1:
    print(f"[+] Found auth check at file offset: 0x{position:x}")
    
    # Patch it: make the comparison happen with 1 instead of 999
    # Change: cmp $0x3e7,%eax to cmp $0x1,%eax
    # 0x3e7 = 999, 0x1 = 1
    # 3d e7 03 00 00 -> 3d 01 00 00 00
    
    patched = binary.copy()
    patched[position:position+5] = bytes([0x3d, 0x01, 0x00, 0x00, 0x00])
    
    # Save patched binary
    with open('/mnt/d/xploit/chal_patched', 'wb') as f:
        f.write(patched)
    
    print("[+] Patched binary saved as: chal_patched")
    print("[*] Changed comparison from 0x3e7 (999) to 0x1")
    
else:
    print("[-] Could not find the auth check pattern")
    print("[*] Trying alternative approach...")
    
    # Alternative: look for the pattern more generically and replace it
    # cmp with immediate 3d XX XX XX XX
    # Let's search for 3d e7 03
    pattern2 = bytes([0x3d, 0xe7, 0x03])
    position2 = binary.find(pattern2)
    
    if position2 != -1:
        print(f"[+] Found potential match at: 0x{position2:x}")
