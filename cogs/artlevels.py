import discord_slash 
import requests
async def create_thread(self,name,minutes,message):
    token = 'Bot ' + self._state.http.token
    url = f"https://discord.com/api/v9/channels/{self.id}/messages/{message.id}/threads"
    headers = {
        "authorization" : token,
        "content-type" : "application/json"
    }
    data = {
        "name" : name,
        "type" : 11,
        "auto_archive_duration" : minutes
    }
 
    return requests.post(url,headers=headers,json=data).json()
from discord_slash import cog_ext, SlashContext, SlashCommand, ComponentContext
import discord
discord.TextChannel.create_thread = create_thread
import discord.ext
import random
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageColor
import io
import mysql.connector
import re
from discord.ext import commands
from discord_slash.utils.manage_commands import create_choice, create_option, create_permission, create_multi_ids_permission
from discord_slash.utils.manage_components import create_actionrow, create_button, wait_for_component
from discord_slash.model import SlashCommandPermissionType, ButtonStyle
import asyncio
import sqlite3
MODS = [339866237922181121,479691334332973066,819466383175712780,374219910433210368]
DEVS = [339866237922181121]
ranks = (("Unranked", 906652680821284924), ("Bronze", 906652841299566694), ("Silver", 906652999395450920), ("Gold", 906653136201080832), ("Diamond", 906653275892371527), ("Elite", 906653374487879711))
guild_id = [826814545099358238]
POST_EXP_LOWER  = 50
POST_EXP_UPPER = 100
UPVOTE_EXP_AMOUNT = 50
con = mysql.connector.connect(
    host="127.0.0.1",
    user="sneaky",
    passwd="Dominus7206!",
    database="coolart"
)

cur = con.cursor(buffered=True)

