import os
from typing import List
from rich.table import Table
from datetime import datetime
from rich.console import Console
from discord.ext.commands import Bot

console = Console()


def log(bots: List[Bot], start_time: datetime, clear_console: bool) -> None:
    elapsed_time = datetime.now() - start_time
    hours = elapsed_time.seconds // 3600
    minutes = (elapsed_time.seconds % 3600) // 60
    seconds = elapsed_time.seconds % 60

    table = Table(
        show_header=True,
        title=f"PokeGrinder ETA {hours} hours {minutes} minutes {seconds} seconds",
        header_style="bold green",
        title_style="bold red"
    )

    [
        table.add_column(
            name,
            style="bold blue"
        ) for name in ["Username", "Encounters", "Catches", "Fish Encounters", "Fish Catches", "Coins Earned"]
    ]

    total_encounters, total_catches, total_fish_encounters, total_fish_catches, total_coins_earned = 0, 0, 0, 0, 0

    for bot in bots:
        if not bot.is_ready():
            continue

        table.add_row(
            str(bot.user.name),
            str(bot.encounters),
            str(bot.catches),
            str(bot.fish_encounters),
            str(bot.fish_catches),
            str(bot.coins_earned)
        )

        total_encounters += bot.encounters
        total_catches += bot.catches
        total_fish_encounters += bot.fish_encounters
        total_fish_catches += bot.fish_catches
        total_coins_earned += bot.coins_earned

    table.add_section()

    table.add_row(
        "Total",
        str(total_encounters),
        str(total_catches),
        str(total_fish_encounters),
        str(total_fish_catches),
        str(total_coins_earned),
        style="bold red"
    )

    if clear_console:
        os.system("cls" if os.name == "nt" else "clear")

    console.print(r"""__________       __            ________      .__            .___            
\______   \____ |  | __ ____  /  _____/______|__| ____    __| _/___________ 
 |     ___/  _ \|  |/ // __ \/   \  __\_  __ \  |/    \  / __ |/ __ \_  __ \
 |    |  (  <_> )    <\  ___/\    \_\  \  | \/  |   |  \/ /_/ \  ___/|  | \/
 |____|   \____/|__|_ \\___  >\______  /__|  |__|___|  /\____ |\___  >__|   
                     \/    \/        \/              \/      \/    \/       """, style='bold blue')
    console.print(table)
