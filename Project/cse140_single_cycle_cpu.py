'''
cse140 single cycle cpu - part 1 starter

10 instrs for now: lw sw add addi sub and andi or ori beq
part 2 later: jal jalr

just skeleton rn - fill in as we go, check pdf + slides
'''

from __future__ import annotations

from typing import Optional

# lines from the txt file, each line = one 32-bit instruction
program_instructions: list[str] = []

# pc in bytes, starts 0, +4 each instr unless branch
pc: int = 0

# normal "next line" = pc + 4
next_pc: int = 0

# where beq wants to go if we take it - fetch has to pick this vs next_pc
branch_target: int = 0

# 32 regs, x0 = rf[0] stays 0
rf: list[int] = [0] * 32

# 32 words of "ram" - slot i = address 4*i (0x70 -> index 28 etc)
d_mem: list[int] = [0] * 32

# 1 if alu output was 0, for beq
alu_zero: int = 0

# bump this in writeback every time an instr finishes
total_clock_cycles: int = 0

# control stuff - control_unit sets these from opcode (names from slides)
reg_write: int = 0
branch: int = 0
mem_read: int = 0
mem_write: int = 0
mem_to_reg: int = 0
alu_src: int = 0
alu_op: int = 0  # goes into alu_control w funct fields

# 4 bits, tells execute what op (+ & | etc)
alu_ctrl: int = 0

# decode fills these so execute/mem/writeback can use em
current_instruction: str = ""
opcode: str = ""
rd: int = 0
rs1: int = 0
rs2: int = 0
funct3: int = 0
funct7: int = 0
imm_i: int = 0
imm_s: int = 0
imm_b: int = 0
read_data_1: int = 0
read_data_2: int = 0

# scratch between stages
alu_result: int = 0
mem_read_data: int = 0
write_back_data: int = 0


def init_registers_and_memory_for_part1() -> None:
    # sample init from part1 handout - run once before loop
    global rf, d_mem
    rf = [0] * 32
    d_mem = [0] * 32
    rf[1] = 0x20
    rf[2] = 0x5
    rf[10] = 0x70
    rf[11] = 0x4
    # 0x70 / 4 and 0x74 / 4 for the indices
    d_mem[0x70 // 4] = 0x5
    d_mem[0x74 // 4] = 0x10


def load_program_file(path: str) -> None:
    # read file, strip junk lines, stuff into program_instructions
    global program_instructions
    program_instructions = []
    # open path, read lines, append each binary string


def fetch() -> Optional[str]:
    # pc//4 = which line. next_pc = pc+4. if branch taken use branch_target
    # return None when out of instructions
    global pc, next_pc, branch_target
    # ...
    return None


def control_unit(opcode_bits: str) -> None:
    # opcode -> flip the right flags (lw vs sw vs r-type vs beq...)
    global reg_write, branch, mem_read, mem_write, mem_to_reg, alu_src, alu_op
    # ...


def alu_control() -> None:
    # alu_op + funct3/funct7 -> alu_ctrl (or fold into control_unit idc)
    global alu_ctrl
    # ...


def decode(instruction_bits: str) -> None:
    # same idea as lab decoder + read rf + sign extend imm + call control_unit
    global current_instruction, opcode, rd, rs1, rs2, funct3, funct7
    global imm_i, imm_s, imm_b, read_data_1, read_data_2
    # ...


def execute() -> None:
    # alu from alu_ctrl, set alu_zero, branch_target = (imm_b<<1) + (pc+4) for branches
    global alu_result, alu_zero, branch_target
    # ...


def mem() -> None:
    # lw: read d_mem[alu_result//4]. sw: store. skip if not load/store
    global mem_read_data
    # ...


def writeback() -> None:
    # if reg_write: write to rd (not x0). pick alu vs mem. print like sample output. cycles++
    global total_clock_cycles, rf, d_mem, pc
    # ...


def run_until_done() -> None:
    # while fetch gives something: decode execute mem writeback
    # else print "program terminated" + total cycles
    pass


def main() -> None:
    init_registers_and_memory_for_part1()
    # name = input("Enter the program file name to run:\n").strip()
    # load_program_file(name)
    # run_until_done()
    print("main function")


if __name__ == "__main__":
    main()
