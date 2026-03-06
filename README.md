# Nanotube.py

Interactive nanotube generator from structural files in `.cif`, `.xyz`, or `POSCAR` format.

This script reads an input structure, builds a supercell, and wraps the sheet into a nanotube with **armchair** or **zigzag** winding. The program then exports the generated nanotube in both **XYZ** and **POSCAR** formats.

## Features

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

## Requirements

- Python 3
- [NumPy](https://numpy.org/)
- [ASE - Atomic Simulation Environment](https://wiki.fysik.dtu.dk/ase/)

## Installation

Create a virtual environment if desired, then install the required packages:

```bash
pip install numpy ase
```

> Note: the script uses `readline` for filename autocompletion with the `TAB` key. This usually works out of the box on Linux and macOS terminals.

## How it works

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

## Usage

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

## Input conventions

The current implementation assumes that the precursor structure is already oriented consistently with the intended wrapping direction:

- For **armchair** mode, the **x-axis** of the sheet is wrapped into the circumference and the **y-axis** becomes the tube axis.
- For **zigzag** mode, the **y-axis** of the sheet is wrapped into the circumference and the **x-axis** becomes the tube axis.

## Output files

For an input called `graphene.cif`, `n = 8`, `m = 20`, and armchair winding, the generated files will be:

```text
POSCAR_graphene_8_20_a
nt_graphene_8_20_a.xyz
```

## Notes and limitations

- This script supports **armchair** and **zigzag** wrapping modes in its current form.
- The nanotube radius is estimated from the wrapped supercell perimeter.
- No post-generation structural relaxation is performed.
- The quality of the final nanotube depends on the orientation and periodicity of the input sheet.
- The code was designed for interactive terminal use.

## Possible future improvements

- Support for fully general chiral nanotubes `(n, m)`
- Automatic detection/reorientation of the precursor sheet
- Command-line arguments for batch execution
- Optional geometry optimization after wrapping
- More export formats

## Author

**Hugo X. Rodrigues**

## License

**LCCMat and HXR-Programs**
