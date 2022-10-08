import asyncio
from email import message
from re import T
import asyncio
import discord
import requests
import datetime
import aiohttp
import time
from threading import Thread
import random
import asyncio
from discord import app_commands
from datetime import datetime
# import traceback
from discord.ext import commands
TOKEN = ("MTAxMDk4MTI3MTg1MTI0OTgyNQ.GK-kNC.aEVNVZQTMLQ1ykqpm51z4TdFFangdpoqXG2nNs")
owners = [538533547145822209,900421898108821564] 



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
@commands.guild_only()
async def hi(ctx):
    await ctx.reply('Hello!')
    
@bot.command()
@commands.guild_only()
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
        
@bot.event
@commands.guild_only()
async def on_member_join(member):


  
  channel = bot.get_channel(1001853493541351585)

  
  role = discord.utils.get(member.guild.roles, name="Member")
  await channel.send(f"Hey {member.mention}! :partying_face: **Welcome To {member.guild.name} For More Information Go To <#1004635808915005460>** **also check rules  <#1001854239603175514>**  ")

  #for sending the card
 

@bot.event
@commands.guild_only()
async def on_member_remove(member):

  channel = bot.get_channel(1016935229472124958)

  await channel.send(f"{member.name} Has Left The server, We are going to miss you :cry: ")

    
bot.launch_time = datetime.utcnow()
@bot.command()
@commands.guild_only()
async def uptime(ctx):
    delta_uptime = datetime.utcnow() - bot.launch_time
    hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    days, hours = divmod(hours, 24)
    embed = discord.Embed(colour=discord.Color.blue(),description=f"I've been online since `{days}d, {hours}h, {minutes}m, {seconds}s`")
    await ctx.reply(embed=embed,mention_author=False)

@bot.event
async def on_message_delete(message):
    embed = discord.Embed(title="{} deleted a message".format(message.author.name),description="", color=0xFF0000)
    embed.add_field(name=message.content, value="This is the message that he has deleted",inline=True)           
    channel = bot.get_channel(1013052975373095005)
    await channel.send(channel, embed=embed)


@bot.event
async def on_message_edit(message_before, message_after):
    embed = discord.Embed(title="{} edited a message".format(message_before.author.name),
                          description="", color=0xFF0000)
    embed.add_field(name=message_before.content, value="This is the message before any edit",
                    inline=False)
    embed.add_field(name=message_after.content, value="This is the message after the edit",
                    inline=False)
    channel = bot.get_channel(1016935229472124958)
    await channel.send(channel, embed=embed)

    
@bot.command() #Reminds user about the text that he wrote 
@commands.guild_only()
@commands.is_owner() 
async def remind(ctx, user_seconds, *, user_remind_text):
    #check what end does string have, to set time acordingly
        time_provided = user_seconds
        if user_seconds.endswith('h'): #some pajeet code right there
            user_seconds = user_seconds[:-1]
            user_seconds = int(user_seconds) * 60 * 60
        elif user_seconds.endswith('min'):
            user_seconds = user_seconds[:-3] 
            user_seconds = int(user_seconds) * 60
        elif user_seconds.endswith('s'):
            user_seconds = user_seconds[:-1]
        elif user_seconds.endswith('d'):
            user_seconds = user_seconds[:-1]
            user_seconds = int(user_seconds) * 60 * 60 * 24
        elif user_seconds.endswith('w'):
            user_seconds = user_seconds[:-1]
            user_seconds = int(user_seconds) * 60 * 60 * 24 * 7 
    #checks if it's positive, if all is good it will start the timer
        if int(user_seconds) > 0:
            print(f'{ctx.message.author.name} has used remind_me function, it will last for {user_seconds} seconds')
            await ctx.send(f'You will be reminded of *{user_remind_text}* in **{time_provided}**')
            await asyncio.sleep(int(user_seconds))
            await ctx.send(f'<@{ctx.message.author.id}> I remind you that: {user_remind_text}')
            print(f'{ctx.message.author.name} has been reminded of {user_remind_text}')
        elif user_seconds == 0: #checks if user seconds are equal to 0
            await ctx.send(f"<@{ctx.message.author.id}>, dont choose 0")
            print(f'{ctx.message.author.name} provided wrong information for the function remind_me')
        else:
            await ctx.send('Choose a postive integer')
            print(f'{ctx.message.author.name} provided wrong information for the function remind_me')

