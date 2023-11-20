import os
try:
    import asyncio, json, random
    from discord.ext import commands
    from modules.captcha_solver import solve
except:
    os.system('pip install -r requirements.txt')
    import asyncio, json, random
    from discord.ext import commands
    from modules.captcha_solver import solve
# Load configuration from 'config.json'
with open("config.json") as config_file:
    config = json.load(config_file)

# Initialize the bot
client = commands.Bot(command_prefix="!@#$%^&*())(*&^%$#@!")
client.config = config

# Set bot attributes from the configuration
client.token, client.channel = config["token"], config["channel"]
client.delay, client.timeout, client.auto_buy = config["delay"], config["timeout"], config["auto_buy"]
client.timer = random.uniform(config["timermin"], config["timermax"])

# Set captcha_solver if enabled in the configuration
if config["captcha_solver"] == "True":
    client.captcha_solver = solve

# Load cogs
async def load_cogs() -> None:
    await client.load_extension("cogs.startup")
    await client.load_extension("cogs.hunting")

# Run the bot
asyncio.run(load_cogs())
client.run(client.token)
