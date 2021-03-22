import os
import discord
from discord.ext import commands

from utils.giphy import get_giphy
from utils.lol import Lol
from utils.utl import roman_to_int


bot = commands.Bot(command_prefix='>', description='League of legends bot')


@bot.event
async def on_ready():
    print('I am ready!!')
    print(bot.user.name)
    print(bot.user.id)
    print('-'*10)


@bot.command()
async def hi(ctx):
    giphy = get_giphy()
    await ctx.send(giphy)


@bot.command()
async def me(ctx, name: str, server: str):
    lol = Lol(name, server)
    greetings = lol.greetings()

    emb = discord.Embed(title=greetings['greetings'])
    emb.set_image(url=greetings['icon_url'])
    await ctx.send(embed=emb)


@bot.command()
async def champion(ctx, name: str, server: str):
    lol = Lol(name, server)
    mastery = lol.champion_mastery()
    lvl = mastery['lvl']
    points = mastery['points']
    description =  f'Nivel: {lvl} \nPuntos: {points}'

    emb = discord.Embed(title=mastery['name'], description=description)
    emb.set_image(url=mastery['skin_url'])
    await ctx.send(embed=emb)


@bot.command()
async def rank(ctx, name: str, server: str):
    lol = Lol(name, server)
    ranked = lol.ranks()

    tier = ranked['tier']
    rank = ranked['rank']
    league_points = ranked['leaguePoints']
    wins = ranked['wins']
    losses = ranked['losses']

    num = roman_to_int(rank)
    url = f'https://opgg-static.akamaized.net/images/medals/{tier.lower()}_{num}.png?image=q_auto:best&v=1'

    emb = discord.Embed(title='Clasificatoria en solitario', description=f'{tier} {rank}')
    emb.set_image(url=url)
    emb.insert_field_at(index=0, name='LP', value=league_points)
    emb.insert_field_at(index=1, name='V', value=wins)
    emb.insert_field_at(index=2, name='L', value=losses)
    await ctx.send(embed=emb)


bot.run(os.getenv('TOKEN_DISCORD'))