import json
import asyncio
from time import time
from typing import List
from datetime import datetime

import discord
from discord.ext.commands import Bot

from cogs.fishing import Fishing
from modules.logging import log
from cogs.captcha import Captcha
from cogs.hunting import Hunting
from cogs.startup import Startup, Config

start_time = datetime.now()
discord.utils.setup_logging()
config = json.load(open("config.jsonc"))
bots: List[Bot] = []


async def logger():
    await asyncio.sleep(config["LoggingInterval"])
    log(bots, start_time)
    await asyncio.create_task(logger())


async def start_bots(token: str) -> None:
    if (
        token == ""
        or config[token]["HuntingChannel"] == 0
        and config[token]["FishingChannel"] == 0
    ):
        return

    bot = Bot(command_prefix=token)
    bot.config = Config(
        config[token]["HuntingChannel"],
        config[token]["FishingChannel"],
        config[token]["Balls"],
        config[token]["FishBalls"],
        config[token]["AutoBuy"],
        config[token]["RetryCooldown"],
        config[token]["HuntingCooldown"],
        config[token]["FishingCooldown"],
        config[token]["CaptchaRetries"],
        config["CaptchaSolver"],
    )

    (
        bot.encounters,
        bot.catches,
        bot.fish_encounters,
        bot.fish_catches,
        bot.coins_earned,
        bot.last_hunt,
        bot.last_fish,
    ) = (0, 0, 0, 0, 0, time(), time())

    bots.append(bot)
    await bot.add_cog(Startup(bot))

    if bot.config.fishing_channel_id != 0:
        await bot.add_cog(Fishing(bot))

    if bot.config.hunting_channel_id != 0:
        await bot.add_cog(Hunting(bot))

    if bot.config.captcha_solver:
        await bot.add_cog(Captcha(bot))

    await bot.start(token=token)


async def start() -> None:
    await asyncio.gather(
        *[start_bots(token) for token in list(config.keys())[2:]], logger()
    )


asyncio.run(start())
