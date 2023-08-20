from peepdet.app import common
from pathlib import Path
import cv2
import json


def get_camera(app_data_dir:Path):
    temp_dir = common.mkdirs(app_data_dir / 'temp')

    cameras = []
    for camera_id in range(0, 10):
        cap = cv2.VideoCapture(camera_id)
        ret, frame = cap.read()
        if ret:
            #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            file = temp_dir / f"cap_{camera_id}.jpg"
            cv2.imwrite(str(file), frame)
            cameras.append({'id':camera_id, 'file':file})

    return cameras

def load_camera(app_data_dir:Path):
    conf_dir = common.mkdirs(app_data_dir / 'config')
    file = conf_dir / 'camera.json'
    camera_json = []
    try:
        with open(file, "r", encoding="utf-8") as f:
            camera_json = json.load(f)
    except:
        pass

    return camera_json

def save_camera(app_data_dir:Path, settings:list):
    conf_dir = common.mkdirs(app_data_dir / 'config')
    file = conf_dir / 'camera.json'
    try:
        with open(file, "w", encoding="utf-8") as f:
            json.dump(settings, f, indent=4, ensure_ascii=False)
    except e:
        raise BaseException(f"Don't save camera setting.({str(file)})") from e
