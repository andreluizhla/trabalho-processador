main:
  addi x6, x0, 3
  addi x7, x0, 16
  addi x8, x0, 32
  mul  x14, x6, x6
 
# INICIALIZACAO MATRIZES
  addi x5, x0, 0

inic:
  addi x12, x5, 1
  sw   x12, x5, 0
  rem  x13, x5, x6
  addi x13, x13, 1
  add  x11, x5, x7
  sw   x13, x11, 0
  addi x5, x5, 1
  blt  x5, x14, inic
 
# MULTIPLICACAO
  addi x3, x0, 0

loop_i:
  addi x4, x0, 0

loop_j:
  addi x9, x0, 0
  addi x5, x0, 0

loop_k:
  mul  x10, x3, x6
  add  x10, x10, x5
  lw   x12, x10, 0
  mul  x11, x5, x6
  add  x11, x11, x4
  add  x11, x11, x7
  lw   x13, x11, 0
  mac  x9, x12, x13
  addi x5, x5, 1
  blt  x5, x6, loop_k
 
  mul  x10, x3, x6
  add  x10, x10, x4
  add  x10, x10, x8
  sw   x9, x10, 0
  addi x4, x4, 1
  blt  x4, x6, loop_j
  addi x3, x3, 1
  blt  x3, x6, loop_i
  fim:
  jal x0, fim