

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
la s0, m # row m = 10
lw s0, 0(s0) # s0 = 10 (row)
la s1, n # column = 0
lw s1, 0(s1) #s1 = 9
la s2, matrix_a #load address of mat a into s2
la s3, matrix_b #load address of mat b into s3
la s4, matrix_c #load address of mat c into s4
la a0, msga #load address of msga
la a1, matrix_a #load address of mat a into a1
add a2, s0, zero #load row=10 into a2
add a3, s1, zero #load col=9 into a3
jal PRINT_MAT #jumps to print_mat
la a0, msgb
la a1, matrix_b
add a2, s1, zero
add a3, s0, zero
jal PRINT_MAT
# Your CODE HERE 
# must also use slli for multiplcation !!!!!
addi t0, x0, 0 # i = 0 (rows)
addi t1, x0, 0 # j = 0 (col)
addi t2, x0, 0 # k = 0 (inner index)
loop_1:
bge t0, s0, loop_2
jal loop_1
loop_2:
bge t1, s1, loop_3
jal loop_2
loop_3:
bge t2, s1, done 
jal loop_3
done:

# End CODE
la a0, msgc
la a1, matrix_c
add a2, s1, zero
add a3, s1, zero
jal PRINT_MAT
# Exit
li a7,10
ecall
PRINT_MAT: 
li a7,4 #loads 4 for printing string prints whatever is in a0
ecall #prints string at a7
addi a4,x0,0 # loads constant 0 into a4
PL4: 
bge a4,a3,PL1 
addi a5,x0,0
PL3: 
bge a5,a2,PL2
lw a0,0(a1)
li a7,1
ecall
la a0,space
li a7,4
ecall
addi a1,a1,4
addi a5,a5,1
b PL3
PL2: 
addi a4,a4,1
la a0,nline
li a7,4
ecall
b PL4
PL1: 
jr ra