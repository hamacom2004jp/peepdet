from peepdet.app import common
from peepdet.app import peepdet
from peepdet.app import setting
from pathlib import Path
from pystray import Icon, Menu, MenuItem
from PIL import Image
import cv2
import shutil
import sys
import time
import traceback
import win11toast


def quit_app(icon:Icon, item:MenuItem):
    try:
        peepdet.stop(app_data_dir)
        time.sleep(1)
    except BaseException as e:
        pass
    icon.stop()
    try:
        sys.exit(0)
    except:
        pass

def start_app(icon:Icon, item:MenuItem):
    try:
        peepdet.start(app_data_dir)
        common.toast('Start peep detection.')
    except BaseException as e:
        common.toast(f'Error: {common.e_msg(e)}')

def stop_app(icon:Icon, item:MenuItem):
    try:
        peepdet.stop(app_data_dir)
        common.toast('Stop peep detection.')
    except BaseException as e:
        common.toast(f'Error: {common.e_msg(e)}')

def setting_app(icon:Icon, item:MenuItem):
    if peepdet.peep_th is not None and peepdet.peep_th.is_alive():
        common.toast('Stop the peek detection and then run it.')
        return
    cameras = setting.get_camera(app_data_dir)
    settings = setting.load_camera(app_data_dir)
    conf_dir = common.mkdirs(app_data_dir / 'config')
    common.clean_face_embedding(conf_dir)
    for c in cameras:
        ret = win11toast.toast(common.TITLE, f"Camera No.{c['id']} choise ?",
              image=common.FILE_SCHEMA + str(c["file"].resolve()),
              buttons=['Use Face and Enable', 'Enable Only', 'Disable'])

        find = None
        enable = False
        for i, s in enumerate(settings):
            if s['id'] == c['id']:
                find = i
        if find is not None:
            enable = s['enable']
            del settings[find]
        enable = True if ret['arguments']=='http:Use Face and Enable' else enable
        enable = True if ret['arguments']=='http:Enable Only' else enable
        enable = False if ret['arguments']=='http:Disable' else enable
        settings.append({'id':c['id'],'enable':enable})
        
        if ret['arguments']=='http:Use Face and Enable':
            ifile = shutil.move(c["file"], conf_dir / f"frame_{c['id']}.jpg")
            frame = cv2.imread(str(ifile))
            common.save_face_embedding(frame, ifile)
    setting.save_camera(app_data_dir, settings)

def make_tray(icon_path:Path, title:str):
    image = Image.open(icon_path)
    menu = Menu(MenuItem('Start', start_app), MenuItem('Stop', stop_app), MenuItem('Setting', setting_app), MenuItem('Quit', quit_app))
    icon = Icon(name='peepdet', icon=image, title=title, menu=menu)
    icon.run()

def main(data_dir:str):
    global app_data_dir
    app_data_dir = Path(data_dir)
    make_tray(common.ICON_FILE, common.TITLE)
