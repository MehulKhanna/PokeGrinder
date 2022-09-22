from datetime import datetime
from discord.ext import commands
from discord.channel import TextChannel


class Startup(commands.Cog):
    def __init__(self, client) -> None:
        self.client: commands.Bot = client

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        print("PokeGrinder is ready to grind!")
        print(f"Username: {self.client.user.name}" f"#{self.client.user.discriminator}")

        self.client.start_time = datetime.now().replace(microsecond=0)
        channel: TextChannel = self.client.get_channel(self.client.channel)

        commands = [
            commands
            async for commands in channel.slash_commands(
                command_ids=[1015311085441654824]
            )
        ]

        await commands[0]()
        self.client.pokemon = commands[0]


async def setup(client: commands.Bot) -> None:
    await client.add_cog(Startup(client))
