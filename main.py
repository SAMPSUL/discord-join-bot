import os
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

WELCOME_CHANNEL_ID = CHANNEL_ID_HERE  # vaihda tähän serverisi welcome-kanavan ID

invites_cache = {}

@bot.event
async def on_ready():
    print(f"Botti käynnistynyt nimellä {bot.user}")
    for guild in bot.guilds:
        invites = await guild.invites()
        invites_cache[guild.id] = {invite.code: invite.uses for invite in invites}

@bot.event
async def on_member_join(member):
    guild = member.guild
    welcome_channel = guild.get_channel(WELCOME_CHANNEL_ID)
    
    invites = await guild.invites()
    inviter = None
    
    for invite in invites:
        if invite.code in invites_cache[guild.id]:
            if invite.uses > invites_cache[guild.id][invite.code]:
                inviter = invite.inviter
        else:
            if invite.uses > 0:
                inviter = invite.inviter
    
    invites_cache[guild.id] = {invite.code: invite.uses for invite in invites}
    
    if welcome_channel:
        if inviter:
            await welcome_channel.send(f"WELCOME TO THIS SERVER {member.mention} INVITED BY {inviter.mention}")
        else:
            await welcome_channel.send(f"WELCOME TO THIS SERVER {member.mention}")

TOKEN = os.environ["DISCORD_TOKEN"]
bot.run(DISCORD_TOKEN_HERE)
