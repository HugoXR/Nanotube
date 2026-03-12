# Nanotube.py

Interactive nanotube generator from structural files in `.cif`, `.xyz`, or `POSCAR` format.

This repository currently includes two interactive utilities:

- **`nanotube.py`**: builds nanotubes from planar precursor structures
- **`Deform.py`**: applies sequential strain to a structure and exports deformed `POSCAR` files

---

## Features

### `nanotube.py`

- Reads structures from `.cif`, `.xyz`, and `POSCAR`
- Interactive terminal workflow
- `TAB` autocompletion for input filenames
- Supports two winding modes:
  - `a` = armchair
  - `z` = zigzag
- Builds the precursor sheet using a supercell transformation
- Wraps the structure into cylindrical geometry
- Automatically centers the nanotube and adds **10 Å of vacuum**
- Saves output in:
  - `POSCAR_<name>_<n>_<m>_<winding>`
  - `nt_<name>_<n>_<m>_<winding>.xyz`

### `Deform.py`

- Reads structures from `.cif`, `.xyz`, and `POSCAR`
- Interactive terminal workflow
- `TAB` autocompletion for input filenames
- Applies cumulative strain in user-defined steps
- Supports the following deformation modes:
  - `x`, `y`, `z` for axial strain
  - `xy`, `xz`, `yz` for shear-like cell deformation
- Preserves the original fractional atomic coordinates during cell deformation
- Exports one `POSCAR` file for each deformation step

## Requirements

- Python 3
- [NumPy](https://numpy.org/)
- [ASE - Atomic Simulation Environment](https://wiki.fysik.dtu.dk/ase/)

## Installation

Create a virtual environment if desired, then install the required packages:

```bash
pip install numpy ase
```

> Note: the scripts use `readline` for filename autocompletion with the `TAB` key. This usually works out of the box on Linux and macOS terminals.

---

## `nanotube.py`

### How it works

The program follows these steps:

1. Reads a structure from `.cif`, `.xyz`, or `POSCAR`
2. Asks for the winding type:
   - `a` for armchair
   - `z` for zigzag
3. Requests the replication parameters `n` and `m`
4. Builds a supercell of the original structure
5. Converts planar Cartesian coordinates into cylindrical coordinates
6. Centers the final nanotube and adds vacuum
7. Writes the resulting structure to `XYZ` and `POSCAR`

### Usage

Run the script from the terminal:

```bash
python3 nanotube.py
```

The program will ask for:

- Input file name (`.cif`, `.xyz`, or `POSCAR`)
- Winding type (`a` or `z`)
- Geometric parameters `n` and `m`

### Example session

```text
--- Gerador de Nanotubo Interativo (Pressione TAB para completar nomes) ---
Digite o nome do arquivo (.cif, .xyz, POSCAR): graphene.cif
Digite o tipo de enrolamento (a - armchair, z - zigzag): a
Digite o perímetro da estrutura (n): 8
Digite o comprimento da estrutura (m): 20
Arquivos POSCAR: POSCAR_graphene_8_20_a e xyz; nt_graphene_8_20_a.xyz gerados com sucesso!
Nanotubo gerado com sucesso! Raio aproximado: 3.14 Å
```

### Input conventions

The current implementation assumes that the precursor structure is already oriented consistently with the intended wrapping direction:

- For **armchair** mode, the **x-axis** of the sheet is wrapped into the circumference and the **y-axis** becomes the tube axis.
- For **zigzag** mode, the **y-axis** of the sheet is wrapped into the circumference and the **x-axis** becomes the tube axis.

### Output files

For an input called `graphene.cif`, `n = 8`, `m = 20`, and armchair winding, the generated files will be:

```text
POSCAR_graphene_8_20_a
nt_graphene_8_20_a.xyz
```

---

## `Deform.py`

### What it does

`Deform.py` applies a sequence of user-defined strains to a structure read from `.cif`, `.xyz`, or `POSCAR` format. For each step, the script modifies the simulation cell, keeps the original fractional coordinates, and writes a new deformed `POSCAR` file.

### Supported deformation directions

The script accepts the following deformation modes:

- `x`: strain along the `a` lattice direction
- `y`: strain along the `b` lattice direction
- `z`: strain along the `c` lattice direction
- `xy`: shear-like deformation by modifying the `(2,1)` cell component
- `xz`: shear-like deformation by modifying the `(3,1)` cell component
- `yz`: shear-like deformation by modifying the `(3,2)` cell component

### Usage

Run the script from the terminal:

```bash
python3 Deform.py
```

The program will ask for:

- Deformation direction: `x`, `y`, `z`, `xy`, `xz`, or `yz`
- Input structure file (`.cif`, `.xyz`, or `POSCAR`)
- Strain percentage per step
- Total number of deformation steps

### Example session

```text
--- Gerador de Strain ---
Digite a direção da deformação (x, y, z, xy, xz ou yz): x
Digite o nome do arquivo (.cif, .xyz, POSCAR): POSCAR
Porcentagem de deformação por passo (ex.: 1, 2, 3, 10, 20, 30, 40): 1
Quantidade total de deformações (passos): 5
--- Strain: 1.0% | Gerado: POSCAR_1.0_x_dir ---
--- Strain: 2.0% | Gerado: POSCAR_2.0_x_dir ---
--- Strain: 3.0% | Gerado: POSCAR_3.0_x_dir ---
--- Strain: 4.0% | Gerado: POSCAR_4.0_x_dir ---
--- Strain: 5.0% | Gerado: POSCAR_5.0_x_dir ---
```

### Output files

For a strain step of `1%`, total range of `5` steps, and deformation along `x`, the script generates:

```text
POSCAR_1.0_x_dir
POSCAR_2.0_x_dir
POSCAR_3.0_x_dir
POSCAR_4.0_x_dir
POSCAR_5.0_x_dir
```

### Notes

- The applied strain is **cumulative**, meaning each step corresponds to:
  - `step × strain_per_step`
- Atomic positions are restored using the original **scaled (fractional) coordinates** after the cell deformation.
- The current version writes only `POSCAR` files.
- The script is intended for interactive terminal execution.

---

## Notes and limitations

- `nanotube.py` currently supports only **armchair** and **zigzag** wrapping modes.
- `Deform.py` applies cell deformation directly and does not perform structural relaxation.
- The quality of the final structures depends on the consistency of the input geometry and lattice orientation.
- Both programs were designed for interactive terminal use.

## Possible future improvements

- Support for fully general chiral nanotubes `(n, m)`
- Automatic detection/reorientation of the precursor sheet
- Command-line arguments for batch execution
- Optional geometry optimization after wrapping or deformation
- More export formats

## Author

**Hugo X. Rodrigues**

## License

**LCCMat and HXR-Programs**
