import asyncio
from email import message
from re import T
import asyncio
import discord
import datetime
import aiohttp
import time
from threading import Thread
import random
import asyncio
from discord import app_commands
# import traceback
from discord.ext import commands
TOKEN = ("MTAxMDk4MTI3MTg1MTI0OTgyNQ.G_ywbS.RqSq0pFyKY3AzFUAGyqO1SvnMMnOmleskq3A_0")
owners = [538533547145822209] 



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
    
@bot.command()
@commands.is_owner() 
async def av(ctx, *, avamember: discord.Member = None):
    if avamember == None:
        embed = discord.Embed(description='❌ Error! Please specify a user',
                                  color=discord.Color.red())
        await ctx.reply(embed=embed, mention_author=False)
    else:
        userAvatarUrl = avamember.avatar.url
        embed = discord.Embed(title=('{}\'s Avatar'.format(avamember.name)), colour=discord.Colour.red())
        embed.set_image(url='{}'.format(userAvatarUrl))
        embed.set_footer(
                text=f"Requested by {ctx.author}", icon_url=ctx.author.display_avatar.url)
        await ctx.reply(embed=embed, mention_author=False)
        
@bot.command()
@commands.is_owner() 
async def userinfo(ctx, *, user: discord.Member = None):
    if user is None:
        user = ctx.author      
    date_format = "%a, %d %b %Y %I:%M %p"
    embed = discord.Embed(color=0xdfa3ff, description=user.mention)
    embed.set_author(name=str(user), icon_url=user.avatar.url)
    embed.set_thumbnail(url=user.avatar.url)
    embed.add_field(name="Joined", value=user.joined_at.strftime(date_format))
    members = sorted(ctx.guild.members, key=lambda m: m.joined_at)
    embed.add_field(name="Join position", value=str(members.index(user)+1))
    embed.add_field(name="Registered", value=user.created_at.strftime(date_format))
    if len(user.roles) > 1:
        role_string = ' '.join([r.mention for r in user.roles][1:])
        embed.add_field(name="Roles [{}]".format(len(user.roles)-1), value=role_string, inline=False)
    perm_string = ', '.join([str(p[0]).replace("_", " ").title() for p in user.guild_permissions if p[1]])
    embed.add_field(name="Guild permissions", value=perm_string, inline=False)
    embed.set_footer(text='ID: ' + str(user.id))
    return await ctx.send(embed=embed)

@bot.command()
async def invites(ctx, user = None):
  if user == None:
    totalInvites = 0
    for i in await ctx.guild.invites():
        if i.inviter == ctx.author:
            totalInvites += i.uses
    await ctx.send(f"You've invited {totalInvites} member{'' if totalInvites == 1 else 's'} to the server!")
  else:
    totalInvites = 0
    for i in await ctx.guild.invites():
       member = ctx.message.guild.get_member_named(user)
       if i.inviter == member:
         totalInvites += i.uses
    await ctx.send(f"{member} has invited {totalInvites} member{'' if totalInvites == 1 else 's'} to the server!")
    
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
async def help(ctx):
    em = discord.Embed(title= "Help", description= "Use !help <command> for more information ",color=0x9208ea)
    
    em.set_thumbnail(url="https://cdn.discordapp.com/attachments/1011618287328698508/1012699108160581763/hj.jpeg") 
    em.add_field(name= "Moderation{6}", value= "Kick,Ban,Mute,Tempmute,Warn,purge",inline=False)
    em.add_field(name="Utility{4}", value= "avatar,userifo,Member-roles,MemberCount",inline=False)
    em.add_field(name= "Fun{1}", value="meme",inline=False)
    em.set_footer(text='Developed By Ayush',
                     icon_url='https://cdn.discordapp.com/attachments/1011618287328698508/1012358771516903554/th.jpg')   
    em.timestamp = datetime.datetime.now()         
    await ctx.reply(embed=em)
    

@bot.command()
async def owner(ctx,):
    await ctx.reply(f'My Owner Is Ayush')


@bot.command()
async def hey(ctx):
    await ctx.reply('Hello! How are you!')




@bot.command()
async def ping(ctx):
   embed = discord.Embed(title=f"🏓Pong! {round(ctx.bot.latency * 1000)}ms", colour=discord.Color.blue())
   await ctx.reply(embed=embed)

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
async def messages(ctx, channel: discord.TextChannel = None):
    channel = channel or ctx.channel
    count = 0
    async for _ in channel.history(limit=None):
        count += 1
    await ctx.reply("There were {} messages in {}".format(count, channel.mention))


