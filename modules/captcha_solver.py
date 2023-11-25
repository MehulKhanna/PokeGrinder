import os
try:
    import torch
except:
    os.system('pip install -U ultralytics')
    import torch
# Load YOLOv5 model
model = torch.hub.load("ultralytics/yolov5", "custom", "assets/CaptchaSolver.pt")
model.max_det = 6
model.agnostic = True

def solve(image: str) -> str:
    answer = ""

    # Get predictions from the YOLOv5 model
    results = model(image, 640)
    results = results.pandas().xyxy[0].sort_values("xmin")["name"]

    # Concatenate the predicted numbers
    answer = "".join(results)

    return answer