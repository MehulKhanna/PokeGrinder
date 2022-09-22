# PokeGrinder
An Auto-Grinding Self-Bot for the Discord Bot PokéMeow. As efficient as can be.

## Supported Features
1. Hunting
- Encounters Pokemons and uses a ball depending on the rarity of the Pokemon.
- Stops if a captcha appears and automatically continues after the captcha is solved.
- Logs elapsed time, encounters and catches.

## Installating

### On your PC
1. Install Python 3.8 or higher.
2. Download this repo then unzip it.
3. Inside of the repo type the following command `python -m pip install -r requirements.txt`
4. Paste your Dicord Auth Token, User ID and the Channel ID you want to grind in inside `config.json`.
5. You may also edit the rarities section in `config.json` according to your convenience.

## Launching 
1. Run `main.py`.
2. Make sure to buy balls before launching.
3. The bot will take some time (depending on your hardware) to start. When it is ready it will do ;p in the channel you provided in `config.json` and then start grinding.

## Stoping
To stop the program simply close the command prompt.

## Disclamer ⚠️
- I am of course not responsible for any ban you recieve for using this bot.
- Please keep an eye on the bot to solve captchas. Do not be irresponsible if you don't want to get banned.
- Please do not grind in public servers.