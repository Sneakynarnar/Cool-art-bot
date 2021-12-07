import discord_slash 
from discord_slash import cog_ext, SlashContext, SlashCommand
import discord
import discord.ext
from discord.ext import commands


MODS = [339866237922181121,479691334332973066,819466383175712780,374219910433210368]
class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        

def setup(bot):
    bot.add_cog(Events(bot))