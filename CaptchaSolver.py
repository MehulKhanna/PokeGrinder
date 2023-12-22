from typing import Dict

from fastapi import FastAPI
from ultralytics import YOLO


model = YOLO('Solver1850.pt')
app = FastAPI()


@app.get("/")
async def read_root():
    return {"Status": 200}


@app.get("/solve/{url:path}")
async def read_item(url: str) -> dict[str, str]:
    result = model.predict(
        url,
        imgsz=320,
        save=False,
        agnostic_nms=True
    )[0]

    classes, boxes = list(map(int, result.boxes.cls)), list(result.boxes.xyxy)
    detections = [(name, float(boxes[index][0])) for index, name in enumerate(classes)]
    detections.sort(key=lambda v: v[1])

    answer = "".join([str(detection[0]) for detection in detections])
    return {"answer": answer}
