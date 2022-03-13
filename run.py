import os
from rich.traceback import install
from Wordle_Bot import create_bot


install(show_locals=True)
bot = create_bot()

if __name__ == "__main__":
    bot.run(os.environ["DISCORD_TOKEN"])
