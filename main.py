import discord
import pokebase as pb
from BuildTeam import create_lists
from discord.ext import commands

# Setup

intents = discord.Intents.default()
intents.members = True
TOKEN = 'OTcwMDU4NjQ4ODU4NTU4NTI0.Ym2bhA.rU-letHOGdmReRzJSEvv0wqGPEU'
bot = commands.Bot(command_prefix='.', intents=intents)

cogs = ['poke']


@bot.event
async def on_ready():  # On bot startup
    print('Bot has started up')
    channel = await bot.fetch_channel(970078329229176863)
    await channel.send("@everyone Bot is now running")
    await bot.change_presence(activity=discord.Game("Pokemon Enjoyer"))
    bot.lists = create_lists()


if __name__ == "__main__":
    for cog in cogs:
        bot.load_extension(cog)

bot.run(TOKEN)
