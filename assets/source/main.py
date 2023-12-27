configname = "config.json"
import json
from modules.title_changer import set_terminal_title
set_terminal_title("Loading stuff...")
from modules.clear import clear_screen as clear
import os
font1 = """
       __________       __            ________       __             ___                  __   __ ___
       \______   \____ |  | __ ____  /  _____/______|__| ____    __| _/___________   ___ \ \ / /|_  )
        |     ___/  _ \|  |/ // __ \/   \  __\_  __ \  |/    \  / __ |/ __ \_  __ \ |___| \ V /  / /
        |    |  (  <_> )    <\  ___/\    \_\  \  | \/  |   |  \/ /_/ \  ___/|  | \/        \_/  /___|
        |____|   \____/|__|_  \___  >\______  /__|  |__|___|  /\____ |\___  >__|        (with python)
                            \/    \/        \/              \/      \/    \/
"""
print(font1)
with open(f"config/{configname}") as config_file:
    config = json.load(config_file)
    
if config["captcha_solver"] == "True":
    try:
        from ultralytics import YOLO
    except:
        os.system('pip install -U ultralytics')
    from ultralytics import YOLO
    if config["captcha_ver"] == "1":
        import urllib.request
        file_url = 'https://github.com/lufy20106/PokeGrinder-V2-python/releases/download/Captcha/CaptchaSolver.pt'
        custom_path = 'assets/'
        os.makedirs(custom_path, exist_ok=True)
        file_name = os.path.join(custom_path, 'CaptchaSolver.pt')
        if not os.path.exists(file_name):
            urllib.request.urlretrieve(file_url, file_name)
            print(f'{file_name} downloaded successfully')
        else:
            print(f'{file_name} already exists. Skipping download.')
        import torch
        model = torch.hub.load("ultralytics/yolov5", "custom", "assets/CaptchaSolver.pt")
        model.max_det = 6
        model.agnostic = True
        def solve(image: str) -> str:
            answer = ""
            results = model(image, 640)
            results = results.pandas().xyxy[0].sort_values("xmin")["name"]
            answer = "".join(results)
            return answer
    if config["captcha_ver"] == "2":
        import urllib.request
        file_url = 'https://github.com/lufy20106/PokeGrinder-V2-python/releases/download/Captcha/CaptchaSolver2.pt'
        custom_path = 'assets/'
        os.makedirs(custom_path, exist_ok=True)
        file_name = os.path.join(custom_path, 'CaptchaSolver2.pt')
        if not os.path.exists(file_name):
            urllib.request.urlretrieve(file_url, file_name)
            print(f'{file_name} downloaded successfully')
        else:
            print(f'{file_name} already exists. Skipping download.')
        model = YOLO("assets/CaptchaSolver2.pt")
        def solve(url):
            result = model.predict(url.split("?")[0], save=False, agnostic_nms=True, max_det=6)[0]
            classes, boxes = list(map(int, result.boxes.cls)), list(result.boxes.xyxy)
            detections = [(name, float(boxes[index][0])) for index, name in enumerate(classes)]
            detections.sort(key=lambda v: v[1])
            answer = "".join([str(detection[0]) for detection in detections])
            imagename = url.split("?")[0].split("/")[-1]
            os.remove(imagename)
            return answer    
    if config["captcha_ver"] == "3":
        import urllib.request
        file_url = 'https://github.com/lufy20106/PokeGrinder-V2-python/releases/download/Captcha/CaptchaSolver3.pt'
        custom_path = 'assets/'
        os.makedirs(custom_path, exist_ok=True)
        file_name = os.path.join(custom_path, 'CaptchaSolver3.pt')
        if not os.path.exists(file_name):
            urllib.request.urlretrieve(file_url, file_name)
            print(f'{file_name} downloaded successfully')
        else:
            print(f'{file_name} already exists. Skipping download.')
        from ultralytics import YOLO
        model = YOLO("assets/CaptchaSolver3.pt")
        def solve(url):
            result = model.predict(url.split("?")[0], imgsz=320, save=False, agnostic_nms=True, max_det=6)[0]
            classes, boxes = list(map(int, result.boxes.cls)), list(result.boxes.xyxy)
            detections = [(name, float(boxes[index][0])) for index, name in enumerate(classes)]
            detections.sort(key=lambda v: v[1])
            answer = "".join([str(detection[0]) for detection in detections])
            imagename = url.split("?")[0].split("/")[-1]
            os.remove(f"{imagename}")
            return answer

clear()
print(f"\u001b[33m{font1}")
try:
    import asyncio, json, random
    from discord.ext import commands
except:
    os.system('pip install -r requirements.txt')
    import asyncio, json, random
    from discord.ext import commands

# Initialize the bot
client = commands.Bot(command_prefix="696969696969696969")

# Set bot attributes from the configuration
client.config = config
client.token, client.channel= config["token"], config["channel"]
client.delay, client.timeout, client.auto_buy = config["delay"], config["timeout"], config["auto_buy"]
client.timer = random.uniform(config["timermin"], config["timermax"])
client.title_set = set_terminal_title

if config["captcha_solver"] == "True":
    client.captcha_solver = solve
if config["save_captcha"] == "True":
    client.save_captcha_path = config["save_captcha_path"]

# Load cogs
async def load_cogs() -> None:
    await client.load_extension("cogs.startup")
    await client.load_extension("cogs.hunting")

# Run the bot
asyncio.run(load_cogs())
client.run(client.token)