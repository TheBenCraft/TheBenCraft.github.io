import json
import discord
from discord import channel
from discord.ext import commands
import simplejson as sj
import requests as rq

# settings.json öffnen und lesen
with open("settings.json","r",encoding="utf-8") as settingsFile:
    settings = json.load(settingsFile)
    settingsFile.close

# settings aufschlüssel/zuweisen
token = settings["client"]["token"]
status = settings["client"]["status"]
prefix = settings["client"]["prefix"]

guildID = settings["discord"]["ID"]
memberID = settings["discord"]["roles"]["member"]
inhaberID = settings["discord"]["roles"]["inhaber"]
reportID = settings["discord"]["roles"]["report"]

intents = discord.Intents.default()
intents.members = True

# unser discord bot
client = commands.Bot(intents=intents,command_prefix = prefix)
client.remove_command("help")

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game(name=status))
    print(f'Name: {client.user.name}')
    print(f'Prefix: {prefix}')
    print(f'--------------------------')


# YouTube Game Command
@client.command(aliases=['youtube', 'YouTube', 'yt'])
async def YT(ctx):
    if not ctx.message.author.voice:
        await ctx.send('You are not connected to a voice channel', delete_after=10)
        await ctx.channel.purge(limit=1)
    else:
     await ctx.channel.purge(limit=1)
     author = ctx.message.author
     voice_channel = ctx.message.author.voice.channel.id
     data = {'max_uses': '0', 'target_type': '2', 'target_application_id': '755600276941176913'}
     data_json = sj.dumps(data)
     payload = {'json_payload': data_json}
     voiceid = str(voice_channel)
     headers = {'Content-type': 'application/json', 'Authorization': 'Bot [TOKEN]'}
     r = rq.post("https://discord.com/api/v8/channels/" + voiceid +"/invites", json=data, headers=headers)
     if(r.status_code == 200):
        respose =  r.json()
        invite_code = respose["code"]
        invite_link = "Klicke [hier](https://discord.com/invite/" + invite_code +") um YouTube zu starten!"
        embed = discord.Embed(colour=discord.Colour(0x4ef0f4))
        embed.set_footer(text=" Bot by TheBenCraft")
        embed.add_field(name="YouTube", value=invite_link, inline=False)
        embed.add_field(name="Ersteller", value=f"YouTube Together wurde erstellt von `{author}`")

        await ctx.send(embed=embed, delete_after = 120)


client.run(token)
