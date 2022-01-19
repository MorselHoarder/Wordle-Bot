import discord
from discord.ext.commands import Bot

desc = """This bot tracks statistics for the Wordle players in the server."""

intents = discord.Intents.default()
intents.members = True

bot = Bot(command_prefix="w!", intents=intents, description=desc)
bot.score = []  # 0: user.id, 1: Wordle score by day
# TODO figure out if we want NumPy array or Pandas DataFrame
# Maybe use Tabulate to print the dataframe nicely


@bot.event
async def on_ready():
    print("Bot is ready!")
    # TODO figure out startup sequence for building array of scores


@bot.command()
async def score(ctx, *members: discord.Member):
    """
    Displays the score of the members passed in. If no members are passed in,
    the score of the current user is displayed.
    """
    if not members:
        members = (ctx.message.author,)
