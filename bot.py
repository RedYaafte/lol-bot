import os
import discord


client = discord.Client()


@client.event
async def on_ready():
    print('I am ready!!')


client.run(os.getenv('TOKEN_DISCORD'))