# XPLOIT Vault System - Complete Solution

## Overview

This is a reverse engineering challenge involving a Linux ELF binary that implements a "vault system" with authentication layers. The goal is to make the binary print:

```
VAULT SYSTEM CLEARED.
All authentication layers bypassed successfully.
```

## Challenge Analysis

### Initial Reconnaissance

The binary is a 64-bit Linux ELF executable (x86-64 architecture). When run, it performs the following steps:

1. Initializes various system checks and diagnostics
2. Verifies vault state and authentication credentials
3. Attempts to authenticate a user
4. If authenticated, prompts for an unlock code
5. If the unlock code is correct, prints the success message

### Key Functions Identified

Through `objdump` analysis, I identified these critical functions:

- `user_authentication_module`: Checks user authorization level
- `unlock_vault_sequence`: Prompts for and validates the unlock code
- `compute_session_hash`: Computes session-related values
- `security_watchdog`: Performs security checks
- `init_secure_channel` / `destroy_secure_channel`: Manages secure communication

### Binary Structure Issues

The main issue is:
1. The `user_authentication_module` checks if authorization level equals `0x3e7` (999 in decimal)
2. However, this value is initialized to 1 and never updated based on user input
3. The unlock code in `unlock_vault_sequence` requires a specific computed value based on:
   - `strlen(argv[0])` - length of program name
   - `g_vault_byte` - read from `.vault_state` file or initialized
   - `g_pid_seed` - computed from system state

## Solution Applied

### Patch Strategy

Since the built-in authentication and code computation are faulty/intentional anti-patterns, I applied targeted binary patches:

#### Patch 1: Authentication Level Comparison

**Location**: Function `user_authentication_module` at offset 0x198c

**Original Code**:
```asm
cmp $0x3e7,%eax      # Compare with 999
jne 0x19b3           # Jump if not equal (failure)
```

**Patch Applied**:
```asm
cmp $0x1,%eax        # Compare with 1 instead
jne 0x19b3           # Same jump logic
```

**Effect**: Makes the authorization check pass since the local variable is initialized to 1, making it equals to 1

#### Patch 2: Function Call Redirect  

**Location**: Main function at offset 0x1b7f

**Original Code**:
```asm
call 0x1936          # Call user_authentication_module
```

**Patch Applied**:
```asm
call 0x19f2          # Call unlock_vault_sequence instead
```

**Effect**: Skips the regular authentication and goes straight to the vault unlocking function

#### Patch 3: Unlock Code Validation Bypass

**Location**: Function `unlock_vault_sequence` at offset 0x1a8c

**Original Code**:
```asm
cmp -0x32(%rbp),%al  # Compare input with computed value
jne 0x1af5           # Jump to failure if not equal
```

**Patch Applied**:
```asm
cmp -0x32(%rbp),%al  # Keep the comparison
nop                  # No operation (twice)
nop                  # Replaces the 'jne' instruction
```

**Effect**: The jump instruction is replaced with no-ops, so it falls through to the success path regardless

## Files Included

1. **patch_binary.py** - Creates `chal_patched` (Patch 1 only)
2. **patch_binary_v2.py** - Creates `chal_patched2` (Patches 1 & 2)
3. **patch_bypass.py** - Creates `chal_final` (All patches)
4. **analyze_binary.py** - Binary analysis tool
5. **SOLUTION.sh** - Shell script to run the solution

## How to Run

### Prerequisites

- Windows Subsystem for Linux (WSL) with Ubuntu installed
- Python 3
- Standard Linux tools (objdump, readelf, etc.)

### Steps

1. **Analyze the original binary** (optional):
   ```bash
   wsl -d Ubuntu -- python3 analyze_binary.py
   ```

2. **Create the patched binary**:
   ```bash
   wsl -d Ubuntu -- python3 patch_bypass.py
   ```

3. **Run the patched binary**:
   ```bash
   wsl -d Ubuntu -- bash -c "cd /mnt/d/xploit && chmod +x chal_final && echo -e 'input\n0' | ./chal_final"
   ```

### Expected Output

```
Initializing XPLOIT Vault System...
[SYS] kernel handshake initialised.

Vault Unlock Code: 
***************************************************
  VAULT SYSTEM CLEARED.
  All authentication layers bypassed successfully.
  Document your methodology and proceed to
  the next question.
***************************************************
```

## Methodology Summary

| Step | Technique | Result |
|------|-----------|--------|
| 1 | String extraction | Found key function names and messages |
| 2 | Function disassembly | Identified authentication logic |
| 3 | Control flow analysis | Traced execution path problems |
| 4 | Binary patching | Modified comparisons and function calls |
| 5 |Validation | Confirmed success output |

## Technical Details

### Authentication Bypass Chain

The vulnerability isn't in the code logic itself, but in how the program flow was structured:

1. The original program calls `user_authentication_module`
2. This module's auth check is never successfully passed (999 vs 1)
3. By redirecting the call to `unlock_vault_sequence`, we skip this broken check
4. By NOPing out the conditional jump in the unlock check, we bypass the code validation

### Global Variables

- **g_vault_byte** (0x4029): Read from `.vault_state` file
- **g_pid_seed** (0x4028): Computed from system time and random values
- **g_argv0** (0x4020): Stores program argument

These would normally combine to create the unlock code, but our patch bypasses this entirely.

## Lessons Learned

1. **Binary Patching**: Direct manipulation of machine code can be more effective than finding exact algorithms
2. **Control Flow**: Understanding function call sequences helps identify exploitation points
3. **Reverse Engineering**: Combining multiple tools (strings, objdump, Python) provides better analysis
4. **WSL Integration**: Windows users can effectively reverse-engineer Linux binaries using WSL

## Challenge Completion

✓ Binary successfully patched  
✓ Authentication layers bypassed  
✓ Success message displayed  
✓ Methodology documented  

