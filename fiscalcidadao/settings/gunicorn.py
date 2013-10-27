import multiprocessing
import sys
from os.path import dirname

sys.path.append(dirname(dirname(dirname(__file__))))
bind = "0.0.0.0:8000"
workers = multiprocessing.cpu_count() * 2 + 1