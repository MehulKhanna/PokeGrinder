import shutil, os
def copy_and_modify_files(new_name):

    # Define file paths based on the provided name
    main_file = f'.\\assets\\source\\main.py'
    config_file = f'.\\assets\\source\\config.json'
    start_bat_file = f'.\\assets\\source\\start.bat'

    # Define new file names with the updated counter
    new_main_file = f'main_{new_name}.py'
    new_config_file = f'config_{new_name}.json'
    new_start_bat_file = f'!start_{new_name}.bat'
    
    for directory in ['instances', 'configs']:
        if not os.path.exists(directory):
            os.makedirs(directory)

    # Copy the main.py file
    shutil.copy(main_file, f"instances/{new_main_file}")
    modify_first_line(f"instances/{new_main_file}", f'configname = "{new_config_file}"')

    # Copy the config.py file with the new name
    shutil.copy(config_file, f'configs/{new_config_file}')

    # Copy and modify the start.bat file
    shutil.copy(start_bat_file, new_start_bat_file)
    modify_first_line(new_start_bat_file, f'python instances/{new_main_file}')

def modify_first_line(file_path, new_line):
    # Read the content of the file
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Modify the first line
    lines[0] = new_line + '\n'

    # Write the modified content back to the file
    with open(file_path, 'w') as file:
        file.writelines(lines)

if __name__ == '__main__':
    copy_and_modify_files(input("Name new instances: "))
