#!python3

import json
import threading

from ircc import *
from discordc import *

# Get the application settings
f = open("settings.json", encoding="utf-8")
settings = json.loads(f.read())
f.close()

thread_lock = threading.Lock()

irc = IRC(settings)
discord = Discord(settings)

irc.set_discord(discord)
discord.set_irc(irc)

irc.set_thread_lock(thread_lock)
discord.set_thread_lock(thread_lock)

t1 = threading.Thread(target=irc.run)
t1.daemon = True                                    # Thread dies when main thread (only non-daemon thread) exits.
t1.start()

discord.run()
irc.close()
