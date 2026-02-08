.data
array:
.word 5, 1, 4, 2, 8          # numbers to sort
msg_input:
.string "Input array is: "     # label before array
msg_sorted:
.string "\nSorted array is: "  # label after sort
space:
.string " "                   # space between numbers
newline:
.string "\n"                  # newline at end
.text
.globl _start
_start:
##################################################
# Print input array
##################################################
la a0, msg_input              # load message address
li a7, 4                      # print string syscall
ecall
la t0, array                  # load array start
li t1, 5                      # number of elements
li t2, 0                      # loop index i = 0
jal print_loop
##################################################
# Call bubble sort
##################################################
la a0, array                  # array pointer arg
li a1, 5                      # length arg
call bubble_sort
##################################################
# Print sorted
##################################################
la a0, msg_sorted             # load sorted message
li a7, 4                      # print string
ecall
la t0, array                  # load array again
li t1, 5                      # element count
li t2, 0                      # index = 0
jal print_loop
li a7, 10                     # exit program syscall
ecall
############################################################
# bubble_sort
############################################################
bubble_sort:
li a6, 1                      # constant 1
sub t0, a1, a6                # n - 1 (outer limit)
blez t0, done                 # skip if empty/one
outer_loop:
li t1, 0                      # inner index j = 0
mv t2, a0                     # current element pointer
li t6, 0                      # swap flag = false
inner_loop:
lw t3, 0(t2)                  # load current element
lw t4, 4(t2)                  # load next element
ble t3, t4, no_swap           # skip if in order
sw t4, 0(t2)                  # swap: write next here
sw t3, 4(t2)                  # swap: write current there
li t6, 1                      # set swap happened
no_swap:
addi t2, t2, 4                # move to next element
addi t1, t1, 1                # j++
blt t1, t0, inner_loop        # repeat inner loop
beqz t6, done                 # done if no swaps
sub t0, t0, a6                # outer limit--
bgtz t0, outer_loop           # repeat outer loop
done:
ret
############################################################
# print messages
############################################################
print_loop:
beq t2, t1, print_done        # done when i == count
lw a0, 0(t0)                  # load element to print
li a7, 1                      # print integer syscall
ecall
la a0, space                  # load space string
li a7, 4                      # print string
ecall
addi t0, t0, 4                # next array element
addi t2, t2, 1                # i++
j print_loop
print_done:
la a0, newline                # load newline
li a7, 4                      # print string
ecall
ret