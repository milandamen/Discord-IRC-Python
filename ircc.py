import aiohttp
import asyncio
import async_timeout
import irc.bot

# Based on irccat2.py and testbot.py from https://github.com/jaraco/irc


class IRC(irc.bot.SingleServerIRCBot):
    thread_lock = None
    event_loop = None
    
    settings = None
    connection = None
    discord = None
    
    def __init__(self, settings):
        irc.bot.SingleServerIRCBot.__init__(self, [(settings["irc"]["server"], int(settings["irc"]["port"]))], settings["irc"]["nickname"], settings["irc"]["nickname"])
        self.settings = settings["irc"]
    
    def set_discord(self, discordc):
        self.discord = discordc
    
    def set_thread_lock(self, lock):
        self.thread_lock = lock
    
    def send_my_message(self, message):
        self.connection.privmsg(self.settings["channel"], message.strip())
        
    def close(self):
        self.connection.quit("Using DiscordIRCBot")
    
    def on_nicknameinuse(self, connection, event):
        connection.nick(connection.get_nickname() + "_")
    
    def on_welcome(self, connection, event):
        self.connection = connection
        channel = self.settings["channel"]
        
        connection.join(channel)
        
        with self.thread_lock:
            print("[IRC] Connected to server")
    
    def on_join(self, connection, event):
        with self.thread_lock:
            print("[IRC] Connected to channel")
    
    #def on_privmsg(self, connection, event):
        #print("Private from %s: %s" % (event.source.nick, event.arguments[0].strip()))
        #if event.source.nick == "david171971":
            #connection.privmsg(self.settings["channel"], event.arguments[0].strip())
    
    def on_pubmsg(self, connection, event):
        message = event.arguments[0].strip()
        with self.thread_lock:
            print("[IRC] %s: %s" % (event.source.nick, message))
        
        event_loop = asyncio.get_event_loop()
        event_loop.run_until_complete(self.discord.send_my_message("%s: %s" % (event.source.nick, message)))
    
    def run(self):
        #self.event_loop = asyncio.new_event_loop()
        #asyncio.set_event_loop(self.event_loop)
        self.start()
        