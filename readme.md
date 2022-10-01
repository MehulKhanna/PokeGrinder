# PokeGrinder
An Auto-Grinding Self-Bot for the Discord Bot PokéMeow. As efficient as can be.

## Supported Features
1. Hunting
- Encounters Pokemons and uses a ball depending on the rarity of the Pokemon.
- Stops if a captcha appears and automatically continues after the captcha is solved.
- Logs elapsed time, encounters and catches.

## Upcoming Features
1. Fishing
2. Captcha Solver (Free In-Built)
3. Auto Battling
4. Auto Buy Balls
5. Auto Release Duplicates
6. Auto Checklist

## Installating

### With Executable (Windows only, easier install)
1. Download PokeGrinderExecutable.zip from https://github.com/MehulKhanna/PokeGrinder/releases and unzip it.
2. Paste your Dicord Auth Token, User ID and the Channel ID you want to grind in inside `config.json`.
3. You may also edit the rarities section in `config.json` according to your convenience.

#### Disclaimer ⚠️
- Windows Defender may mark the executable as a virus.
- The executable is not a virus and the code will be exactly the same as the code in this repository.
- If Windows Defender tries to delete or block the executable from running please disable it temporarily or whitelist the executable.

### Without Executable (Windows, Linux and Mac)
1. Install Python 3.8 or higher.
2. Download this repo then unzip it.
3. Install git from https://git-scm.com/downloads
4. Inside of the repository run command `python -m pip install -r requirements.txt`
5. Paste your Dicord Auth Token, User ID and the Channel ID you want to grind in inside `config.json`.
6. You may also edit the rarities section in `config.json` according to your convenience.

## Launching 
1. Run `main.py` or the PokeGrinder.exe file as Administrator (Executable installation).
2. Make sure to have enough balls before starting the bot, you can purchase balls between ;p commands if you have none left.
3. The bot will take some time (depending on your hardware) to start. When it is ready it will do ;p in the channel you provided in `config.json` and then start grinding.

## Stopping
To stop the program simply close the command prompt.

## Disclaimer ⚠️
- I am of course not responsible for any ban you recieve for using this bot.
- Please keep an eye on the bot to solve captchas. Do not be irresponsible if you don't want to get banned.
- Please do not grind in public servers.
