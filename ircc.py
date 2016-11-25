import irc.bot

# Based on irccat2.py and testbot.py from https://github.com/jaraco/irc

class IRC(irc.bot.SingleServerIRCBot):
    settings = None
    connection = None
    
    def __init__(self, settings):
        irc.bot.SingleServerIRCBot.__init__(self, [(settings["irc"]["server"], int(settings["irc"]["port"]))], settings["irc"]["nickname"], settings["irc"]["nickname"])
        self.settings = settings["irc"]
    
    def on_nicknameinuse(self, connection, event):
        connection.nick(connection.get_nickname() + "_")
    
    def on_welcome(self, connection, event):
        self.connection = connection
        channel = self.settings["channel"]
        
        connection.join(channel)
    
    def on_privmsg(self, connection, event):
        print("Private from %s: %s" % (event.source.nick, event.arguments[0].strip()))
        if event.source.nick == "david171971":
            connection.privmsg(self.settings["channel"], event.arguments[0].strip())
    
    def on_pubmsg(self, connection, event):
        print("Public from %s: %s" % (event.source.nick, event.arguments[0].strip()))
    
    def run(self):
        try:
            self.start()
        except KeyboardInterrupt:
            self.connection.quit("Using DiscordIRCBot, see ya!")