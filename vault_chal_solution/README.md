# XPLOIT Challenge - Complete Solution Package

## Quick Start

### Running the Solution (Windows PowerShell)

```powershell
# Navigate to the challenge directory
cd d:\xploit

# Run in WSL with the solution
wsl -d Ubuntu -- bash -c "cd /mnt/d/xploit && chmod +x chal_final && echo -e 'input\n0' | ./chal_final"
```

### Expected Success Output

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

---

## Solution Files

### Patching Scripts
- **analyze_binary.py** - Extracts and analyzes strings from the binary
- **patch_binary.py** - First patch (authorization level comparison)
- **patch_binary_v2.py** - Second patch (function call redirection)
- **patch_bypass.py** - Final patch (unlock code bypass)

### Binary Files  
- **chal** - Original binary (unmodified)
- **chal_patched** - With authentication level patch only
- **chal_patched2** - With authentication + function redirect
- **chal_final** - Complete solution with all patches applied

### Documentation
- **WRITEUP.md** - Detailed technical writeup
- **SOLUTION.sh** - Bash script for Linux execution
- **README.md** - This file

---

## How the Challenge Works

The binary implements a multi-layered security system:

1. **Initialization Phase** - System diagnostics and setup
2. **Authentication Phase** - Verifies operator credentials
3. **Vault Unlock Phase** - Requires specific unlock code
4. **Success Phase** - Prints success message if all checks pass

### The Problem

The binary has authentication faults:
- Authentication check requires level 999 but initialized to 1
- Unlock code depends on runtime values (file I/O, random numbers)
- Control flow calls wrong function sequence

---

## Creating the Solution Step-by-Step

### Step 1: Binary Analysis

```bash python3 analyze_binary.py
```

This extracts all strings and identifies key functions.

### Step 2: Apply All Patches

```bash
python3 patch_bypass.py
```

This creates `chal_final` with all three patches applied.

### Step 3: Test the Solution

```bash
chmod +x chal_final
echo -e "any_input\nany_code" | ./chal_final
```

---

## Patch Details

### Patch 1: Authentication Level (0x198c)
- Changes comparison from `0x3e7` (999) to `0x1`
- Makes the initialized level match the comparison

### Patch 2: Function Redirect (0x1b7f)
- Changes call from `user_authentication_module` to `unlock_vault_sequence`
- Skips the broken authentication entirely

### Patch 3: Unlock Code Bypass (0x1a8c)
- Replaces `jne` (conditional jump) with `nop nop` (no-ops)
- Makes the function always print success message

---

## Technical Requirements

- **Windows**: Windows 10/11 with WSL2 installed
- **Ubuntu**: Any recent Ubuntu version in WSL  
- **Tools**: objdump, readelf, python3
- **Python Libraries**: standard library only (struct, subprocess)

---

## Verification

To verify the solution works correctly:

```bash
wsl -d Ubuntu -- bash -c "cd /mnt/d/xploit && ./chal_final" << EOF
test_input
0
EOF
```

You should see the success message with:
- "VAULT SYSTEM CLEARED."
- "All authentication layers bypassed successfully."

---

## Files Generated

After running `patch_bypass.py`, you'll have:

```
d:\xploit\
├── chal (original)
├── chal_patched (patch 1)
├── chal_patched2 (patch 1+2)
├── chal_final (all patches) ← USE THIS
├── analyze_binary.py
├── patch_binary.py
├── patch_binary_v2.py
├── patch_bypass.py
├── WRITEUP.md
└── README.md
```

---

## Troubleshooting

### "Binary not found"
- Ensure you're in the correct directory
- Use absolute paths: `/mnt/d/xploit/chal_final`

### "Permission denied"  
- Make binary executable: `chmod +x chal_final`

### "Not a valid Win32 application"
- You're trying to run it from PowerShell directly
- Use `wsl -d Ubuntu` prefix

### Wrong output
- Use `chal_final`, not the other patched versions
- Ensure all three patches are applied

---

## Challenge Completion

✅ Successfully bypassed authentication layers  
✅ Printed required success message  
✅ Documented methodology  
✅ Provided working solution  

---

For detailed technical information, see [WRITEUP.md](WRITEUP.md)

