"""
Fetch stage: read instruction at pc (byte address), set next_pc, update pc after cycle.

Call fetch() then decode/execute/mem/writeback, then update_pc() so branch_target is known.
"""

# Daniel Implementation

from typing import Optional

import state #for global state (pc, next_pc, branch_target, program_instructions)

# returns 32-bit string or None when done
def fetch() -> Optional[str]: #optional because it returns either str or none
    index = state.pc // 4 #get the index of the instruction in the program instructions (turns byte address into index) -> 0//4 = 0, 4//4 1, and so on
    if index >= len(state.program_instructions): #if index is greater than the length of the program instructions, return None (finished)
        return None
    state.next_pc = state.pc + 4 #increment the pc by 4 because instructions are 4 bytes long
    return state.program_instructions[index] #return the instruction



# updates the pc after the cycle
# will add more logic for jal and jalr later
def update_pc() -> None:
    if state.jump == 1 and state.jump_reg == 1:
        state.pc = state.branch_target
    #After execute: pc = branch_target if beq taken, else next_pc.
    elif state.branch and state.alu_zero: #if branch is 1 and alu_zero is 1, then the branch is taken
        state.pc = state.branch_target #update the pc to the branch target
    else:
        state.pc = state.next_pc #update the pc to the next pc
