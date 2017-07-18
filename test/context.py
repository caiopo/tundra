import sys
import os.path

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.append(BASE_DIR)

from graph import Graph
from graph.algorithm import *
from graph.util import *
