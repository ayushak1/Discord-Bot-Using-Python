import asyncio
from email import message
from re import T
import asyncio
import discord
import aiohttp
import time
from threading import Thread
import random
import asyncio
from discord import app_commands
# import traceback
from discord.ext import commands
TOKEN = ("MTAxMDk4MTI3MTg1MTI0OTgyNQ.G_ywbS.RqSq0pFyKY3AzFUAGyqO1SvnMMnOmleskq3A_0")
owners = [995000644660383764,538533547145822209] 



bot = commands.Bot(command_prefix='!', case_insensitive=True,intents=discord.Intents.all(),owner_ids=set(owners),help_command=None)

# with open("./config.json", 'r') as configjsonFile:
#         configData = json.load(configjsonFile)
#         TOKEN = configData["DISCORD_TOKEN"]




@bot.event
async def on_ready():
    await bot.load_extension("jishaku")
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{len(bot.users)} users"))
    print("I am Ready")


@bot.command()
async def hi(ctx):
    await ctx.reply('Hello!')

@bot.command(help="Show's funny random reddit memes")
@commands.guild_only()
async def meme(ctx):
    embed = discord.Embed(color=discord.Color.random())

    async with aiohttp.ClientSession() as cs:
        async with cs.get('https://www.reddit.com/r/dankmemes/new.json?sort=hot') as r:
            res = await r.json()
            embed.set_image(url=res['data']['children'] [random.randint(0, 25)]['data']['url'])
            embed.set_footer(text=f"Requested by {ctx.author}",icon_url=ctx.author.display_avatar.url)

            await ctx.reply(embed=embed,mention_author=False)    


@bot.command()
async def owner(ctx,):
    await ctx.reply(f'My Owner Is Ayush')


@bot.command()
async def hey(ctx):
    await ctx.reply('Hello! How are you!')


@bot.command()
async def ping(ctx):
    await ctx.reply(f'Latency Is {round(bot.latency * 1000)}ms')


@bot.command()
async def joined(ctx, *, member: discord.Member):
    await ctx.reply(f'{member} joined on {member.joined_at}')

# member count


@bot.command(aliases=["mc"])
async def member_count(ctx):
    a = ctx.guild.member_count
    b = discord.Embed(
        title=f" Total Members in {ctx.guild.name}", description=a, color=discord.Color.random())
    await ctx.send(embed=b)


class MemberRoles(commands.MemberConverter):
    async def convert(self, ctx, argument):
        member = await super().convert(ctx, argument)
        # Remove everyone role!
        return [role.name for role in member.roles[1:]]


@bot.command()
async def roles(ctx, *, member: MemberRoles):
    """Tells you a member's roles."""
    await ctx.reply('I see the following roles: ' + ', '.join(member))


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
async def job(ctx, *, message):
    embed = discord.Embed(title="JOB UPDATES",color=discord.Color.random(), description=message)
    # embed.set_author(name=ctx.author)
    # embed.set_thumbnail(url = 'https://cdn.discordapp.com/attachments/1001874634142126172/1011282329580339220/hp.jpeg')
    embed.set_footer(text='Courses Hub',
                     icon_url='https://cdn.discordapp.com/attachments/1001874634142126172/1011282329580339220/hp.jpeg')
    await ctx.message.delete()
    await ctx.send(embed=embed)


@job.error
async def job_error(ctx, error):
    async def say_error(ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Please Specify The Numbers Of Message To Delete')
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You Can't Use That Command")

@bot.command()
@commands.has_permissions(manage_messages=True)
async def say(ctx, *, message):
    embed = discord.Embed(color=discord.Color.random(), description=message)
    # embed.set_author(name=ctx.author)
    # embed.set_thumbnail(url = 'https://cdn.discordapp.com/attachments/1001874634142126172/1011282329580339220/hp.jpeg')
    embed.set_footer(text='Courses Hub',
                     icon_url='https://cdn.discordapp.com/attachments/1001874634142126172/1011282329580339220/hp.jpeg')
    await ctx.message.delete()
    await ctx.send(embed=embed)


@job.error
async def say_error(ctx, error):
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
@commands.has_permissions(manage_messages=True)
async def timer(ctx, seconds):
    try:
        secondint = int(seconds)
        if secondint > 600:
            await ctx.send("I don't think i can go over 10 mins.")
            raise BaseException
        if secondint <= 0:
            await ctx.send("I DONT THINK I CAN GO NEGATIVES")
            raise BaseException
        message = await ctx.reply(f"Timer: {seconds} ")
        while True:
            secondint -= 1
            if secondint == 0:
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
#     role = discord.utils.get(member.guild.roles, name='Member')
#     role = discord.utils.get(bot.get_guild(ctx.guild.id).roles, id ="1001856320217038868")
#     await member.add_roles(role)
#     channel = bot.get_channel(1001853493541351585)
#     embed = discord.Embed(description=f'Hi {member.metion}, Welcome to the guild', color=0x0085ff)
#     await ctx.member.add_roles(role)
#     await ctx.channel.send(embed=embed)

# @bot.command()
# async def on_member_remove(ctx, member):
#     channel = bot.get_channel(1001853493541351585)
#     embed = discord.Embed(description=f' {member.metion}, just le the guild', color=0x0085ff)
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

# DM COMMAND
@bot.command()
@commands.is_owner()
async def dm(ctx, user: discord.Member, *, args):

    if args != None:
        try:
            await user.send(args)
            await ctx.send(f'DM SENT TO = {user.name}')
        except:
            await ctx.send('User Has his dm closed')


# # BAN COMMAND
# @bot.command
# @commands.has_permissions(kick_members=True)
# async def kick(ctx, member: discord.Member,*,reason=None):
#     await member.kick(reason=reason)
#     await ctx.send(f'KICKED BY = {member.name} for {reason}')

# @kick.error
# async def kick_error(ctx, error):
#     if isinstance(error, commands.MissingRequiredArgument):
#         await ctx.send('Please Specify The Person To Kick')
#     if isinstance(error, commands.MissingPermissions):
#         await ctx.send("You Can't Use That Command")

@bot.command
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'Banned BY = {member.name} for {reason}')

