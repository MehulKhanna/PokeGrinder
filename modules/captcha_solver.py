import torch

model = torch.hub.load("ultralytics/yolov5", "custom", "assets/CaptchaSolver.pt")
model.max_det = 6
model.agnostic = True


def solve(image: str) -> str:
    answer = ""

    results = model(image, 640)
    results = results.pandas().xyxy[0].sort_values("xmin")["name"]

    for number in results:
        answer = answer + number

    return answer
