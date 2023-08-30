from peepdet.app import common
from peepdet.app import setting
from pathlib import Path
from PIL import Image
import cv2
import shutil
import threading
import time


peep_th = None
peep_loop = False

def start(app_data_dir:Path, logger):
    camera_json = setting.load_camera(app_data_dir)
    camera_ids = []
    for c in camera_json:
        if c['enable']:
            camera_ids.append(c['id'])
    global peep_th, peep_loop
    if peep_th is not None and peep_th.is_alive():
        raise BaseException("Already running.")
    peep_loop = True
    peep_th = threading.Thread(target=process, args=(app_data_dir, camera_ids, logger), name="peepdet")
    peep_th.start()

def process(app_data_dir:Path, camera_ids:list, logger):
    temp_dir = common.mkdirs(app_data_dir / 'temp')
    peep_dir = common.mkdirs(app_data_dir / 'peep')

    caps = []
    for camera_id in camera_ids:
        cap = cv2.VideoCapture(camera_id)
        width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        fa = common.create_fa()
        caps.append({'id':camera_id, 'cap':cap, 'fa':fa})

    conf_dir = common.mkdirs(app_data_dir / 'config')
    store = common.load_face_embedding(conf_dir, logger)

    global peep_loop
    last_peep_tm = time.time()
    while peep_loop:
        for cap in caps:
            tm = time.time()
            file = temp_dir / f"frame_{cap['id']}.jpg"
            ret, frame = cap['cap'].read()
            if ret:
                faces, rimg = common.fa_frame(frame, file, cap['fa'])
                ret, idx, score = common.compare_face_embedding(store, faces)
                if ret and time.time()-last_peep_tm > common.DETECT_PEEP_TIME:
                    common.toast(f"Peepers detected.", f'Some peeps are peeking in. Click on Notifications to see previous records.',
                                 image=common.FILE_SCHEMA + str(file.resolve()),
                                 on_click=str(peep_dir),
                                 logger=logger)
                    peep_file = peep_dir / f"{time.strftime('%Y%m%d%H%M%S')}_{file.name}"
                    shutil.move(file, peep_file)
                    last_peep_tm = time.time()
                elif not ret:
                    last_peep_tm = time.time()
                logger.debug(f"{str(file)}\t{score}\t{time.time()-tm}")
            time.sleep(common.CAPTURE_TIME)

def stop(app_data_dir:Path):
    global peep_th, peep_loop
    peep_loop = False
    if peep_th is None or not peep_th.is_alive():
        raise BaseException("Not yet started.")
    pass

