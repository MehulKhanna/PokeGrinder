# PokeGrinder V2

A robust and efficient discord self-bot for automating Pokémeow with a free captcha solver.

![image](/assets/image.png)

## Supported Features

1. Hunting

- Encounters Pokémon and uses a ball depending on the rarity of the Pokémon.
- Uses a ball of lower price if missing the specified ball in the config.

2. Fishing

- Spawns a fish, pulls the fishing rod and uses a ball depending on the rarity of the fish.
- Knows the rarity of each and every fish with the help of a json file.

3. Captcha Solver

- Automatically solves captcha with about 93% accuracy.
- Retries for the specified number of times in the config.
- About 0.0024% chance of getting banned with 3 retries.
- About 0.00016% chance of getting banned with 4 retries.

4. Auto Buy Balls

- Auto buys balls when none are left.
- Amount of balls to buy can be specified in the config.
- Works while both hunting and fishing.

5. Multiple Accounts

- Allows you to run as many accounts as you want.

6. Logging

- Logs encounters, catches as well as coins earned.
- Displays a table containing stats for all accounts with time elapsed.
- Frequency of logging can be changed in the config.

## Upcoming Features

1. Quests
2. Eggs

## Config

```
{
  "CaptchaSolver": true,
  // Automatically solve captcha true/false
  "LoggingInterval": 10,
  // Interval between updating log table in seconds
  "": {
    // Token between the double quotes
    "HuntingChannel": 0,
    // Hunting Channel ID, 0 to disable hunting
    "FishingChannel": 0,
    // Fishing Channel ID, 0 to disable fishing
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
    "RetryCooldown": 1,
    // Time to wait in seconds after "Please wait" messages
    "HuntingCooldown": 8.4,
    // Time between /pokemon commands
    "FishingCooldown": 22.4,
    // Time between /fish spawn commands
    "CaptchaRetries": 3
    // How may times to retry after one incorrect captcha
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

## Requirements

- Python 3.8 or higher is required.
- `python -m pip install -r requirements.txt`

## Launching

1. Clone the repository.
2. Download `Solver1850.pt` from releases and place it into the assets folder.
3. Run the `main.py` file from the terminal.

## Stopping

Press `CTRL+C` while in the terminal.

## Disclaimer ⚠️

- I am not responsible for any bans you get.
- Please always keep an eye on the bot.
- Please do not grind on public servers.


- Sometimes it will not use a ball (extremely rare). This is an issue with discord not registering button clicks
  sometimes. This can not be fixed until a workaround is found.