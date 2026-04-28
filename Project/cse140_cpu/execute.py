"""
Execute stage — ALU (alu_ctrl), alu_zero, branch_target (see project PDF).
"""

import state


def Execute():
    """Run ALU operation and update zero/branch target outputs."""
    operand_1 = state.read_data_1
    operand_2 = state.imm if state.alu_src == 1 else state.read_data_2

    ctrl = state.alu_ctrl & 0b1111
    if ctrl == 0b0000:  # AND
        result = operand_1 & operand_2
    elif ctrl == 0b0001:  # OR
        result = operand_1 | operand_2
    elif ctrl == 0b0010:  # ADD
        result = operand_1 + operand_2
    elif ctrl == 0b0110:  # SUB
        result = operand_1 - operand_2
    elif ctrl == 0b0111:  # SLT (signed)
        result = 1 if operand_1 < operand_2 else 0
    elif ctrl == 0b1100:  # NOR
        result = ~(operand_1 | operand_2)
    else:
        result = operand_1 + operand_2

    state.alu_result = result
    state.alu_zero = 1 if result == 0 else 0
    if state.jump == 1 and state.jump_reg == 1:
        # jalr target: rs1 + imm, clear bit 0 for alignment
        state.branch_target = (state.read_data_1 + state.imm) & ~1 #& ~1 clears the least significant bit to make it word aligned
    elif state.jump == 1:
        # jal target is PC-relative byte offset
        state.branch_target = state.pc + state.imm
    elif state.branch == 1:
        # branch immediate is already byte aligned in decode
        state.branch_target = state.pc + state.imm


def execute():
    #Keep lowercase API for existing imports/calls
    Execute()
