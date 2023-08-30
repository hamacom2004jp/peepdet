from peepdet.app import common
from peepdet.app import peepdet
from peepdet.app import setting
from pathlib import Path
from pystray import Icon, Menu, MenuItem
from PIL import Image
import cv2
import logging
import logging.config
import shutil
import sys
import time
import traceback
import yaml


def quit_app(icon:Icon, item:MenuItem):
    try:
        peepdet.stop(app_data_dir)
        time.sleep(common.CAPTURE_TIME+1)
    except BaseException as e:
        pass
    icon.stop()
    try:
        sys.exit(0)
    except:
        pass

def start_app(icon:Icon, item:MenuItem):
    logger = logging.getLogger(common.APP_ID)
    try:
        peepdet.start(app_data_dir, logger)
        common.toast(f'Start peep detection.', f'The camera will not be available in other applications.', logger=logger)
    except BaseException as e:
        logger.error(f'An error has occurred.', f'Error: {common.e_msg(e, logger)}', exc_info=True)
        common.toast(f'An error has occurred.', f'Error: {common.e_msg(e, logger)}', logger=logger)

def stop_app(icon:Icon, item:MenuItem):
    logger = logging.getLogger(common.APP_ID)
    try:
        peepdet.stop(app_data_dir)
        common.toast(f'Stop peep detection.', f'The camera can now be used in other applications.', logger=logger)
    except BaseException as e:
        logger.error(f'An error has occurred.', f'Error: {common.e_msg(e, logger)}', exc_info=True)
        common.toast(f'An error has occurred.',f'Error: {common.e_msg(e, logger)}', logger=logger)

def select_app(icon:Icon, item:MenuItem):
    logger = logging.getLogger(common.APP_ID)
    if peepdet.peep_th is not None and peepdet.peep_th.is_alive():
        common.toast(f'An warning has occurred.', f'Stop the peek detection and then run it.', logger=logger)
        return
    cameras = setting.get_camera(app_data_dir)
    settings = setting.load_camera(app_data_dir)
    conf_dir = common.mkdirs(app_data_dir / 'config')
    common.clean_face_embedding(conf_dir)
    for c in cameras:
        ret = common.toast(f'Select your face image.', f"Camera No.{c['id']} choise ?",
                           image=common.FILE_SCHEMA + str(c["file"].resolve()),
                           buttons=['Use Face and Enable', 'Enable Only', 'Disable'],
                           logger=logger)

        find = None
        enable = False
        for i, s in enumerate(settings):
            if s['id'] == c['id']:
                find = i
        if find is not None:
            enable = s['enable']
            del settings[find]
        if 'arguments' in ret:
            enable = True if ret['arguments']=='http:Use Face and Enable' else enable
            enable = True if ret['arguments']=='http:Enable Only' else enable
            enable = False if ret['arguments']=='http:Disable' else enable
            settings.append({'id':c['id'],'enable':enable})
        
            if ret['arguments']=='http:Use Face and Enable':
                ifile = shutil.move(c["file"], conf_dir / f"frame_{c['id']}.jpg")
                frame = cv2.imread(str(ifile))
                common.save_face_embedding(frame, ifile, logger)
    setting.save_camera(app_data_dir, settings)

def folder_app(icon:Icon, item:MenuItem):
    logger = logging.getLogger(common.APP_ID)
    peep_dir = common.mkdirs(app_data_dir / 'peep')
    common.toast(f'Click hear.', f'Clicking on this notification opens the data folder.', on_click=str(peep_dir), logger=logger)

def make_tray(icon_path:Path, app_id:str):
    image = Image.open(icon_path)
    menu = Menu(MenuItem('Start', start_app),
                MenuItem('Stop', stop_app),
                MenuItem('Setting', Menu(MenuItem('Open Folder', folder_app),
                                         MenuItem('Select Face', select_app)
                                         )),
                MenuItem('Quit', quit_app)
                )
    icon = Icon(name='peepdet', icon=image, title=app_id, menu=menu)
    icon.run()

def main(data_dir:str):
    global app_data_dir, logger
    app_data_dir = Path(data_dir)
    common.load_config()
    logging.config.dictConfig(yaml.safe_load(open(common.PGM_DIR / "logconf.yml", encoding='UTF-8').read()))
    logger = logging.getLogger(common.APP_ID)
    logger.info("start application.")
    make_tray(common.ICON_FILE, common.APP_ID)
