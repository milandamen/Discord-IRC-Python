#!python3

import json
from ircc import *
from discordc import *

# Get the application settings
f = open("settings.json", encoding="utf-8")
settings = json.loads(f.read())
f.close()

#irc = IRC(settings)
#irc.run()

discord = Discord(settings)
discord.run()
#discord.close()