# Discord-IRC-Python
Bot that syncs messages between Discord and IRC

## Installation
Install the following python libraries using pip:

- irc
- discord.py

Download the code from this repository, then copy `settings.example.json` to `settings.json` and configure it.

Add a new application and bot user to your Discord account, then invite your bot to a server you manage:

https://discordapp.com/oauth2/authorize?client_id=<client_id>&scope=bot&permissions=3072
(change <client_id> to your application's client_id)