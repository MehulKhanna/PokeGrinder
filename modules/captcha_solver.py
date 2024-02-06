from os import remove
from ultralytics import YOLO

model = YOLO("assets/Solver1850.pt")


def solve_captcha(url: str) -> str:
    result = model.predict(
        url, imgsz=320, save=False, agnostic_nms=True, max_det=6, verbose=False
    )[0]

    remove(url.split("/")[-1])

    classes, boxes = list(map(int, result.boxes.cls)), list(result.boxes.xyxy)
    detections = [(name, float(boxes[index][0])) for index, name in enumerate(classes)]
    detections.sort(key=lambda v: v[1])

    return "".join([str(detection[0]) for detection in detections])
