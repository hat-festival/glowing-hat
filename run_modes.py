from lib.modes import Modes
from lib.redis_starter import initialise_redis

initialise_redis()
m = Modes()
m.run()
