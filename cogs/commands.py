import discord_slash 
from discord_slash import cog_ext, SlashContext, SlashCommand, ComponentContext
import discord
import discord.ext
import asyncio
import mysql.connector
import random
import sqlite3
from discord.ext import commands, tasks
from discord_slash.utils.manage_commands import create_choice, create_option, create_permission, create_multi_ids_permission
from discord_slash.utils.manage_components import create_actionrow, create_button, wait_for_component
from discord_slash.model import SlashCommandPermissionType, ButtonStyle
ruleChoices = [create_choice(name="Rule 1", value=1), create_choice(name="Rule 2", value=2), create_choice(name="Rule 3", value=3), create_choice(name="Rule 4", value=4), \
 create_choice(name="Rule 5", value=5), create_choice(name="Rule 6", value=6)]
censorChoices = [create_choice(value=1, name="Spoiler"), create_choice(value=2, name="Banned"), create_choice(value=3, name="Allow")]
MODS = [339866237922181121,479691334332973066,819466383175712780,374219910433210368]
guild_id=[826814545099358238]
host = "localhost"

con = mysql.connector.connect(
    host=host,
    user="sneaky",
    passwd="Dominus7206!",
    database="coolart"
)


cur = con.cursor(buffered=True)
class commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.utility = self.bot.get_cog("utility")
        self.colour = self.utility.colour
        self.version = self.utility.version
        self.guild_id = self.utility.guild_id

    @cog_ext.cog_subcommand(base="howto",name="post", description="Shows how to post!", guild_ids=guild_id)
    async def howToPostCommand(self, ctx):
        
        embed= discord.Embed(title="How gallery channels work!", description="Simply post your image and the bot will format it!", inline=False)
        embed.add_field(name="But what about EXP?", value="Once you post, the mods get a message in a channel, they can choose to verify images. Once an image is verified, you instantly get between 50-100 exp. Upvotes are then also enabled! You currently get 50exp per upvote (even if they un-upvoting).",inline=False)
        embed.add_field(name="What does exp do?", value="Exp allows you to rank up, you start with no rank and you can have a max rank of ELITE",inline=False)
        embed.colour=self.colour
        file= discord.File(fp="resources/Images/howtopost.gif",filename="howtopost.gif")
        embed.set_image(url="attachment://howtopost.gif") 
        await ctx.send(embed=embed, file=file)       

    @cog_ext.cog_subcommand(base="howto",name="postlinks", description="Shows how to add spoilers to images", guild_ids=guild_id)
    async def howToPostLinksCommand(self, ctx):
        embed= discord.Embed(title="How to add spoiler tags", description="Simply add caption after link!\n**NOTE** it is strongly recommended you post the file instead, because discord only stores the link for a certain amount of time after the message is deleted.")

        embed.colour=self.colour
        file= discord.File(fp="resources/Images/howtopostlink.gif",filename="howtopostlink.gif")
        embed.set_image(url="attachment://howtopostlink.gif") 
        await ctx.send(embed=embed, file=file) 
    
    @cog_ext.cog_subcommand(base="howto",name="spoiler", description="Shows how to add spoilers to images", guild_ids=guild_id)
    async def howToSpoilerCommand(self, ctx):
        file= discord.File(fp="resources/Images/howtospoiler.gif",filename="howtospoiler.gif")
        embed= discord.Embed(title="How to add spoiler tags", description="Simply check the spoiler box when uploading images to the gallery channel")
        embed.colour=self.colour
        
        embed.set_image(url="attachment://howtospoiler.gif") 
        await ctx.send(embed=embed, file=file) 
    @cog_ext.cog_slash(name="version", guild_ids=guild_id,description="Version of the bot")
    async def versionCommand(self, ctx):
        embed= discord.Embed(title="Cool-art-bot", colour=self.colour)
        embed.add_field(name="Version", value=self.version)
        dev = self.bot.get_user(339866237922181121)
        name = dev.name +"#"+ dev.discriminator
        embed.add_field(name="Bot developer",value=f"{name}")

        embed.set_thumbnail(url=self.utility.bot_url)
        await ctx.send(embed=embed) 

    @cog_ext.cog_slash(name="nameeveryone", guild_ids=guild_id,default_permission=False, permissions={826814545099358238: create_multi_ids_permission(ids=MODS, id_type = SlashCommandPermissionType.USER, permission=True)},
     options=[create_option(name="nick", description="Everyone should be nicked",option_type=3, required=True)])
    async def nameAllCommand(self, ctx, nick):
        guild = self.bot.get_guild(guild_id[0])
        await ctx.defer()
        for member in guild.members:
            try:
                await member.edit(nick=nick)
            except Exception as e:
                pass
        await ctx.send("Done.")
    @cog_ext.cog_slash(name="reverteveryone",guild_ids=guild_id,default_permission=False, permissions={826814545099358238: create_multi_ids_permission(ids=MODS, id_type = SlashCommandPermissionType.USER, permission=True)},
     )
    async def revertAllCommand(self, ctx, nick):
        guild = self.bot.get_guild(guild_id[0])
        await ctx.defer()
        for member in guild.members:
            await asyncio.sleep(0.1)
            try:
                await member.edit(nick=None) 
            except:
                pass
        await ctx.send("Done.")
            
    @cog_ext.cog_slash(name="invite", guild_ids=guild_id,description="Invite link to the server")
    async def inviteCommand(self,ctx):
        await ctx.send("You can invite your friends to the server with this link, thanks in advance!: https://discord.com/invite/BMpcY6nn49")
    
    @cog_ext.cog_slash(name="rules",description="Shows a rule (1-6)",guild_ids=guild_id, options=[create_option(
        name="rule", description="Which rule 1-6 should be displayed", option_type=4, required=False, choices=ruleChoices)])
    async def rulesCommand(self, ctx,rule):
        rules= ["1. No harassment/bullying (This includes using slurs)", "2. No spamming outside the <#826871523792519168> channel","3. Use the correct channels (We understand this may not happen by mistake but at least try)", "4. Speak English unless you're in <#902939158404800542>","5. No politics or serious debates", "6. Be Nice! and Have fun!"]
        if rule > 0 and rule < 7:
            await ctx.send("**{0}**".format(rules[rule-1]))
        else:
            await ctx.send("That is not a rule!")

    
    @cog_ext.cog_slash(name="artrules",description="Shows censorship rules",guild_ids=guild_id, options=[create_option(
        name="rule", description="Which rule 1-6 should be displayed", option_type=4, required=True, choices=censorChoices)])
    async def artRulesCommand(self, ctx,rule):
        embed = discord.Embed()
        embed.color= self.colour
        if rule == 1:
            embed.title="Art you should add a spoiler for"
            embed.description="- graphic wounds, lots of blood, general disturbing content\n- sexually suggestive content (non nsfw)\n- art about mental health or sensitive topics"
        elif rule == 3:
            embed.title="Art that is completely fine"
            embed.description="Any low levels of gore that aren't too graphic"
        elif rule == 2:
            embed.title="Banned art"
            embed.description="- Any type of nsfw content.\n- Extreme gore" 

        await ctx.send(embed=embed)  



    @cog_ext.cog_slash(name="rockpaperscissors",guild_ids=guild_id, options = [create_option(
                                    name= "choice",
                                    description="Rock paper or scisors?",
                                    required=True,
                                    option_type=3, 
                                    choices = [create_choice(name="rock", value="rock"),
                                            create_choice(name="paper", value="paper"),
                                            create_choice(name="scissors", value="scissors"),]
    )])
    async def rpsCommand(self, ctx: discord_slash.SlashContext, choice):
        choice = choice.lower()
        choices = ["rock", "paper", "scissors"]
        if choice not in choice:
            await ctx.send("That is not a valid choice.")
            return
        

        aiChoice = random.choice(choices)
        if (aiChoice == "rock" and choice=="paper") or (aiChoice== "scissors" and choice=="rock") or (aiChoice=="paper" and choice=="scissors"):
            await ctx.send(f"You picked {choice} and I picked {aiChoice} so I lose :(")
        elif choice == aiChoice:
            await ctx.send(f"We both picked {choice}! So its a draw! We are so connected <3")

        else:
            await ctx.send(f"You picked {choice} and I picked {aiChoice} so I win ;)")

    """     @commands.Cog.listener()
        async def on_member_join(self, member):
            async def waitForMessage():
                def check(m):
                    valid = m.channel == member.dm_channel
                    typeValid = False
                    rangeValid = False
                    dbValid = False
                    try:
                        code = int(m)
                        typeValid = True
                    except ValueError:
                        pass

                    rangeValid = True if code in range(100000, 999999) else False
                    cur.execute("SELECT * FROM refferals WHERE refferalCode = %s", (code,))
                    if cur.fetchone() is not None:
                        dbValid = True
                    
                    return valid and typeValid and rangeValid and dbValid 
                try:
                    message = await self.bot.wait_for('message', timeout=3600, check=check)
                except asyncio.TimeoutError:
                    await ctx.channel.send("Timed out.")
                return message
            embed=discord.Embed(title="Welcome to The Cool Art Community!!", description="We are so happy to have you here! I am this servers exclusive bot and here is some information about the server to get you started!")

            embed.add_field(name= "•Art sharing•", 
            value="If you want to share art with other artists then check out our art sharing channel on the gallery category! We have the <#907766279635632168> for you to post on! do /howto post to see how to post there. (Don't worry its very easy)")
            embed.add_field(name="•Art help•", 
            value="If you want some advice on what you are working on then feel free to ask on our <#872544265480318986> channel.")
            embed.add_field(name="Just a quick note",
            value="Bare in mind that most people on the server are from Europe so if no one welcomes you we could all be asleep. As the server grows this will become less of an issue but in the mean time if you want to chat with some other artists check out <#826814547141722145>! Lets all have fun making art together!")
            await member.create_dm()
            await member.dm_channel.send(embed=embed)
            await member.dm_channel.send("If you have a refferal code, send it here! You and your friend that invited you would get a 2X EXP booster for 24 hours! If you don't give a valid code in an hour, you can't claim this offer, the bot only replies to valid codes.")
            message= await waitForMessage()
            cur.execute("SELECT memberId FROM refferals WHERE refferalCode = %s", (code,))
            record = cur.fetchone()
            if record is None:
                return

            
            self.addBooster(message.author.id)
            self.seld.addBooster(record[0])
    """

    @cog_ext.cog_slash(name="apply", guild_ids=guild_id,description="Apply for mod!")
    async def applyCommand(self, ctx):
        await ctx.send("Thank's for your consideration! Check your DMs")
        async def waitForMessage():
            def check(m):

                return m.channel == ctx.author.dm_channel

            try:
                message = await self.bot.wait_for('message', timeout=600, check=check)
            except asyncio.TimeoutError:
                await ctx.channel.send("Timed out.")
            return message
        await ctx.author.create_dm()
        embed = discord.Embed(title="Thank you for applying for mod", description="Give us a some reasons why we should pick you to be mod! (responses will be sent to moderation team)")
        embed.add_field(name="What we look for", value="- **Good people skills!** You must have good people skills, so people like you, and would co-operate eith you \
        \n-**Good knowledge of the rules**, you must know the rules and the info inside out. Exactly what channels people should use, and art that is and isn't allowed \
        \n-**Be active**, we should see you in chat alot, posting alot and on the leaderboards etc. \n\n**GOOD LUCK**")
        await ctx.author.dm_channel.send(embed=embed)
        application = await waitForMessage()
        await ctx.author.dm_channel.send("Application received! You will receive a response from this bot soon!")
        cur.execute("INSERT INTO applications VALUES (%s,%s)", (application.id, ctx.author.id))

        actionrow = create_actionrow(create_button(style=ButtonStyle.green, label="Accept for interview", custom_id=f"accept{application.id}"),create_button(style=ButtonStyle.red, label="Decline", custom_id=f"decline{application.id}"))

        channel = ctx.guild.get_channel(914651900618608700)
        embed = discord.Embed(title=f"{ctx.author.name}'s application", description=f"{application.content}\n\n- {ctx.author.mention}", )
        await channel.send(embed=embed,components=[actionrow] )      
        con.commit()
        


    @commands.Cog.listener()
    async def on_component(self, ctx: ComponentContext):
        guild = self.bot.get_guild(guild_id[0])
        if ctx.custom_id.startswith("accept"):
            await ctx.defer(edit_origin=True)
            msgId = int(ctx.custom_id[6:])
            print(msgId)
            
            cur.execute("SELECT memberId FROM applications WHERE appMessageId = %s",(msgId,))
            memberId = cur.fetchone()
            if memberId is None:
                return
            memberId = memberId[0]
            print(memberId)
            user = guild.get_member(memberId)
            await user.dm_channel.send("Good news! We liked your application and would like to talk to you more about being a mod! A staff member should DM you")
            cur.execute("DELETE FROM applications WHERE appMessageId = %s",(msgId,))
            await ctx.edit_origin(content=f"Accepted for interview by {ctx.author.mention}!", components=None)
            con.commit()

            
        elif ctx.custom_id.startswith("decline"):
            await ctx.defer(edit_origin=True)
            msgId = int(ctx.custom_id[7:])
            print(msgId)
            cur.execute("SELECT memberId FROM applications WHERE appMessageId = %s",(msgId,))
            memberId = cur.fetchone()
            if memberId is None:
                return
            memberId = memberId[0]
            user = guild.get_member(memberId)
            await user.dm_channel.send("We appreciate you wanting to help out in the server! But we have decided are not what we are looking for in a mod right now, thank you for applying.\n\nSincerely - The Mod Team :)")
            cur.execute("DELETE FROM applications WHERE appMessageId = %s",(msgId,))
            await ctx.edit_origin(content=f"Declined by {ctx.author.mention}!", components=None)
            con.commit()
          
    @commands.command(name ="status", hidden = True)
    async def _status(self, ctx, status,*, thing=None):
        if ctx.author.id in MODS:
            activity = None
            if status == "listen":
                activity=discord.Activity(type=discord.ActivityType.listening, name=thing)
                act = "Listening to"
            elif status == "watch":
                act = "Watching"
                activity=discord.Activity(type=discord.ActivityType.watching, name=thing)
            elif status == "play":
                act = "Playing"
                activity=discord.Game(name=thing)
            elif status == "me":
                await ctx.send(f"activity is {ctx.author.activity}")
                return
            else:
                await ctx.send("Non valid syntax")
        await self.bot.change_presence(activity=activity)
        await ctx.channel.send('Status changed to "{0} {1}"'.format(act, thing))

            
def setup(bot):
    bot.add_cog(commands(bot))