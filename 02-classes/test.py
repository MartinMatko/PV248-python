import sys
from scorelib import *

if not len(sys.argv) == 2:
    raise Exception("Invalid number of parameters")
else:
    file_name = sys.argv[1]
    prints = load(file_name)
    for print_entity in prints:
        print_entity.format()
