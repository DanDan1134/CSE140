# holds global state for the cpu

# pc is byte address: 0, 4, 8, ... ; instruction index = pc // 4 (integer division to give index)
pc = 0 #program counter
next_pc = 0 #next program counter
branch_target = 0 #branch target
program_instructions = [] #program instructions

# beq: take branch when branch==1 and alu_zero==1 (set in decode/execute)
branch = 0 #branch flag
alu_zero = 0 #alu zero flag

# will later hold rf, d_mem, more control flags, etc.