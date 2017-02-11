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

client = discord.Client()

async def my_background_task(channelID, filename, time, truncate):
    await client.wait_until_ready()
    channel = discord.Object(id=channelID)
    file = open(filename, 'r')
    file.seek(0, os.SEEK_END)
    print('------')
    print('Tailing {} every {} seconds. Max size {} bytes.'.format(filename, time, truncate))
    
    while not client.is_closed:
        lines = file.readlines()
        file.seek(0, os.SEEK_END)     # Reset EOF flag by seeking to current position
        if lines != []:    # Not EOF
            output = ''.join(lines)
            if len(output) > truncate:
                output = '.....' + output[-truncate:]
            await client.send_message(channel, output)
        await asyncio.sleep(time)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

parser = argparse.ArgumentParser(description='Tail a file and output as a Discord bot to a Discord channel.')

parser.add_argument('--token',
                    '-t',
                    help='The bot token that will connect to Discord.',
                    required=True)
parser.add_argument('--channel',
                    '-c',
                    type=int,
                    help='Discord channel to output to.',
                    required=True)
parser.add_argument('--file',
                    '-f',
                    help='The file to tail.',
                    required=True)
parser.add_argument('--wait',
                    '-W',
                    metavar='SEC',
                    type=int,
                    help='Try to read new lines every SEC seconds. (default: 60)',
                    default=60)
parser.add_argument('--truncate',
                    '-T',
                    metavar='SIZE',
                    type=int,
                    help='Limit the size of every message to SIZE bytes. The oldest lines will be removed first. (default: 4096)',
                    default=4096)

args = parser.parse_args()

client.loop.create_task(my_background_task(args.channel, args.file, args.wait, args.truncate))
client.run(args.token)