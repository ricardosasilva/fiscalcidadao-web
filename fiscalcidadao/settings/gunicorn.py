import multiprocessing
import sys
from os.path import dirname

django_settings = 'dev.diogo'
bind = "0.0.0.0:8000"
workers = multiprocessing.cpu_count() * 2 + 1