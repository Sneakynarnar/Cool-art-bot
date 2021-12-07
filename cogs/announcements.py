import discord_slash 
from discord_slash import cog_ext, SlashContext, SlashCommand
import discord
import discord.ext
import sqlite3
import datetime
import mysql.connector
from datetime import datetime, timedelta, datetime
#from backports.datetime_isoformat import MonkeyPatch
from discord.ext import commands, tasks
from discord_slash.utils.manage_commands import create_choice, create_option, create_permission, create_multi_ids_permission
from discord_slash.utils.manage_components import create_actionrow, create_button, wait_for_component
from discord_slash.model import SlashCommandPermissionType, ButtonStyle
import asyncio
import regex as re
#MonkeyPatch.patch_fromisoformat()
MODS = [339866237922181121,479691334332973066,819466383175712780,374219910433210368,749202146074951681]
guild_id = [826814545099358238]
con = mysql.connector.connect(
    host="127.0.0.1",
    user="sneaky",
    passwd="Dominus7206!",
    database="coolart"
)


cur = con.cursor(buffered=True)
class announcements(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.now = datetime.utcnow()
        



    class scheduledAnnouncement():
        def __init__(self, bot, payload):
            title = payload[0]
            content = payload[1]
            mentions = payload[2]
            time = payload[3]
            showIcon = payload[4]
            showAuthor= payload[5]
            authorId = payload[6]
            channelId = payload[7]
            guild = bot.get_guild(guild_id[0])
            self.author = guild.get_member(authorId)
            self.embed = discord.Embed(title=title, description=content, colour=0x8018f0)
            if showIcon:
                self.embed.set_thumbnail(url=guild.icon_url)
            if showAuthor:
                self.embed.set_footer(text=f"This is a scheduled announcement made by {self.author.display_name}", icon_url=self.author.avatar_url)

            self.time = datetime.fromisoformat(time)
            self.mentions = mentions
            self.channel = guild.get_channel(channelId)
        async def send(self):
            await self.channel.send(content=self.mentions,embed=self.embed)

            
    @commands.Cog.listener()
    async def on_ready(self):
        #await self.checkForAnnouncement.start()
        pass
    @cog_ext.cog_slash(name="makeannouncement",default_permission=False,guild_ids=guild_id, options = [create_option(name="title",description="The title of the announcement", option_type=3, required=True ), 
                                                           create_option(name="channel", description="The channel you want to send the announcemnt in", option_type=7,required=True),
                                                           create_option(name="showauthor", description="Show who sent this announcemnt", required=False,option_type=5,),
                                                           create_option(name="mentions", description="Mentions will be before the embed", required=False, option_type=3,),
                                                           create_option(name="includeservericon", description="This will include the server picture", required=False, option_type=5),
                                                           create_option(name="skipdesc", description="This will skip the description and go straight to adding a field", option_type=5,required=False)
                                                           ],permissions={826814545099358238: create_multi_ids_permission(ids=MODS, id_type = SlashCommandPermissionType.USER, permission=True)})
    async def makeAnnouncements(self, ctx: SlashContext, title, channel: discord.TextChannel, showauthor=None, mentions=None, includeservericon=None, skipdesc=None):
        showauthor = False if showauthor is None else showauthor
        includeservericon = False if includeservericon is None else includeservericon
        skipdesc = False if skipdesc is None else skipdesc

        async def waitForMessage():
            def check(m):
                return m.author == ctx.author and m.channel == ctx.channel

            try:
                message = await self.bot.wait_for('message', timeout=600, check=check)
            except asyncio.TimeoutError:
                await ctx.channel.send("Timed out.")
            return message

        await ctx.defer()
        if not skipdesc:
            delmessage = await ctx.channel.send(
                "Send a message of the content of this announcement! (You can use any text modifications such as **BOLD** and __underline__)")
            message = await waitForMessage()
            description = message.content
        else:
            description = ""
        embed = discord.Embed(title=title, description=description)
        embed.color = 0x8018f0
        if showauthor:
            embed.set_footer(text=f"This announcement was made by {ctx.author.display_name}",
                             icon_url=ctx.author.avatar_url, )
        if includeservericon:
            embed.set_thumbnail(url=ctx.guild.icon_url)
        actionrow = create_actionrow(
            create_button(style=ButtonStyle.green, label="Looks good! Send it!", custom_id="confirm"),
            create_button(style=ButtonStyle.blurple, label="Add a new field", custom_id="field"),
            create_button(style=ButtonStyle.red, label="Delete last field", custom_id="del", ),
            create_button(style=ButtonStyle.red, label="Cancel", custom_id="cancel"))
        if not skipdesc:

            await message.delete()
            await delmessage.delete()

        embedMessage = await ctx.send(content="This is a preview of the message that will be sent in the channel.",
                                          embed=embed, components=[actionrow], )
        buttonCtx: ComponentContext = await wait_for_component(self.bot, components=actionrow)
        confirmed = False
        while not confirmed:
            await buttonCtx.defer(edit_origin=True)

            if not skipdesc:
                if buttonCtx.custom_id == "confirm" and buttonCtx.author == ctx.author:
                    await channel.send(content=mentions, embed=embed)
                    await buttonCtx.edit_origin(embed=None, content="Sent!", components=None)
                    confirmed = True
                    return
                elif buttonCtx.custom_id == "cancel" and buttonCtx.author == ctx.author:
                    await buttonCtx.edit_origin(embed=None, content="Cancelled", components=None)
                    return
                elif buttonCtx.custom_id == "field" and buttonCtx.author == ctx.author :
                    delMessage = await ctx.channel.send("What is the title of the field?")
                    message = await waitForMessage()
                    name = message.content
                    await message.delete()
                    await asyncio.sleep(0.1)
                    await delMessage.delete()
                    delMessage = await ctx.channel.send("What is the content of the field?")
                    message = await waitForMessage()
                    value = message.content
                    await message.delete()
                    await asyncio.sleep(0.1)
                    await delMessage.delete()
                    embed.add_field(name=name, value=value, inline=False)

                    await buttonCtx.edit_origin(embed=embed)
                elif buttonCtx.custom_id == "del" and buttonCtx.author == ctx.author:
                    index = len(embed.fields) -1
                    embed.remove_field(index)
                    
            else:

                delMessage = await ctx.channel.send("What is the title of the field?")
                message = await waitForMessage()
                name = message.content
                await message.delete()
                await asyncio.sleep(0.1)
                await delMessage.delete()
                delMessage = await ctx.channel.send("What is the content of the field?")
                message = await waitForMessage()
                value = message.content
                await message.delete()
                await asyncio.sleep(0.1)
                await delMessage.delete()
                embed.add_field(name=name, value=value)

                embedMessage = await ctx.send(content="This is a preview of the message that will be sent in the channel.",embed=embed, components=[actionrow], )
                skipdesc = False


            buttonCtx: ComponentContext = await wait_for_component(self.bot, components=actionrow)
                  
        
    @cog_ext.cog_slash(name="makescheduledannouncement",guild_ids=guild_id,default_permission=False, options = [
                                                           create_option(name="time", description="Time and date DD/MM/YYYY HH:MM in the timezone UTC", option_type=3, required=True),
                                                           create_option(name="title",description="The title of the announcement", option_type=3, required=True ), 
                                                           create_option(name="content", description="Content of the embed", option_type=3, required=True),
                                                           create_option(name="channel", description="The channel you want to send the announcemnt in", option_type=7,required=True),
                                                           create_option(name="showauthor", description="Show who sent this announcemnt", required=False,option_type=5,),
                                                           create_option(name="mentions", description="Mentions will be before the embed", required=False, option_type=3,),
                                                           create_option(name="includeservericon", description="This will include the server picture", required=False, option_type=5)
                                                           ],permissions={826814545099358238: create_multi_ids_permission(ids=MODS, id_type = SlashCommandPermissionType.USER, permission=True)})
    async def makeScheduledAnnouncement(self, ctx: SlashContext, time, title, content, channel: discord.TextChannel, showauthor=None, mentions=None, includeservericon=None):
        dateMatch = re.match("(\d{2})\/(\d{2})\/(\d{4}) (\d{2}):(\d{2})", time) # matching to the syntax XX/XX/XXXX XX:XX
        if dateMatch:
            time = "" + dateMatch.group(3) + "-"+dateMatch.group(2) + "-" + dateMatch.group(1) + " " + dateMatch.group(4) + ":" + dateMatch.group(5) #putting the date in the right format
        else:
            await ctx.send("Incorrect syntax for time")
            return
        try:
            timeObject = datetime.fromisoformat(time) # gets datetime object from ISO format string
        except Exception as e:
            print(e)
            await ctx.send("There is something wrong with the time you entered. Are you sure it's right?") # Error is most likely because of an invalid time
            return
        
        cur.execute("SELECT * FROM announcements")
        announcement = self.scheduledAnnouncement(self.bot, (title, content, mentions, time, includeservericon, showauthor, ctx.author_id, channel.id))
        actionrow = create_actionrow(create_button(style=ButtonStyle.green, label="Confirm", custom_id="confirm"), create_button(style=ButtonStyle.red, label="Cancel", custom_id="cancel"))
        await ctx.send(content=f"The embed below will be sent at {announcement.time} in {announcement.channel.mention}",embed=announcement.embed, components=[actionrow])
        buttonCtx: ComponentContext = await wait_for_component(self.bot, components=actionrow)

        if buttonCtx.custom_id == "confirm":
            
            cur.execute("INSERT INTO announcements VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (title, content, mentions, time, includeservericon, showauthor, ctx.author_id, channel.id))
            await buttonCtx.edit_origin(embed=None, content=f"Announcement scheduled for {time}.", components=None)
            con.commit()
            return   
        elif buttonCtx.custom_id == "cancel":
            await buttonCtx.edit_origin(embed=None, content="Cancelled", components=None)
            return
    @tasks.loop(seconds=60)
    async def checkForAnnouncement(self):
        now = datetime.utcnow() + timedelta(minutes=1) # now
        frmt = "%Y-%m-%d %H:%M"  
        nowstrf = now.strftime(frmt)
        cur.execute("SELECT * FROM announcements WHERE time = %s", (nowstrf,))
        for record in cur.fetchall():
            announcement = self.scheduledAnnouncement(self.bot, record)
            await announcement.send()
        
        cur.execute("DELETE FROM announcements WHERE time = %s", (nowstrf,))
        con.commit()
        con.close()
    @checkForAnnouncement.before_loop
    async def before_check(self):
        await self.bot.wait_until_ready() # Make sure the bot is ready before doing anything
        now = datetime.utcnow()
        future = datetime(now.year, now.month, now.day, now.hour, now.minute, 0, 0) + timedelta(minutes=1) # waiting until the next minute
        print("Sleeping for {0} seconds".format((future - now).seconds))
        await asyncio.sleep((future - now).seconds) # Sleep for however many seconds it takes to get to the next minute
        
        



def setup(bot):
    bot.add_cog(announcements(bot))
