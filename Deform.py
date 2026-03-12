#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK
# -*- coding: utf-8 -*-

"""
Nome do Arquivo: Deform.py
Autor: Hugo X. Rodrigues
Data: 12/03/2026
Descrição: A partir de um arquivo .cif, .xyz ou POSCAR aplica varios strains na estrutura e cria novos arquivos, POSCAR, igual ao range e ao passo de strain indicado.
Licença: LCCMat e HXR-Programs
"""


import numpy as np
import readline
import glob
import os
import re
from ase.io import read
from ase.io.vasp import write_vasp
from ase.build import make_supercell
import warnings

warnings.filterwarnings("ignore", category=UserWarning, module='ase.io.cif')
 
# --- Configuração do Autocomplete ---
def completer(text, state):
    # Procura arquivos que começam com o texto digitado
    options = [f for f in glob.glob(text + '*') if os.path.isfile(f)]
    return options[state] if state < len(options) else None
 
# Configura o readline para usar a função de completar e a tecla Tab
readline.set_completer_delims(' \t\n;')
readline.parse_and_bind("tab: complete")
readline.set_completer(completer)

print("--- Gerador de Strain ---")

strain_dir = input("Digite a direção da deformação (x, y, z, xy, xz ou yz): ")
types_strain = ["x", "y", "z", "xy", "xz", "yz"]

if strain_dir not in types_strain:
    print("Deformação não está dentre as válidas (x, y, z, xy, xz ou yz)!!!")
    exit(1)

file_structure = input("Digite o nome do arquivo (.cif, .xyz, POSCAR): ")

try:
    atoms = read(file_structure)
    # Salvando as coordenadas fracionárias originais
    original_scaled_pos = atoms.get_scaled_positions()
    original_cell = atoms.get_cell()
except Exception as e:
    print(f"Erro ao carregar arquivo {file_structure}: {e}")
    exit()

strain_percent = float(input("Porcentagem de deformação por passo (ex.: 1, 2, 3, 10, 20, 30, 40): "))
strain_val = strain_percent/100
strain_range = int(input("Quantidade total de deformações (passos): "))

def apply_strain(cell, direct, magnitude):
    new_cell = cell.copy()
    
    if direct == "x":
        new_cell[0, 0] *= (1 + magnitude)
    elif direct == "y":
        new_cell[1, 1] *= (1 + magnitude)
    elif direct == "z":
        new_cell[2, 2] *= (1 + magnitude)
    elif direct == "xy":
        new_cell[1,0] += magnitude*cell[0,0]
    elif direct == "xz":
        new_cell[2,0] += magnitude*cell[0,0]
    elif direct == "yz":
        new_cell[2,1] += magnitude*cell[1,1]

    return new_cell

for step in range(1, strain_range+1):
    current_strain = strain_val * step
    
    new_cell_vectors = apply_strain(original_cell, strain_dir, current_strain)
    
    atoms.set_cell(new_cell_vectors, scale_atoms=False)

    atoms.set_scaled_positions(original_scaled_pos)

    percent_label = round(current_strain * 100, 2)
    name_poscar = f"POSCAR_{percent_label}_{strain_dir}_dir"
    
    write_vasp(name_poscar, atoms, direct=True, sort=False)

    print(f"--- Strain: {percent_label}% | Gerado: {name_poscar} ---\n")

