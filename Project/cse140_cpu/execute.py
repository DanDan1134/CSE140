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
        state.branch_target = (state.read_data_1 + state.imm) & ~1  # jalr: jump addr = (rs1+imm) with bit0 cleared
    elif state.jump == 1:
        state.branch_target = state.pc + state.imm  # jal: jump addr = this insn PC + UJ offset (decode gives byte offset)
    elif state.branch == 1:
        state.branch_target = state.pc + state.imm  # beq: target = branch insn PC + B-immediate (bytes; decode already even)


def execute():
    #Keep lowercase API for existing imports/calls
    Execute()
