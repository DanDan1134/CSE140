# holds global state for the cpu

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

# data memory
d_mem = {}  # for byte addresses (int keys for each byte, values as ints)

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

# ALU control line for execute (set in decode or start of execute)
alu_ctrl = 0

# execute / memory / writeback
alu_result = 0
mem_read_data = 0
write_back_data = 0
