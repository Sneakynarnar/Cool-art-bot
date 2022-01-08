MODS = [339866237922181121,479691334332973066,819466383175712780,374219910433210368]
import re
from datetime import datetime
import asyncio
from discord.ext import commands, tasks
import discord
import logging
from discord import Embed
import discord_slash
from discord_slash.context import ComponentContext
from discord_slash.utils.manage_components import create_button, create_actionrow
from discord_slash.model import ButtonStyle
from discord_slash import cog_ext
logger = logging.getLogger('bot')
import sqlite3
import mysql.connector



# buttons = [
# create_button(style=ButtonStyle.grey, label="There is a server announcement", custom_id="announcement"), 
# create_button(style=ButtonStyle.grey, label="Details about events!", custom_id="events"), 

# ]
buttons = [create_button(style=ButtonStyle.grey, label="Male", custom_id="male",emoji="♂️"),
create_button(style=ButtonStyle.grey, label="Female", custom_id="female", emoji="♀️"),
create_button(style=ButtonStyle.grey, label="Other", custom_id="other",),
]
actionrow =create_actionrow(*buttons)
class Roles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    



    @commands.command(name="srm")
    async def sendCommand(self, ctx):
        buttons = [create_button(style=ButtonStyle.grey, label="Male", custom_id="male",emoji="♂️"),
        create_button(style=ButtonStyle.grey, label="Female", custom_id="female", emoji="♀️"),
        create_button(style=ButtonStyle.grey, label="Other", custom_id="other",),
        ]
        actionrow =create_actionrow(*buttons)

        if ctx.author.id == 339866237922181121:
           guild = ctx.guild
           channel = guild.get_channel(827020439980474408)
           message = await channel.fetch_message(909824369478496276)
           await message.edit(content="Click your gender! :P",components=[actionrow])
           await ctx.send("Done.")
        else:
            print("blocked.") 

    @cog_ext.cog_slash(name="ping", guild_ids=[720323009503690762], description="Pong!")
    async def anotherPingCommand(self, ctx: discord_slash.context):
        await ctx.send("Pong")
    @commands.Cog.listener()
    async def on_component(self,ctx: ComponentContext):
        guild = self.bot.get_guild(ctx.guild_id)
        if guild.id == 826814545099358238:
            if ctx.custom_id == "male":
                role = guild.get_role(827025544892645378)
            elif ctx.custom_id == "female":
                role = guild.get_role(827025551087632414)
            elif ctx.custom_id == "other":
                role = guild.get_role(872774262375718912)
            elif ctx.custom_id == "13-14":
                role = guild.get_role(830809858730360833)
            elif ctx.custom_id == "15-17":
                role = guild.get_role(830809969334419527)
            elif ctx.custom_id == "18+":
                role = guild.get_role(830810047570771968)
            elif ctx.custom_id == "beginner":
                role = guild.get_role(827026512908910592)
            elif ctx.custom_id == "intermediate":
                role = guild.get_role(827026592719044658)
            elif ctx.custom_id == "pro":
                role = guild.get_role(827026739255181324)
            elif ctx.custom_id == "digital":
                role = guild.get_role(827588271902818304)
            elif ctx.custom_id == "traditional":
                role = guild.get_role(827587922307973172)
            elif ctx.custom_id == "commissions":
                role = guild.get_role(908001474196439050)
            else:
                return
            try:
                if role in ctx.author.roles:
                    await ctx.author.remove_roles(role)
                    await ctx.send(content=f"I have removed the {role.name} role!", hidden=True, )
                else:
                    await ctx.author.add_roles(role)
                    await ctx.send(content=f"I have given you the {role.name} role!", hidden=True, )
            except:
                pass

def setup(bot):     
    bot.add_cog(Roles(bot)) 