@bot.command()
async def roles(ctx, *, member: MemberRoles):
    """Tells you a member's roles."""
    await ctx.reply('I see the following roles: ' + ', '.join(member))



@bot.command()
@commands.has_permissions(manage_messages=True)
async def course(ctx, *, message):
    embed = discord.Embed(title="Courses",
                         color=discord.Color.blue(), description=message)
    # embed.set_author(name=ctx.author)
    # embed.set_thumbnail(url = 'https://cdn.discordapp.com/attachments/1001874634142126172/1011282329580339220/hp.jpeg')
    embed.set_footer(text='Courses Hub',
                     icon_url='https://cdn.discordapp.com/attachments/1001874634142126172/1011282329580339220/hp.jpeg')
    await ctx.message.delete()
    await ctx.send(embed=embed)


@course.error
async def course_error(ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Please Specify The Numbers Of Message To Delete')
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You Can't Use That Command")

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


        
        
@bot.command()
@commands.is_owner()
async def warn_user(ctx, member: discord.Member, *, reason=None):

  try:
      mbed = discord.Embed(title='You Have Been Warned ',
                            color=discord.Color.red())
      mbed.add_field(name="Reason", value=reason, inline=True)
      await member.send(embed=mbed)
      await ctx.channel.send(member.mention + ' Has Been Warned!')
  except:
      await ctx.channel.send("Couldn't Dm The Given User")
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



@bot.command()
@commands.is_owner()
async def dm(ctx, user: discord.Member, *, args):

    if args != None:
        try:
            await user.send(args)
            await ctx.send(f'DM SENT TO = {user.name}')
        except:
            await ctx.send('User Has his dm closed')



@bot.command
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'Banned BY = {member.name} for {reason}')

@bot.command()
@commands.has_permissions(manage_messages=True)
async def ns(ctx, *, message):
    embed = discord.Embed(color=discord.Color.random(), description=message)
    await ctx.message.delete()
    await ctx.send(embed=embed)




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
  channel = bot.get_channel(1002063464828780624)
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
@bot.command()
@commands.has_permissions(manage_messages=True)
@commands.cooldown(1, 5, commands.BucketType.guild)
async def tempmute(self, ctx, member: discord.Member, time, d, reason=None):
    guild = ctx.guild
    role = discord.utils.get(guild.roles, name="Muted")

    for channel in guild.channels:
        await channel.set_permissions(role, speak=False, send_messages=False, read_message_history=True, read_messages=False)
        await member.add_roles(role)
        embed = discord.Embed(title="Muted!", description=f"{member.mention} has been muted", colour=discord.Colour.blue(
        ), timestamp=datetime.datetime.utcnow())
        embed.add_field(name="Reason:", value=reason, inline=False)
        embed.add_field(name="Time left for the mute:",
                            value=f"{time}{d}", inline=False)
        await ctx.reply(embed=embed)
        if d == "s":
            await asyncio.sleep(int(time))
        if d == "m":
           await asyncio.sleep(int(time*60))
        if d == "h":
           await asyncio.sleep(int(time*60*60))
        if d == "d":
            await asyncio.sleep(int(time*60*60*24))
            await member.remove_roles(role)
            embed = discord.Embed(title="Unmuted", description=f"Unmuted {member.mention} ", colour=discord.Colour.blue(
            ), timestamp=datetime.datetime.utcnow())
            await ctx.reply(embed=embed)

@bot.command()
@commands.has_permissions(manage_messages=True)
@commands.cooldown(1, 5, commands.BucketType.guild)
async def mute(ctx, member: discord.Member, *, reason=None):
    guild = ctx.guild
    mutedRole = discord.utils.get(guild.roles, name="Muted")

    if not mutedRole:
        mutedRole = await guild.create_role(name="Muted")

        for channel in guild.channels:
            await channel.set_permissions(mutedRole, speak=False, send_messages=False, read_message_history=True, read_messages=False)
            embed = discord.Embed(title="Muted", description=f"{member.mention} was muted ", colour=discord.Colour.blue(
            ), timestamp=datetime.datetime.utcnow())
            embed.add_field(name="Reason:", value=reason, inline=False)
            await ctx.reply(embed=embed)
            await member.add_roles(mutedRole, reason=reason)
            await member.send(f"You have been muted from: {guild.name} Reason: {reason}")

