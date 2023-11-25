import ctypes

def set_terminal_title(title):
    ctypes.windll.kernel32.SetConsoleTitleW(title)
