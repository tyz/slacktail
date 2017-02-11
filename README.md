# Discord Tail

Discord Tail is made to monitor a file and display any new lines on [Discord](https://discordapp.com/).
This was made with monitoring in-game chat and posting it to a Discord channel in mind.

## Additional Libraries

discord.py - https://github.com/Rapptz/discord.py

## Usage

```
usage: Discord_tail.py [-h] --token TOKEN --channel CHANNEL --file FILE
                       [--wait SEC]

Tail a file and output as a Discord bot to a Discord channel.

optional arguments:
  -h, --help            show this help message and exit
  --token TOKEN, -t TOKEN
                        The bot token that will connect to Discord.
  --channel CHANNEL, -c CHANNEL
                        Discord channel to output to.
  --file FILE, -f FILE  The file to tail.
  --wait SEC, -W SEC    Try to read new lines every SEC seconds. (default: 60)
```