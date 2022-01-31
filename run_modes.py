from lib.modes import Modes
from lib.redis_manager import RedisManager

redisman = RedisManager("hat")
redisman.populate()
m = Modes()
m.run()
