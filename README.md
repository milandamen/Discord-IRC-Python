# Discord-IRC-Python
Bot that syncs messages between Discord and IRC

## Installation
Install the following python libraries using pip:

- irc
- discord.py

Download the code from this repository, then copy `settings.example.json` to `settings.json` and configure it.

Add a new application and bot user to your Discord account, then invite your bot to a server you manage:

https://discordapp.com/oauth2/authorize?client_id=CLIENT_ID&scope=bot&permissions=3072  
(change CLIENT_ID to your application's client_id)

## Running
Just launch the bot using `python3 main.py`.
To quit the bot, type `!quit` in the IRC or Discord channel.