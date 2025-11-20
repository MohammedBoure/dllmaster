import argparse
import sys
import os

# Relative imports for the modular structure
from .utils.ui import print_banner, Colors
from .core.analyzer import get_exports
from .core.executor import run_function
from .core.generator import generate_proxy

# Dynamic path for the template file (relative to this script)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_TEMPLATE = os.path.join(BASE_DIR, "template.cpp")

class ColoredHelpFormatter(argparse.ArgumentDefaultsHelpFormatter):
    """Custom formatter to add colors to help messages."""
    def _get_help_string(self, action):
        return Colors.CYAN + super()._get_help_string(action) + Colors.ENDC

def main():
    print_banner()
    
    # 1. Main Parser Configuration
    # We explicitly set 'usage' to show the correct command order visually
    main_usage = f"{Colors.BOLD}python -m dllmaster <command> [options]{Colors.ENDC}"
    
    parser = argparse.ArgumentParser(
        prog="dllmaster",
        usage=main_usage,
        description=f"{Colors.BOLD}DLLMaster: The Ultimate DLL Hacking Tool{Colors.ENDC}",
        formatter_class=ColoredHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest="command", help=f"{Colors.WARNING}Available Commands{Colors.ENDC}")

    # --- Analyze Command ---
    analyze_usage = f"{Colors.BOLD}python -m dllmaster analyze <dll_path>{Colors.ENDC}"
    p_analyze = subparsers.add_parser(
        "analyze", 
        help="Scan DLL for exports & signatures",
        formatter_class=ColoredHelpFormatter,
        usage=analyze_usage
    )
    p_analyze.add_argument("dll_path", help="Target .dll file to analyze")

    # --- Run Command ---
    run_usage = f"{Colors.BOLD}python -m dllmaster run <dll_path> <function> [args...]{Colors.ENDC}"
    p_run = subparsers.add_parser(
        "run", 
        help="Execute a specific DLL function",
        formatter_class=ColoredHelpFormatter,
        usage=run_usage
    )
    p_run.add_argument("dll_path", help="Target .dll file")
    p_run.add_argument("function", help="Function name to call")
    p_run.add_argument("args", nargs="*", help="Function arguments (int or string)")

    # --- Proxy Command ---
    proxy_usage = f"{Colors.BOLD}python -m dllmaster proxy <dll_path> --hook <func> [options]{Colors.ENDC}"
    p_proxy = subparsers.add_parser(
        "proxy", 
        help="Generate Proxy DLL C++ code",
        formatter_class=ColoredHelpFormatter,
        usage=proxy_usage
    )
    p_proxy.add_argument("dll_path", help="Original Target DLL")
    p_proxy.add_argument("--hook", "-f", required=True, help="Function to intercept (The Hook)")
    p_proxy.add_argument("--template", "-t", default=DEFAULT_TEMPLATE, help="Path to template.cpp")
    p_proxy.add_argument("--output", "-o", default="proxy_result", help="Output filename base")
    p_proxy.add_argument("--payload", "-p", default="calc.exe", help="Payload executable to run")
    p_proxy.add_argument("--compile", "-c", action="store_true", help="Compile immediately using MSVC (cl.exe)")

    # If no arguments provided, print help and exit
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()

    # 2. Execution Logic Dispatch
    if args.command == "analyze":
        # Calls the analyzer module
        funcs = get_exports(args.dll_path)
        if funcs:
            print(f"\n{Colors.BOLD}{'ID':<4} | {'Function Name':<35} | {'Signature'}{Colors.ENDC}")
            print(Colors.CYAN + "-" * 85 + Colors.ENDC)
            for i, f in enumerate(funcs):
                dname = (f['raw_name'][:32] + '..') if len(f['raw_name']) > 32 else f['raw_name']
                print(f"{i:<4} | {dname:<35} | {f['signature']}")
            print(Colors.CYAN + "-" * 85 + Colors.ENDC)
            print(f"{Colors.GREEN}Found {len(funcs)} exported functions.{Colors.ENDC}\n")

    elif args.command == "run":
        # Calls the executor module
        run_function(args.dll_path, args.function, args.args)

    elif args.command == "proxy":
        # Calls the generator module
        generate_proxy(
            args.dll_path, args.template, args.output, 
            args.hook, args.payload, args.compile
        )

if __name__ == "__main__":
    main()