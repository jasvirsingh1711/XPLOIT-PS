import sys

def run_wut(code):
    stack = []
    pc = 0

    # Precompute jumps for loops (& and *)
    jump_map = {}
    loop_stack = []
    for i, char in enumerate(code):
        if char == '&':
            loop_stack.append(i)
        elif char == '*':
            start = loop_stack.pop()
            jump_map[start] = i
            jump_map[i] = start

    print("Output: ", end="")
    
    # Execute the code
    while pc < len(code):
        char = code[pc]
        
        if char == '~':
            stack.append(65)
        elif char == '(':
            pc += 1
            num_str = ""
            while pc < len(code) and code[pc].isdigit():
                num_str += code[pc]
                pc += 1
            stack.append(int(num_str))
            continue # Skip the normal pc increment since we advanced it
        elif char == '#':
            stack[-1] = -stack[-1]
        elif char == '%':
            a = stack.pop()
            b = stack.pop()
            stack.append(b + a)
        elif char == '^':
            print(chr(stack[-1]), end="")
        elif char == '@':
            stack[-1] -= 1
        elif char == '!':
            stack[-1] += 1
        elif char == '$':
            stack[-1], stack[-2] = stack[-2], stack[-1]
        elif char == '*':
            if stack[-1] != 0:
                pc = jump_map[pc] # Jump back to loop start
                
        pc += 1
    print() # Print final newline

# Read the file from the command line and run it
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python wut_compiler.py <filename.wut>")
        sys.exit(1)
        
    with open(sys.argv[1], "r") as f:
        code = f.read().strip()
    run_wut(code)