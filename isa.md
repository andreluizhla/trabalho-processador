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
      <td colspan="2" align="center"><b>rs2</b></td>
      <td colspan="2" align="center"><b>rs1</b></td>
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

<table align="center" style="text-align: center; border-collapse: collapse; width: 100%;">
  <thead>
    <tr>
      <th align="center">Tipo</th>
      <th align="center">Instrução</th>
      <th align="center">Descrição</th>
      <th align="center">Modo de Uso</th>
      <th align="center">Opcode</th>
      <th align="center">Funct</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>R</td><td>add</td><td>rd = rs1 + rs2</td><td>add rd, rs1, rs2</td><td>0000</td><td>0000</td></tr>
    <tr><td>R</td><td>sub</td><td>rd = rs1 - rs2</td><td>sub rd, rs1, rs2</td><td>0000</td><td>0001</td></tr>
    <tr><td>R</td><td>mul</td><td>rd = rs1 * rs2</td><td>mul rd, rs1, rs2</td><td>0000</td><td>0010</td></tr>
    <tr><td>R</td><td>div</td><td>rd = rs1 / rs2</td><td>div rd, rs1, rs2</td><td>0000</td><td>0011</td></tr>
    <tr><td>R</td><td>rem</td><td>rd = rs1 % rs2</td><td>rem rd, rs1, rs2</td><td>0000</td><td>0100</td></tr>
    <tr><td>R</td><td>or</td><td>rd = rs1 | rs2</td><td>or rd, rs1, rs2</td><td>0000</td><td>0101</td></tr>
    <tr><td>R</td><td>and</td><td>rd = rs1 & rs2</td><td>and rd, rs1, rs2</td><td>0000</td><td>0110</td></tr>
    <tr><td>R</td><td>xor</td><td>rd = rs1 ^ rs2</td><td>xor rd, rs1, rs2</td><td>0000</td><td>0111</td></tr>
    <tr><td>R</td><td>sll</td><td>rd = rs1 &lt;&lt; rs2</td><td>sll rd, rs1, rs2</td><td>0000</td><td>1000</td></tr>
    <tr><td>R</td><td>srl</td><td>rd = rs1 &gt;&gt; rs2</td><td>srl rd, rs1, rs2</td><td>0000</td><td>1001</td></tr>
    <tr><td>R</td><td>not</td><td>rd = !rs1</td><td>not rd, rs1, x0</td><td>0000</td><td>1010</td></tr>
    <tr><td>R</td><td>sra</td><td>rd = rs1 &gt;&gt; rs2</td><td>sra rd, rs1, rs2</td><td>0000</td><td>1011</td></tr>
    <tr><td>R</td><td>mac</td><td>rd = rd + (rs1 * rs2)</td><td>mac rd, rs1, rs2</td><td>0000</td><td>1100</td></tr>
    
    <tr><td>I</td><td>addi</td><td>rd = rs1 + imm</td><td>addi rd, rs1, imm</td><td>0001</td><td></td></tr>
    <tr><td>I</td><td>slli</td><td>rd = rs1 &lt;&lt; imm</td><td>slli rd, rs1, imm</td><td>0010</td><td></td></tr>
    <tr><td>I</td><td>srli</td><td>rd = rs1 &gt;&gt; imm</td><td>srli rd, rs1, imm</td><td>0011</td><td></td></tr>
    <tr><td>I</td><td>sw</td><td>M[rd + imm] = rs1</td><td>sw rd, rs1, imm</td><td>0100</td><td></td></tr>
    <tr><td>I</td><td>lw</td><td>rd = M[rs1 + imm]</td><td>lw rd, rs1, imm</td><td>0101</td><td></td></tr>
    
    <tr><td>B</td><td>beq</td><td>if (rs1 == rs2) PC += imm</td><td>beq rs1, rs2, imm</td><td>0110</td><td></td></tr>
    <tr><td>B</td><td>bne</td><td>if (rs1 != rs2) PC += imm</td><td>bne rs1, rs2, imm</td><td>0111</td><td></td></tr>
    <tr><td>B</td><td>blt</td><td>if (rs1 &lt; rs2) PC += imm</td><td>blt rs1, rs2, imm</td><td>1000</td><td></td></tr>
    <tr><td>B</td><td>bge</td><td>if (rs1 &gt;= rs2) PC += imm</td><td>bge rs1, rs2, imm</td><td>1001</td><td></td></tr>
    
    <tr><td>J</td><td>jal</td><td>rd = PC + 1; PC += imm</td><td>jal rd, imm</td><td>1010</td><td></td></tr>
    <tr><td>I</td><td>jalr</td><td>rd = PC + 1; PC = rs1 + imm</td><td>jalr rd, rs1, imm</td><td>1011</td><td></td></tr>
    <tr><td>I</td><td>ebreak</td><td colspan="3">Finaliza o programa</td><td>1100</td><td></td></tr>
   
    <tr>
      <td rowspan="3" style="vertical-align: middle;">Expansão<br>Futura</td>
      <td rowspan="3" colspan="3" style="vertical-align: middle; color: gray;">Reservado para implementações futuras</td>
      <td>1101</td>
      <td></td>
    </tr>
    <tr>
      <td>1110</td>
      <td></td>
    </tr>
    <tr>
      <td>1111</td>
      <td></td>
    </tr>
  </tbody>
</table>

# Registradores

| Registrador | Convenção | Descrição |
| :---- | :---- | :---- |
| x0 | zero | Constante Zero |
| x1 | ra | Endereço de Retorno |
| x2 | sp | Ponteiro de Pilha |
| x3 \- x4 | a0 \-a1 | Argumento / Retorno de Função  |
| x5 \- x8 | a2 \- a5 | Argumentos de Função |
| x9 \- x15 | t0 \- t6 | Temporários |

