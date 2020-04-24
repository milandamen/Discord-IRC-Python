import logging
import discord
import asyncio
from asyncio import coroutines
import concurrent.futures
from asyncio import futures

logging.basicConfig(level=logging.INFO)

thread_lock = None

settings = None
client = discord.Client()
server = None
channel = None
irc = None

class Discord:
    def __init__(self, sett):
        global settings
        global thread_lock
        
        settings = sett["discord"]
        
        if not settings["token"]:
            with thread_lock:
                print("[Discord] No token given. Get a token at https://discordapp.com/developers/applications/me")
            exit()
    
    def set_irc(self, ircc):
        global irc
        irc = ircc
    
    def set_thread_lock(self, lock):
        global thread_lock
        thread_lock = lock
    
    def send_my_message(self, message):
        global client
        asyncio.run_coroutine_threadsafe(send_my_message_async(message), client.loop)
    
    def run(self):
        global settings
        global client
        
        client.run(settings["token"])
    
    def close(self):
        global client
        global irc
        irc.set_running(False)
        asyncio.run_coroutine_threadsafe(client.close(), client.loop)

async def send_my_message_async(message):
    await channel.send(message.strip())
    
@client.event
async def on_message(message):
    global settings
    global client
    global channel
    global thread_lock
    global irc
    
    # Don't reply to itself
    if message.author == client.user:
        return
    
    if message.channel != channel:
        return

    if message.author.name == settings["botowner"]:
        if message.content.strip() == "!quit":
            await client.close()
            return

    with thread_lock:
        print("[Discord] %s: %s" % (message.author.name, message.content.strip()))

    content = message.content
    if len(message.attachments) > 0:
        content += ' ' + message.attachments[0].url

    irc.send_my_message("%s: %s" % (message.author.name, content))

@client.event
async def on_ready():
    global server
    global channel
    global thread_lock
    
    with thread_lock:
        print("[Discord] Logged in as:")
        print("[Discord] " + client.user.name)
        print("[Discord] " + str(client.user.id))
        
        if len(client.guilds) == 0:
            print("[Discord] Bot is not yet in any server.")
            await client.close()
            return
        
        if settings["server"] == "":
            print("[Discord] You have not configured a server to use in settings.json")
            print("[Discord] Please put one of the server IDs listed below in settings.json")
            
            for server in client.guilds:
                print("[Discord] %s: %s" % (server.name, server.id))
            
            await client.close()
            return
        
        findServer = [x for x in client.guilds if str(x.id) == settings["server"]]
        if not len(findServer):
            print("[Discord] No server could be found with the specified id: " + settings["server"])
            print("[Discord] Available servers:")
            
            for server in client.guilds:
                print("[Discord] %s: %s" % (server.name, server.id))
                
            await client.close()
            return
        
        server = findServer[0]
        
        if settings["channel"] == "":
            print("[Discord] You have not configured a channel to use in settings.json")
            print("[Discord] Please put one of the channel IDs listed below in settings.json")
            
            for channel in server.channels:
                if channel.type == discord.ChannelType.text:
                    print("[Discord] %s: %s" % (channel.name, channel.id))
            
            await client.close()
            return
        
        findChannel = [x for x in server.channels if str(x.id) == settings["channel"] and x.type == discord.ChannelType.text]
        if not len(findChannel):
            print("[Discord] No channel could be found with the specified id: " + settings["server"])
            print("[Discord] Note that you can only use text channels.")
            print("[Discord] Available channels:")
            
            for channel in server.channels:
                if channel.type == discord.ChannelType.text:
                    print("[Discord] %s: %s" % (channel.name, channel.id))
            
            await client.close()
            return
        
        channel = findChannel[0]
