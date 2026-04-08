# splices binary into opcode, finds opcode type
# keys are funct3 and funct7 for R-type and I-type, funct3 for other types
# (funct3, funct7) or (funct3,) -> instruction name

# Daniel Implementation
INSTRUCTION_MAP = {
    # R-type (opcode 0110011)
    "0110011": {
        (0, 0): "add",  # funct3 = 0, funct7 = 0
        (0, 32): "sub",  # funct3 = 0, funct7 = 32
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
        (0,): "lb",
        (1,): "lh",
        (2,): "lw",
    },
    # I-type jalr (opcode 1100111)
    "1100111": {
        (0,): "jalr",
    },
    # S-type store (opcode 0100011)
    "0100011": {
        (0,): "sb",
        (1,): "sh",
        (2,): "sw",
    },
    # SB-type branch (opcode 1100011)
    "1100011": {
        (0,): "beq",
        (1,): "bne",
        (4,): "blt",
        (5,): "bge",
        (6,): "bltu",
        (7,): "bgeu",
    },
    # UJ-type jump (opcode 1101111)
    "1101111": {
        (0,): "jal",
    },
}


# Manjot Implementation
def get_immediate(bits, opcode):
    # Using opcode, take the immediate bits from the instruction and convert to signed decimal.
    if opcode in ("0010011", "0000011", "1100111"):
        imm_bits = bits[0:12]
        n = 12
    elif opcode == "0100011":
        imm_bits = bits[0:7] + bits[20:25]
        n = 12
    elif opcode == "1100011":
        imm_bits = bits[0] + bits[24] + bits[1:7] + bits[20:24] + "0"
        n = 13
    elif opcode == "1101111":
        imm_bits = bits[0] + bits[12:20] + bits[11] + bits[1:11] + "0"
        n = 21
    else:
        return None, 0
    val = int(imm_bits, 2)
    if val >= (1 << (n - 1)):
        val -= 1 << n
    return val, n


# Manjot Implementation
def format_immediate(imm, bits=32):
    n = 1 << bits
    hex_val = imm % n
    return str(imm) + " (or 0x" + hex(hex_val)[2:].upper() + ")"


# Daniel Implementation
def decode_instruction(binary_instruction):
    binary_instruction = binary_instruction.strip().zfill(32)
    opcode = binary_instruction[25:32]
    if opcode == "0110011":
        ins_type = "R"
    elif opcode == "0010011":
        ins_type = "I"
    elif opcode == "0000011":
        ins_type = "I"
    elif opcode == "1100111":
        ins_type = "I"
    elif opcode == "0010111":
        ins_type = "U"
    elif opcode == "0100011":
        ins_type = "S"
    elif opcode == "0110111":
        ins_type = "U"
    elif opcode == "0111011":
        ins_type = "R"
    elif opcode == "1100011":
        ins_type = "SB"
    elif opcode == "1101111":
        ins_type = "UJ"
    elif opcode == "1110011":
        ins_type = "I"
    else:
        ins_type = "Unknown"
    type_ = ins_type
    funct7_bits = binary_instruction[0:7]
    funct3_bits = binary_instruction[17:20]
    funct3_int = int(funct3_bits, 2)
    funct7_int = 32 if funct7_bits == "0100000" else int(funct7_bits, 2)
    rd_bits = binary_instruction[20:25]
    rs1_bits = binary_instruction[12:17]
    rs2_bits = binary_instruction[7:12]
    rs1_int = int(rs1_bits, 2)
    rs2_int = int(rs2_bits, 2)
    rd_int = int(rd_bits, 2)

    if opcode in ("0100011", "1100011", "1101111"):
        type_map = INSTRUCTION_MAP[opcode]
        key = (funct3_int,)
        instruction = type_map.get(key, "Unknown")
        immediate_val, imm_bits = get_immediate(binary_instruction, opcode)
    else:
        type_map = INSTRUCTION_MAP[opcode]
        if opcode in ("0110011", "0010011"):
            key = (funct3_int, funct7_int)
        else:
            key = (funct3_int,)
        instruction = type_map[key]
        immediate_val, imm_bits = get_immediate(binary_instruction, opcode)

    return (
        type_,
        instruction,
        rs1_int,
        rs2_int,
        rd_int,
        funct3_int,
        funct7_int,
        immediate_val,
        imm_bits,
    )


def print_decoded_instruction(
    type_,
    instruction,
    rs1_int,
    rs2_int,
    rd_int,
    funct3_int,
    funct7_int,
    immediate_val,
    imm_bits,
):
    """Human-readable output for one decoded instruction (used by main and decode-only demo)."""
    print("Instruction Type:", type_)
    print("Operation:", instruction)
    if type_ == "R":
        print("Rs1: x" + str(rs1_int))
        print("Rs2: x" + str(rs2_int))
        print("Rd: x" + str(rd_int))
        print("Funct3:", funct3_int)
        print("Funct7:", funct7_int)
    elif type_ == "I":
        print("Rs1: x" + str(rs1_int))
        print("Rd: x" + str(rd_int))
        if immediate_val is not None:
            print("Immediate:", format_immediate(immediate_val, imm_bits))
    elif type_ == "S":
        print("Rs1: x" + str(rs1_int))
        print("Rs2: x" + str(rs2_int))
        if immediate_val is not None:
            print("Immediate:", format_immediate(immediate_val, imm_bits))
    elif type_ == "SB":
        print("Rs1: x" + str(rs1_int))
        print("Rs2: x" + str(rs2_int))
        if immediate_val is not None:
            print("Immediate:", format_immediate(immediate_val, imm_bits))
    elif type_ == "UJ":
        print("Rd: x" + str(rd_int))
        if immediate_val is not None:
            print("Immediate:", format_immediate(immediate_val, imm_bits))
    elif type_ == "U":
        print("Rd: x" + str(rd_int))
        if immediate_val is not None:
            print("Immediate:", format_immediate(immediate_val, imm_bits))