@bot.command(help="Shows Weather of any place")
# @cooldown(1,7, BucketType.user)
@commands.guild_only()
async def weather(ctx,*,place = None):
            if not place: 
                embed = discord.Embed(color=discord.Color.random(),description="Write a location to see their weather!")
                return await ctx.reply(embed = embed)    
            response = requests.get(f"https://apiv1.spapi.ga/fun/weather?place={place}")
            data = response.json()
            weather = discord.Embed(color=discord.Color.random())
            weather.set_thumbnail(url=f"{data['location']['imagerelativeurl']}")
            weather.add_field(name="Location",value=f"{data['location']['name']}",inline=False)
            weather.add_field(name="Temperature",value=f"{data['current']['temperature']}°{data['location']['degreetype']}",inline=False)
            weather.add_field(name="Sky Text",value=f"{data['current']['skytext']}",inline=False)
            weather.add_field(name="Observation Time",value=f"{data['current']['observationtime']}",inline=False)
            weather.add_field(name="Observation Point",value=f"{data['current']['observationpoint']}",inline=False)
            weather.add_field(name="Humidity",value=f"{data['current']['humidity']}",inline=False)
            weather.add_field(name="Wind Speed",value=f"{data['current']['windspeed']}",inline=False)
            weather.set_footer(text=f"Requested by {ctx.author}",icon_url=ctx.author.display_avatar.url)
            async with ctx.typing():
                await ctx.reply(embed=weather,mention_author=False)
  
@bot.command()
@commands.guild_only()
@commands.is_owner() 
async def joke(ctx):
        r = requests.get('https://sv443.net/jokeapi/v2/joke/Any')
        status = r.status_code
        print(f'{ctx.message.author.name} has requested a joke, status = {status}')
        joke_data = r.json()
        joke_type = joke_data["type"]
        if joke_type == 'twopart': #Basically this let's me know what kind of type of joke this is
            joke_setup, joke_delivery = joke_data["setup"], joke_data["delivery"]
            await ctx.send(joke_setup + '\n' + joke_delivery)
        else:
            await ctx.send(joke_data['joke'])

@bot.command()
@commands.guild_only()
@commands.is_owner() 
async def search(ctx, *, user_question):
        r = requests.get(f'https://api.duckduckgo.com/?q={user_question}&format=json')
        print(f'{ctx.message.author.name} has asked a question on duckduckgo about {user_question}, status = {r.status_code}')
        if r.status_code == 200:
            answer_data = r.json()
            try:
                if answer_data['AbstractText'] != '': #It prioritizes the text from wikipedia
                    answer_source = answer_data['AbstractSource']
                    answer_text = answer_data["AbstractText"]
                    await ctx.send(f'**Answer: **{answer_text}\n**Source: **{answer_source}')
                elif answer_data["Definition"] !='':
                    answer_text = answer_text["Definition"]
                    answer_source = answer_text["DefinitionSource"]
                    await ctx.send(f'**Answer: **{answer_text}\n**Source: **{answer_source}')
                elif answer_data["RelatedTopics"][0]["Text"] != '':
                    answer_text = answer_data["RelatedTopics"][0]["Text"]
                    await ctx.send(f'**Answer: **{answer_text}')
                if answer_data["Image"] != '':
                    url = answer_data["Image"]
                    async with aiohttp.ClientSession() as session:  
                        async with session.get(url) as resp:
                            if resp.status != 200:
                                return print(f'Could not download file...from {url}')
                            data = io.BytesIO(await resp.read())
                    await ctx.send(file=discord.File(data, 'reference.png'))
            except: #This is some shitty pajeet spagheti code, but I dont care at this point, it was suppost to be temp fix
                i = 0
                list_len = 0
                related_answer_main_text = []
                while True: #Till it's not IndexError it will keep searching for related stuff
                    try:
                        answer_related = answer_data["RelatedTopics"][0]["Topics"][i]['FirstURL']
                        related_url, related_word = answer_related.split('.com/')
                        related_url = related_url.title #only done this so that vscode would stop bitching
                        if '%' not in related_word:
                            related_word = related_word.replace('_', ' ')
                            related_word = related_word.replace('d/', '')
                            list_len += 1
                            related_answer_main_text.append(f'{list_len}. {related_word}')
                        i += 1
                    except IndexError:
                        break
                if related_answer_main_text != []:
                    related_answer_main_text.insert(0, f"I dont have information about {user_question}, but I do have information about:")
                    await ctx.send("\n".join(related_answer_main_text))
                else:
                    await ctx.send(f'I dont have information about {user_question}')    
        else: #If status code is not 200 it prints out this
            await ctx.send(f'Something went wrong....') 
            
