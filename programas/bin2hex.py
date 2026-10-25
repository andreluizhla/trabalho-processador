#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
bin2hex.py - Converte um arquivo de texto com palavras binárias (20 bits)
para o formato "v3.0 hex words plain" do Logisim.
"""

import sys
import os

def main():
    if len(sys.argv) < 2:
        print("Uso: python3 bin2hex.py <arquivo.bin> [-o <arquivo.hex>]")
        sys.exit(1)

    bin_path = sys.argv[1]
    
    # Define o nome do arquivo de saída (padrão: mesmo nome, extensão .hex)
    hex_path = os.path.splitext(bin_path)[0] + ".hex"
    if "-o" in sys.argv:
        idx = sys.argv.index("-o")
        if idx + 1 < len(sys.argv):
            hex_path = sys.argv[idx + 1]
        else:
            print("Erro: -o requer um nome de arquivo.")
            sys.exit(1)

    try:
        with open(bin_path, "r") as f_in, open(hex_path, "w") as f_out:
            f_out.write("v3.0 hex words plain\n")
            for line in f_in:
                line = line.strip()
                if not line:
                    continue
                try:
                    val = int(line, 2)
                    # Formata como 5 dígitos hexadecimais (20 bits)
                    f_out.write(f"{val:04x}\n")
                except ValueError:
                    print(f"Erro: linha inválida no binário: '{line}'")
                    sys.exit(1)
        print(f"Arquivo gerado: {hex_path}")
    except FileNotFoundError:
        print(f"Erro: arquivo '{bin_path}' não encontrado.")
        sys.exit(1)

if __name__ == "__main__":
    main()
