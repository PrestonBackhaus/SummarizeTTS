import sys
import os

# Assuming the 'summarizer' module is at the root of the project
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'subdirectory')))