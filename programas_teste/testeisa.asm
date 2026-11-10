# ARQUIVO PARA TESTAR TODAS AS OPERAÇÕES DA ISA

# JALR __________________

# INICIALIZACAO DE TESTES
  addi x5, x0, 5
  jalr x6, x5, 0
  addi x7, x0, 1
  jal x0, fim_jalr
  addi x8, x0, 3
  addi x9, x0, 2
  jalr x0, x6, 0

  fim_jalr:


# INSTRUCOES ARITMETICAS

# INICIALIZACAO DE TESTES
  addi x5, x0, 10
  addi x6, x0, 5
  addi x7, x0, 2

  add x9, x5, x6   #15
  sub x10, x5, x6  #5
  mul x11, x5, x6  #50
  div x12, x5, x6  #2
  rem x13, x5, x6  #0
  mac x10, x6, x7  #15


# INSTRUCOES LOGICAS __________________

# INICIALIZACAO DE TESTES
  addi x5, x0, 10
  addi x6, x0, 12

  or x9, x5, x6
  and x10, x5, x6
  xor x11, x5, x6
  not x12, x5, x0


# INSTRUCOES DE BRANCH ________________

# INICIALIZACAO DE TESTES
  addi x5, x0, 4
  addi x6, x0, 2
  addi x7, x0, 8
  addi x8, x0, -8

  #SEM IMEDIATO
  sll x9, x5, x6
  srl x10, x7, x6
  sra x11, x8, x6
  
  #COM IMEDIATO
  slli x12, x5, 2
  srli x13, x11, 2


# INSTRUCOES DE MEMORIA ________________

# INICIALIZACAO DE TESTES
  addi x5, x0, 20
  addi x6, x0, 4

  sw x6, x5, 2
  lw x7, x6, 2 #x7 = 20


# INSTRUCOES DE SALTO (retorno 2 = ocorreu desvio|retorno 1 = nao ocorreu desvio)

# INICIALIZACAO DE TESTES
  addi x5, x0, 10
  addi x6, x0, 8
  add x7, x0, x5
  addi x8, x0, -8


  #igualdade sucedida
  beq x5, x7, beq_s
  addi x9, x0, 1
  jal x0, prox1
  beq_s:
  addi x9, x0, 2

  prox1:
  #igualdade falha
  beq x5, x6, beq_n
  addi x9, x0, 1
  jal x0, prox2
  beq_n:
  addi x9, x0, 2


  prox2:
  #desigualdade sucedida
  bne x5, x6, bne_s
  addi x10, x0, 1
  jal x0, prox3
  bne_s:
  addi x10, x0, 2

  prox3:
  #desigualdade falha
  bne x5, x7, bne_n
  addi x10, x0, 1
  jal x0, prox4
  bne_n:
  addi x10, x0, 2


  prox4:
  #menor sucedido
  blt x6, x5, blt_s
  addi x11, x0, 1
  jal x0, prox5
  blt_s:
  addi x11, x0, 2

  prox5:
  #menor falho
  blt x5, x6, blt_n
  addi x11, x0, 1
  jal x0, prox6
  blt_n:
  addi x11, x0, 2


  prox6:
  #maior ou igual sucedido
  bge x5, x7, bge_s
  addi x13, x0, 1
  jal x0, prox7
  bge_s:
  addi x13, x0, 2

  prox7:
  #maior ou igual falho
  bge x8, x7, bge_n
  addi x13, x0, 1
  jal x0, fim_saltos
  bge_n:
  addi x13, x0, 2


fim_saltos: