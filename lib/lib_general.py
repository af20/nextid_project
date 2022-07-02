import os, sys, inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from datetime import date

def libg_get_python_date_from_date(my_date):
    spl = my_date.split('-')
    Y = int(spl[0])
    M = int(spl[1])
    D = int(spl[2])
    py_date = date(Y,M,D)
    return py_date
