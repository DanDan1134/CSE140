"""
Entry point — run from Project/cse140_cpu: python main.py

Pipelined mode: same print lines as Part 1–2. One loop iteration = one clock tick (extra credit).
"""

import copy  # shallow copy for holding IF/ID when stalled (stall = wait cycle; no new decode)
import state
from fetch import fetch, update_pc
from decode import decode_and_fill_state
from execute import execute
from mem import mem
from writeback import writeback

REG_NAMES = [ 
    "zero", "ra", "sp", "gp", "tp", "t0", "t1", "t2",
    "s0", "s1", "a0", "a1", "a2", "a3", "a4", "a5",
    "a6", "a7", "s2", "s3", "s4", "s5", "s6", "s7",
    "s8", "s9", "s10", "s11", "t3", "t4", "t5", "t6",
]
use_reg_names = False #use the ABI register names if the filename ends with sample_part2.txt

#check if the pipeline is empty
#returns true if the pipeline is empty, false otherwise
def pipeline_empty():
    return (
        not state.if_id.valid
        and not state.id_ex.valid
        and not state.ex_mem.valid
        and not state.mem_wb.valid
    )


def pipeline_data_hazard(if_id, id_ex, ex_mem, mem_wb):
    """True if IF/ID needs a register still in flight in EX, MEM, or MEM/WB (no forwarding = stall)."""
    if not if_id.valid or not if_id.instr:
        return False
    bits = if_id.instr.strip().zfill(32)
    opc = bits[25:32]  # main opcode field
    rs1 = int(bits[12:17], 2)  # first source register number
    uses_rs2 = opc in ("0110011", "0100011", "1100011")  # R-type, store, branch use rs2
    rs2 = int(bits[7:12], 2) if uses_rs2 else None
    for pipe in (id_ex, ex_mem, mem_wb):
        if pipe.valid and pipe.reg_write == 1 and pipe.rd != 0:
            if pipe.rd == rs1:
                return True
            if rs2 is not None and pipe.rd == rs2:
                return True
    return False

# reset all control signals to 0
def reset_control_signals():
    state.reg_write = 0
    state.mem_read = 0
    state.mem_write = 0
    state.mem_to_reg = 0
    state.alu_src = 0
    state.alu_op = 0
    state.branch = 0
    state.jump = 0
    state.jump_reg = 0
    state.wb_pc4 = 0

    state.alu_ctrl = 0
    state.alu_zero = 0
    state.alu_result = 0
    state.branch_target = 0
    state.mem_read_data = 0
    state.write_back_data = 0

#reset the cpu state
def reset_cpu_state():
    state.pc = 0
    state.fetch_pc = 0  # IF starts fetching from address 0
    state.next_pc = 0
    state.total_clock_cycles = 0
    state.program_instructions = []

    state.rf = [0] * 32
    state.d_mem = [0] * 32

    state.opcode = ""
    state.instruction_type = ""
    state.instruction_name = ""
    state.rs1 = 0
    state.rs2 = 0
    state.rd = 0
    state.funct3 = 0
    state.funct7 = 0
    state.imm = 0
    state.read_data_1 = 0
    state.read_data_2 = 0

    reset_control_signals()

