#!/usr/bin/env python3
"""
Improved patch: Redirect the call from user_authentication_module to unlock_vault_sequence
"""

import struct

# Read the original binary
with open('/mnt/d/xploit/chal', 'rb') as f:
    binary = bytearray(f.read())

# The call to user_authentication_module is at 0x1b7f
# call 1936 => e8 b2 fd ff ff
# We want to change it to call unlock_vault_sequence at 0x19f2

# Current instruction: e8 b2 fd ff ff at offset 0x1b7f
pattern = bytes([0xe8, 0xb2, 0xfd, 0xff, 0xff])
position = binary.find(pattern)

if position != -1:
    print(f"[+] Found call to user_authentication at file offset: 0x{position:x}")
    
    # Calculate the offset to unlock_vault_sequence (0x19f2)
    # The call instruction size is 5 bytes
    # Offset is relative to the next instruction
    # Next instruction would be at: position + 5 = 0x1b7f + 5 = 0x1b84
    
    instruction_addr = 0x1b7f
    next_addr = instruction_addr + 5
    target_addr = 0x19f2
    
    # Calculate relative offset
    rel_offset = target_addr - next_addr
    print(f"[*] Instruction at: 0x{instruction_addr:x}")
    print(f"[*] Next instruction at: 0x{next_addr:x}")
    print(f"[*] Target (unlock_vault_sequence) at: 0x{target_addr:x}")
    print(f"[*] Relative offset: 0x{rel_offset & 0xffffffff:x} ({rel_offset})")
    
    # Pack as little-endian signed 32-bit
    offset_bytes = struct.pack('<i', rel_offset)
    
    # Create the new call instruction: e8 + offset
    new_instr = bytes([0xe8]) + offset_bytes
    
    # Patch the binary
    patched = binary.copy()
    patched[position:position+5] = new_instr
    
    # Save patched binary
    with open('/mnt/d/xploit/chal_patched2', 'wb') as f:
        f.write(patched)
    
    print("[+] Patched binary saved as: chal_patched2")
    print(f"[+] Changed call target from 0x1936 (user_authentication_module) to 0x19f2 (unlock_vault_sequence)")
else:
    print("[-] Could not find the call instruction")
