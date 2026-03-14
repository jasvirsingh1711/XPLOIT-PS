#!/usr/bin/env python3
"""
XPLOIT Vault System - Binary Analysis Tool
Reverse engineer the 'chal' binary to find and bypass authentication
"""

import sys
import struct

def read_elf_header(data):
    """Parse ELF header"""
    if data[:4] != b'\x7fELF':
        print("[-] Not an ELF file")
        return None
    
    # ELF header structure for 64-bit
    ei_class = data[4]  # 1 = 32-bit, 2 = 64-bit
    ei_data = data[5]   # 1 = little-endian, 2 = big-endian
    ei_version = data[6]
    
    print(f"[+] ELF Header:")
    print(f"    Class: {'64-bit' if ei_class == 2 else '32-bit'}")
    print(f"    Endianness: {'Little-endian' if ei_data == 1 else 'Big-endian'}")
    
    # Read e_entry (entry point) - offset 24, 8 bytes for 64-bit
    if ei_data == 1:  # little-endian
        entry_point = struct.unpack('<Q', data[24:32])[0]
    else:
        entry_point = struct.unpack('>Q', data[24:32])[0]
    
    print(f"    Entry Point: 0x{entry_point:x}")
    
    return {
        'class': ei_class,
        'endianness': ei_data,
        'entry_point': entry_point
    }

def extract_strings(data):
    """Extract readable ASCII strings from binary"""
    strings_list = []
    current_string = b''
    
    for byte in data:
        if 32 <= byte <= 126:  # Printable ASCII
            current_string += bytes([byte])
        else:
            if len(current_string) >= 4:  # Minimum string length
                strings_list.append(current_string.decode('ascii', errors='ignore'))
            current_string = b''
    
    return strings_list

def find_patterns(data):
    """Look for common patterns in binary"""
    print("\n[+] Searching for interesting patterns...")
    
    # Look for common strings
    strings = extract_strings(data)
    
    # Print strings that might be related to vault/auth
    interesting_keywords = ['vault', 'auth', 'key', 'code', 'unlock', 'clear', 
                           'pass', 'secret', 'check', 'verify', 'fail', 'success']
    
    print("\n[+] Potentially interesting strings found:")
    for s in strings:
        s_lower = s.lower()
        if any(keyword in s_lower for keyword in interesting_keywords):
            print(f"    > {s}")
        if len(s) > 15:  # Long strings might be clues
            print(f"    > {s}")

def main():
    try:
        with open('chal', 'rb') as f:
            binary_data = f.read()
        
        print("[*] Analyzing chal binary...")
        print(f"[+] Binary size: {len(binary_data)} bytes\n")
        
        # Parse ELF header
        elf_info = read_elf_header(binary_data)
        
        # Find patterns
        find_patterns(binary_data)
        
        # Look for common function signatures
        print("\n[+] Looking for function patterns...")
        
        # Exit successfully
        print("\n[*] Analysis complete!")
        
    except Exception as e:
        print(f"[-] Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
