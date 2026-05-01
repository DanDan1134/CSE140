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

REG_NAMES = [ 
    "zero", "ra", "sp", "gp", "tp", "t0", "t1", "t2",
    "s0", "s1", "a0", "a1", "a2", "a3", "a4", "a5",
    "a6", "a7", "s2", "s3", "s4", "s5", "s6", "s7",
    "s8", "s9", "s10", "s11", "t3", "t4", "t5", "t6",
]
use_reg_names = False #use the ABI register names if the filename ends with sample_part2.txt

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
    # default init for all non-part2 samples (same setup as part1)
    if not filename.endswith("sample_part2.txt"):
        state.rf[1] = 0x20 
        state.rf[2] = 0x5 
        state.rf[10] = 0x70
        state.rf[11] = 0x4
        state.d_mem[0x70 // 4] = 0x5 #// 4 means divide by 4 to get the index of the memory
        state.d_mem[0x74 // 4] = 0x10

    #part 2 sample init
    else: #assigns the values to the registers and memory
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

#print the cycle changes
def print_cycle_changes(old_rf, old_mem):
    cycle = state.total_clock_cycles
    print(f"\ntotal_clock_cycles {cycle} :")

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

    print(f"pc is modified to 0x{state.pc:x}") #print the pc changes




def main():
    global use_reg_names # for use in print_cycle_changes
    print("Enter the program file name to run:")
    filename = input().strip()
    use_reg_names = filename.endswith("sample_part2.txt") #set the use_reg_names to true if the filename ends with sample_part2.txt
    reset_cpu_state()
    load_program(filename)
    init_samples(filename)

    while True: #loop through the program instructions
        old_rf = state.rf[:] #store the old register file
        old_mem = state.d_mem[:] #store the old memory 
        inst = fetch()
        if inst is None: #if the instruction is None, break the loop
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
