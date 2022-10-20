# PokeGrinder
An Auto-Grinding Self-Bot for the Discord Bot PokéMeow. As efficient as can be.

![PokeGrinder](assets/PokeGrinder.jpg)

## Supported Features
1. Hunting
- Encounters Pokemons and uses a ball depending on the rarity of the Pokemon.
- Stops if a captcha appears and automatically continues after the captcha is solved.
- Logs elapsed time, encounters and catches.

2. Captcha Solver
- Solves captchas automatically under 2-3 seconds (depending on your CPU).
- Has an accuracy of ~98.7% with 290 layers and 20,889,303 parameters.
- Free forever!

3. Auto Buy Balls
- Buys balls automatically when you run out of them!
- Amount of balls to buy can be specified in `config.json`.

## Upcoming Features
1. Fishing
2. Auto Battling
3. Auto Release Duplicates
4. Auto Checklist

## Installating

### With Executable (Windows only, easier install)
1. Download PokeGrinderExecutable.zip from https://github.com/MehulKhanna/PokeGrinder/releases and unzip it.
2. Paste your Discord Auth Token, User ID and the Channel ID you want to grind in inside `config.json`.
3. You may also edit the rarities section in `config.json` according to your convenience.

### Without Executable (Windows, Linux and Mac)
1. Install Python 3.8 or higher.
2. Download this repo then unzip it.
3. Download `CaptchaSolver.pt` from https://github.com/MehulKhanna/PokeGrinder/raw/master/assets/CaptchaSolver.pt and move it into the assets folder in the unzipped folder.
4. Install git from https://git-scm.com/downloads
5. Inside of the repository run command `python -m pip install -r requirements.txt`
6. Paste your Discord Auth Token, User ID and the Channel ID you want to grind in inside `config.json`.
7. You may also edit the rarities section in `config.json` according to your convenience.

### Install PyTorch for CaptchaSolver
#### On Windows
- Run `pip3 install torch torchvision torchaudio` command in terminal or powershell.
#### On Linux
- Run `pip3 install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cpu` in terminal.
#### On MacOS
- Run `pip3 install torch torchvision torchaudio` in terminal.

## Launching 
1. Run `main.py` or the `main.exe` file as Administrator (Executable installation).
2. Please buy at least 1 ball for each rarity specified in the config before starting.
3. The bot will take some time (depending on your hardware) to start. When it is ready it will do ;p in the channel you provided in `config.json` and then start grinding.

## Stopping
To stop the program simply close the command prompt or press ctrl+c in the command prompt.

## Disclaimer ⚠️
- I am of course not responsible for any ban you recieve for using this bot.
- Please keep an eye on the bot. Do not be irresponsible if you don't want to get banned.
- Please do not grind in public servers.
