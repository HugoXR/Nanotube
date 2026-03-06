#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK
# -*- coding: utf-8 -*-

"""
Nome do Arquivo: Nanotube.py
Autor: Hugo X. Rodrigues
Data: 06/03/2026
Descrição: A partir de um arquivo .cif, .xyz ou POSCAR gera um nanotubo com enrolamento armchair ou zigzag, com quiralidades n e m.
Licença: LCCMat e HXR-Programs
"""

import os
import readline
import glob
import numpy as np
from ase.io import read
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

print("--- Gerador de Nanotubo Interativo (Pressione TAB para completar nomes) ---")

# 1. Entrada do arquivo com suporte a TAB
file_structure = input("Digite o nome do arquivo (.cif, .xyz, POSCAR): ")

try:
    atoms = read(file_structure)
except Exception as e:
    print(f"Erro ao carregar arquivo: {e}")
    exit()

structure_name = file_structure.split(".")[0]

winding = input("Digite o tipo de enrolamento (a - armchair, z - zigzag): ")

if winding == "a":
    n = int(input("Digite o perímetro da estrutura (n): "))
    m = int(input("Digite o comprimento da estrutura (m): "))
elif winding == "z":
    m = int(input("Digite o perímetro da estrutura (m): "))
    n = int(input("Digite o comprimento da estrutura (n): "))
else:
    print("Não foi selecionado o enrolamento correto!!! (digite a ou z)")
    exit(1)

# 2. Criar a folha (Supercélula)
P = np.array([[n, 0, 0], [0, m, 0], [0, 0, 1]])
sheet = make_supercell(atoms, P)

# 3. Matemática do Enrolamento
pos = sheet.get_positions()
cell = sheet.get_cell()

# O comprimento da base (eixo x) será o nosso perímetro (L)
if winding == "a":
    L = cell[0,0]
    R = L / (2 * np.pi)  # Raio do nanotubo
    
    # Transformando coordenadas cartesianas (x, y, z) em cilíndricas (x', y', z')
    # O eixo 'x' da folha vira o ângulo do círculo
    theta = pos[:, 0] / R
    new_x = R * np.cos(theta)
    new_y = R * np.sin(theta)
    new_z = pos[:, 1]  # O eixo 'y' da folha vira o eixo axial do tubo
elif winding == "z":
    L = cell[1,1]
    R = L / (2*np.pi)
    
    # Transformando coordenadas cartesianas (x, y, z) em cilíndricas (x', y', z')
    # O eixo 'y' da folha vira o ângulo do círculo
    theta = pos[:, 1] / R
    new_x = R * np.cos(theta)
    new_y = R * np.sin(theta)
    new_z = pos[:, 0]  # O eixo 'x' da folha vira o eixo axial do tubo
else:
    exit(1)


# 4. Atualizar posições e adicionar vácuo
sheet.set_positions(np.column_stack((new_x, new_y, new_z)))

# Centraliza o tubo e adiciona 10 Angstroms de vácuo para evitar interação periódica
sheet.center(vacuum=10.0)

# 5. Salvar o resultado
nome_poscar = f"POSCAR_{structure_name}_{n}_{m}_{winding}"
nome_xyz = f"nt_{structure_name}_{n}_{m}_{winding}.xyz"

sheet.write(nome_xyz)
sheet.write(nome_poscar)

print(f"Arquivos POSCAR: {nome_poscar} e xyz; {nome_xyz} gerados com sucesso!")
print(f"Nanotubo gerado com sucesso! Raio aproximado: {R:.2f} Å")
