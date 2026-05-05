"""
Mem stage — lw / sw on d_mem (see project PDF).
"""

import state


def Mem(address, write_data=0):
    # Non-memory instructions should not touch or validate data memory.
    if state.mem_read != 1 and state.mem_write != 1:
        return

    #Convert byte address to word index with 4 bytes per entry
    word_index = address // 4

    #Stop if address is outside the 32-entry data memory
    if word_index < 0 or word_index >= len(state.d_mem):
        raise IndexError("Data memory address out of range")

    #LW: read one word from data memory
    if state.mem_read == 1:
        state.mem_read_data = state.d_mem[word_index]

    #SW: write one word to data memory
    if state.mem_write == 1:
        state.d_mem[word_index] = write_data


def mem():
    #Use ALU result as memory address and rs2 value as store data
    Mem(state.alu_result, state.read_data_2)
