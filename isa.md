# Trabalho ISA e Microarquitetura

Feito por:   
André Luiz Hlatchuk (GRR20261342)   
Renan Feitosa (GRR2026XXXX)

# Formato de Instruções

<table align="center" style="text-align: center; border-collapse: collapse;">
  <thead>
    <tr>
      <th align="center">19</th>
      <th align="center">16</th>
      <th align="center">15</th>
      <th align="center">12</th>
      <th align="center">11</th>
      <th align="center">8</th>
      <th align="center">7</th>
      <th align="center">4</th>
      <th align="center">3</th>
      <th align="center">0</th>
      <th align="center">Tipo</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td colspan="2" align="center"><b>funct</b></td>
      <td colspan="2" align="center"><b>rs2</b></td>
      <td colspan="2" align="center"><b>rs1</b></td>
      <td colspan="2" align="center"><b>rd</b></td>
      <td colspan="2" align="center"><b>opcode</b></td>
      <td align="center"><b>R</b></td>
    </tr>
    <tr>
      <td colspan="4" align="center"><b>imm</b></td>
      <td colspan="2" align="center"><b>rs1</b></td>
      <td colspan="2" align="center"><b>rd</b></td>
      <td colspan="2" align="center"><b>opcode</b></td>
      <td align="center"><b>I</b></td>
    </tr>
    <tr>
      <td colspan="4" align="center"><b>imm</b></td>
      <td colspan="2" align="center"><b>rs1</b></td>
      <td colspan="2" align="center"><b>rs2</b></td>
      <td colspan="2" align="center"><b>opcode</b></td>
      <td align="center"><b>B</b></td>
    </tr>
    <tr>
      <td colspan="6" align="center"><b>imm</b></td>
      <td colspan="2" align="center"><b>rd</b></td>
      <td colspan="2" align="center"><b>opcode</b></td>
      <td align="center"><b>J</b></td>
    </tr>
  </tbody>
</table>

# Instruções 

| Tipo | Instrução | Descrição | Modo de Uso | Opcode | Funct |
| :---: | :---: | :---: | :---: | :---: | :---: |
| R | add | rd \= rs1 \+ rs2 | add, rd, rs1, rs2 | 0000 | 0000 |
| R | sub | rd \= rs1 \- rs2 | sub rd, rs1, rs2 | 0000 | 0001 |
| R | mul | rd \= rs1 \* rs2 | mul rd, rs1, rs2 | 0000 | 0010 |
| R | div | rd \= rs1 / rs2 | div rd, rs1, rs2 | 0000 | 0011 |
| R | rem | rd \= rs1 % rs2 | rem rd, rs1, rs2 | 0000 | 0100 |
| R | or | rd \= rs1 | rs2 | or rd, rs1, rs2 | 0000 | 0101 |
| R | and | rd \= rs1 & rs2 | and rd, rs1, rs2 | 0000 | 0110 |
| R | xor | rd \= rs1 ^ rs2 | xor rd, rs1, rs2 | 0000 | 0111 |
| R | sll | rd \= rs1 \<\< rs2 | sll rd, rs1, rs2 | 0000 | 1000 |
| R | srl | rd \= rs1 \>\> rs2 | srl rd, rs1, rs2 | 0000 | 1001 |
| R | not | rd \= \!rs1 | not rd, rs1, x0 | 0000 | 1010 |
| R | sra | rd \= rs1 \>\> rs2 | sra rd, rs1, sr2 | 0000 | 1011 |
| R | mac | rd \= rd \+ (rs1 \* rs2) | mac rd, rs1, rs2 | 0000 | 1100 |
| I | addi | rd \= rs1 \+ imm | addi rd, rs1, imm | 0001 |  |
| I | slli | rd \= rs1 \<\< imm | slli rd, rs1, imm | 0010 |  |
| I | srli | rd \= rs1 \>\> imm | srli rd, rs1, imm | 0011 |  |
| I | sw | M \[rd \+ imm\] \= rs1 | sw rd, rs1, imm | 0100 |  |
| I | lw | rd \= M \[rs1 \+ imm\] | lw rd, rs1, imm | 0101 |  |
| B | beq | if (rs1 \== rs2) PC \+= imm | beq rs1, rs2, imm | 0110 |  |
| B | bne | if (rs1 \!= rs2) PC \+= imm | bne rs1, rs2, imm | 0111 |  |
| B | blt | if (rs1 \< rs2) PC \+= imm | blt rs1, rs2, imm | 1000 |  |
| B | bge | if (rs1 \>= rs2) PC \+= imm | bge rs1, rs2, imm | 1001 |  |
| J | jal | rd \= PC \+ 1; PC \+= imm | jal rd, imm | 1010 |  |
| I | jalr | rd \= PC \+ 1; PC \= rs1 \+ imm | jalr rd, rs1, imm | 1011 |  |
| I | ebreak | Finaliza o programa | ebreak | 1100 |  |
| Expansão Futura |  |  |  | 1101 |  |
| Expansão Futura |  |  |  | 1110 |  |
| Expansão Futura |  |  |  | 1111 |  |

# Registradores

| Registrador | Convenção | Descrição |
| :---- | :---- | :---- |
| x0 | zero | Constante Zero |
| x1 | ra | Endereço de Retorno |
| x2 | sp | Ponteiro de Pilha |
| x3 \- x4 | a0 \-a1 | Argumento / Retorno de Função  |
| x5 \- x8 | a2 \- a5 | Argumentos de Função |
| x9 \- x15 | t0 \- t6 | Temporários |

