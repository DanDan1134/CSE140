"""

Writeback stage — MemToReg mux, write rf when RegWrite.

Clock cycles are counted in main.py (one per pipeline tick), not here.

"""

import state


def writeback():

    if state.reg_write == 0:
        return
        
    if state.rd == 0: return # x0 is not writable so we just return
          

    if state.wb_pc4 == 1: # jalr instruction: use next_pc
        data = state.next_pc
    
    elif state.mem_to_reg == 1: # lw instruction: use memory data
        data = state.mem_read_data
    else: # R-type and I-type instructions: use ALU result
        data = state.alu_result
        
    state.write_back_data = data # for logging and debugging
    state.rf[state.rd] = data # write the data to the register file, we will print rd (data) to console later
    state.rf[0] = 0  # keep x0 hard-wired to 0 because it is always 0


