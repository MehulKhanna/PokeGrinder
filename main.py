import json
import asyncio
from discord.ext import commands


config = open(r"config.json")
config = json.load(config)

client = commands.Bot(command_prefix="$")
client.config = config


async def load_cogs() -> None:
    await client.load_extension("cogs.startup")
    await client.load_extension("cogs.hunting")


asyncio.run(load_cogs())
client.token, client.channel = config["token"], config["channel"]
client.run(client.token)
