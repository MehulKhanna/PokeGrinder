import json
import asyncio
from time import time
from random import randint

from discord import Message, InvalidData
from discord.ext import commands

from cogs.hunting import auto_buy
from cogs.startup import Config

fishes = json.load(open("fishes.json"))


class Fishing(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.config: Config = bot.config

    @commands.Cog.listener()
    async def on_message(self, message: Message) -> None:
        if not message.interaction:
            return

        if (
            message.interaction.name != "fish spawn"
            or message.interaction.user != self.bot.user
            or message.channel.id != self.config.fishing_channel_id
        ):
            return

        if "Please wait" not in message.content:
            return

        await asyncio.sleep(self.config.retry_cooldown)
        await asyncio.sleep(randint(0, self.config.suspicion_avoidance) / 1000)
        await self.bot.fishing_channel_commands["fish spawn"]()

    @commands.Cog.listener()
    async def on_message_edit(self, before: Message, after: Message) -> None:
        if not after.interaction or not after.embeds:
            return

        if (
            after.interaction.user != self.bot.user
            or after.interaction.name != "fish spawn"
            or after.channel.id != self.config.fishing_channel_id
        ):
            return

        if (
            "Not even a nibble" in after.embeds[0].description
            or "The Pokemon got away..." in after.embeds[0].description
        ):
            self.bot.last_fish = time()
            await asyncio.sleep(self.config.fishing_cooldown)
            await asyncio.sleep(randint(0, self.config.suspicion_avoidance) / 1000)
            await self.bot.fishing_channel_commands["fish spawn"]()
            return

        elif (
            "cast out a" in after.embeds[0].description
            and "click the" in after.embeds[0].description
        ):
            self.bot.last_fish = time()

            try:
                await after.components[0].children[0].click()

            except InvalidData:
                pass

            return

        elif "fished out a wild" in after.embeds[0].description:
            self.bot.fish_encounters += 1

            if "shiny" in after.embeds[0].description.lower():
                ball = self.config.fish_balls["Shiny"]

            elif "golden" in after.embeds[0].description.lower():
                ball = self.config.fish_balls["Golden"]

            else:
                rarity = fishes[after.embeds[0].description.split("**")[3]]
                ball = self.config.fish_balls[rarity]

            balls = ["mb", "db", "prb", "ub", "gb", "pb"]
            balls = balls[balls.index(ball) :]

            buttons = [
                button
                for button in after.components[0].children
                for ball in balls
                if button.custom_id == ball + "_fish"
            ]

            if not buttons:
                return

            await asyncio.sleep(randint(0, self.config.suspicion_avoidance) / 1000)
            await buttons[-1].click()
            return

        elif "fished out a wild" in before.embeds[0].description:
            if "caught" in after.embeds[0].description:
                self.bot.fish_catches += 1

            tasks = []

            if "Your next Quest is now ready!" in before.content:
                tasks.append(asyncio.create_task(
                    self.bot.fishing_channel_commands["quest info"]()
                ))

            tasks.append(asyncio.create_task(
                auto_buy(self.bot, self.config, self.bot.fishing_channel_commands, after)
            ))

            await asyncio.sleep(self.config.fishing_cooldown)
            await asyncio.sleep(randint(0, self.config.suspicion_avoidance) / 1000)
            await self.bot.fishing_channel_commands["fish spawn"]()
            [await task for task in tasks]
            return
