import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from civ_game import main

if __name__ == "__main__":
    main.main()