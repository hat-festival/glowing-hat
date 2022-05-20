import sys

from lib.custodian import Custodian
from lib.hat import Hat
from lib.modes_list import modes

m = modes[sys.argv[1]](Hat(), Custodian())
m.run()
