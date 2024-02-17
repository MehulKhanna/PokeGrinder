import asyncio
from random import randint
from discord import Message
from discord.ext import commands

from cogs.startup import Config
from modules.captcha_solver import solve_captcha


class Captcha(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.config: Config = bot.config

    @commands.Cog.listener()
    async def on_message(self, message: Message) -> None:
        if not message.interaction or not message.embeds:
            return

        if (
            message.interaction.channel.id != self.config.hunting_channel_id
            and message.interaction.channel.id != self.config.fishing_channel_id
            or message.interaction.user.id != self.bot.user.id
        ):
            return

        if "captcha" not in message.embeds[0].description:
            return

        await asyncio.sleep(1 + randint(0, self.config.suspicion_avoidance) / 1000)
        await message.channel.send(
            solve_captcha(message.embeds[0].image.url)
        )

    @commands.Cog.listener()
    async def on_message_edit(self, _, after: Message) -> None:
        if not after.interaction:
            return

        if (
            after.interaction.channel.id != self.config.hunting_channel_id
            and after.interaction.channel.id != self.config.fishing_channel_id
            or after.interaction.user.id != self.bot.user.id
        ):
            return

        if "Thank you" in after.content:
            await asyncio.sleep(randint(0, self.config.suspicion_avoidance) / 1000)
            if after.channel.id == self.config.hunting_channel_id:
                await self.bot.hunting_channel_commands[after.interaction.name]()

            else:
                await self.bot.fishing_channel_commands[after.interaction.name]()

            return

        if not after.embeds:
            return

        if "captcha" not in after.embeds[0].description:
            return

        if int(after.embeds[0].description.split("**")[5]) < (
            5 - self.config.captcha_retries
        ):
            return

        await asyncio.sleep(1 + randint(0, self.config.suspicion_avoidance) / 1000)
        await after.channel.send(solve_captcha(after.embeds[0].image.url))