#initialize the sample data for part 1 and part 2
def init_samples(filename):
    # part 1 sample init
    if filename.endswith("sample_part1.txt"): #assigns the values to the registers and memory
        state.rf[1] = 0x20 
        state.rf[2] = 0x5 
        state.rf[10] = 0x70
        state.rf[11] = 0x4
        state.d_mem[0x70 // 4] = 0x5 #// 4 means divide by 4 to get the index of the memory
        state.d_mem[0x74 // 4] = 0x10

    #part 2 sample init
    elif filename.endswith("sample_part2.txt"): #assigns the values to the registers and memory
        state.rf[8] = 0x20   # s0
        state.rf[10] = 0x5   # a0
        state.rf[11] = 0x2   # a1
        state.rf[12] = 0xA   # a2
        state.rf[13] = 0xF   # a3

#load the program file and store the instructions in the program_instructions list
def load_program(filename):
    lines = []
    with open(filename, "r") as f:
        for line in f:
            bits = line.strip()
            if bits != "":
                lines.append(bits)
    state.program_instructions = lines

# Same print shape as Part 1–2: header, optional first register or memory change, then pc.
# Pipelining: early cycles often only show pc (instruction still in flight). Stalls add extra
# cycles that may also be pc-only unless you print a separate stall line.
def print_cycle_changes(old_rf, old_mem, stage_line):
    cycle = state.total_clock_cycles
    print(f"\ntotal_clock_cycles {cycle} : {stage_line}")

    reg_changed = False #check if the register has changed
    for i in range(32):
        if old_rf[i] != state.rf[i]: #check if the register has changed
            reg_label = REG_NAMES[i] if use_reg_names else f"x{i}" #use the register names (ra, a0, etc.) if the filename ends with sample_part2.txt
            print(f"{reg_label} is modified to 0x{state.rf[i]:x}")
            reg_changed = True #set the register changed to true
            break
    if not reg_changed: #if the register has not changed, check if the memory has changed
        for i in range(len(state.d_mem)): 
            if old_mem[i] != state.d_mem[i]: #check if the memory has changed
                addr = i * 4 #get the address of the memory
                print(f"memory 0x{addr:x} is modified to 0x{state.d_mem[i]:x}") #print the memory changess
                break

    print(f"pc is modified to 0x{state.fetch_pc:x}")  # show next fetch address (architectural PC for pipeline)
def main():
    global use_reg_names  # for use in print_cycle_changes
    print("Enter the program file name to run:")
    filename = input().strip()
    use_reg_names = filename.endswith("sample_part2.txt")  # use ABI names for part2 sample
    reset_cpu_state()
    load_program(filename)
    init_samples(filename)
    state.reset_pipeline_regs()

    fetch_done = False

    while True:  # one loop = one clock tick (extra credit)
        state.total_clock_cycles += 1
        old_rf = state.rf[:]
        old_mem = state.d_mem[:]
        saved_fpc = state.fetch_pc

        state.if_id_next = state.IF_ID()
        state.id_ex_next = state.ID_EX()
        state.ex_mem_next = state.EX_MEM()
        state.mem_wb_next = state.MEM_WB()

        wb_active = state.mem_wb.valid
        mem_active = state.ex_mem.valid
        ex_active = state.id_ex.valid
        decode_active = False
        fetch_active = False

        if state.mem_wb.valid:
            state.rd = state.mem_wb.rd
            state.alu_result = state.mem_wb.alu_result
            state.mem_read_data = state.mem_wb.mem_read_data
            state.reg_write = state.mem_wb.reg_write
            state.mem_to_reg = state.mem_wb.mem_to_reg
            state.wb_pc4 = state.mem_wb.wb_pc4
            state.next_pc = state.mem_wb.pc4
        else:
            state.reg_write = 0
            state.mem_to_reg = 0
            state.wb_pc4 = 0
        writeback()

        if state.ex_mem.valid:
            state.alu_result = state.ex_mem.alu_result
            state.read_data_2 = state.ex_mem.store_data
            state.mem_read = state.ex_mem.mem_read
            state.mem_write = state.ex_mem.mem_write
            mem()

            state.mem_wb_next.valid = True
            state.mem_wb_next.pc4 = state.ex_mem.pc4
            state.mem_wb_next.rd = state.ex_mem.rd
            state.mem_wb_next.alu_result = state.ex_mem.alu_result
            state.mem_wb_next.mem_read_data = state.mem_read_data
            state.mem_wb_next.reg_write = state.ex_mem.reg_write
            state.mem_wb_next.mem_to_reg = state.ex_mem.mem_to_reg
            state.mem_wb_next.wb_pc4 = state.ex_mem.wb_pc4

        stall = pipeline_data_hazard(state.if_id, state.id_ex, state.ex_mem, state.mem_wb)

        branch_taken = False
        if state.id_ex.valid:
            state.pc = state.id_ex.pc
            state.next_pc = state.id_ex.pc4
            state.imm = state.id_ex.imm
            state.read_data_1 = state.id_ex.read_data_1
            state.read_data_2 = state.id_ex.read_data_2
            state.alu_src = state.id_ex.alu_src
            state.alu_ctrl = state.id_ex.alu_ctrl
            state.branch = state.id_ex.branch
            state.jump = state.id_ex.jump
            state.jump_reg = state.id_ex.jump_reg
            execute()

            state.ex_mem_next.valid = True
            state.ex_mem_next.pc4 = state.id_ex.pc4
            state.ex_mem_next.rd = state.id_ex.rd
            state.ex_mem_next.alu_result = state.alu_result
            state.ex_mem_next.zero = state.alu_zero
            state.ex_mem_next.branch_target = state.branch_target
            state.ex_mem_next.store_data = state.id_ex.read_data_2
            state.ex_mem_next.reg_write = state.id_ex.reg_write
            state.ex_mem_next.mem_read = state.id_ex.mem_read
            state.ex_mem_next.mem_write = state.id_ex.mem_write
            state.ex_mem_next.mem_to_reg = state.id_ex.mem_to_reg
            state.ex_mem_next.branch = state.id_ex.branch
            state.ex_mem_next.jump = state.id_ex.jump
            state.ex_mem_next.wb_pc4 = state.id_ex.wb_pc4

            branch_taken = (state.id_ex.branch == 1 and state.alu_zero == 1) or (state.id_ex.jump == 1)
            if branch_taken and (not stall):
                update_pc()

        if stall:
            state.fetch_pc = saved_fpc
            state.pc = state.fetch_pc

        if state.if_id.valid and (not stall) and (not branch_taken):
            decode_active = True
            decode_and_fill_state(state.if_id.instr)

            state.id_ex_next.valid = True
            state.id_ex_next.pc = state.if_id.pc
            state.id_ex_next.pc4 = state.if_id.pc4
            state.id_ex_next.opcode = state.opcode
            state.id_ex_next.funct3 = state.funct3
            state.id_ex_next.funct7 = state.funct7
            state.id_ex_next.rs1 = state.rs1
            state.id_ex_next.rs2 = state.rs2
            state.id_ex_next.rd = state.rd
            state.id_ex_next.imm = state.imm
            state.id_ex_next.read_data_1 = state.read_data_1
            state.id_ex_next.read_data_2 = state.read_data_2
            state.id_ex_next.reg_write = state.reg_write
            state.id_ex_next.mem_read = state.mem_read
            state.id_ex_next.mem_write = state.mem_write
            state.id_ex_next.mem_to_reg = state.mem_to_reg
            state.id_ex_next.alu_src = state.alu_src
            state.id_ex_next.alu_op = state.alu_op
            state.id_ex_next.branch = state.branch
            state.id_ex_next.jump = state.jump
            state.id_ex_next.jump_reg = state.jump_reg
            state.id_ex_next.wb_pc4 = state.wb_pc4
            state.id_ex_next.alu_ctrl = state.alu_ctrl

        if stall:
            state.if_id_next = copy.copy(state.if_id)
        elif branch_taken:
            state.if_id_next = state.IF_ID()
            instr_pc = state.fetch_pc
            inst = fetch()
            if inst is None:
                fetch_done = True
            else:
                fetch_active = True
                state.if_id_next.valid = True
                state.if_id_next.pc = instr_pc
                state.if_id_next.pc4 = state.next_pc
                state.if_id_next.instr = inst
                state.fetch_pc = state.next_pc
        else:
            instr_addr = state.fetch_pc
            inst = fetch()
            if inst is None:
                fetch_done = True
            else:
                fetch_active = True
                state.if_id_next.valid = True
                state.if_id_next.pc = instr_addr
                state.if_id_next.pc4 = state.next_pc
                state.if_id_next.instr = inst
                state.fetch_pc = state.next_pc
        state.pc = state.fetch_pc

        state.if_id = state.if_id_next
        state.id_ex = state.id_ex_next
        state.ex_mem = state.ex_mem_next
        state.mem_wb = state.mem_wb_next

        stage_parts = []
        if fetch_active:
            stage_parts.append("IF")
        if decode_active:
            stage_parts.append("ID")
        if ex_active:
            stage_parts.append("EX")
        if mem_active:
            stage_parts.append("MEM")
        if wb_active:
            stage_parts.append("WB")
        if stall:
            stage_parts.append("STALL")
        if branch_taken:
            stage_parts.append("FLUSH")
        stage_line = " | ".join(stage_parts) if stage_parts else "-"

        print_cycle_changes(old_rf, old_mem, stage_line)

        if fetch_done and pipeline_empty():
            break

    print("\nprogram terminated:")
    print(f"total execution time is {state.total_clock_cycles} cycles")


if __name__ == "__main__":
    main()
