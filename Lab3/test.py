import sys
sys.path.insert(0, '/workspaces/CSE140/Lab3')
from daniel_sanchez_manjot_uppal import decode_instruction, format_immediate

# Test cases: (binary_instruction, expected_type, expected_instruction)
test_cases = [
    # R-type: add x1, x2, x3 (0x00310633)
    ("00000000001100010000000110110011", "R", "add"),
    
    # I-type: addi x1, x1, 10 (0x00A08093)
    ("00000000101000001000000010010011", "I", "addi"),
    
    # I-type: lw x1, 0(x2) (0x00012083)
    ("00000000000000010010000010000011", "I", "lw"),
    
    # S-type: sw x1, 0(x2) (0x00112023)
    ("00000000000100010010000000100011", "S", "sw"),
    
    # SB-type: beq x1, x2, 0 (0x00208063)
    ("00000000001000010000000001100011", "SB", "beq"),
    
    # UJ-type: jal x1, 0 (0x0000006F)
    ("00000000000000000000000011101111", "UJ", "jal"),
]

def run_tests():
    passed = 0
    failed = 0
    
    for binary, expected_type, expected_instr in test_cases:
        try:
            type_result, instruction, rs1, rs2, rd, f3, f7, imm, imm_bits = decode_instruction(binary)
            
            if type_result == expected_type and instruction == expected_instr:
                print(f"PASS: {expected_instr} ({expected_type}-type)")
                passed += 1
            else:
                print(f"FAIL: Expected {expected_instr} ({expected_type}-type), got {instruction} ({type_result}-type)")
                failed += 1
        except Exception as e:
            print(f"ERROR: {binary} - {str(e)}")
            failed += 1
    
    print(f"\n{passed} passed, {failed} failed")

if __name__ == "__main__":
    run_tests()