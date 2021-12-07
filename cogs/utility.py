import discord_slash 
from discord_slash import cog_ext, SlashContext, SlashCommand
import discord
import discord.ext
import configparser
from discord.ext import commands
config = configparser.ConfigParser()
config.read("resources/config.ini")
MODS = [339866237922181121,479691334332973066,819466383175712780,374219910433210368]
class utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.guild = bot.get_guild(826814545099358238)
        self.versioncon = config["version"]
        self.version = self.versioncon["version"]
        self.colour = 0x8018f0
        self.guild_id = [826814545099358238]
        self.bot_url= "https://cdn.discordapp.com/avatars/902236467596759060/3abdc60eefd46711a13da9890740dda7.webp?size=1024"

def setup(bot):
    bot.add_cog(utility(bot))