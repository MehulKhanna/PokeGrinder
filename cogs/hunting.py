import asyncio
from datetime import datetime
from discord.ext import commands
from discord import InvalidData, HTTPException

from discord import (
    Message,
    Interaction,
    InteractionType,
    Button,
    SelectMenu,
    SelectOption,
    ActionRow,
)

rarities = [
    "Common",
    "Uncommon",
    "Super Rare",
    "Rare",
    "Event",
    "Full-odds",
    "Shiny",
    "Legendary",
]


async def timer(command) -> None:
    await asyncio.sleep(8.3)
    await command()


class Hunting(commands.Cog):
    def __init__(self, client) -> None:
        self.client: commands.Bot = client
        self.catches, self.encounters = 0, 0

    @commands.Cog.listener()
    async def on_interaction(self, interaction: Interaction) -> None:
        if (
            interaction.type != InteractionType.application_command
            or interaction.name != "pokemon"
        ):
            return

        try:
            message: Message = await self.client.wait_for(
                "message",
                check=lambda message: interaction.channel.id == message.channel.id,
                timeout=2,
            )

        except asyncio.TimeoutError:
            asyncio.create_task(timer(self.client.pokemon))
            return

        if "wait" in message.content:
            await asyncio.sleep(2)
            await self.client.pokemon()
            return

        elif "answer the captcha below" in message.embeds[0].description:
            print("\033[1;31m A captcha has appeared!!")
            if self.client.config["captcha_solver"] != "True":
                print(
                    "\033[1;33m Not solving the captcha as captcha solver is disabled!"
                )
                return
            print("\033[1;33m Solving the captcha...")

            image = message.embeds[0].image.url

            dropdown: ActionRow = message.components[0]
            menu: SelectMenu = dropdown.children[0]
            options = menu.options

            option: SelectOption = [
                option
                for option in options
                if option.value == self.client.captcha_solver(image)
            ][0]

            try:
                await menu.choose(option)

            except InvalidData:
                pass

            return

        self.encounters += 1

        index = [
            index
            for index, rarity in enumerate(rarities)
            if rarity in message.embeds[0].footer.text
        ][0]

        ball = list((self.client.config["rarities"]).values())[index]

        button: Button = [
            component
            for component in message.components[0].children
            if component.custom_id == ball
        ][0]

        try:
            await button.click()

        except InvalidData:
            pass

        try:
            before, after = await self.client.wait_for(
                "message_edit",
                check=lambda before, after: before == message,
                timeout=2,
            )
            after: Message

        except asyncio.TimeoutError:
            try:
                await button.click()

            except HTTPException:
                pass

            asyncio.create_task(timer(self.client.pokemon))
            return

        asyncio.create_task(timer(self.client.pokemon))
        if "caught" in after.embeds[0].description:
            self.catches += 1

        current_time = datetime.now().replace(microsecond=0)

        print(
            "\033[1;0m"
            f"| Time Elapsed: {current_time - self.client.start_time} | "
            f"Encounters: {self.encounters} | "
            f"Catches: {self.catches}"
        )

    @commands.Cog.listener()
    async def on_message_edit(self, before, message: Message) -> None:
        if (
            message.channel.id != self.client.channel
            or message.author.id != 664508672713424926
            or "continue playing!" not in message.content
        ):
            return

        print("\033[1;32m The captcha has been solved!")

        await asyncio.sleep(2)
        await self.client.pokemon()


async def setup(client: commands.Bot) -> None:
    await client.add_cog(Hunting(client))
