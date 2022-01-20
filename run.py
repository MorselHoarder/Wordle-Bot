import os

from Wordle_Bot import create_bot

if __name__ == "__main__":
    bot = create_bot()
    bot.run(os.environ["DISCORD_TOKEN"])
