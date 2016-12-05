# Discord-IRC-Python
Bot that syncs messages between Discord and IRC

## Requirements
A minimum of Python 3.5

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

## Licence

### Running the bot
If you use this bot, you must let the users in the Discord and IRC channels know that their messages are being sent to one-another. The contributors to this repositories are not responsible for anything done by the program.

### Developing
You may change the code from this repository, but you have to credit this repository.  
If you want to help developing this bot, make a fork, make changes in your own repo, then make a Pull Request here.
