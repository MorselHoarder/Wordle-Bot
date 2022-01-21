import discord
from Wordle_Bot.bot import WordleBot
from Wordle_Bot.commands import WordleCommands


def create_bot(
    command_prefix="w!",
    description="""Hi! I track statistics for the Wordle players in the server.""",
    intents=None,
    channel_names_list=["wordle", "general", "games"],
):
    if intents is None:
        intents = discord.Intents.default()
        intents.members = True
        intents.presences = True
        intents.guilds = True

    bot = WordleBot(
        command_prefix=command_prefix, description=description, intents=intents
    )
    bot.add_cog(WordleCommands(bot))
    bot.channel_names_list = channel_names_list
    return bot
