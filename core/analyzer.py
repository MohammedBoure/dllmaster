import os
import ctypes
import sys
from ..utils.ui import log

try:
    import pefile
except ImportError:
    log("Library 'pefile' is missing. Install with: pip install pefile", "ERROR")
    sys.exit(1)

try:
    dbghelp = ctypes.WinDLL('dbghelp.dll')
    UnDecorateSymbolName = dbghelp.UnDecorateSymbolName
    UnDecorateSymbolName.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_long, ctypes.c_long]
    UnDecorateSymbolName.restype = ctypes.c_long
except Exception:
    dbghelp = None

def demangle_name(name):
    """Decodes C++ Mangled names."""
    if not dbghelp: return name
    buffer_size = 256
    output_buffer = ctypes.create_string_buffer(buffer_size)
    if UnDecorateSymbolName(name.encode('utf-8'), output_buffer, buffer_size, 0x0000) > 0:
        return output_buffer.value.decode('utf-8')
    return None

def get_exports(dll_path, silent=False):
    """Extracts exported functions from a DLL."""
    if not os.path.exists(dll_path):
        if not silent: log(f"File not found: {dll_path}", "ERROR")
        return []

    pe = None
    try:
        # FIXED: Removed 'fast_load=True' to ensure Exports are parsed
        pe = pefile.PE(dll_path)
        
        if not hasattr(pe, 'DIRECTORY_ENTRY_EXPORT'):
            if not silent: log("No exported functions found.", "WARN")
            return []
        
        exports = []
        for exp in pe.DIRECTORY_ENTRY_EXPORT.symbols:
            if exp.name:
                raw_name = exp.name.decode('utf-8')
                signature = demangle_name(raw_name)
                exports.append({
                    "raw_name": raw_name,
                    "signature": signature if signature and signature != raw_name else "C Export / Unknown",
                    "ordinal": exp.ordinal
                })
        return exports

    except Exception as e:
        if not silent: log(f"Error parsing PE: {e}", "ERROR")
        return []
        
    finally:
        # Keep this to fix the [WinError 32] file locking issue
        if pe:
            pe.close()