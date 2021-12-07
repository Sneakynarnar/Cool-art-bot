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
import asyncio
import configparser as cp
from dotenv import load_dotenv
import discord 
discord.TextChannel.create_thread = create_thread
from discord_slash import SlashCommand
import discord.ext 
from discord.ext import commands
import os
from threading import Thread
import websockets
import mysql.connector
import sqlite3

con = mysql.connector.connect(
    host="127.0.0.1",
    user="sneaky",
    passwd="Dominus7206!",
    database="coolart"
)


cur = con.cursor(buffered=True)
def calculateTotalExp(rank, exp):
    if rank == 0:
        return exp
    else:
        return int( ((rank+1)/2) * ((2*1000 + (rank*500))) ) +exp
def getLeaderBoardJson():
    cur.execute("SELECT * FROM artLevels")
    records = cur.fetchall()

    def takeTotalExp(elem):
        exp = calculateTotalExp(elem[3], elem[1])
        return exp

    embed = discord.Embed(title="Exp leaderboard")
    counter=1
    leaderboard = {}
    for record in sorted(records, key=takeTotalExp, reverse=True):
        leaderboard[str(record[0])] = {"rank": record[3], "artAmount": record[2], "exp": record[1]}

    return leaderboard


async def startWebSocketServer(ip= "127.0.0.1", port=5050):
    print(f"Running websocket server at ip: {ip} and port: {port}")
    async def send(websocket, path):
        async for message in websocket:
            if message == "leaderboard":
                await websocket.send(str(getLeaderBoardJson()))
        

    await websockets.serve(send, ip, port) 
    
    


async def runBot():
    load_dotenv()
    config = cp.ConfigParser()

    config.read("resources/config.ini")
    intents = discord.Intents.all()
    TOKEN = os.getenv("DISCORD_TOKEN")
    bot = commands.Bot(command_prefix="!", help_command=None, intents=intents)
    slash = SlashCommand(bot, sync_commands=True)
    
    def loadExtentions():
        extentions = config["cogs"]
        for ext in extentions:
            try:
                bot.load_extension("cogs." +ext)
            except Exception as e:
                print(f"Error loading {ext}: ({e})")
                
        print("Loaded Cogs")
    loadExtentions()
    try:
        await bot.start(TOKEN)
    except:
        await bot.start(TOKEN)

async def main():
    asyncio.gather(startWebSocketServer(), runBot())
    
if __name__ == "__main__":
    asyncio.run(main()) 