from lib.custodian import Custodian
from lib.hat import Hat
from lib.modes.music_bounce import MusicBounce

hat = Hat()
cust = Custodian("test")

mb = MusicBounce(hat, cust)
mb.run()
