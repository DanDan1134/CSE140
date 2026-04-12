"""
Writeback stage — write rf, increment total_clock_cycles, print state (see project PDF).
"""
import state

def writeback():
    if state.reg_write == 0:
        return # no register update this cycle
    
    if state.rd == 0:
        return # x0 is not writable because it is always 0

    if state.mem_to_reg == 1:
        data = state.mem_read_data # lw instruction: use memory data
    else:
        data = state.alu_result # R-type and I-type instructions: use ALU result

    state.write_back_data = data # for logging and debugging
    state.rf[state.rd] = data # write the data to the register file
    
