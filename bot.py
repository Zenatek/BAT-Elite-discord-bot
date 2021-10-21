from discord import channel
import requests
import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions
import time
import os


intents = discord.Intents.default()
intents.members = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='BATman'))


@client.event
async def on_member_update(before, after):
    if len(before.roles) < len(after.roles):
        # The user has gained a new role, so lets find out which one
        member = client.get_guild(before.guild.id).get_member(before.id)
        newRole = next(role for role in after.roles if role not in before.roles)
        if newRole.id == 878737866337959947:
            member = client.get_guild(before.guild.id).get_member(before.id)
            await member.send(str(member.name) + " we are glad to have you in the 📣bat-elites!  🥳")
            await member.send("Please enter your twitter profile link below. ⬇️ ")


@client.event
@commands.dm_only()
async def on_message(message):
    user = message.author
    server = client.get_guild(839283762843484192)
    role = discord.utils.find(lambda r: r.id == 878737866337959947, server.roles)
    if(role in server.get_member(user.id).roles):
        if "https://twitter.com/" in message.content:
            if isinstance(message.channel, discord.channel.DMChannel):
                myfile = open('bat_elite_list.txt','a')
                myfile.write('\n'+'@' + str(message.author).replace(" ", "") + '\t\t\t' + str(message.content))
                myfile.close()
                await message.add_reaction("✅")
        elif "!elites list" in message.content:
            embed=discord.Embed(
            title="BAT Elites",
                url="https://twitter.com/i/lists/1449766564966895625",
                description="Below the BAT Elites Twitter list",
                color=discord.Color.from_rgb(204,0,204))            
            embed.set_thumbnail(url="https://raw.githubusercontent.com/Zenatek/BAT-Elite-discord-bot/165f20e9f953732994f4af1d543b547a5aa101ff/img/BATElite.png")
            with open('bat_elite_list.txt','r') as f:
                counter = 0
                new_embed = False
                for line in f:
                    counter += 1
                    if(new_embed == True):
                        embed=discord.Embed(
                            title="BAT Elites",
                            url="https://twitter.com/i/lists/1449766564966895625",
                            description="",
                            color=discord.Color.from_rgb(204,0,204))
                        new_embed = False
                    if(counter % 25 == 0):
                        embed.set_footer(text="Follow them on Twitter")
                        await message.channel.send(embed=embed)
                        new_embed = True
                    else:
                        discord_id = line.split()[0]
                        twitter_link = line.split()[1]
                        embed.add_field(name=str(discord_id), value=twitter_link, inline=True)
                embed.set_footer(text="Follow them on Twitter")
                await message.channel.send(embed=embed)
        elif "!elites download" in message.content:
            file = discord.File("bat_elite_list.txt")
            await message.channel.send(file=file, content="BAT Elites Twitter list")
        elif "!elites help" in message.content:
            await message.channel.send("!elites list - to view all BAT Elites twitter profile\n!elites download - to download the twitter profile list")



if __name__ == '__main__':
    print("Running")
    client.run(os.environ.get('BATELITE'))