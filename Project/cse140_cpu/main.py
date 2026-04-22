"""
Entry point — the only script you run (python cse140_cpu/main.py from Project).

Later: load program file, loop fetch -> decode -> execute -> mem -> writeback.
"""

import state
from fetch import fetch, update_pc
from decode import decode_and_fill_state
from execute import execute
from mem import mem
from writeback import writeback

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

def reset_cpu_state():
    state.pc = 0
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

def init_samples(filename):
    # part 1 sample init
    if filename.endswith("sample_part1.txt"):
        state.rf[1] = 0x20
        state.rf[2] = 0x5
        state.rf[10] = 0x70
        state.rf[11] = 0x4
        state.d_mem[0x70 // 4] = 0x5
        state.d_mem[0x74 // 4] = 0x10

    #part 2 sample init
    elif filename.endswith("sample_part2.txt"):
        state.rf[8] = 0x20   # s0
        state.rf[10] = 0x5   # a0
        state.rf[11] = 0x2   # a1
        state.rf[12] = 0xA   # a2
        state.rf[13] = 0xF   # a3

def load_program(filename):
    lines = []
    with open(filename, "r") as f:
        for line in f:
            bits = line.strip()
            if bits != "":
                lines.append(bits)
    state.program_instructions = lines

def print_cycle_changes(old_rf, old_mem):
    cycle = state.total_clock_cycles
    print(f"\ntotal_clock_cycles {cycle} :")

    reg_changed = False
    for i in range(32):
        if old_rf[i] != state.rf[i]:
            print(f"x{i} is modified to 0x{state.rf[i]:x}")
            reg_changed = True
            break
    if not reg_changed:
        for i in range(len(state.d_mem)):
            if old_mem[i] != state.d_mem[i]:
                addr = i * 4
                print(f"memory 0x{addr:x} is modified to 0x{state.d_mem[i]:x}")
                break

    print(f"pc is modified to 0x{state.pc:x}")




def main():
    print("Enter the program file name to run:")
    filename = input().strip()
    reset_cpu_state()
    load_program(filename)
    init_samples(filename)

    while True:
        old_rf = state.rf[:]
        old_mem = state.d_mem[:]
        inst = fetch()
        if inst is None:
            break

        decode_and_fill_state(inst)
        execute()
        mem()
        writeback()
        update_pc()


        print_cycle_changes(old_rf, old_mem)

    print("\nprogram terminated:")
    print(f"total execution time is {state.total_clock_cycles} cycles")



if __name__ == "__main__":
    main()
