import os
import sys
from os import path

script_dir = getattr(sys, '_MEIPASS', path.abspath(os.path.dirname(__file__)))
sys.path.insert(0, os.path.join(script_dir, 'main'))

from gamestate import main

if __name__ == "__main__":
    main()