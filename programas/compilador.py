#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
montador.py - Montador (assembler) para a ISA do trabalho de ISA e Microarquitetura.

Codifica um programa .asm em palavras de 20 bits e gera um arquivo no
formato "v3.0 hex words plain", que o Logisim carrega em uma memoria
(RAM/ROM) com Data Bits = 20.

Uso:
    python3 montador.py programa.asm
    python3 montador.py programa.asm -o programa.hex
    python3 montador.py programa.asm -o programa.hex --bin
    python3 montador.py programa.asm -v

Formato das instrucoes (20 bits):
    R: funct[19:16] rs2[15:12] rs1[11:8] rd[7:4] opcode[3:0]
    I: imm[19:12]   rs1[11:8]  rd[7:4]  opcode[3:0]
    B: imm[7:4][19:16] rs2[15:12] rs1[11:8] imm[3:0][7:4] opcode[3:0]
    J: imm[19:8]               rd[7:4]  opcode[3:0]

Convencao de deslocamento (branch/jump): imm = rotulo - endereco_da_instrucao.
Se a sua microarquitetura somar o imediato DEPOIS de PC+1, troque a constante
BRANCH_REL_TO_NEXT para True.
"""

import argparse
import os
import re
import sys

WORD_BITS = 20

# Se True: imm = rotulo - (endereco_da_instrucao + 1)
# Se False: imm = rotulo - endereco_da_instrucao
BRANCH_REL_TO_NEXT = False


# ---------------------------------------------------------------------------
# Erros
# ---------------------------------------------------------------------------
class AsmError(Exception):
    pass


# ---------------------------------------------------------------------------
# Registradores
# ---------------------------------------------------------------------------
REGISTERS = {
    "zero": 0, "ra": 1, "sp": 2,
    "a0": 3, "a1": 4,
    "a2": 5, "a3": 6, "a4": 7, "a5": 8,
    "t0": 9, "t1": 10, "t2": 11, "t3": 12, "t4": 13, "t5": 14, "t6": 15,
}
for _i in range(16):
    REGISTERS["x%d" % _i] = _i


# ---------------------------------------------------------------------------
# Opcodes / functs
# ---------------------------------------------------------------------------
OP_R      = 0x0
OP_ADDI   = 0x1
OP_SLLI   = 0x2
OP_SRLI   = 0x3
OP_SW     = 0x4
OP_LW     = 0x5
OP_BEQ    = 0x6
OP_BNE    = 0x7
OP_BLT    = 0x8
OP_BGE    = 0x9
OP_JAL    = 0xA
OP_JALR   = 0xB
OP_EBREAK = 0xC

R_FUNCT = {
    "add": 0x0, "sub": 0x1, "mul": 0x2, "div": 0x3,
    "rem": 0x4, "or":  0x5, "and": 0x6, "xor": 0x7,
    "not": 0x8, "sll": 0x9, "srl": 0xA, "sra": 0xB,
    "mac": 0xC,
}

I_OPCODE = {
    "addi": OP_ADDI, "slli": OP_SLLI, "srli": OP_SRLI,
    "sw":   OP_SW,   "lw":   OP_LW,
}

B_OPCODE = {"beq": OP_BEQ, "bne": OP_BNE, "blt": OP_BLT, "bge": OP_BGE}

J_OPCODE = {"jal": OP_JAL}


# ---------------------------------------------------------------------------
# Codificadores (20 bits)
# ---------------------------------------------------------------------------
def r_type(funct, rs2, rs1, rd):
    return (((funct & 0xF) << 16) | ((rs2 & 0xF) << 12) |
            ((rs1 & 0xF) << 8)   | ((rd & 0xF) << 4) | OP_R)


def i_type(imm, rs1, rd, opcode):
    return (((imm & 0xFF) << 12) | ((rs1 & 0xF) << 8) |
            ((rd & 0xF) << 4)    | (opcode & 0xF))


def b_type(imm, rs2, rs1, opcode):
    imm_hi = (imm >> 4) & 0xF
    imm_lo = imm & 0xF
    return (((imm_hi & 0xF) << 16) | ((rs2 & 0xF) << 12) |
            ((rs1 & 0xF) << 8)   | ((imm_lo & 0xF) << 4) | (opcode & 0xF))


def j_type(imm, rd, opcode):
    return (((imm & 0xFFF) << 8) | ((rd & 0xF) << 4) | (opcode & 0xF))


# ---------------------------------------------------------------------------
# Helpers de parsing
# ---------------------------------------------------------------------------
def strip_comment(line):
    for marker in ("#", "//", ";"):
        idx = line.find(marker)
        if idx >= 0:
            line = line[:idx]
    return line


def reg(tok):
    t = tok.strip().lower()
    if t not in REGISTERS:
        raise AsmError("registrador invalido: '%s'" % tok)
    return REGISTERS[t]


def number(tok):
    t = tok.strip()
    try:
        return int(t, 0)          # 0x.., 0b.., 0o.., decimal, negativo
    except ValueError:
        pass
    try:
        return int(t, 10)         # evita falhar em coisas como "08"
    except ValueError:
        raise AsmError("numero invalido: '%s'" % tok)


def check_range(value, bits, what):
    lo = -(1 << (bits - 1))
    hi = (1 << (bits - 1)) - 1
    if not (lo <= value <= hi):
        raise AsmError("%s fora do intervalo de %d bits com sinal (%d..%d): %d"
                       % (what, bits, lo, hi, value))


def expect_ops(mnem, ops, n):
    if len(ops) != n:
        raise AsmError("'%s' espera %d operando(s), mas recebeu %d"
                       % (mnem, n, len(ops)))


def branch_offset(tok, labels, addr):
    t = tok.strip()
    if t in labels:
        base = addr + 1 if BRANCH_REL_TO_NEXT else addr
        return labels[t] - base
    return number(t)


# ---------------------------------------------------------------------------
# Parsing do fonte
# ---------------------------------------------------------------------------
def parse_source(source):
    entries = []
    for lineno, raw in enumerate(source.splitlines(), 1):
        line = strip_comment(raw).strip()

        labels = []
        while True:
            m = re.match(r"^([A-Za-z_.$][A-Za-z0-9_.$]*)\s*:\s*(.*)$", line)
            if not m:
                break
            labels.append(m.group(1))
            line = m.group(2).strip()

        mnem = None
        ops = []
        if line:
            parts = line.split(None, 1)
            mnem = parts[0].lower()
            rest = parts[1].strip() if len(parts) > 1 else ""
            if rest:
                ops = [o.strip() for o in rest.split(",")]

        entries.append({"line": lineno, "labels": labels,
                        "mnem": mnem, "ops": ops, "addr": None})
    return entries


def first_pass(entries):
    labels = {}
    addr = 0
    for e in entries:
        for lab in e["labels"]:
            if lab in labels:
                raise AsmError("rotulo duplicado: '%s' (linha %d)" % (lab, e["line"]))
            labels[lab] = addr
        if e["mnem"] is None:
            continue
        e["addr"] = addr
        addr += 1
    return labels


# ---------------------------------------------------------------------------
# Codificacao de uma instrucao
# ---------------------------------------------------------------------------
def encode_instruction(entry, labels):
    mnem = entry["mnem"]
    ops = entry["ops"]
    addr = entry["addr"]

    # ---------------- pseudo-instrucoes (1 instrucao cada) ----------------
    if mnem == "nop":
        expect_ops(mnem, ops, 0)
        return r_type(0x0, 0, 0, 0)                       # add x0, x0, x0

    if mnem == "li":
        expect_ops(mnem, ops, 2)
        rd, imm = reg(ops[0]), number(ops[1])
        check_range(imm, 8, "imediato de 'li'")
        return i_type(imm, 0, rd, OP_ADDI)                # addi rd, x0, imm

    if mnem == "mv":
        expect_ops(mnem, ops, 2)
        rd, rs = reg(ops[0]), reg(ops[1])
        return r_type(0x0, 0, rs, rd)                     # add rd, rs, x0

    if mnem == "j":
        expect_ops(mnem, ops, 1)
        off = branch_offset(ops[0], labels, addr)
        check_range(off, 12, "deslocamento de 'j'")
        return j_type(off, 0, OP_JAL)                     # jal x0, off

    if mnem == "ret":
        expect_ops(mnem, ops, 0)
        return i_type(0, 1, 0, OP_JALR)                   # jalr x0, ra, 0

    if mnem in ("beqz", "bnez"):
        expect_ops(mnem, ops, 2)
        rs = reg(ops[0])
        off = branch_offset(ops[1], labels, addr)
        check_range(off, 8, "deslocamento de '%s'" % mnem)
        op = OP_BEQ if mnem == "beqz" else OP_BNE
        return b_type(off, 0, rs, op)                     # rs1 = rs, rs2 = x0

    # ------------------------------- R -------------------------------
    if mnem in R_FUNCT:
        expect_ops(mnem, ops, 3)
        rd, rs1, rs2 = reg(ops[0]), reg(ops[1]), reg(ops[2])
        return r_type(R_FUNCT[mnem], rs2, rs1, rd)

    # ------------------------------- I -------------------------------
    if mnem in I_OPCODE:
        expect_ops(mnem, ops, 3)
        rd, rs1 = reg(ops[0]), reg(ops[1])
        imm = number(ops[2])
        check_range(imm, 8, "imediato de '%s'" % mnem)
        return i_type(imm, rs1, rd, I_OPCODE[mnem])

    if mnem == "jalr":
        expect_ops(mnem, ops, 3)
        rd, rs1 = reg(ops[0]), reg(ops[1])
        imm = number(ops[2])
        check_range(imm, 8, "imediato de 'jalr'")
        return i_type(imm, rs1, rd, OP_JALR)

    if mnem == "ebreak":
        expect_ops(mnem, ops, 0)
        return i_type(0, 0, 0, OP_EBREAK)

    # ------------------------------- B -------------------------------
    if mnem in B_OPCODE:
        expect_ops(mnem, ops, 3)
        rs1, rs2 = reg(ops[0]), reg(ops[1])
        off = branch_offset(ops[2], labels, addr)
        check_range(off, 8, "deslocamento de '%s'" % mnem)
        return b_type(off, rs2, rs1, B_OPCODE[mnem])

    # ------------------------------- J -------------------------------
    if mnem in J_OPCODE:
        expect_ops(mnem, ops, 2)
        rd = reg(ops[0])
        off = branch_offset(ops[1], labels, addr)
        check_range(off, 12, "deslocamento de '%s'" % mnem)
        return j_type(off, rd, J_OPCODE[mnem])

    raise AsmError("instrucao desconhecida: '%s'" % mnem)


# ---------------------------------------------------------------------------
# Montagem
# ---------------------------------------------------------------------------
def assemble(source, listing=None):
    entries = parse_source(source)
    labels = first_pass(entries)

    words = []
    for e in entries:
        if e["mnem"] is None:
            continue
        try:
            w = encode_instruction(e, labels)
        except AsmError as ex:
            raise AsmError("linha %d: %s" % (e["line"], ex))
        words.append(w)
        if listing is not None:
            listing.append((e["addr"], w, e["mnem"], e["ops"]))
    return words


def write_logisim_hex(words, path):
    """
    Gera o arquivo que o Logisim entende ("v3.0 hex words plain").
    Cada palavra de 20 bits ocupa 5 digitos hexadecimais.
    """
    with open(path, "w", encoding="ascii", newline="\n") as f:
        f.write("v3.0 hex words plain\n")
        for w in words:
            f.write("%05x\n" % w)


def write_binary(words, path):
    with open(path, "w", encoding="ascii", newline="\n") as f:
        for w in words:
            f.write(format(w, "0%db" % WORD_BITS) + "\n")


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------
def main(argv=None):
    ap = argparse.ArgumentParser(description="Montador para a ISA de 20 bits.")
    ap.add_argument("arquivo", help="programa .asm de entrada")
    ap.add_argument("-o", "--saida", help="arquivo .hex de saida (padrao: mesmo nome do .asm)")
    ap.add_argument("--bin", action="store_true", help="tambem gera um .bin com as palavras em binario")
    ap.add_argument("-v", "--verbose", action="store_true", help="imprime o listing")
    args = ap.parse_args(argv)

    try:
        with open(args.arquivo, "r", encoding="utf-8") as f:
            source = f.read()
        listing = [] if args.verbose else None
        words = assemble(source, listing)
    except AsmError as e:
        print("erro: %s" % e, file=sys.stderr)
        return 1
    except OSError as e:
        print("erro: %s" % e, file=sys.stderr)
        return 1

    out = args.saida or (os.path.splitext(args.arquivo)[0] + ".hex")
    write_logisim_hex(words, out)

    if args.bin:
        binpath = os.path.splitext(out)[0] + ".bin"
        write_binary(words, binpath)
        print("gerado: %s" % binpath)

    if args.verbose and listing:
        print("%-5s %-6s %-20s %s" % ("addr", "hex", "binario", "fonte"))
        for addr, w, mnem, ops in listing:
            print("%-5d %05X  %s  %s %s"
                  % (addr, w, format(w, "020b"), mnem, ", ".join(ops)))

    print("gerado: %s  (%d palavras de %d bits)" % (out, len(words), WORD_BITS))
    return 0


if __name__ == "__main__":
    sys.exit(main())
