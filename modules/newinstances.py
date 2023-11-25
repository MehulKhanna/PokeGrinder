import shutil

def copy_and_modify_files():
    # Define the base file names
    main_file = '.\\assets\\source\\main.py'
    config_file = '.\\assets\\source\\config.json'
    start_bat_file = '.\\assets\\source\\start.bat'
    counter_file_path = '.\\assets\\instancescount'

    # Check if the counter file exists, and create it if not
    try:
        with open(counter_file_path, 'r'):
            # The file exists, do nothing
            pass
    except FileNotFoundError:
        # The file doesn't exist, create it with the initial value '0'
        with open(counter_file_path, 'w') as new_counter_file:
            new_counter_file.write('0')

    # Read the current counter value
    with open(counter_file_path, 'r') as counter_file:
        counter = int(counter_file.read().strip())

    # Increment the counter for the next run
    counter += 1

    # Define new file names with the updated counter
    new_main_file = f'main{counter}.py'
    new_config_file = f'!config{counter}.json'
    new_start_bat_file = f'!start{counter}.bat'

    # Copy the main.py file
    shutil.copy(main_file, new_main_file)

    # Modify the first line of the new main.py copy
    modify_first_line(new_main_file, f'configname = "{new_config_file}"')

    # Copy the config.py file with the new name
    shutil.copy(config_file, new_config_file)

    # Copy and modify the start.bat file
    shutil.copy(start_bat_file, new_start_bat_file)
    modify_first_line(new_start_bat_file, f'python {new_main_file}')

    # Save the updated counter value
    with open(counter_file_path, 'w') as counter_file:
        counter_file.write(str(counter))

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
    copy_and_modify_files()