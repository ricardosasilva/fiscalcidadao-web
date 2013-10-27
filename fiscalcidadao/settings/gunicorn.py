import multiprocessing
import sys
from os.path import dirname

django_settings = 'dev.diogo'
bind = "0.0.0.0:80"
workers = multiprocessing.cpu_count() * 2 + 1