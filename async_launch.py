from lib.conf import conf
from lib.custodian import Custodian
from lib.hat import Hat
from lib.modes.music_bounce import MusicBounce

hat = Hat()
custodian = Custodian(conf=conf, namespace="hat")
custodian.populate(flush=True)

mb = MusicBounce(hat, custodian)
mb.run()
