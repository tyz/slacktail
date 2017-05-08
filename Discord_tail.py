#! python3

"""
Tail implementation from https://github.com/tyz/slacktail
Discord.py library from https://github.com/Rapptz/discord.py
Basis for Discord communication from https://github.com/Rapptz/discord.py/blob/async/examples/background_task.py
"""

import argparse
import os
import discord
import asyncio
import re
import sys

client = discord.Client()

def prepend_dont_starve_emoticon(line):
    # Join
    if re.match(r'\[(\d+):(\d+):(\d+)\]: \[Join Announcement\] (.+)$', line):
        return "<:balloons:290486234956955648> <:balloons:290486234956955648> " + line
    
    # Leave
    elif re.match(r'\[(\d+):(\d+):(\d+)\]: \[Leave Announcement\] (.+)$', line):
        return ":warning: :warning: " + line
    
    # Say
    elif re.match(r'\[(\d+):(\d+):(\d+)\]: \[Say\] \(.+\) (.+): (.+)$', line):
        return ":speech_balloon: :speech_balloon: " + line
    
    # Whisper
    elif re.match(r'\[(\d+):(\d+):(\d+)\]: \[Whisper\] \(.+\) (.+): (.+)$', line):
        return ":envelope: :envelope: " + line
    
    # Death
    elif re.match(r'\[(\d+):(\d+):(\d+)\]: \[Death Announcement\] (.+) was killed by (.+)\.', line):
        return "<:dead:290486234957217792> <:dead:290486234957217792> " + line
    
    # Resurrect
    elif re.match(r'\[(\d+):(\d+):(\d+)\]: \[Resurrect Announcement\] (.+) was resurrected by (.+)\.$', line):
        return ":heart: :heart: " + line
    
    # Skin
    elif re.match(r'\[(\d+):(\d+):(\d+)\]: \[Skin Announcement\] (.+)$', line):
        return "<:gift:290486235137572864> <:gift:290486235137572864> " + line
    
    # Roll
    elif re.match(r'\[(\d+):(\d+):(\d+)\]: \[Roll Announcement\] \(.+\) (.+) (.+)$', line):
        return ":game_die: :game_die: " + line
    
    # Vote
    elif re.match(r'\[(\d+):(\d+):(\d+)\]: \[Vote Announcement\] (.+)$', line):
        return "" + line
    
    # Kick
    elif re.match(r'\[(\d+):(\d+):(\d+)\]: \[Kick Announcement\] (.+)$', line):
        return "" + line
    
    # Announcement
    elif re.match(r'\[(\d+):(\d+):(\d+)\]: \[Announcement\] (.+)$', line):
        return "" + line
    
    # No match found
    else:
        return "" + line

async def my_background_task(channelID, filename, time):
    await client.wait_until_ready()
    channel = discord.Object(id=channelID)
    
    try:
        file = open(filename, 'r', encoding='utf-8')
    except IOError:
        sys.exit("FATAL ERROR: There was a problem opening \"{}\".".format(filename))
    
    file.seek(0, os.SEEK_END)
    print("------")
    print("Tailing {} every {} seconds.".format(filename, time))
    
    while not client.is_closed:
        try:
            lines = file.readlines()
        except UnicodeDecodeError:
            print("Encountered unknown character in server log, skipping lines.")
        else:
            for line in lines:    # Not EOF
                line = prepend_dont_starve_emoticon(line)    # This line can be removed if you want `line` as is
                try:
                    await client.send_message(channel, line)
                except discord.DiscordException as e:    # For full list of exceptions https://github.com/Rapptz/discord.py/blob/async/discord/errors.py
                    print("There was a problem communicating with Discord.")
                    print("TYPE: {}".format(type(e)))
                    print("ARGS: {}".format(e))
        
        file.seek(0, os.SEEK_END)    # Reset EOF flag by seeking to current position
        await asyncio.sleep(time)

@client.event
async def on_ready():
    print("Logged in as")
    print(client.user.name)
    print(client.user.id)
    print("------")

parser = argparse.ArgumentParser(description="Tail a file and output as a Discord bot to a Discord channel.")

parser.add_argument('--token',
                    '-t',
                    help="The bot token that will connect to Discord.")
parser.add_argument('--channel',
                    '-c',
                    type=int,
                    help="Discord channel to output to.")
parser.add_argument('--file',
                    '-f',
                    help="The file to tail.",
                    required=True)
parser.add_argument('--wait',
                    '-W',
                    metavar='SEC',
                    type=int,
                    help="Try to read new lines every SEC seconds. (default: 60)",
                    default=30)

args = parser.parse_args()

client.loop.create_task(my_background_task(args.channel, args.file, args.wait))
try:
    client.run(args.token)
except discord.LoginFailure:
    sys.exit("FATAL ERROR: Couldn't login with token \"{}\".".format(args.token))