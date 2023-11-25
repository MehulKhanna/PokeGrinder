configname = "config.json"
from modules.title_changer import set_terminal_title
set_terminal_title("Loading stuff...")
import os
coolest_ascii_font = """
       __________       __            ________      .__            .___
       \______   \____ |  | __ ____  /  _____/______|__| ____    __| _/___________
        |     ___/  _ \|  |/ // __ \/   \  __\_  __ \  |/    \  / __ |/ __ \_  __ \ 
        |    |  (  <_> )    <\  ___/\    \_\  \  | \/  |   |  \/ /_/ \  ___/|  | \/
        |____|   \____/|__|_  \___  >\______  /__|  |__|___|  /\____ |\___  >__|
                            \/    \/        \/              \/      \/    \/
"""
print(coolest_ascii_font)
from modules.captcha_solver import solve
try:
    import asyncio, json, random
    from discord.ext import commands
except:
    os.system('pip install -r requirements.txt')
    import asyncio, json, random
    from discord.ext import commands

# Load configuration from 'config.json'
with open(configname) as config_file:
    config = json.load(config_file)

# Initialize the bot
client = commands.Bot()

# Set bot attributes from the configuration
client.config = config
client.token, client.channel, client.cap_channel = config["token"], config["channel"], config["cap_channel"]
client.delay, client.timeout, client.auto_buy = config["delay"], config["timeout"], config["auto_buy"]
client.timer = random.uniform(config["timermin"], config["timermax"])
client.title_set = set_terminal_title

if config["captcha_solver"] == "True":
    client.captcha_solver = solve
if config["save_captcha"] == "True":
    client.save_captcha_path = config["save_captcha_path"]

# Load cogs
async def load_cogs() -> None:
    await client.load_extension("cogs.startup")
    await client.load_extension("cogs.hunting")

# Run the bot
asyncio.run(load_cogs())
client.run(client.token)