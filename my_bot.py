from discord.ext import commands
from bot_result import BotResult
from bot_db import BotDb

"""Connect to Database"""
print('Connecting to Database..')
try:
    db_object = BotDb()
    TOKEN = db_object.fetch_token('search_bot')
except Exception as e:
    print(e)
    print('Some error in initializing database.')

bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

"""Google command implementation"""
@bot.command(name='google')
async def search_command(ctx):
    #get query from message
    search_command_query = ctx.message.content.split()
    if len(search_command_query) > 1:
        query = " ".join(ctx.message.content.split()[1:])
        #Get google search results for the query
        br = BotResult('google',ctx.message.author.name)
        result = "\n".join(br.execute_command(query,db_object))
    else:
        #If no query specified please tell the user to enter a query along with the command
        result = 'Please enter a search query!'
    await ctx.send(result)


"""Recent command implementation"""
@bot.command(name='recent')
async def recent_command(ctx):
    # get query from message
    search_command_query = ctx.message.content.split()
    if len(search_command_query) > 1:
        query = " ".join(ctx.message.content.split()[1:])
        # Get google search results for the query
        br = BotResult('recent', ctx.message.author.name)
        res = br.execute_command(query,db_object)
        if res:
            result = "\n".join(res)
        else:
            result = 'No Searches done for the keyword!'
    else:
        # If no query specified please tell the user to enter a query along with the command
        result = 'Please enter a recent query!'
    await ctx.send(result)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')

@bot.event
async def on_message(message):
    content = message.content.lower()
    if content.lower().strip() == 'hi':
        await message.channel.send(f'Hey {message.author.name}')
    message.content = message.content.lower()
    await bot.process_commands(message)

bot.run(TOKEN)
