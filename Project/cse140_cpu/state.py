# holds global state for the cpu
from dataclasses import dataclass, field

# IF/ID register
@dataclass
class IF_ID:
    valid:bool = False # if the instruction is valid (false, so new objects start as bubble (bubble means no instruction is being executed))
    pc: int = 0 # program counter
    pc4: int = 0 # next program counter
    instr: str = "" # instruction

# ID/EX register
@dataclass
class ID_EX:
    valid: bool = False
    pc: int = 0
    pc4: int = 0
    # decoded fields
    opcode: str = ""
    funct3: int = 0
    funct7: int = 0
    rs1: int = 0
    rs2: int = 0
    rd: int = 0
    imm: int = 0

    # register values read in decode
    read_data_1: int = 0
    read_data_2: int = 0
    # control bits generated in decode
    reg_write: int = 0
    mem_read: int = 0
    mem_write: int = 0
    mem_to_reg: int = 0
    alu_src: int = 0
    alu_op: int = 0
    branch: int = 0
    jump: int = 0
    jump_reg: int = 0
    wb_pc4: int = 0
    alu_ctrl: int = 0

# EX/MEM register
@dataclass
class EX_MEM:
    valid: bool = False
    pc4: int = 0
    rd: int = 0
    # EX outputs
    alu_result: int = 0
    zero: int = 0
    branch_target: int = 0
    store_data: int = 0   # value to write for sw
    # control bits that MEM/WB still need
    reg_write: int = 0
    mem_read: int = 0
    mem_write: int = 0
    mem_to_reg: int = 0
    branch: int = 0
    jump: int = 0
    wb_pc4: int = 0

# MEM/WB register
@dataclass
class MEM_WB:
    valid: bool = False
    pc4: int = 0
    rd: int = 0
    # values available for WB mux
    alu_result: int = 0
    mem_read_data: int = 0
    # control bits needed only in WB
    reg_write: int = 0
    mem_to_reg: int = 0
    wb_pc4: int = 0

#global pipeline register objects
#objects are used to store the state of the pipeline
if_id = IF_ID()
id_ex = ID_EX()
ex_mem = EX_MEM()
mem_wb = MEM_WB()

#next cycle buffers (write here during cycle, then commit at end)
#used for storing the state of the pipeline for the next cycle
if_id_next = IF_ID()
id_ex_next = ID_EX()
ex_mem_next = EX_MEM()
mem_wb_next = MEM_WB()

#reset the pipeline registers
def reset_pipeline_regs():
    global if_id, id_ex, ex_mem, mem_wb
    global if_id_next, id_ex_next, ex_mem_next, mem_wb_next
    if_id = IF_ID()
    id_ex = ID_EX()
    ex_mem = EX_MEM()
    mem_wb = MEM_WB()
    if_id_next = IF_ID()
    id_ex_next = ID_EX()
    ex_mem_next = EX_MEM()
    mem_wb_next = MEM_WB()

# pc is byte address: 0, 4, 8, ... ; instruction index = pc // 4 (integer division to give index)
pc = 0  # program counter
next_pc = 0  # next program counter
branch_target = 0  # branch target (byte address)
program_instructions = []  # list of 32-bit instruction strings

# beq: take branch when branch==1 and alu_zero==1 (set in decode/execute)
branch = 0  # branch flag (control)
alu_zero = 0  # ALU zero output (for beq)


# register file x0..x31 (x0 reads as 0; keep rf[0] == 0)
rf = [0] * 32

# data memory: 32 entries, each entry is one 4-byte word
d_mem = [0] * 32

# decoded instruction (set in decode)
opcode = ""  # 7-bit opcode string, bits [6:0] as in instruction word
instruction_type = ""  # R, I, S, SB, U, UJ, Unknown
instruction_name = ""  # mnemonic e.g. "lw", "add"
rs1 = 0
rs2 = 0
rd = 0
funct3 = 0
funct7 = 0
imm = 0  # sign-extended immediate for I/S/SB/UJ as produced by decode

# register file read ports (set in decode)
read_data_1 = 0
read_data_2 = 0

# control signals (set in decode; naming matches typical datapath)
reg_write = 0
mem_read = 0
mem_write = 0
mem_to_reg = 0
alu_src = 0
# ALUOp: encode to match your lecture table (e.g. 00=add, 01=sub/beq, 10=funct)
alu_op = 0

#jump control signals
jump = 0 #jump flag 1=jal, 0=no jump
jump_reg = 0 #register based jump 1=jalr, 0=jal target is rs1 + imm
wb_pc4 = 0 #tells wb to store pc+4 (return address) into rd

# ALU control line for execute (set in decode or start of execute)
alu_ctrl = 0

# execute / memory / writeback
alu_result = 0
mem_read_data = 0
write_back_data = 0
total_clock_cycles = 0
