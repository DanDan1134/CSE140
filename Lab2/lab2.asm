

# Traditional Matrix Multiply program
.data
matrix_a:
.word 1, 2, 3, 4, 5, 6, 7, 8, 9, 10
.word 2, 3, 4, 5, 6, 7, 8, 9, 10, 1
.word 3, 4, 5, 6, 7, 8, 9, 10, 1, 2
.word 4, 5, 6, 7, 8, 9, 10, 1, 2, 3
.word 5, 6, 7, 8, 9, 10, 1, 2, 3, 4
.word 6, 7, 8, 9, 10, 1, 2, 3, 4, 5
.word 7, 8, 9, 10, 1, 2, 3, 4, 5, 6
.word 8, 9, 10, 1, 2, 3, 4, 5, 6, 7
.word 9, 10, 1, 2, 3, 4, 5, 6, 7, 8
matrix_b:
.word 1, 2, 3, 4, 5, 6, 7, 8, 9
.word 2, 3, 4, 5, 6, 7, 8, 9, 1
.word 3, 4, 5, 6, 7, 8, 9, 1, 2
.word 4, 5, 6, 7, 8, 9, 1, 2, 3
.word 5, 6, 7, 8, 9, 1, 2, 3, 4
.word 6, 7, 8, 9, 1, 2, 3, 4, 5
.word 7, 8, 9, 1, 2, 3, 4, 5, 6
.word 8, 9, 1, 2, 3, 4, 5, 6, 7
.word 9, 1, 2, 3, 4, 5, 6, 7, 8
.word 8, 7, 6, 5, 4, 3, 2, 1, 9
matrix_c:
.word 0, 0, 0, 0, 0, 0, 0, 0, 0,
.word 0, 0, 0, 0, 0, 0, 0, 0, 0,
.word 0, 0, 0, 0, 0, 0, 0, 0, 0,
.word 0, 0, 0, 0, 0, 0, 0, 0, 0,
.word 0, 0, 0, 0, 0, 0, 0, 0, 0,
.word 0, 0, 0, 0, 0, 0, 0, 0, 0,
.word 0, 0, 0, 0, 0, 0, 0, 0, 0,
.word 0, 0, 0, 0, 0, 0, 0, 0, 0,
.word 0, 0, 0, 0, 0, 0, 0, 0, 0
m: .word 10
n: .word 9
nline: .string "\n" #Define new line string
space: .string " "
msga: .string "Matrix A is: \n"
msgb: .string "Matrix B is: \n"
msgc: .string "Matrix C=A*B is: \n"
.text
.globl main
main:
la s0, m
lw s0, 0(s0)
la s1, n
lw s1, 0(s1)
la s2, matrix_a
la s3, matrix_b
la s4, matrix_c
la a0, msga
la a1, matrix_a
add a2, s0, zero
add a3, s1, zero
jal PRINT_MAT
la a0, msgb
la a1, matrix_b
add a2, s1, zero
add a3, s0, zero
jal PRINT_MAT
# Your CODE HERE
# End CODE
la a0, msgc
la a1, matrix_c
add a2, s1, zero
add a3, s1, zero
jal PRINT_MAT
# Exit
li a7,10
ecall
PRINT_MAT: li a7,4
ecall
addi a4,x0,0
PL4: bge a4,a3,PL1
addi a5,x0,0
PL3: bge a5,a2,PL2
lw a0,0(a1)
li a7,1
ecall
la a0,space
li a7,4
ecall
addi a1,a1,4
addi a5,a5,1
b PL3
PL2: addi a4,a4,1
la a0,nline
li a7,4
ecall
b PL4
PL1: jr ra
