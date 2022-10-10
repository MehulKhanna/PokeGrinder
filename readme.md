# PokeGrinder
An Auto-Grinding Self-Bot for the Discord Bot PokéMeow. As efficient as can be.

## Supported Features
1. Hunting
- Encounters Pokemons and uses a ball depending on the rarity of the Pokemon.
- Stops if a captcha appears and automatically continues after the captcha is solved.
- Logs elapsed time, encounters and catches.

2. Captcha Solver
- Solves captchas automatically under 2-3 seconds (depending on your CPU).
- Has an accuracy of ~98.7% with 290 layers and 20,889,303 parameters.
- Free forever!
### Disclaimer ⚠️
- Even with the high accuracy you should not be fully dependent on the Captcha Solver and keep an eye on the bot.
- I will not be reponsible for any captcha bans recieved even after using this Captcha Solver.

## Upcoming Features
1. Fishing
2. Auto Battling
3. Auto Buy Balls
4. Auto Release Duplicates
5. Auto Checklist

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
3. Download `CaptchaSolver.pt` from https://github.com/MehulKhanna/PokeGrinder/raw/master/assets/CaptchaSolver.pt and move it into the assets folder in the unzipped folder.
4. Install git from https://git-scm.com/downloads
5. Inside of the repository run command `python -m pip install -r requirements.txt`
6. Paste your Dicord Auth Token, User ID and the Channel ID you want to grind in inside `config.json`.
7. You may also edit the rarities section in `config.json` according to your convenience.

### Install PyTorch for CaptchaSolver
#### On Windows
- Run `pip3 install torch torchvision torchaudio` command in terminal or powershell.
#### On Linux
- Run `pip3 install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cpu` in terminal.
#### On MacOS
- Run `pip3 install torch torchvision torchaudio` in terminal.

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
