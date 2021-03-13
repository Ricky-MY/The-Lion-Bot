import discord
import re

from discord.ext import commands

class API(commands.Cog):

    async def do_rtfm(self, ctx, key, obj):
        page_types = {'latest': 'https://discordpy.readthedocs.io/en/latest',
            'python': 'https://docs.python.org/3',}
        ...
        
def setup(bot):
    bot.add_cog(API(bot))
    print('API.cog is loaded')
