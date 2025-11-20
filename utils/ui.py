import sys

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def log(msg, level="INFO"):
    if level == "INFO":
        print(f"{Colors.BLUE}[*]{Colors.ENDC} {msg}")
    elif level == "SUCCESS":
        print(f"{Colors.GREEN}[+]{Colors.ENDC} {msg}")
    elif level == "ERROR":
        print(f"{Colors.FAIL}[!] {msg}{Colors.ENDC}")
    elif level == "STEP":
        print(f"{Colors.CYAN}[>]{Colors.ENDC} {msg}")
    elif level == "WARN":
        print(f"{Colors.WARNING}[?]{Colors.ENDC} {msg}")

def print_banner():
    banner = f"""{Colors.CYAN}
    ██████╗ ██╗     ██╗     ███╗   ███╗ █████╗ ███████╗████████╗███████╗██████╗ 
    ██╔══██╗██║     ██║     ████╗ ████║██╔══██╗██╔════╝╚══██╔══╝██╔════╝██╔══██╗
    ██║  ██║██║     ██║     ██╔████╔██║███████║███████╗   ██║   █████╗  ██████╔╝
    ██║  ██║██║     ██║     ██║╚██╔╝██║██╔══██║╚════██║   ██║   ██╔══╝  ██╔══██╗
    ██████╔╝███████╗███████╗██║ ╚═╝ ██║██║  ██║███████║   ██║   ███████╗██║  ██║
    ╚═════╝ ╚══════╝╚══════╝╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝   ╚═╝   ╚══════╝╚═╝  ╚═╝
    {Colors.ENDC}{Colors.BOLD}v1.0.0 - Modular DLL Analysis & Proxy Toolkit{Colors.ENDC}
    """
    print(banner)