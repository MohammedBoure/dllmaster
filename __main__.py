# dllmaster/__main__.py
import sys

# للتأكد من أن الاستيراد يعمل سواء تم استدعاؤه كملف أو موديول
try:
    from .cli import main
except ImportError:
    # Fallback setup if run directly improperly
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from dllmaster.cli import main

if __name__ == "__main__":
    main()