# @ban.error
# async def ban_error(ctx, error):
#     if isinstance(error, commands.MissingRequiredArgument):
#         await ctx.send('Please Specify The Person To Ban')
#     if isinstance(error, commands.MissingPermissions):
#         await ctx.send("You Can't Use That Command")


# @bot.command
# async def unban(ctx, * , member):
#     banned_users = await ctx.guild.bans()
#     member_name, member_discriminator = member.split('#')

#     for ban_entry in banned_users:
#         user = ban_entry.user

#         if(user.name, user.discriminator) == (member_name, member_discriminator):
#             await ctx.guild.unban(user)
#             await ctx.send(f'{member.name} was unbaneed')

# @unban.error
# async def unban_error(ctx, error):
#     if isinstance(error,commands.MissingRequiredArgument):
#         await ctx.send('Please Mention user to unban')


# Setting `Watching ` status
# await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="a movie"))

@bot.command()
async def poll(ctx, question, option1=None, option2=None):
  if option1==None and option2==None:
    await ctx.channel.purge(limit=1)
    message = await ctx.send(f"```New poll: \n{question}```\n**✅ = Yes**\n**❎ = No**")
    await message.add_reaction('❎')
    await message.add_reaction('✅')
  elif option1==None:
    await ctx.channel.purge(limit=1)
    message = await ctx.send(f"```New poll: \n{question}```\n**✅ = {option1}**\n**❎ = No**")
    await message.add_reaction('❎')
    await message.add_reaction('✅')
  elif option2==None:
    await ctx.channel.purge(limit=1)
    message = await ctx.send(f"```New poll: \n{question}```\n**✅ = Yes**\n**❎ = {option2}**")
    await message.add_reaction('❎')
    await message.add_reaction('✅')
  else:
    await ctx.channel.purge(limit=1)
    message = await ctx.send(f"```New poll: \n{question}```\n**✅ = {option1}**\n**❎ = {option2}**")
    await message.add_reaction('❎')
    await message.add_reaction('✅')

@bot.command()
async def suggest(ctx, *, content: str):
  title, description= content.split('/')
  embed = discord.Embed(title=title, description=description, color=0x00ff40)
  channel = bot.get_channel(1004595078502813736)
  vote = await channel.send(embed=embed)
  await vote.add_reaction("✅")
  await vote.add_reaction("❌")
  await ctx.reply("your suggestion has been send")

# @bot.command()
# async def on_member_join(ctx, member):
#     role = discord.utils.get(member.guild.roles, name='Member')
#     role = discord.utils.get(bot.get_guild(ctx.guild.id).roles, id ="1001856320217038868")
#     await member.add_roles(role)
#     channel = bot.get_channel(1001853493541351585)
#     embed = discord.Embed(description=f'Hi {member.metion}, Welcome to the guild', color=0x4a3d9a)
#     embed.set_image(url="https://media1.tenor.com/images/8b07ee1e31fa6131f883ad0fce50189d/tenor.gif?itemid=15667320")
#     await ctx.member.add_roles(role)
    # await ctx.channel.send(embed=embed)

    


import os
os.environ["JISHAKU_HIDE"] = "True"
os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
os.environ["JISHAKU_NO_DM_TRACEBACK"] = "True"
os.environ["JISHAKU_FORCE_PAGINATOR"] = "True"
bot.run(TOKEN)
