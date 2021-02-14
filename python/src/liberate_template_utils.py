from typing import Sequence
from src.file_io import IFile


def update_liberate_template_cell_names(
        file: IFile,
        cell_names: Sequence[str],
        backup_file: IFile = None
) -> None:
    if backup_file is not None:
        backup_file.write(file.read())

    cell_name_block_lines = ['set cells {'] + [f'    {cell_name}' for cell_name in cell_names]
    lines = file.read().splitlines()

    looking_for_end_idx = False
    set_name_lines_start_idx = 0
    set_name_lines_end_idx = 0
    for idx, line in enumerate(lines):
        if line.strip().upper().replace(' ', '').startswith('SETCELLS{'):
            set_name_lines_start_idx = idx
            looking_for_end_idx = True
            continue

        if looking_for_end_idx and line.strip() == '}':
            set_name_lines_end_idx = idx
            looking_for_end_idx = False

    new_lines = lines[:set_name_lines_start_idx] \
                + cell_name_block_lines \
                + lines[set_name_lines_end_idx:]
    file.write("\n".join(new_lines))
