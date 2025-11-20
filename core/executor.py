import os
import ctypes
# Use relative import
from ..utils.ui import log, Colors

def run_function(dll_path, func_name, cli_args=None):
    """Loads DLL and runs a specific function."""
    dll_abs_path = os.path.abspath(dll_path)
    try:
        dll_dir = os.path.dirname(dll_abs_path)
        if hasattr(os, 'add_dll_directory'):
            os.add_dll_directory(dll_dir)
        
        try:
            my_dll = ctypes.CDLL(dll_abs_path)
        except:
            log("CDLL failed, switching to WinDLL...", "WARN")
            my_dll = ctypes.WinDLL(dll_abs_path)
        
        func = getattr(my_dll, func_name)
        
        parsed_args = []
        if cli_args:
            for a in cli_args:
                if a.isdigit():
                    parsed_args.append(ctypes.c_int(int(a)))
                else:
                    parsed_args.append(ctypes.c_char_p(a.encode('utf-8')))
        else:
            log(f"Interactive Mode: Running '{func_name}'", "INFO")
            count = input(f"{Colors.BOLD}How many arguments? (0 for none): {Colors.ENDC}")
            if count.isdigit() and int(count) > 0:
                for i in range(int(count)):
                    val = input(f"Enter arg {i+1} (int/str): ")
                    if val.isdigit():
                        parsed_args.append(ctypes.c_int(int(val)))
                    else:
                        parsed_args.append(ctypes.c_char_p(val.encode('utf-8')))

        print(f"\n{Colors.CYAN}--- Execution Start ---{Colors.ENDC}")
        res = func(*parsed_args)
        print(f"{Colors.CYAN}--- Execution Finished ---{Colors.ENDC}")
        log(f"Return Value: {res}", "SUCCESS")
        
    except AttributeError:
        log(f"Function '{func_name}' not found.", "ERROR")
    except Exception as e:
        log(f"Execution failed: {e}", "ERROR")