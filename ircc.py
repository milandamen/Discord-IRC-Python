import sys

import irc.client

# Based on irccat2.py

class IRC(irc.client.SimpleIRCClient):
    settings = None
    connection = None
    
    def __init__(self, settings):
        irc.client.SimpleIRCClient.__init__(self)
        self.settings = settings["irc"]
    
    def on_welcome(self, connection, event):
        self.connection = connection
        channel = self.settings["channel"]
        
        if irc.client.is_channel(channel):
            connection.join(channel)
        else:
            self.main_loop()
    
    def on_join(self, connection, event):
        self.main_loop()
    
    def on_disconnect(self, conenction, event):
        sys.exit(0)
    
    def main_loop(self):
        connection = self.connection
        settings = self.settings
        
        while 1:
            line = sys.stdin.readline().strip()
            if not line:
                break
            
            connection.privmsg(settings["channel"], line)
        connection.quit("Using DircBot, see ya!")
    
    def run(self):
        server = self.settings["server"]
        port = int(self.settings["port"])
        nickname = self.settings["nickname"]
        
        try:
            self.connect(server, port, nickname)
        except irc.client.ServerConnectionError as x:
            print(x)
            sys.exit(1)
        
        self.start()