@bot.command()
@commands.guild_only()
@commands.is_owner() 
async def quote(ctx):
        main_text = []
        host = 'https://quotes.rest/qod?category=inspire'
        api_key = "api_key" #You need to get your own api key, from that site
        headers = {'content-type': 'application/json',
            'X-TheySaidSo-Api-Secret': format(api_key)}
        response = requests.get(host, headers=headers)
        print(f'{ctx.message.author.name} has requested a quote, status = {response.status_code}')
        if response.status_code == 200:
            quotes=response.json()['contents']['quotes'][0]["quote"]
            main_text.append(quotes)
            author = response.json()['contents']['quotes'][0]["author"]
            main_text.append(f'**Author: **{author}')
            await ctx.send("\n".join(main_text))
        elif response.status_code == 429: 
            await ctx.send('Hourly quote limit has been reached')
        else:
            await ctx.send('Something went wrong.... ')          
            
            
            
            

@bot.command()
@commands.guild_only()
@commands.is_owner() 
async def info(ctx, *, user: discord.Member = None):
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
@commands.guild_only()
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
    
snipe_message_author = {}
snipe_message_content = {}
 
@bot.event
async def on_message_delete(message):
     snipe_message_author[message.channel.id] = message.author
     snipe_message_content[message.channel.id] = message.content
     await sleep(60)
     del snipe_message_author[message.channel.id]
     del snipe_message_content[message.channel.id]
 
@bot.command(name='snipe', help='Shows the last deleted message of the current channel')
@commands.has_permissions(manage_messages=True)
async def snipe(ctx):
    channel = ctx.channel 
    try:
        snipeEmbed = discord.Embed(title=f"Last deleted message in #{channel.name}", description =  snipe_message_content[channel.id])
        snipeEmbed.set_footer(text=f"Message sent by {snipe_message_author[channel.id]}")

        await ctx.send(embed = snipeEmbed)
    except:
        await ctx.send(f"There are no deleted messages in <#{channel.id}>")



@bot.command()
@commands.guild_only()
async def hey(ctx):
    await ctx.reply('Hello! How are you!')




@bot.command()
@commands.guild_only()
async def ping(ctx):
   embed = discord.Embed(title=f"🏓Pong! {round(ctx.bot.latency * 1000)}ms", colour=discord.Color.blue())
   await ctx.reply(embed=embed)

# member count


@bot.command(aliases=["mc"])
@commands.guild_only()
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
@commands.guild_only()
async def messages(ctx, channel: discord.TextChannel = None):
    channel = channel or ctx.channel
    count = 0
    async for _ in channel.history(limit=None):
        count += 1
    await ctx.reply("There were {} messages in {}".format(count, channel.mention))


@bot.command()
@commands.guild_only()
@commands.is_owner()
async def roles(ctx, *, member: MemberRoles):
    """Tells you a member's roles."""
    await ctx.reply('I see the following roles: ' + ', '.join(member))


    
@bot.command()
@commands.is_owner()
async def mega(ctx, *, message):
    embed = discord.Embed(title="MEGA LINK OF ALL CODING PLATFORM COURSES FOR 2 HR ",
                         color=discord.Color.blue(), description=message)
    embed.set_thumbnail(url = 'https://cdn.discordapp.com/attachments/1011618287328698508/1013358291037991002/unknown.png')
    embed.set_footer(text='Courses Hub',
                     icon_url='https://cdn.discordapp.com/attachments/1001874634142126172/1011282329580339220/hp.jpeg')
    await ctx.message.delete()
    await ctx.send(embed=embed)
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
@commands.guild_only()
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
    async def course_error(ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('Please Specify The Numbers Of Message To Delete')
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You Can't Use That Command")

@bot.command()
@commands.guild_only()
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
@commands.guild_only()
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
@commands.guild_only()
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
@commands.guild_only()
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
@commands.guild_only()
@commands.has_permissions(manage_messages=True)
async def timer(ctx, seconds):
    try:
        secondint = int(seconds)
        if secondint > 7200:
            await ctx.send("I don't think i can go over 2 hour")
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
@commands.guild_only()
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
@commands.guild_only()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'Banned BY = {member.name} for {reason}')

@bot.command()
@commands.guild_only()
@commands.has_permissions(manage_messages=True)
async def ns(ctx, *, message):
    embed = discord.Embed(color=discord.Color.random(), description=message)
    await ctx.message.delete()
    await ctx.send(embed=embed)
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
@commands.guild_only()
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
@commands.guild_only()
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
@commands.guild_only()
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
@commands.guild_only()
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
@commands.guild_only()
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
@commands.guild_only()
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
@commands.guild_only()
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
@commands.guild_only()
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
