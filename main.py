import json
import asyncio
from time import time
from typing import List
from datetime import datetime

import discord
from discord.ext.commands import Bot

from cogs.fishing import Fishing
from cogs.captcha import Captcha
from cogs.hunting import Hunting
from modules.logging import logger
from cogs.startup import Startup, Config

start_time = datetime.now()
discord.utils.setup_logging()
config = json.load(open("config.json"))
bots: List[Bot] = []


async def log_function():
    logger(bots, start_time, config["ClearConsole"])


async def start_bots(token: str) -> None:
    if (
        token == ""
        or config[token]["HuntingChannel"] == 0
        and config[token]["FishingChannel"] == 0
    ):
        return

    bot = Bot(command_prefix=token)
    bot.log = log_function
    bot.hunting_status = ""
    bot.fishing_status = ""
    bot.config = Config(
        config[token]["HuntingChannel"],
        config[token]["FishingChannel"],
        config[token]["ExceptionBalls"],
        config[token]["Balls"],
        config[token]["FishBalls"],
        config[token]["AutoBuy"],
        config[token]["AutoReleaseDuplicates"],
        config["Cooldowns"]["RetryCooldown"],
        config["Cooldowns"]["HuntingCooldown"],
        config["Cooldowns"]["FishingCooldown"],
        config["CaptchaRetries"],
        config["CaptchaSolver"],
        config["SuspicionAvoidance"],
    )

    (
        bot.encounters,
        bot.catches,
        bot.fish_encounters,
        bot.fish_catches,
        bot.coins_earned,
        bot.duplicates,
        bot.last_hunt,
        bot.last_fish,
        bot.auto_buy_queued,
        bot.limit,
    ) = (0, 0, 0, 0, 0, 0, time(), time(), False, False)

    bots.append(bot)
    await bot.add_cog(Startup(bot))

    if bot.config.fishing_channel_id != 0:
        bot.fishing_status = "Starting..."
        await bot.log()
        await bot.add_cog(Fishing(bot))
    else:
        bot.fishing_status = "Disabled"

    if bot.config.hunting_channel_id != 0:
        bot.hunting_status = "Starting..."
        await bot.log()
        await bot.add_cog(Hunting(bot))
    else:
        bot.hunting_status = "Disabled"

    if bot.config.captcha_solver:
        await bot.add_cog(Captcha(bot))

    await bot.start(token=token)


async def start() -> None:
    await asyncio.gather(*[start_bots(token) for token in list(config.keys())[5:]])


asyncio.run(start())
