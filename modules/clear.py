import os
import platform
# Function to clear the terminal screen
def clear_screen():
    system_platform = platform.system()
    
    if system_platform == "Windows":
        os.system('cls')
    elif system_platform == "Linux" or system_platform == "Darwin":  # "Darwin" corresponds to macOS
        os.system('clear')
    else:
        print("Unsupported operating system")