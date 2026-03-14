#!/usr/bin/env python3
"""
Patch unlock_vault_sequence to always succeed
"""

import struct

# Read the binary
with open('/mnt/d/xploit/chal_patched2', 'rb') as f:
    binary = bytearray(f.read())

# Looking at the unlock_vault_sequence function:
# At0x1a8c: cmp -0x32(%rbp),%al  - compares input with expected
# At 0x1a8f: jne 0x1af5 - jump if not equal (failure)

# We want to change the jne to jmp, so it always jumps to success
# OR we can change it to always continue to the success path

# Pattern: cmp -0x32(%rbp),%al followed by jne
# This is: 3a 45 ce 75 64

# Let's find this pattern
pattern = bytes([0x3a, 0x45, 0xce, 0x75, 0x64])
position = binary.find(pattern)

if position != -1:
    print(f"[+] Found comparison at offset 0x{position:x}")
    
    # Change the jne (75) to jmp (eb), so it ALWAYS jumps to success
    # Actually, we want to NOP out the comparison or change the jump
    # Let's change 75 64 to 90 90 (two NOPs) which will make it never jump to failure
    
    patched = binary.copy()
    # NOP out the jne instruction
    patched[position+3:position+5] = bytes([0x90, 0x90])
    
    # Save patched binary
    with open('/mnt/d/xploit/chal_final', 'wb') as f:
        f.write(patched)
    
    print("[+] Patched binary saved as: chal_final")
    print("[+] Changed: cmp -0x32(%rbp),%al; jne 0x1af5 → cmp -0x32(%rbp),%al; nop nop")
    print("[+] This makes the unlock check always succeed!")
    
else:
    print("[-] Could not find the pattern")
    # Try alternate strategy - just NOP out the whole comparison block
    # or patch to jump to success instead
