import requests
from PIL import Image
from io import BytesIO
from ultralytics import YOLO

model = YOLO("assets/Solver100k.pt")


def solve_captcha(url: str) -> str:
    resp = requests.get(url)
    if resp.status_code != 200:
        print("Encountered an error while downloading captcha image!!")
        exit()

    image_buffer = BytesIO(resp.content)
    image = Image.open(image_buffer)

    result = model.predict(
        image, imgsz=320, save=False, agnostic_nms=True, max_det=6, verbose=False
    )[0]

    classes, boxes = list(map(int, result.boxes.cls)), list(result.boxes.xyxy)
    detections = [(name, float(boxes[index][0])) for index, name in enumerate(classes)]
    detections.sort(key=lambda v: v[1])

    return "".join([str(detection[0]) for detection in detections])
