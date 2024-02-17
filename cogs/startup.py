import asyncio
from time import time
from typing import Tuple
from dataclasses import dataclass

from discord.ext import commands, tasks
from discord import SlashCommand, UserCommand, MessageCommand, SubCommand, TextChannel


@dataclass
class Config:
    hunting_channel_id: int
    fishing_channel_id: int
    balls: dict[str, str]
    fish_balls: dict[str, str]
    auto_buy: dict[str, int]
    retry_cooldown: float
    hunting_cooldown: float
    fishing_cooldown: float
    captcha_retries: int
    captcha_solver: bool
    suspicion_avoidance: int


async def get_commands(bot: commands.Bot, channel_id: int) -> (
    Tuple[
        TextChannel,
        dict[str, SlashCommand | UserCommand | MessageCommand | SubCommand],
    ]
    | Tuple[None, None]
):
    if channel_id == 0:
        return None, None

    channel = bot.get_channel(channel_id)
    commands: dict[str, SlashCommand | UserCommand | MessageCommand | SubCommand] = {
        command.name: command
        for command in await channel.application_commands()
        if command.application_id == 664508672713424926
    }

    for command in list(commands.values()):
        for sub_command in command.children:
            commands[f"{command.name} {sub_command.name}"] = sub_command

    return channel, commands


class Startup(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.config: Config = bot.config

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        print(f"Started grinding as {self.bot.user.name}!")
        self.bot.hunting_channel, self.bot.hunting_channel_commands = (
            await get_commands(self.bot, self.config.hunting_channel_id)
        )

        self.bot.fishing_channel, self.bot.fishing_channel_commands = (
            await get_commands(self.bot, self.config.fishing_channel_id)
        )

        if self.bot.hunting_channel_commands:
            await self.bot.hunting_channel_commands["pokemon"]()
            self.hunting_check.start()

        if self.bot.fishing_channel_commands:
            await self.bot.fishing_channel_commands["fish spawn"]()
            self.fishing_check.start()

    @tasks.loop(seconds=30)
    async def hunting_check(self) -> None:
        if time() - self.bot.last_hunt < 30:
            return

        await self.bot.hunting_channel_commands["pokemon"]()

    @tasks.loop(seconds=60)
    async def fishing_check(self) -> None:
        if time() - self.bot.last_fish < 60:
            return

        await self.bot.fishing_channel_commands["fish spawn"]()