@bot.command()
@commands.cooldown(1, 5, commands.BucketType.guild)
@commands.has_permissions(manage_messages=True)
async def unmute(ctx, member: discord.Member):
    mutedRole = discord.utils.get(ctx.guild.roles, name="Muted")
    await member.remove_roles(mutedRole)
    await member.send(f"You have unmuted from: {ctx.guild.name}")
    embed = discord.Embed(title="Unmute", description=f"Unmuted {member.mention}", colour=discord.Colour.blue(
    ), timestamp=datetime.datetime.utcnow())
    await ctx.reply(embed=embed)
            
# @bot.command()
# @commands.command()
# @commands.has_permissions(kick_members=True)
# @commands.cooldown(1, 5, commands.BucketType.guild)
# async def kick(self, ctx, member: discord.Member, reason="No Reason"):
#     if member == None:
#         embed = discord.Embed(f"{ctx.message.author}, Please enter a valid user!")
#         await ctx.reply(embed=embed)

#     else:
#         guild = ctx.guild
#         embed = discord.Embed(title="Kicked!", description=f"{member.mention} has been kicked!!", colour=discord.Colour.blue(
#         ), timestamp=datetime.datetime.utcnow())
#         embed.add_field(name="Reason: ", value=reason, inline=False)
#         await ctx.reply(embed=embed)
#         await guild.kick(user=member)

@bot.command()
@commands.has_permissions(kick_members=True)
@commands.cooldown(1, 5, commands.BucketType.guild)
async def tempban(ctx, member: discord.Member, time, d, *, reason="No Reason"):
    if member == None:
        embed = discord.Embed( f"{ctx.message.author}, Please enter a valid user!")
        await ctx.reply(embed=embed)

    else:
        guild = ctx.guild
        embed = discord.Embed(title="Banned!", description=f"{member.mention} has been banned!", colour=discord.Colour.blue(
        ), timestamp=datetime.datetime.utcnow())
        embed.add_field(name="Reason: ", value=reason, inline=False)
        embed.add_field(name="Time left for the ban:", value=f"{time}{d}", inline=False)
        await ctx.reply(embed=embed)
        await guild.ban(user=member)
        if d == "s":
          await asyncio.sleep(int(time))
          await guild.unban(user=member)
        if d == "m":
            await asyncio.sleep(int(time*60))
            await guild.unban(user=member)
        if d == "h":
            await asyncio.sleep(int(time*60*60))
            await guild.unban(user=member)
            if d == "d":
                await asyncio.sleep(time*60*60*24)
                await guild.unban(int(user=member))   
                

@bot.command()
@commands.has_permissions(kick_members=True)
@commands.cooldown(1, 5, commands.BucketType.guild)
async def ban(ctx, member: discord.Member, reason="No Reason"):
    if member == None:
        embed = discord.Embed(
        f"{ctx.message.author}, Please enter a valid user!")
        await ctx.reply(embed=embed)
    else:
        guild = ctx.guild
        embed = discord.Embed(title="Banned!", description=f"{member.mention} has been banned!", colour=discord.Colour.blue(
        ), timestamp=datetime.datetime.utcnow())
        embed.add_field(name="Reason: ", value=reason, inline=False)
        await ctx.reply(embed=embed)
        await guild.ban(user=member)


@bot.command()
@commands.has_permissions(kick_members=True)
@commands.cooldown(1, 5, commands.BucketType.guild)
async def unban(ctx, user: discord.User):
    if user == None:
        embed = discord.Embed(
        f"{ctx.message.author}, Please enter a valid user!")
        await ctx.reply(embed=embed)

    else:
        guild = ctx.guild
        embed = discord.Embed(title="Unbanned!", description=f"{user.display_name} has been unbanned!", colour=discord.Colour.blue(
        ), timestamp=datetime.datetime.utcnow())
        await ctx.reply(embed=embed)
        await guild.unban(user=user)

    


import os
os.environ["JISHAKU_HIDE"] = "True"
os.environ["JISHAKU_NO_UNDERSCORE"] = "True"
os.environ["JISHAKU_NO_DM_TRACEBACK"] = "True"
os.environ["JISHAKU_FORCE_PAGINATOR"] = "True"
bot.run(TOKEN)