class artlevels(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.utility = self.bot.get_cog("utility")
        self.colour = self.utility.colour
        self.guild_id = self.utility.guild_id
        self.galleryChannel = 907766279635632168
        self.controlRoom = 903363404964696125

    def generateCode(self):
        while True: 
            refCode = random.randint(100000, 999999)
            cur.execute("SELECT * FROM refferals WHERE refferalCode = %s", (refCode,))

            if cur.fetchone() is None:
                return refCode
            else: # You never know.... 
                print(cur.fetchone())
                continue
    class multiplier():
        def __init__(self, bot, payload):
            self.guild = bot.get_guild(guild_id[0])
            self.owner = guild.get_member(payload[0])
            self.multiplier = payload[1]
            self.duration = payload[2]


        
    # @cog_ext.cog_slash(name="refcode", guild_ids=guild_id, description="Shows your refferal code!")
    # async def refcodeCommand(self, ctx: SlashContext):
    #     guild = ctx.guild

    #     cur.execute("SELECT refferalCode FROM refferals WHERE memberId =?", (ctx.author.id,))

    #     code = cur.fetchone()
    #     if code is None:
    #         code = self.generateCode()
    #         cur.execute("INSERT INTO refferals VALUES (%s,%s)", (ctx.author.id, code))
    #     else:
    #         code = code[0]
    #     embed = discord.Embed(description=f"Your refferal code is **{code}**! Get your friend to enter this code when they join then you and them will recieve a **24 HOUR 2X EXP BOOSTER**!")
    #     embed.colour = self.colour
    #     await ctx.send(embed=embed)






    @cog_ext.cog_slash(name="exp", default_permission=False,guild_ids=guild_id, description="Give exp", options=[create_option(name="member", description="Member to give exp to", option_type=6, required=True), 
    create_option(name="amount", description="amount to give", option_type=4, required=True)],
    permissions= {826814545099358238: create_multi_ids_permission(ids=MODS, id_type = SlashCommandPermissionType.USER, permission=True)})
    async def expCommand(self, ctx: discord_slash.SlashContext, member, amount):
        if amount > 0:
            exp = await self.addExp(member, amount)
            if exp:
                await ctx.send(f"{member.name} has been awarded {amount} exp")
            else:
                await ctx.send(f"{member.name} member already max level")
        else:
            await ctx.send("Cannot add exp below 0")
            

    @cog_ext.cog_slash(name="leaderboard", guild_ids=guild_id, description="Shows top 10 on the exp leaderboards")
    async def leaderboardCommand(self, ctx: discord_slash.SlashContext):
        def calculateTotalExp(rank, exp):
            if rank == 0:
                return exp
            else:
                return int( ((rank+1)/2) * ((2*1000 + (rank*500))) ) +exp
        cur.execute("SELECT * FROM artLevels")

        records = cur.fetchall()
        def takeTotalExp(elem):
            exp = calculateTotalExp(elem[3], elem[1])
            return exp

        embed = discord.Embed(title="Exp leaderboard")
        counter=1
        for record in sorted(records, key=takeTotalExp, reverse=True):
            member = self.bot.get_user(record[0])
            if counter == 1:
                place = ":first_place:"
            elif counter == 2:
                place = ":second_place:"
            elif counter == 3:
                place = ":third_place:"
            elif counter == 11:
                break
            else:
                place= "#" + str(counter)
            rank = record[3]
            threashold = 1000 + rank*500
            exp = record[1]
            roleId = ranks[rank][1]
            role = ctx.guild.get_role(ranks[rank][1])
            total = calculateTotalExp(rank, exp)
            mention = member.mention if member is not None else "Deleted user"
            name = member.name if member is not None else "Deleted user"
            embed.add_field(name=f"{place} {name}", value=f"{mention}, Rank: {role.mention}\nExp`{exp}/{threashold}`\n", inline=False)
            counter+=1
        
        await ctx.send(embed=embed)

    @cog_ext.cog_slash(name="rank", guild_ids=guild_id, description="Shows someones rank", options=[create_option(name="member", description="Member to display rank of", option_type=6, required=False)])
    async def rankCommand(self, ctx: discord_slash.SlashContext, member=None):
        if member is None:
            member = ctx.author

        cur.execute("SELECT * FROM artLevels WHERE member = %s", (member.id,))
        record = cur.fetchone()
        if record is None:
            cur.execute("INSERT INTO artLevels VALUES (%s,%s,%s,%s)", (member.id,0,0,0)) # member, exp, artAmount, rank
            record = (member.id,0,0,0)  
        buffer = await self.getRankImage(member, record[1], record[3], ctx.guild)
        await ctx.send(file=discord.File(buffer, "rank.png"))           
        con.commit()
    cur.execute("SELECT * FROM artLevels")
    @commands.Cog.listener()
    async def on_message(self, msg):
        try:
            galleryChannel = msg.guild.get_channel(self.galleryChannel)
        except:
            return
        controlRoom = msg.guild.get_channel(self.controlRoom)
        if msg.author == self.bot.user:
            return
        
        if msg.channel == galleryChannel:
            caption = msg.content
            isLink = False
            media = False
            file = None
            spoiler=False
            attachment = msg.attachments
            if len(attachment) > 1 :
                await msg.author.create_dm()
                await msg.author.dm_channel.send("You cannot upload more than one picture at once")
                msg.delete()
                return
            
            elif len(attachment) == 0:
                linkMatch = re.search("|| (\w+) ||", msg.content)
                if linkMatch:
                    url = linkMatch.group(1)
                    if url.startswith("https://cdn.discordapp.com/attachments/"):
                        mList = msg.content.split()
                        url = mList[0]
                        mList.remove(url)
                        caption = ""
                        for x in mList:
                            caption+= x + " "
                        isLink = True
                        spoiler = True
                if msg.content.startswith("https://cdn.discordapp.com/attachments/"):
                    mList = msg.content.split()
                    url = mList[0]
                    mList.remove(url)
                    caption = ""
                    for x in mList:
                        caption+= x + " "
                    isLink = True
                    spoiler=True

                else:
                    await msg.author.create_dm()
                    await msg.author.dm_channel.send("You can only upload pictures in the gallery channel! If you want to comment on someones art you can use the thread that was created!")                   
                    await msg.delete()
                    return
            else:
                attachment = attachment[0]
                url=attachment.proxy_url
                if attachment.content_type.startswith("image") or attachment.content_type.startswith("video"):
                    media = True
                
            spoiler = attachment.is_spoiler()
            if isLink or media:
            
                artist = msg.author
                caption = "No caption" if caption == "" else caption
                embed = discord.Embed(description=f"**Caption**: {caption}")
                
                if not isLink:
                    if spoiler:
                        file = await attachment.to_file(spoiler=True)
                    else:
                        embed.set_image(url=url)
                else:
                    embed.set_image(url=url)
                embed.set_footer(text=f"Uploaded by {artist.name} (post unverified)", icon_url=artist.avatar_url)
                embed.colour=self.colour
                embed.add_field(name="Tags", value="-")
            else:

                await msg.author.create_dm()
                await msg.author.dm_channel.send("You cannot upload files that arent images or videos in this channel!")
                await msg.delete()
            
            message = await galleryChannel.send( embed=embed,file =file)
            await galleryChannel.create_thread(f"Art discussion ({message.id})", 1440, message)
            
            embed = message.embeds[0]
            link = "https://discord.com/channels/826814545099358238/" + str(galleryChannel.id) +"/"+ str(message.id)
            if not isLink:
                if spoiler:
                    embed.add_field(name="This post has been spoilered", value=f"[click here to go to the message]({link})" )
            else:
                embed.add_field(name="This post has been spoilered", value=f"[click here to go to the message]({link})" )
            actionrow = create_actionrow(create_button(style=ButtonStyle.green, label="Verify!", custom_id=f"verify{message.id}"),create_button(style=ButtonStyle.red, label="Remove", custom_id=f"remove{message.id}"))
            await controlRoom.send(content="Content for verification:",embed=embed, components=[actionrow])

            cur.execute("INSERT INTO gallery VALUES (%s,%s,0)", (message.id, artist.id))
            con.commit()
            await msg.delete()
            await artist.create_dm()
            await artist.dm_channel.send("Do you want to add any tags? If you do type them separated with commas\n\nExample: pro, digital, awesome ")
            async def waitForMessage():
                
                    
                def check(m):
                    if m.author == self.bot.user:
                        return False
                    return m.channel == m.author.dm_channel

                try:
                    message = await self.bot.wait_for('message', timeout=600, check=check)
                except asyncio.TimeoutError:
                    await m.author.dm_channel.send("Timed out.")
                return message

            tags = await waitForMessage()
            tags = tags.content
            tags = tags.split(",")
            newTags = [tag.strip() for tag in tags]
            formattedTags = ""
            for tag in newTags:
                formattedTags += f"{tag.title()}, "

            formattedTags = formattedTags[:-2]
            embed.set_field_at(0, name="Tags", value=formattedTags)
            embed.remove_field(1)
            await message.edit(embed=embed)
            await artist.dm_channel.send("Tags added!")
            

    
    @commands.Cog.listener()
    async def on_component(self, ctx: ComponentContext):
        if ctx.custom_id.startswith("verify"):
            msgId = int(ctx.custom_id[6:])
            cur.execute("SELECT memberId FROM gallery WHERE messageId = %s", (msgId,))
            record = cur.fetchone()
            artist = ctx.guild.get_member(record[0])
            exp = random.randint(POST_EXP_LOWER, POST_EXP_UPPER)
            await self.addExp(artist, exp)
            actionrow = create_actionrow(create_button(style=ButtonStyle.green, label="Upvote!", custom_id="upvote"+str(msgId)))
            galleryChannel = ctx.guild.get_channel(self.galleryChannel)
            message = await galleryChannel.fetch_message(msgId)
            embed = message.embeds[0]
            embed.set_footer(text=f"Uploaded by {artist.name}", icon_url=artist.avatar_url)
            if len(embed.fields) <2:
                embed.insert_field_at(1, name="Upvotes", value="This post has **0** upvotes")
                await message.edit(embed=embed, components=[actionrow])
                await ctx.edit_origin(content=f"Accepted by {ctx.author.mention}!", components=None)
            else:
                await message.edit(embed=embed, components=[actionrow])
        elif ctx.custom_id.startswith("upvote"):
            msgId = int(ctx.custom_id[6:])
            cur.execute("SELECT memberId, upvotes FROM gallery WHERE messageId = %s", (msgId,))
            record = cur.fetchone()
            artist = ctx.guild.get_member(record[0])
            upvotes = record[1]
            if artist == ctx.author:
                await ctx.send(hidden=True, content="We love your pride in your art, however, you cannot upvote your own post.")
                return
            cur.execute("SELECT * FROM upvotesExp WHERE memberId = %s AND postMessageId= %s", (ctx.author.id, msgId))
            record = cur.fetchone()
            if record is None:
                cur.execute("INSERT INTO upvotesExp VALUES (%s,%s)",(ctx.author.id, msgId))
                await self.addExp(member=artist, amount=UPVOTE_EXP_AMOUNT)
            cur.execute("SELECT * FROM upvotes WHERE memberId = %s AND postMessageId= %s", (ctx.author.id, msgId))
            record = cur.fetchone()
            #cur.execute("SELECT * FROM upvotes WHERE memberId = %s AND postMessageId= %s", (ctx.author.id, msgId))
            if record is None:
                cur.execute("INSERT INTO upvotes VALUES (%s,%s)", (ctx.author.id, msgId))
                upvotes+=1
                
            else:
                cur.execute("DELETE FROM upvotes WHERE memberId = %s AND postMessageId = %s", (ctx.author.id, msgId))
                upvotes -=1

            galleryChannel = ctx.guild.get_channel(self.galleryChannel)
            message = await galleryChannel.fetch_message(msgId)
            embed = message.embeds[0]
            embed.set_footer(text=f"Uploaded by {artist.name}", icon_url=artist.avatar_url)
            upstring = f"This post has **{upvotes}** upvotes" if upvotes > 1 else "This post has **1** upvote"
            if len(embed.fields) > 1:
                embed.set_field_at(1, name="Upvotes", value=upstring)
            else:
                embed.add_field(name="Upvotes", value=upstring)
            await message.edit(embed=embed)
            cur.execute("UPDATE gallery SET upvotes = %s WHERE messageId = %s", (upvotes, msgId))

            if record is None:
                await ctx.send(hidden=True, content="Upvote added!")
            else:
                await ctx.send(hidden=True, content="Upvote removed!")

        elif ctx.custom_id.startswith("remove"):
            
            msgId = int(ctx.custom_id[6:])
            cur.execute("DELETE FROM gallery WHERE messageId = %s", (msgId,))
            galleryChannel = ctx.guild.get_channel(self.galleryChannel)
            message = await galleryChannel.fetch_message(msgId)
            await message.delete()
            await ctx.edit_origin(content=f"Removed by {ctx.author.mention}", components=None)


        con.commit()
    async def addExp(self, member, amount): 
        
        guild = self.bot.get_guild(guild_id[0])
        cur.execute(f"SELECT * FROM artLevels WHERE member = {member.id}")
        record = cur.fetchone()
        
        if record is None:
            cur.execute("INSERT INTO artLevels VALUES (%s,%s,%s,%s)", (member.id,0,0,0)) # member, exp, artAmount, rank
            record = (member.id,0,0,0)    
        member = id = record[0]
        exp = record[1] + amount
        
        art = record[2]
        level = baseLevel = record[3]
        threashold = 1000 + level*500
        art+=1
        leveledUp=False 
        while exp >= threashold:
            level +=1
            exp -=threashold
            leveledUp = True
            threashold = 1000 + level*500
        if level >5:
            level = 5
            return False
        levelDifference = level - baseLevel 
        if leveledUp:
            member = guild.get_member(member)
            await member.create_dm()
            name = member.name + member.discriminator
            rank = ranks[level][0]
            
            embed = discord.Embed(title="You leveled up!", description=f"You are now rank **{rank}**", colour=0x00FF00)
            embed.set_thumbnail(url=member.avatar_url)
            await member.dm_channel.send(embed=embed)
            roles = cur.fetchall()

            removeRole = guild.get_role(ranks[baseLevel][1])
            role = guild.get_role(ranks[level][1])
            await member.remove_roles(removeRole)
            await member.add_roles(role)
            id = member.id
        cur.execute(f"UPDATE artLevels SET exp = {exp}, artAmount = {art}, rank = {level} WHERE member = {id}", )
        con.commit()
        return True

        


    async def getRankImage(self,member: discord.Member, exp,  level, guild):
            def drawProgressBar(d, x, y, w, h, progress, bg="black", fg="#a400fc"):
                # draw background
                d.ellipse((x+w, y, x+h+w, y+h), fill=bg)
                d.ellipse((x, y, x+h, y+h), fill=bg)
                d.rectangle((x+(h/2), y, x+w+(h/2), y+h), fill=bg)

                # draw progress bar
                w *= progress
                d.ellipse((x+w, y, x+h+w, y+h),fill=fg)
                d.ellipse((x, y, x+h, y+h),fill=fg)
                d.rectangle((x+(h/2), y, x+w+(h/2), y+h),fill=fg)

            
            rank = guild.get_role(ranks[level][1])
            if level == 5:
                nextRank =None
            else:
                nextRank = guild.get_role(ranks[level+1][1])
                nextRankColour = nextRank.colour.to_rgb()
            
            rankColour = rank.colour.to_rgb()
            
            size = width, height = 900, 200
            image = Image.new("RGB", size, "#342e38")
            image = image.convert("RGBA")

            
            font = ImageFont.truetype("resources/Fonts/impact.ttf",40)
            rankfont = ImageFont.truetype("resources/Fonts/light.ttf",30)
            titlefont = ImageFont.truetype("resources/Fonts/med.ttf",27)
            
            draw = ImageDraw.Draw(image)
            #draw.rounded_rectangle([10, 20, width-300, height-20], fill=(74,74,74, 355))
            #draw.rounded_rectangle([10, 20, width-300, height-20], fill=(74,74,74, 200), width=3,radius=20)
            #draw.rounded_rectangle([650, 20, width-30, height-20], fill=(74,74,74,200), width=3,radius=20)
            draw.rounded_rectangle([10, 20, width-10, height-20], fill=(74,74,74, 200), width=3,radius=20)
            
            
            buffer_avatar = io.BytesIO()
            avatar_asset = member.avatar_url_as(format='jpg', size=128) # read JPG from server to buffer (file-like object)
            await avatar_asset.save(buffer_avatar) 
            buffer_avatar.seek(0)
            threashold = 1000 + level*500
            progress=exp/threashold if nextRank is not None else 1

            # read JPG from buffer to Image
            avatar_image = Image.open(buffer_avatar)
            avatar_image = avatar_image.resize((128,128))
            circle_image = Image.new("L", (128, 128))
            circle_draw = ImageDraw.Draw(circle_image)
            circle_draw.ellipse((0,0, 128,128), fill=255)
            image.paste(avatar_image, (20,35), circle_image)
            name = member.name + "#" + member.discriminator
            draw.multiline_text((175,35), name, font=font, fill=(0, 166, 255))
            draw.multiline_text((175,90), rank.name, font=titlefont, fill=rankColour)
            
            
            #draw.multiline_text((662,50), f"RANK: #1", font=rankfont, fill=(0, 166, 255) ) 
            if nextRank is not None:
                draw.multiline_text((700,100), nextRank.name, font=titlefont, fill=nextRankColour)
                draw.multiline_text((790,135), f"{exp}/{threashold}", font=titlefont, fill=nextRankColour)
            else:
                draw.multiline_text((790,135), f"Max rank!", font=titlefont, fill=(235, 30, 30) )
                nextRankColour = (235, 30, 30)
            #draw.multiline_text((662,130), f"People helped: {total}", font=rankfont, fill=(0, 166, 255))

            draw = drawProgressBar(d=draw, x=155,y=135, w=600, h=25, progress=progress, fg='#%02x%02x%02x' %rankColour)
            image.resize((1350,300))
            buffer_output = io.BytesIO()
            
            
            image.save(buffer_output, "PNG")
            buffer_output.seek(0)
            return buffer_output

def setup(bot):
    bot.add_cog(artlevels(bot))