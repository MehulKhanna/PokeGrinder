# Disclaimer ⚠️
Pokemeow has recently changed its captchas, so the captcha solver won't work until a new one is trained. Please disable the captcha solver before you run PokeGrinder.

# PokeGrinder V2 

A robust and efficient discord self-bot for automating Pokémeow with a free captcha solver.

<a target="_blank" href="https://colab.research.google.com/github/MehulKhanna/PokeGrinder/blob/master/assets/PokeGrinder.ipynb">
  <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>
</a>

![image](/assets/image.png)

The logs may look different for you depending on your terminal config ;).

## Supported Features

1. Hunting

- Encounters Pokémon and uses a ball depending on the rarity of the Pokémon.
- Use a ball of lower price if missing the specified ball in the config.

2. Fishing

- Spawns a fish, pulls the fishing rod and uses a ball depending on the rarity of the fish.
- Knows the rarity of each and every fish with the help of a json file.

3. Captcha Solver

- Automatically solves captcha with 96% accuracy.
- Retries for the specified number of times in the config.
- Special thanks to @Faust404 for training a captcha solver with 100k+ images.

4. Auto Buy Balls

- Auto buys balls when none are left.
- The Number of balls to buy can be specified in the config.
- Works while both hunting and fishing.

5. Multiple Accounts

- Allows you to run as many accounts as you want.

6. Logging

- Logs encounters, catches as well as coins earned.
- Displays a table containing stats for all accounts with time elapsed.

7. Quests
- Automatically sends `/quest info` when a new quest is ready.

8. Auto Release Duplicates
- Automatically sends `/release duplicates` after the bot has caught the specified number of duplicates in the config.
- Counts the number of duplicates caught based on "has been added to your Pokedex" messages.

## Upcoming Features

1. PokeGrinderV3 [PAID]

## Config

```jsonc
{
  "CaptchaRetries": 3,
  // How may times to retry after one incorrect captcha
  "ClearConsole": true,
  // Whether to clear console or not (set false to see errors)
  "CaptchaSolver": true,
  // Automatically solve captcha true/false
  "SuspicionAvoidance": 250,
  // Random delay (b/w 0 and the value) for responses in milliseconds
  "Cooldowns": {
    "RetryCooldown": 1,
    // Time to wait in seconds after "Please wait" messages
    "HuntingCooldown": 8.4,
    // Time between /pokemon commands
    "FishingCooldown": 22.4
    // Time between /fish spawn commands
  },
  "": {
    // Token between the double quotes
    "HuntingChannel": 0,
    // Hunting Channel ID, 0 to disable hunting
    "FishingChannel": 0,
    // Fishing Channel ID, 0 to disable fishing
    "ExceptionBalls": {
      "Crystal Onix": "mb",
      "Another pokemon name": "ball"
    },
    // Set which balls to send on specific pokemons
    "Balls": {
      // Which ball for which rarity (hunting)
      "Common": "pb",
      "Uncommon": "pb",
      "Rare": "gb",
      "Super Rare": "ub",
      "Legendary": "mb",
      "Shiny": "mb",
      "Shiny Event": "mb",
      "Shiny Full-odds": "prb"
    },
    "FishBalls": {
      // Which ball for which rarity (fishing)
      "Common": "pb",
      "Uncommon": "gb",
      "Rare": "ub",
      "Super Rare": "ub",
      "Legendary": "db",
      "Shiny": "mb",
      "Golden": "mb"
    },
    "AutoBuy": {
      // How many balls to buy when none left, set 0 to disable
      "pb": 50,
      "gb": 25,
      "ub": 5,
      "mb": 1
    },
    "AutoReleaseDuplicates": 100
    // Number of duplicates before auto releasing duplicates, set 0 to disable
  },
  // Add multiple accounts below :-
  "Second Token": {...}
}
```

- Use different channels for each account.
- Fishing and Hunting channels may not be in the same server.
- Grind in servers with Pokémeow only and no other bot.

## Get Token?

[How to Find Your Discord Token](https://youtu.be/YEgFvgg7ZPI?si=bHkK506fdRibR8QI)

### Run on Google Colab (no install required)
1. Click on the "Open in Colab" button at the top of this readme.
2. Follow through the steps on colab.

## Requirements
- [Install Git Here](https://git-scm.com/downloads)
- Python 3.8 or higher is required.
- `pip install git+https://github.com/dolfies/discord.py-self`
- `python -m pip install -r requirements.txt`

## Launching

1. Clone the repository.
2. Run the `main.py` file from the terminal.

## Stopping

Press `CTRL+C` while in the terminal.

## Disclaimer ⚠️

- I am not responsible for any bans you get.
- Please always keep an eye on the bot.
- Please do not grind on public servers.


- Sometimes it will not use a ball (extremely rare). This is an issue with discord not registering button clicks
  sometimes. This cannot be fixed until a workaround is found.
