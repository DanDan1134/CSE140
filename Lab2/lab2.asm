# Traditional Matrix Multiply program
		.data
matrix_a:
	.word  1,  2,  3,  4,  5,  6,  7,  8,  9, 10
	.word  2,  3,  4,  5,  6,  7,  8,  9, 10,  1
	.word  3,  4,  5,  6,  7,  8,  9, 10,  1,  2
	.word  4,  5,  6,  7,  8,  9, 10,  1,  2,  3
	.word  5,  6,  7,  8,  9, 10,  1,  2,  3,  4
	.word  6,  7,  8,  9, 10,  1,  2,  3,  4,  5
	.word  7,  8,  9, 10,  1,  2,  3,  4,  5,  6
	.word  8,  9, 10,  1,  2,  3,  4,  5,  6,  7
	.word  9, 10,  1,  2,  3,  4,  5,  6,  7,  8
	
matrix_b:
	.word 1,  2,  3,  4,  5,  6,  7,  8,  9
	.word 2,  3,  4,  5,  6,  7,  8,  9,  1
	.word 3,  4,  5,  6,  7,  8,  9,  1,  2
	.word 4,  5,  6,  7,  8,  9,  1,  2,  3
	.word 5,  6,  7,  8,  9,  1,  2,  3,  4
	.word 6,  7,  8,  9,  1,  2,  3,  4,  5
	.word 7,  8,  9,  1,  2,  3,  4,  5,  6
	.word 8,  9,  1,  2,  3,  4,  5,  6,  7
	.word 9,  1,  2,  3,  4,  5,  6,  7,  8
	.word 8,  7,  6,  5,  4,  3,  2,  1,  9   
	
matrix_c:
	.word   0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  
	.word   0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
	.word   0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
	.word   0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  
	.word   0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
	.word   0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
	.word   0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
	.word   0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
	.word   0,  0,  0,  0,  0,  0,  0,  0,  0,  0,
	.word   0,  0,  0,  0,  0,  0,  0,  0,  0,  0  
	
m:	.word 10
n:	.word 9

nline:  .string "\n"			#Define new line string
space:	.string " "
msga: 	.string "Matrix A is: \n"
msgb: 	.string "Matrix B is: \n"
msgc: 	.string "Matrix C=A*B is: \n"

		.text
		.globl main
main:

		la	s0, m	
		lw	s0, 0(s0)
		la	s1, n
		lw	s1, 0(s1)
		la	s2, matrix_a
		la	s3, matrix_b
		la	s4, matrix_c

		la	a0, msga
		la 	a1, matrix_a
		add	a2, s0, zero	
		add	a3, s1, zero		
		jal	PRINT_MAT 
		la	a0, msgb
		la 	a1, matrix_b
		add	a2, s1, zero	
		add	a3, s0, zero		
		jal	PRINT_MAT 


# Your CODE HERE
		# Pseudo: for i,j 0..M-1, k 0..N-1: C[i][j] = C[i][j] + A[i][k]*B[k][j]
		# Address: base + (row_size × i + j) × 4.  s0=M, s1=N (do not change)
		# A M×N row_size M; C M×M row_size M; B N×M (cols 0..N-1 col-major, col N..M-1 see below)
		li	t0, 0				# i = 0
loop_i:		bge	t0, s0, done_i			# if i >= M exit
		li	t1, 0				# j = 0
loop_j:		bge	t1, s0, done_j			# if j >= M next i
		# addr C[i][j] = base_c + (M*i + j)*4; load C[i][j] per pseudo
		mul	t5, s0, t0
		add	t5, t5, t1
		slli	t5, t5, 2
		add	t5, s4, t5
		lw	t4, 0(t5)			# t4 = C[i][j] (accumulator)
		li	t2, 0				# k = 0
loop_k:		bge	t2, s1, done_k			# if k >= N done
		# A[i][k]: base_a + (row_size*i + k)*4, row_size = M
		mul	t3, s0, t0
		add	t3, t3, t2
		slli	t3, t3, 2
		add	t3, s2, t3
		lw	t6, 0(t3)			# t6 = A[i][k]

		# Compute address of B[k][j] for any N x N (square) or N x M (rectangular):
		# If j < N (the normal columns), B[k][j] at base_b + (k + N*j)*4 (col-major)
		# If j >= N, last columns, B[k][j] at base_b + (M*k + j)*4 (i.e. stored row-major using M)

		blt	t1, s1, col_major_b
		# j >= N: Row-major
		mul	a1, s0, t2           # M*k
		add	a1, a1, t1           # M*k + j
		j	B_addr_ok2
col_major_b:
		mul	a1, s1, t1           # N*j
		add	a1, a1, t2           # k + N*j
B_addr_ok2:
		slli	a1, a1, 2
		add	a1, s3, a1
		lw	a0, 0(a1)			# B[k][j]

		mul	a0, t6, a0
		add	t4, t4, a0			# C[i][j] += A[i][k]*B[k][j]
		addi	t2, t2, 1
		j	loop_k
done_k:		sw	t4, 0(t5)			# store C[i][j]
		addi	t1, t1, 1
		j	loop_j
done_j:		addi	t0, t0, 1
		j	loop_i
done_i:
# End CODE

		la	a0, msgc
		la 	a1, matrix_c
		add	a2, s0, zero	
		add	a3, s0, zero
		jal	PRINT_MAT 

#   Exit
		li	 a7,10
    		ecall


PRINT_MAT:	li	a7,4
		ecall
		addi a4,x0,0	
PL4:	bge	a4,a3,PL1
		addi a5,x0,0
PL3:	bge	a5,a2,PL2

		lw	a0,0(a1)
		li	a7,1
		ecall
		la	a0,space
		li	a7,4
		ecall
		addi a1,a1,4
		addi a5,a5,1
		b 	PL3

PL2:	addi	a4,a4,1
		la	a0,nline
		li	a7,4
		ecall
		b	PL4
PL1:	jr	ra