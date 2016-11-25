import logging
import discord
import asyncio

logging.basicConfig(level=logging.INFO)

settings = None
client = discord.Client()

class Discord:
    def __init__(self, sett):
        global settings
        settings = sett["discord"]
        
        if not settings["token"]:
            print("No token given. Get a token at https://discordapp.com/developers/applications/me")
            exit()
    
    def run(self):
        global settings
        global client
        
        client.run(settings["token"])
    
    def close(self):
        global client
        
        client.close()
    
@client.event
async def on_message(message):
    # Don't reply to itself
    if message.author == client.user:
        return
    
    print(message)

@client.event
async def on_ready():
    print("Logged in as:")
    print(client.user.name)
    print(client.user.id)
    print("-------")
    if len(client.servers) == 0:
        print("Bot is not yet in any server.")
        await client.close()
