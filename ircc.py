import irc.bot

# Based on irccat2.py and testbot.py from https://github.com/jaraco/irc


class IRC(irc.bot.SingleServerIRCBot):
    thread_lock = None
    running = True
    
    settings = None
    connection = None
    discord = None
    
    def __init__(self, settings):
        irc.client.ServerConnection.buffer_class.encoding = "latin-1"
        irc.bot.SingleServerIRCBot.__init__(self, [\
            (settings["irc"]["server"],\
            int(settings["irc"]["port"]))],\
            settings["irc"]["nickname"],\
            settings["irc"]["nickname"])

        self.settings = settings["irc"]
    
    def set_discord(self, discordc):
        self.discord = discordc
    
    def set_thread_lock(self, lock):
        self.thread_lock = lock
    
    def send_my_message(self, message):
        self.connection.privmsg(self.settings["channel"], message.strip())
        
    def close(self):
        self.running = False
        self.connection.quit(self.settings.get("quitmsg", "Using DiscordIRCBot"))
    
    def set_running(self, value):
        self.running = False
    
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
    
    def on_pubmsg(self, connection, event):
        message = event.arguments[0].strip()
        message = "%s: %s" % (event.source.nick, message)
        with self.thread_lock:
            print("[IRC] " + message)
        
        if event.source.nick == self.settings["botowner"]:
            if event.arguments[0].strip() == "!quit":
                self.discord.close()
                return
        
        self.discord.send_my_message(message)
    
    def run(self):
        self.start()
        
        if self.running:
            self.running = False
            ircc = IRC({"irc": self.settings})
            ircc.set_discord(self.discord)
            self.discord.set_irc(ircc)
            ircc.set_thread_lock(self.thread_lock)
            ircc.run()
