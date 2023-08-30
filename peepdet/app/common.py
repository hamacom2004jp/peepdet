from insightface.app import FaceAnalysis
from pathlib import Path
import cv2
import glob
import numpy as np
import os
import traceback
import sys
import yaml
import win11toast


PGM_DIR = Path("peepdet")
APP_ID = 'peepdet'
ICON_FILE = PGM_DIR / 'start.ico'
FILE_SCHEMA = 'file:///'

def load_config():
    global FACE_ANA_NAME
    global FONT
    global FONT_SCALE
    global DETECT_THRESHOLD
    global DETECT_PEEP_TIME
    global CAPTURE_TIME
    with open(PGM_DIR / 'config.yaml') as f:
        config = yaml.safe_load(f)
        c = config['peepdet']['common']
        FACE_ANA_NAME = c['FACE_ANA_NAME']
        FONT = int(c['FONT'])
        FONT_SCALE = cv2.getFontScaleFromHeight(FONT, int(c['FONT_SCALE']))
        DETECT_THRESHOLD = int(c['DETECT_THRESHOLD'])
        DETECT_PEEP_TIME = int(c['DETECT_PEEP_TIME'])
        CAPTURE_TIME = int(c['CAPTURE_TIME'])

def create_fa():
    fa = FaceAnalysis(name=FACE_ANA_NAME, providers=['CPUExecutionProvider']) #'CUDAExecutionProvider'
    fa.prepare(ctx_id=0, det_size=(640, 640))
    return fa

def mkdirs(dir_path:Path):
    if not dir_path.exists():
        dir_path.mkdir(parents=True)
    if not dir_path.is_dir():
        raise BaseException(f"Don't make diredtory.({str(dir_path)})")
    return dir_path

def toast(title:str, message:str, image:str=None, buttons:list=None, on_click:str=print, logger=None):
    ret = win11toast.toast(title, message, icon=FILE_SCHEMA + str(ICON_FILE.resolve()),
                            image=image, buttons=buttons, on_click=on_click, app_id=APP_ID)
    if logger is not None:
        logger.info(f"toast : {title}, {message}, {ret}")
    return ret

def fa_frame(frame:np.array, file:Path, fa:FaceAnalysis):
    faces = fa.get(frame)
    rimg = np.copy(frame)
    for fi, face in enumerate(faces):
        face.bbox = face.bbox.astype(int)
        face.kps = face.kps.astype(int)
        rimg = cv2.rectangle(rimg, (face.bbox[0],face.bbox[1]), (face.bbox[2],face.bbox[3]), (0,255,0), 2)
        #print(f"{fi}:{face.det_score}:{(face.bbox[0],face.bbox[1])}")
        rimg = cv2.putText(rimg, f"{fi}:{face.det_score}", (face.bbox[0],face.bbox[1]), FONT, FONT_SCALE, (0,255,0))
    if file is not None:
        cv2.imwrite(str(file), rimg)
    return faces, rimg

def clean_face_embedding(conf_dir:Path):
    for p in glob.glob(str(conf_dir) + '/*.npy', recursive=True):
        if os.path.isfile(p):
            os.remove(p)

def save_face_embedding(frame:np.array, file:Path, logger):
    faces, rimg = fa_frame(frame, file, create_fa())
    for fi, face in enumerate(faces):
        efile = file.parent / f"face_{fi}.npy"
        logger.info(f"save_face_embedding : {efile}")
        np.save(efile, face.embedding)

def load_face_embedding(conf_dir:Path, logger):
    face_embedding = []
    for file in glob.glob(str(conf_dir) + '/*.npy', recursive=True):
        if os.path.isfile(file):
            logger.info(f"load_face_embedding : {file}")
            face_embedding.append(np.load(file))
    return face_embedding

def compare_face_embedding(store:list, faces:list):
    last_score = -1
    for i,face in enumerate(faces):
        for feat in store:
            score = _compute_sim(feat, face.embedding)
            #print(f"{score} < {th}")
            if score < DETECT_THRESHOLD:
                return True, i, score
            last_score = score
    return False, -1, last_score

# REF: https://github.com/deepinsight/insightface/blob/f474870cc5b124749d482cf175818413a9fe12cd/python-package/insightface/model_zoo/arcface_onnx.py#L70
def _compute_sim(feat1:np.array, feat2:np.array):
    return np.dot(feat1, feat2) / (np.linalg.norm(feat1) * np.linalg.norm(feat2))

def e_msg(e:Exception, logger):
    tb = sys.exc_info()[2]
    logger.debug(traceback.format_exc())
    return e.with_traceback(tb)

