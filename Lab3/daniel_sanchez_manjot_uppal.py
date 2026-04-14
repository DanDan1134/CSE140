#splices binary into opcode, finds opcode type
#keys are funct3 and funct7 for R-type and I-type, funct3 for other types
#(funct3, funct7) or (funct3,) -> instruction name

#Daniel Implementation
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

    # S-type store (opcode 0100011)
     "0100011": {
         (0,): "sb", #funct3 = 0, no
         (1,): "sh", #funct3 = 1, funct7 not used
         (2,): "sw", #funct3 = 2, funct7 not used

     },

    # SB-type branch (opcode 1100011)
    "1100011": {
        (0,): "beq", #funct3 = 0, no funct7
        (1,): "bne", #funct3 = 1, no funct7
        (4,): "blt", #funct3 = 4, no funct7
        (5,): "bge", #funct3 = 5, no funct7
        (6,): "bltu", #funct3 = 6, no funct7
        (7,): "bgeu", #funct3 = 7, no funct7

    },

    # UJ-type jump (opcode 1101111)
    "1101111": {
        (0,): "jal", #funct3 = 0, no funct7
    },
}

#Manjot Implementation
def get_immediate(bits, opcode):
    #Using opcode, take the immediate bits from the instruction and convert to signed decimal.

    # I-type: imm is one chunk at [31:20]
    if opcode in ("0010011", "0000011", "1100111"):
        imm_bits = bits[0:12] #first 12 bits are the immediate field for I-type, load, and jalr
        n = 12 #12 bits for immediate

    # S-type store
    elif opcode == "0100011":
        imm_bits = bits[0:7] + bits[20:25]
        n = 12 # 12 bits for immediate in S-type

    # SB-type branch: imm[12]|imm[11]|imm[10:5]|imm[4:1]|0 -> bits[0], bits[24], bits[1:7], bits[20:24], "0"
    elif opcode == "1100011":
        imm_bits = bits[0] + bits[24] + bits[1:7] + bits[20:24] + "0"
        n = 13 # 13 bits for immediate in SB-type

    # UJ-type jump
    elif opcode == "1101111":
        imm_bits = bits[0] + bits[12:20] + bits[11] + bits[1:11] + '0' 
        n = 21 # 21 bits for immediate in UJ-type
    else:
        return None, 0 #if opcode is not in the dictionary, return None and 0
    #convert binary to decimal
    val = int(imm_bits, 2)
    #used to interpret negative values correctly
    #if the value is greater than or equal to 2^(n-1), subtract 2^n from the value
    if val >= (1 << (n - 1)):
        val -= 1 << n
    return val, n

#Manjot Implementation
def format_immediate(imm, bits=32): #default bit is 32 if no bits are passed
    #format immediate as value (or 0xHEX) for display and handle negative values correctly
    n = 1 << bits #n = 2^bits for defining bit-width range for unsigned values
    hex_val = imm % n  # for converting imm to unsigned value within given bit-width (n)
    return str(imm) + " (or 0x" + hex(hex_val)[2:].upper() + ")" #turns into hex using hex(), [2:] to remove 0x, .upper() to make uppercase


#Daniel Implementation
def decode_instruction(binary_instruction):
    binary_instruction = binary_instruction.strip().zfill(32) #remove whitespace and fill with 0s to make 32 bits
    
    # Determine instruction type based on opcode
    # instructions are 32 bits, opcode is 7 bits, so we need to get the opcode from bits [25:32]
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
        ins_type = "I" #ecall and ebreak are I-type with funct3 = 0 and funct7 = 0 or 1
    else:
        ins_type = "Unknown"
    type = ins_type
    #get funct7 and funct3 bits
    funct7_bits = binary_instruction[0:7]   # bits [31:25]
    funct3_bits = binary_instruction[17:20] # bits [14:12]
    #convert funct3 and funct7 bits to integers
    funct3_int = int(funct3_bits, 2) #int(string_value, base) — e.g., int("1010", 2) returns 10 (binary to decimal).
    funct7_int = 32 if funct7_bits == "0100000" else int(funct7_bits, 2)  # 32 if bits are 0100000, otherwise convert to decimal
    #get rd, rs1, and rs2 bits
    rd_bits = binary_instruction[20:25]   # bits [11:7]
    rs1_bits = binary_instruction[12:17]  # bits [19:15]
    rs2_bits = binary_instruction[7:12]  # bits [24:20]
    #convert rs1, rs2, and rd bits to integers
    rs1_int = int(rs1_bits, 2)
    rs2_int = int(rs2_bits, 2)
    rd_int = int(rd_bits, 2)
   
    #get instruction name based on opcode and funct3 and funct7 bits
    if opcode in ("0100011", "1100011", "1101111"):
        type_map = INSTRUCTION_MAP[opcode]
        key = (funct3_int,)  # S-type, SB-type, and UJ-type only use funct3 for instruction mapping
        instruction = type_map.get(key, "Unknown")  #.get(arg1, arg2) tries to fetch the value for key arg1 from the dictionary; if not found, it returns arg2 instead of raising an error.
        immediate_val, imm_bits = get_immediate(binary_instruction, opcode)
    else:
        type_map = INSTRUCTION_MAP[opcode]
        if opcode in ("0110011", "0010011"):  # R-type and I-type ALU: need (funct3, funct7)
            key = (funct3_int, funct7_int)
        else:
            key = (funct3_int,)
        instruction = type_map[key]
        immediate_val, imm_bits = get_immediate(binary_instruction, opcode)

    return type, instruction, rs1_int, rs2_int, rd_int, funct3_int, funct7_int, immediate_val, imm_bits
 


#Daniel Implementation
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

    elif type == "S":
        print ("Rs1: x" + str(rs1_int))
        print ("Rs2: x" + str(rs2_int))
        if immediate_val is not None:
            print ("Immediate:", format_immediate(immediate_val, imm_bits))

    elif type == "SB":
        print ("Rs1: x" + str(rs1_int))
        print ("Rs2: x" + str(rs2_int))
        if immediate_val is not None :
            print ("Immediate:", format_immediate(immediate_val, imm_bits))
    
    elif type == "UJ":
        print ("Rd: x" + str(rd_int))
        if immediate_val is not None:
            print ("Immediate:", format_immediate(immediate_val, imm_bits))

    elif type == "U":
        print ("Rd: x" + str(rd_int))
        if immediate_val is not None:
            print ("Immediate:", format_immediate(immediate_val, imm_bits))


if __name__ == "__main__":
    main()