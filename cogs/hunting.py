import asyncio
from datetime import datetime
from discord.ext import commands
from discord import InvalidData, HTTPException

from discord import (
    Message,
    Interaction,
    InteractionType,
    Button,
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

colors = {
    "Common": "\033[1;34m",
    "Uncommon": "\033[1;36m",
    "Super Rare": "\033[1;33m",
    "Rare": "\033[1;31m",
    "Event": "\033[1;35m",
    "Full-odds": "\033[1;35m",
    "Shiny": "\033[1;35m",
    "Legendary": "\033[1;35m",
}

ball_strings = [
    "Pokeballs: 0",
    "Greatballs: 0",
    "Ultraballs: 0",
    "Masterballs: 0",
]


async def timer(command, timer) -> None:
    await asyncio.sleep(timer)
    await command()


class Hunting(commands.Cog):
    def __init__(self, client) -> None:
        self.client: commands.Bot = client
        self.catches, self.encounters = 0, 0
        self.timer, self.delay, self.timeout, self.auto_buy = (
            client.timer,
            client.delay,
            client.timeout,
            client.auto_buy,
        )
        self.auto_buy: dict

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
                timeout=self.timeout,
            )

        except asyncio.TimeoutError:
            asyncio.create_task(timer(self.client.pokemon, self.timer))
            return

        if "wait" in message.content:
            await asyncio.sleep(2)
            await self.client.pokemon()
            return

        if "remove" in message.embeds[0].description:
            print("\n\033[1;31m Reached daily catch limit!")
            print("\033[1;31m Stop Grinder...")
            self.client.close(0)

        elif "captcha" in message.embeds[0].description:
            print("\n\033[1;31m A captcha has appeared!!")
            if self.client.config["captcha_solver"] != "True":
                print(
                    "\033[1;33m Not solving the captcha as captcha solver is disabled!"
                )
                return
            print("\033[1;33m Solving the captcha...")

            image = message.embeds[0].image.url
            answer = self.client.captcha_solver(image)

            try:
                print('\033[1;33m PyTorch answer: ', answer)
                await self.client.get_channel(self.client.channel).send(answer)


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
            await asyncio.sleep(self.delay)
            await button.click()

        except InvalidData:
            pass

        try:
            before, after = await self.client.wait_for(
                "message_edit",
                check=lambda before, after: before == message,
                timeout=self.timeout,
            )
            after: Message

        except asyncio.TimeoutError:
            try:
                await button.click()

            except HTTPException:
                pass

            asyncio.create_task(timer(self.client.pokemon, self.timer))
            return

        asyncio.create_task(timer(self.client.pokemon, self.timer))
        if "caught" in after.embeds[0].description:
            self.catches += 1

        current_time = datetime.now().replace(microsecond=0)

        print(
            f"{list(colors.values())[index]} | \033[1;0m"
            f"Time Elapsed: {current_time - self.client.start_time} | "
            f"Encounters: {self.encounters} | "
            f"Catches: {self.catches}"
        )

        if self.client.config["auto-buy"] != "True":
            return

        index = [
            index
            for index, string in enumerate(ball_strings)
            if string in (after.embeds[0].footer.text).replace(" :", ":")
        ]

        if index == []:
            return

        index = index[0]
        string = list(self.auto_buy.keys())[index]
        amount = list(self.auto_buy.values())[index]

        await asyncio.sleep(4 + self.delay)
        await self.client.shop_buy(item=f"{index + 1}", amount=amount)

        print(f"\n\033[1m Bought {amount} {string}!\n")

    @commands.Cog.listener()
    async def on_message_edit(self, before, message: Message) -> None:
        if message.embeds != []:
            try:
                if "incorrect" in message.embeds[0].description:
                    print("\n\033[1;31m !!!WRONG ANSWER!!!")
                    print("\033[1;33m Retry...")
                    image = message.embeds[0].image.url
                    answer = self.client.captcha_solver(image)
                    try:
                        print('\033[1;33m Pytorch answer: ', answer)
                        await self.client.get_channel(self.client.channel).send(answer)
                        return
                    except:
                        return
            except:
                return
        if (message.channel.id != self.client.channel
            or message.author.id != 664508672713424926
            or "continue playing!" not in message.content):
            return
        print("\033[1;32m The captcha has been solved!\n")

        await asyncio.sleep(2)
        await self.client.pokemon()


async def setup(client: commands.Bot) -> None:
    await client.add_cog(Hunting(client))
