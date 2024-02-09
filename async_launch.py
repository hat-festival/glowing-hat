from lib.custodian import Custodian
from lib.hat import Hat
from lib.modes.music_bounce import MusicBounce
from lib.conf import conf

hat = Hat()
custodian = Custodian(conf=conf, namespace="hat")
custodian.populate(flush=True)

mb = MusicBounce(hat, custodian)
mb.run()
