import shutil,glob

def extract_positions_from_outcar(outcar_file):
    positions = []
    with open(outcar_file, 'r') as f:
        lines = f.readlines()
        num_ion_steps = 0
        for idx, line in enumerate(lines):
            if 'NIONS =' in line:
                num_atoms = int(line.split()[-1])  # extract number of atoms
            if 'POSITION' in line:
                num_ion_steps += 1
                atom_positions = []
                for line in lines[idx + 2:idx + 2 + num_atoms]:
                    line = line.strip()
                    if '--------' in line:
                        break
                    atom_positions.append(line.split()[:3])
                positions.append(atom_positions)
    return positions, num_ion_steps

def write_xdatcar(positions, num_ion_steps, poscar_file, xdatcar_file):
    with open(poscar_file, 'r') as f:
        poscar_lines = f.readlines()
    with open(xdatcar_file, 'w') as f:
        for i in range(num_ion_steps):
            f.write(''.join(poscar_lines[:7]))
            f.write("Cartesian Configuration =         {}\n".format(i+1))
            for atom_pos in positions[i]:
                f.write(' '.join(atom_pos) + '\n')
                
                
# Example usage:
outcar_file = glob.glob('../14/init.poscar.*/02.md/sys*/scale-1.000/000000/OUTCAR')[0]
poscar_file = glob.glob('../14/init.poscar.*/02.md/sys*/scale-1.000/000000/POSCAR')[0]
xdatcar_file = '14.XDATCAR'

source_file = outcar_file
destination_file = "OUTCAR"
try:
    shutil.copy(source_file, destination_file)
    print(f"成功将 {source_file} 复制并重命名为 {destination_file}")
except FileNotFoundError:
    print(f"找不到文件 {source_file}")
except FileExistsError:
    print(f"文件 {destination_file} 已存在")

source_file = poscar_file
destination_file = "POSCAR"
try:
    shutil.copy(source_file, destination_file)
    print(f"成功将 {source_file} 复制并重命名为 {destination_file}")
except FileNotFoundError:
    print(f"找不到文件 {source_file}")
except FileExistsError:
    print(f"文件 {destination_file} 已存在")

positions, num_ion_steps = extract_positions_from_outcar("OUTCAR")
write_xdatcar(positions, num_ion_steps, "POSCAR", "XDATCAR")
