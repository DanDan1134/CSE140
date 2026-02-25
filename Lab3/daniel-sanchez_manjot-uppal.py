#splices binary into opcode, finds opcode type
#keys are funct3 and funct7 for R-type and I-type, funct3 for other types
#(funct3, funct7) or (funct3,) -> instruction name
INSTRUCTION_MAP = {
    # R-type (opcode 0110011)
    "0110011": {
        (0, 0): "add", #funct3 = 0, funct7 = 0
        (0, 32): "sub", #funct3 = 0, funct7 = 32
        (1, 0): "sll", 
        (2, 0): "slt",
        (3, 0): "sltu", 
        (4, 0): "xor", 
        (5, 0): "srl", 
        (5, 32): "sra", 
        (6, 0): "or", 
        (7, 0): "and",
    },
    # I-type ALU immediate (opcode 0010011)
    "0010011": {
        (0, 0): "addi",
        (0, 32): "addi",
        (2, 0): "slti",
        (2, 32): "slti",
        (3, 0): "sltiu",
        (3, 32): "sltiu",
        (4, 0): "xori",
        (4, 32): "xori",
        (6, 0): "ori",
        (6, 32): "ori",
        (7, 0): "andi",
        (7, 32): "andi",
        (1, 0): "slli",
        (5, 0): "srli",
        (5, 32): "srai",
    },
    # I-type load (opcode 0000011)
    "0000011": {
        (0,): "lb", #funct3 = 0, no funct 7
        (1,): "lh", #funct3 = 1, no funct 7
        (2,): "lw",
    },
    # I-type jalr (opcode 1100111)
    "1100111": {
        (0,): "jalr", #funct3 = 0, no funct 7
    },
    # ##########################
    # Need s,SB, UJ types
    # ##########################
}
def get_immediate(bits, opcode):
    #Using opcode, take the immediate bits from the instruction and convert to signed decimal.
    # I-type: imm is one chunk at [31:20]
    if opcode in ("0010011", "0000011", "1100111"):
        imm_bits = bits[0:12]
        n = 12 #12 bits for immediate
    # ##########################
    # Need s,SB, UJ types
    # ##########################

    else:
        return None, 0 #if opcode is not in the dictionary, return None and 0
    #convert binary to decimal
    val = int(imm_bits, 2)
    #if the value is greater than or equal to 2^(n-1), subtract 2^n from the value
    if val >= (1 << (n - 1)):
        val -= 1 << n
    return val, n

def format_immediate(imm, bits=32):
    #format immediate as value (or 0xHEX) for display
    # (1 << bits) creates a value where the lowest 'bits' number of bits are 1, and the rest are 0 (e.g., for 8 bits: 0b11111111 = 255)
    n = 1 << bits
    hex_val = imm % n  # same unsigned value for positive and negative
    return str(imm) + " (or 0x" + hex(hex_val)[2:].upper() + ")"


def decode_instruction(binary_instruction):
    # RISC-V: opcode is bits [6:0] (rightmost 7), funct7 is [31:25], funct3 is [14:12], etc.
    # String index 0 = left = bit 31; index 31 = right = bit 0.
    binary_instruction = binary_instruction.strip().zfill(32)
    # Determine instruction type based on opcode
    
    opcode = binary_instruction[25:32]      # bits [6:0]
    if opcode == "0110011":
        ins_type = "R"
    elif opcode == "0010011":
        ins_type = "I"
    elif opcode == "0000011":
        ins_type = "I"
    elif opcode == "1100111":
        ins_type = "I"
   
    # ##########################
    # Need s,SB, UJ types
    # ##########################
    else:
        ins_type = "Unknown"
    type = ins_type
    funct7_bits = binary_instruction[0:7]   # bits [31:25]
    funct3_bits = binary_instruction[17:20] # bits [14:12]
    funct3_int = int(funct3_bits, 2)
    funct7_int = 32 if funct7_bits == "0100000" else int(funct7_bits, 2)  # 0x20 -> 32 for sub/sra/srai
    rd_bits = binary_instruction[20:25]   # bits [11:7]
    rs1_bits = binary_instruction[12:17]  # bits [19:15]
    rs2_bits = binary_instruction[7:12]  # bits [24:20]
    rs1_int = int(rs1_bits, 2)
    rs2_int = int(rs2_bits, 2)
    rd_int = int(rd_bits, 2)
    # ##########################
    # Need s,SB, UJ types
    # ##########################
   
    if opcode in ("0100011", "1100011", "1101111"):
        instruction = "(need S, SB, UJ)"
        immediate_val, imm_bits = None, 0
    else:
        type_map = INSTRUCTION_MAP[opcode]
        if opcode in ("0110011", "0010011"):  # R-type and I-type ALU: need (funct3, funct7)
            key = (funct3_int, funct7_int)
        else:
            key = (funct3_int,)
        instruction = type_map[key]
        immediate_val, imm_bits = get_immediate(binary_instruction, opcode)

    return type, instruction, rs1_int, rs2_int, rd_int, funct3_int, funct7_int, immediate_val, imm_bits
 



def main():
    input_binary = input("Enter an instruction: ")
    type, instruction, rs1_int, rs2_int, rd_int, funct3_int, funct7_int, immediate_val, imm_bits = decode_instruction(input_binary)

    print("Instruction Type:", type)
    print("Operation:", instruction)
    if type == "R":
        print("Rs1: x" + str(rs1_int))
        print("Rs2: x" + str(rs2_int))
        print("Rd: x" + str(rd_int))
        print("Funct3:", funct3_int)
        print("Funct7:", funct7_int)
    elif type == "I":
        print("Rs1: x" + str(rs1_int))
        print("Rd: x" + str(rd_int))
        if immediate_val is not None:
            print("Immediate:", format_immediate(immediate_val, imm_bits))
    # ##########################
    # Need s,SB, UJ types
    # ##########################



if __name__ == "__main__":
    main()