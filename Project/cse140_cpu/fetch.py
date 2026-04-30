"""
Fetch stage: read instruction at pc (byte address), set next_pc, update pc after cycle.

Call fetch() then decode/execute/mem/writeback, then update_pc() so branch_target is known.
"""

# Daniel Implementation

from typing import Optional

import state #for global state (pc, next_pc, branch_target, program_instructions)

# returns 32-bit string or None when done
def fetch() -> Optional[str]: #optional because it returns either str or none
    index = state.fetch_pc // 4  # IF uses fetch_pc, not EX-stage pc
    if index >= len(state.program_instructions): #if index is greater than the length of the program instructions, return None (finished)
        return None
    state.next_pc = state.fetch_pc + 4 #increment the fetch_pc by 4 because instructions are 4 bytes long
    return state.program_instructions[index] #return the instruction



# updates the pc after the cycle
# will add more logic for jal and jalr later
def update_pc() -> None:
    if state.jump == 1:
        state.fetch_pc = state.branch_target
    #After execute: pc = branch_target if beq taken, else next_pc.
    elif state.branch and state.alu_zero: #if branch is 1 and alu_zero is 1, then the branch is taken
        state.fetch_pc = state.branch_target #update the pc to the branch target
    else:
        state.fetch_pc = state.next_pc #update the pc to the next pc
    state.pc = state.fetch_pc
