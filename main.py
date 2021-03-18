import discord,os,json
from SQLite import DataBase
from discord.ext import commands
intents = discord.Intents.default()
intents.members = True
bot=commands.Bot(command_prefix=commands.when_mentioned_or('!'),intents=intents)
@bot.event
async def on_ready():
    print('Logged in as {0} ({0.id})'.format(bot.user))
if __name__=="__main__":
    bot.database=DataBase.DataBase()
    guildData=bot.database.getGuilds()
    for Data in guildData:
        if(Data[5]==0):
            bot.database.removeQueue(int(Data[0]))
    bot.musicopts=json.load(open('Music.json'))
    for extension in os.listdir('cogs'):
        if(extension.endswith('.py')):
            bot.load_extension('cogs.'+extension[:-3])
    with open('config.json') as f:
        bot.run(json.load(f)['token'])