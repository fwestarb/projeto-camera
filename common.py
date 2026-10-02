"""Shared camera and model setup."""
import os
from pathlib import Path
import sys
import urllib.request
import shutil
import cv2

ROOT = Path(__file__).resolve().parent
MODELS = {
    'hand': ('hand_landmarker.task', 'https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/latest/hand_landmarker.task'),
    'pose': ('pose_landmarker_full.task', 'https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker_full/float16/latest/pose_landmarker_full.task'),
}

def model_path(kind):
    name, url = MODELS[kind]
    path = ROOT / name
    if not path.exists():
        print(f'Baixando modelo MediaPipe: {name}')
        temporary = path.with_suffix('.part')
        try:
            with urllib.request.urlopen(url, timeout=60) as response, temporary.open('wb') as target:
                shutil.copyfileobj(response, target)
            temporary.replace(path)
        finally:
            temporary.unlink(missing_ok=True)
    return str(path)

def open_camera(index=None):
    configured = os.getenv('CAMERA_INDEX')
    if index is None and configured is not None:
        try:
            index = int(configured)
        except ValueError as error:
            raise ValueError('CAMERA_INDEX deve ser um inteiro >= 0.') from error
    if index is not None and index < 0:
        raise ValueError('O indice da camera deve ser >= 0.')
    for candidate in range(5) if index is None else [index]:
        camera = (cv2.VideoCapture(candidate, cv2.CAP_DSHOW) if sys.platform == 'win32' else cv2.VideoCapture(candidate))
        if camera.isOpened():
            ok, _ = camera.read()
            if ok:
                print(f'Camera: {candidate}')
                return camera
        camera.release()
    raise RuntimeError('Nenhuma camera disponivel. Confira permissoes, indice e outros aplicativos usando a webcam.')
