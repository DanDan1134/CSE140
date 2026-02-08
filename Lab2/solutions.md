# Lab 2 Solutions

## 1. Matrix multiplication (RISC-V)

### Algorithm

Standard triple loop:

```
for (i = 0; i < M; i++)
  for (j = 0; j < M; j++)
    for (k = 0; k < N; k++)
      C[i][j] += A[i][k] * B[k][j]
```

- **A** is M×N (rows × cols), **B** is N×M, **C** is M×M.
- Skeleton sets: `s0 = M`, `s1 = N`, `s2 = base_a`, `s3 = base_b`, `s4 = base_c`. Do not change these.

### 2D address formula

Element size = 4 bytes. For a matrix with **row_size** columns:

- Address of element `[i][j]` = **base + (row_size × i + j) × 4**

So (skeleton layout):

- **A[i][k]:** `base_a + (M*i + k)*4`  (A stored with M=10 words per row; use first N=9)
- **B[k][j]:** cols 0..8: `base_b + (k + N*j)*4` (column-major); col 9: indices 9,19,…,79,**81**
- **C[i][j]:** `base_c + (M*i + j)*4`  (C has M columns)

### First row of C = row 0 of A · each column of B (dot products)

Row 0 of A = [1, 2, 3, 4, 5, 6, 7, 8, 9]. Column j of B has 9 entries B[0][j]..B[8][j].

| j | C[0][j] = Σₖ A[0][k]·B[k][j] | Result |
|---|------------------------------|--------|
| 0 | 1·1+2·2+3·3+4·4+5·5+6·6+7·7+8·8+9·9 | **285** |
| 1 | 1·2+2·3+3·4+4·5+5·6+6·7+7·8+8·9+9·1 | **249** |
| 2 | 1·3+2·4+3·5+4·6+5·7+6·8+7·9+8·1+9·2 | **222** |
| 3 | 1·4+2·5+3·6+4·7+5·8+6·9+7·1+8·2+9·3 | **204** |
| 4 | 1·5+2·6+3·7+4·8+5·9+6·1+7·2+8·3+9·4 | **195** |
| 5 | 1·6+2·7+3·8+4·9+5·1+6·2+7·3+8·4+9·5 | **195** |
| 6 | 1·7+2·8+3·9+4·1+5·2+6·3+7·4+8·5+9·6 | **204** |
| 7 | 1·8+2·9+3·1+4·2+5·3+6·4+7·5+8·6+9·7 | **222** |
| 8 | 1·9+2·1+3·2+4·3+5·4+6·5+7·6+8·7+9·8 | **249** |
| 9 | 1·2+2·3+3·4+4·5+5·6+6·7+7·8+8·9+9·**8** | **312** |

So first row of C = 285, 249, 222, 204, 195, 195, 204, 222, 249, 312. (Column 9 needs B[8][9]=8 from index 81.)

**Why 246 instead of 312?** C[0][9] = 1·B[0][9]+…+9·B[8][9]. For 312 we need B[:,9] = [2,3,4,5,6,7,8,9,**8**]. So the last term must load **8** from word index **81** (first element of file row 9). If we use index **89** we load **9** → sum = 321. If we use index **81** we load **8** → sum = 312. So for j=9 and k=8 the code must use offset **81** (e.g. `li a1, 81`), not 89.

### Register usage in the solution

| Register | Role |
|----------|------|
| s0 | M (unchanged) |
| s1 | N (unchanged) |
| s2 | base of matrix_a |
| s3 | base of matrix_b |
| s4 | base of matrix_c |
| t0 | loop index i |
| t1 | loop index j |
| t2 | loop index k |
| t3 | address of A[i][k] |
| t4 | accumulator for C[i][j] |
| t5 | address of C[i][j] |
| t6 | value A[i][k] |
| a0 | value B[k][j], then product A[i][k]*B[k][j] |
| a1 | address of B[k][j] (only inside the loop; PRINT_MAT sets a1 after) |

### Implementation outline

1. **Outer loop (i):** `t0 = 0..M-1`
2. **Middle loop (j):** `t1 = 0..M-1`
   - Compute address of C[i][j] and load current value into `t4`.
3. **Inner loop (k):** `t2 = 0..N-1`
   - Compute address of A[i][k], load into `t6`.
   - Compute address of B[k][j], load into `a0`.
   - `t4 += t6 * a0`.
4. After inner loop: store `t4` back to C[i][j], then increment j or i and branch.

### Expected output (test case)

With the given `matrix_a` and `matrix_b`, the printed **Matrix C = A*B** should be:

```
285 249 222 204 195 195 204 222 249 312
330 294 267 249 240 240 249 267 294 364
285 329 292 264 245 235 234 242 259 336
250 284 327 289 260 240 229 227 234 298
225 249 282 324 285 255 234 222 219 270
210 224 247 279 320 280 249 227 214 252
205 209 222 244 275 315 274 242 219 244
210 204 207 219 240 270 309 267 234 246
225 209 202 204 215 235 264 302 259 258
285 249 222 204 195 195 204 222 249 312
```

### Testing in RARS

1. Assemble and run; compare output to the matrix above.
2. Change `m` and `n` in `.data` and the matrix sizes/data to test other M×N and N×M sizes.
3. For instruction-count extra credit: **Tools → Instruction Counter**, connect to program, then run.

### Submission

- Rename the file to: **`cse140_YourFirst_YourLast_mm.asm`** (e.g. `cse140_Mario_Uppal_mm.asm`).
- Submit this `.asm` file to CatCourse.
- Submit the Performance part (zyBook 1.6, 1.7, and exercises 1.15.6, 1.15.15) as a separate PDF as required.

---

## 2–4. Performance (zyBook)

- **Problem 2:** Complete Participation Activities in zyBook sections 1.6 and 1.7 online.
- **Problem 3:** Exercise 1.15.6 — do in Word, export as PDF, submit.
- **Problem 4:** Exercise 1.15.15 — do in Word, export as PDF, submit.

Submit the PDF for 3 and 4 to CatCourse by the deadline (before the next lab, e.g. 2/17 1:29 PM if lab is 2/10 1:30 PM).
