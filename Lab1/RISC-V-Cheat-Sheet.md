# RISC-V Assembly Cheat Sheet

## Section directives

| Directive | Meaning |
|-----------|--------|
| `.data` | Start of data section (variables, strings, arrays) |
| `.text` | Start of code section (instructions) |

---

## Data directives

| Directive | Meaning | Example |
|-----------|--------|--------|
| `.word` | 32-bit integer(s) | `.word 5, 1, 4` |
| `.half` | 16-bit integer(s) | `.half 100, 200` |
| `.byte` | 8-bit value(s) | `.byte 0x41` |
| `.string` | Null-terminated string | `.string "hello"` |
| `.asciz` | Same as .string | `.asciz "hi"` |
| `.space N` | Reserve N bytes (zeroed) | `.space 16` |
| `.align N` | Align next item to 2^N bytes | `.align 2` |

---

## Other directives

| Directive | Meaning |
|-----------|--------|
| `.globl label` | Make `label` visible to linker (e.g. `_start`) |
| `label:` | Define a label (name for an address) |

---

## Common instructions (short list)

| Instruction | Meaning |
|-------------|--------|
| `la rd, symbol` | Load address of symbol into rd |
| `li rd, imm` | Load immediate (constant) into rd |
| `lw rd, offset(rs)` | Load word from memory [rs + offset] |
| `sw rs, offset(rd)` | Store word to memory [rd + offset] |
| `addi rd, rs, imm` | rd = rs + imm |
| `sub rd, rs1, rs2` | rd = rs1 - rs2 |
| `mv rd, rs` | rd = rs (copy register) |
| `ecall` | System call (use a7 for number, a0 for arg) |
| `jal rd, label` | Jump and link (call; return addr in rd) |
| `jal label` | Short for jal ra, label |
| `call label` | Call function (saves return address) |
| `ret` | Return (jump to return address) |
| `j label` | Unconditional jump |

---

## Branches

| Instruction | Meaning |
|-------------|--------|
| `beq rs1, rs2, label` | Branch if rs1 == rs2 |
| `bne rs1, rs2, label` | Branch if rs1 != rs2 |
| `blt rs1, rs2, label` | Branch if rs1 < rs2 (signed) |
| `ble rs1, rs2, label` | Branch if rs1 <= rs2 (signed) |
| `bgt rs1, rs2, label` | Branch if rs1 > rs2 (signed) |
| `bge rs1, rs2, label` | Branch if rs1 >= rs2 (signed) |
| `bltz rs, label` | Branch if rs < 0 |
| `blez rs, label` | Branch if rs <= 0 |
| `bgtz rs, label` | Branch if rs > 0 |
| `beqz rs, label` | Branch if rs == 0 |
| `bnez rs, label` | Branch if rs != 0 |

---

## Common syscalls (a7 = number, a0 = arg/result)

| a7 | Action | a0 |
|----|--------|-----|
| 1 | Print integer | value to print |
| 4 | Print string | address of string |
| 10 | Exit program | (ignored) |

---

## Registers (abbreviations)

| Name | Use |
|------|-----|
| a0–a7 | Arguments / return value (a0) |
| t0–t6 | Temporaries (caller-saved) |
| ra | Return address |
| sp | Stack pointer |
