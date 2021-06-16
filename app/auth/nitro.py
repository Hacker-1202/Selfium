import requests
import datetime
import discord
import re
from app.auth import token
from app.helpers import getUser
from app.filesystem import cfg, gift

''' This file is part of discord-sniper by lnxcz, licensed under the MIT license:
MIT License

Copyright (c) 2020 LnX

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''


async def giftProcess(message):
    data = gift.load()
    senderData = await getUser.byMember(message.author)
    start = datetime.datetime.now()
    if "discord.gift/" in message.content:
        code = re.findall("discord[.]gift/(\w+)", message.content)
    if "discordapp.com/gifts/" in message.content:
        code = re.findall("discordapp[.]com/gifts/(\w+)", message.content)
    if 'discord.com/gifts/' in message.content:
        code = re.findall("discord[.]com/gifts/(\w+)", message.content)
    if not code in data:
    #if code:
        for code in code:
            if len(code) == 16 or len(code) == 24:
                if not token(cfg['sniperToken']['token']):
                    headers = {'Authorization': cfg['token']}
                else:
                    headers = {'Authorization': cfg['sniperToken']['token']}
                r = requests.post(
                    f'https://discordapp.com/api/v6/entitlements/gift-codes/{code}/redeem',
                    headers=headers,
                ).text
                elapsed = datetime.datetime.now() - start
                elapsed = f'{elapsed.seconds}.{elapsed.microseconds}'
                if 'This gift has been redeemed already.' in r:
                    status = 'Redeemed'
                elif 'subscription_plan' in r:
                    status = 'Success'
                elif 'Unknown Gift Code' in r:
                    status = 'Invalid'

                if message.guild:
                    guild = message.guild.name
                else:
                    guild = 'DM'

                if senderData.name:
                    author = senderData.name
                    authorDiscriminator = senderData.discriminator
                else:
                    author = 'Webhook'
                    authorDiscriminator = '0000'
                
                if hasattr(message.channel, 'name'):
                    channel = message.channel.name
                else:
                    channel = "DM - " + author

                struct = {}
                struct[code] = code
                struct[code]["author"] = author + '#' +authorDiscriminator
                struct[code]["guild"] = guild
                struct[code]["channel"] = channel
                struct[code]["timestamp"] = start.strftime("%H:%M:%S")
                struct[code]["response"] = r
                gift.save(struct)

