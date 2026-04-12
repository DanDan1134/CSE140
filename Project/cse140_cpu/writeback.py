"""

Writeback stage — MemToReg mux, write rf when RegWrite; increment total_clock_cycles

every finished instruction (PDF). Trace printing lives in main.

"""

import state





def writeback():

    # One instruction finished this cycle (including sw / beq with no reg write).

    state.total_clock_cycles += 1



    if state.reg_write == 0: # no register update this cycle

        return



    if state.rd == 0: # x0 is not writable so we just return

        return  



    if state.mem_to_reg == 1: # lw instruction: use memory data

        data = state.mem_read_data

    else: # R-type and I-type instructions: use ALU result

        data = state.alu_result



    state.write_back_data = data # for logging and debugging

    state.rf[state.rd] = data # write the data to the register file

    state.rf[0] = 0  # keep x0 hard-wired to 0 because it is always 0


