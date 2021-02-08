import os

from os import path


def cell_input(file_path, file_name, cell_names):
    replaced = False

    old_path = f"{file_path}/bk_{file_name}"
    new_path = f"{file_path}/{file_name}"

    if path.exists(new_path):
        # rename the original file to create a backup
        os.rename(new_path, old_path)

        with open( old_path, 'rt' ) as fin, open( new_path, 'wt' ) as fout:
            for line in fin.readlines():
                if not replaced:
                    if line.startswith( 'set cells' ):
                        replaced = True
                        fout.write( line )
                    else:
                        fout.write( line )
                elif line.startswith( '}' ):
                    for cell in cell_names:
                        fout.write(f"    {cell}\n")
                    fout.write( line )
                    replaced = False


def get_file_params():
    cell_names = ['']

    file_path = input( "Enter path to file:")
    file_name = input( "Enter file name:")
    cell_names_str = input( "Enter cell names, separted by comma, no space:" )

    # Use if there can only be uppercase lettered cells
    cell_names_str.upper()

    if cell_names_str is not None:
        cell_names = cell_names_str.split( ',' )

    return file_path, file_name, cell_names
