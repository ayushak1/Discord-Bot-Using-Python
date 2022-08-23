import asyncio
# # from distutils import extension
from email import message
# # from distutils import extension
from re import T
from flask import Flask
# from keep_alive import keep_alive
import asyncio
import discord
import time
from threading import Thread
# import sys

# import os
# import traceback
from discord.ext import commands
# import json

intents=discord.Intents.default() 
intents.members = True
bot = commands.Bot(command_prefix='!!', case_insensitive=True,intents=discord.Intents.all())

# with open("./config.json", 'r') as configjsonFile:
#         configData = json.load(configjsonFile)
#         TOKEN = configData["DISCORD_TOKEN"]

@bot.event
async def on_ready():
    await bot.load_extension("jishaku")
    print("I am Ready")

@bot.command()
async def hi(ctx):
    await ctx.send('Hello!')

@bot.command()
async def hey(ctx):
    await ctx.send('Hello! How are you!')

@bot.command()
async def ping(ctx):
    await ctx.send(f'Latency Is {round(bot.latency * 1000)}ms')



@bot.command()
async def joined(ctx, *, member: discord.Member):
    await ctx.send(f'{member} joined on {member.joined_at}')

# member count
@bot.command(aliases=["mc"])
async def member_count(ctx):
    a=ctx.guild.member_count
    b=discord.Embed(title=f"members in {ctx.guild.name}",description=a,color=discord.Color((0xffff00)))
    await ctx.send(embed=b)

class MemberRoles(commands.MemberConverter):
    async def convert(self, ctx, argument):
        member = await super().convert(ctx, argument)
        return [role.name for role in member.roles[1:]] # Remove everyone role!
@bot.command()
async def roles(ctx, *, member: MemberRoles):
    """Tells you a member's roles."""
    await ctx.send('I see the following roles: ' + ', '.join(member))

bot.command(aliases=['dm'])
async def DM(ctx, user : discord.User, *, msg):
    try:
        await user.send(msg)
        await ctx.send(f':white_check_mark: Your Message has been sent')
    except:
        await ctx.send(':x: Member had their dm close, message not sent')


# @bot.command()
# @commands.has_permissions(manage_messages=True)
# async def say(ctx, *,msg):
#     embed=discord.Embed(
#         title="title",
#         description=msg,
#         color = discord.Color.red()
#     )
#     embed.set_author(name=ctx.author,icon_url=ctx.author.display_avatar.url)
#     embed.add_field(name = "field 1", value = 'field value',inline=True)
#     embed.add_field(name = "field 2", value = 'field value2',inline=True)
#     embed.add_field(name = "field 3", value = 'field value3',inline=False)
#     embed.set_footer(text = 'This is Footer')
#     embed.set_image(url = ctx.guild.icon_url)
#     embed.set_thumbnail(url = ctx.guild.icon_url)
#     await ctx.send(embed=embed)
@bot.command()
@commands.has_permissions(manage_messages=True)
async def say(ctx,*,message):
    embed = discord.Embed(color=discord.Color.random(),description=message)
    # embed.set_author(name=ctx.author)
    # embed.set_text("@here @everyone")
    # embed.set_thumbnail(url = 'https://cdn.discordapp.com/attachments/1001874634142126172/1011282329580339220/hp.jpeg')
    embed.set_footer(text = 'COURSES HUB',icon_url='https://cdn.discordapp.com/attachments/1001874634142126172/1011282329580339220/hp.jpeg')
    await ctx.message.delete()
    await ctx.send(embed=embed)

@say.error
async def say_error(ctx,error):
    async def say_error(ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Please Specify The Numbers Of Message To Delete')
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You Can't Use That Command")
    
# Purge Command
@bot.command()
@commands.has_permissions(manage_messages=True)
async def purge(ctx, amount: int):
    await ctx.channel.purge(limit=amount+1)

@purge.error
async def purge_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please Specify The Numbers Of Message To Delete')
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You Can't Use That Command")
    

# timer function
@bot.command()
async def timer(ctx, seconds):
    try:
        secondint = int(seconds)
        if secondint > 600:
            await ctx.send("I don't think i can go over 10 mins.")
            raise BaseException
        if secondint <= 0:
            await ctx.send("I DONT THINK I CAN GO NEGATIVES")
            raise BaseException
        message = await ctx.send(f"Timer: {seconds} ")
        while True:
            secondint -= 1
            if secondint==0:
                await message.edit(content="Ended")
                break

            await message.edit(content=f"Timer: {secondint}")
            await asyncio.sleep(1)
        await ctx.send(f"{ctx.author.mention}, your countdown has been ended!")
    except ValueError:
        await ctx.send('You Must Enter A Number')


# JOIN AND LEAVE CODE

# @bot.command()
# async def on_member_join(ctx, member):
#     # role = discord.utils.get(member.guild.roles, name='new role')
#     # role = discord.utils.get(bot.get_guild(ctx.guild.id).roles, id ="1011225355182415883")
#     # await member.add_roles(role)
#     channel = bot.get_channel(1010527413769355338)
#     embed = discord.Embed(description=f'Hi {member.metion}, Welcome to the guild', color=0x000000)
#     await ctx.member.add_roles(role)
#     await ctx.channel.send(embed=embed)

# @bot.command()
# async def on_member_remove(ctx, member):
#     channel = bot.get_channel(1010527413769355338)
#     embed = discord.Embed(description=f' {member.metion}, just le the guild', color=0x000000)
#     awaitchannel.send(embed=embed)


# FOR MAKING COGS 

# extensions=[
#             'cogs.moderation'

# ]
# if __name__ == "__main__":
#     for extension in extensions:
#         try:
#             bot.load_extension(extension)
#         except Exception as e:
#             print (f'Error loading {extension}', file=sys.stderr)
#             traceback.print_exc()





# keep_alive()
TOKEN="MTAxMDk4MTI3MTg1MTI0OTgyNQ.G_ywbS.RqSq0pFyKY3AzFUAGyqO1SvnMMnOmleskq3A_0"
bot.run(TOKEN)

