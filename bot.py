import os
import discord

from utils.giphy import get_giphy
from utils.lol import Lol


client = discord.Client()


@client.event
async def on_ready():
    print('I am ready!!')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hi'):
        giphy = get_giphy()
        await message.channel.send(giphy)

    if message.content.startswith('$rito please'):
        lol = Lol('', 'LAN')
        greetings = lol.greetings()

        emb = discord.Embed(title=greetings['greetings'])
        emb.set_image(url=greetings['icon_url'])
        await message.channel.send(embed=emb)
    
    if message.content.startswith('$champion'):
        lol = Lol('', 'LAN')
        mastery = lol.champion_mastery()
        lvl = mastery['lvl']
        points = mastery['points']
        description =  f'Nivel: {lvl} \nPuntos: {points}'

        emb = discord.Embed(title=mastery['name'], description=description)
        emb.set_image(url=mastery['skin_url'])
        await message.channel.send(embed=emb)


client.run(os.getenv('TOKEN_DISCORD'))