main:
  addi x2, x0, 100
  slli x2, x2, 1
  addi x4, x0, 3
  addi x5, x0, 4
  jal  x1, exprec
  sw   x3, x0, 10
  fim:
  jal x0, fim
 
exprec:
  addi x9, x0, 1
  bne  x5, x9, exprec_rec
  addi x3, x4, 0
  jalr x0, x1, 0

exprec_rec:
  addi x2, x2, -2
  sw   x1, x2, 0
  sw   x4, x2, 1
  addi x5, x5, -1
  jal  x1, exprec
  lw   x4, x2, 1
  mul  x3, x4, x3
  lw   x1, x2, 0
  addi x2, x2, 2
  jalr x0, x1, 0