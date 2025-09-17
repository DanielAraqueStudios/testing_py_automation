"""
Modern Quote Generator GUI - Launcher Script
"""
import sys
import os

# Add current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

try:
    from quote_gui import main
    main()
except ImportError as e:
    print(f"Error importing PyQt6: {e}")
    print("Please install PyQt6: pip install PyQt6")
except Exception as e:
    print(f"Error running application: {e}")
    input("Press Enter to continue...")