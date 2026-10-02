"""Draw on the webcam canvas with a pinch gesture."""
import argparse
import math
import time
import cv2
import mediapipe as mp
import numpy as np
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from common import model_path, open_camera

def distance(a, b, width, height):
    return math.hypot((a.x - b.x) * width, (a.y - b.y) * height)

def main():
    parser = argparse.ArgumentParser(description='Desenho por gestos / gesture drawing')
    parser.add_argument('--camera', type=int, help='Indice da webcam')
    parser.add_argument('--mouse', action='store_true', help='Ativar controle opcional do mouse do sistema')
    args = parser.parse_args()
    mouse = None
    if args.mouse:
        try:
            import pyautogui as mouse
        except ImportError as error:
            raise RuntimeError('Instale requirements-mouse.txt para usar --mouse.') from error
        mouse.FAILSAFE = True
        screen_w, screen_h = mouse.size()
        mouse_x, mouse_y = mouse.position()
    options = vision.HandLandmarkerOptions(base_options=python.BaseOptions(model_asset_path=model_path('hand')), running_mode=vision.RunningMode.VIDEO, num_hands=1, min_hand_detection_confidence=0.7, min_tracking_confidence=0.7)
    camera = None
    try:
        with vision.HandLandmarker.create_from_options(options) as detector:
            camera = open_camera(args.camera)
            canvas, previous = None, None
            eraser, last_click, timestamp = False, 0.0, 0
            cursor = (0, 0)
            while camera.isOpened():
                ok, frame = camera.read()
                if not ok:
                    print('A camera parou de fornecer imagens.')
                    break
                frame = cv2.flip(frame, 1)
                height, width = frame.shape[:2]
                if canvas is None or canvas.shape != frame.shape:
                    canvas = np.zeros_like(frame)
                    previous, cursor = None, (width // 2, height // 2)
                button = (max(0, width // 2 - 110), 20, min(width, width // 2 + 110), 70)
                image = mp.Image(image_format=mp.ImageFormat.SRGB, data=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                timestamp = max(timestamp + 1, int(time.monotonic() * 1000))
                result = detector.detect_for_video(image, timestamp)
                if result.hand_landmarks:
                    p = result.hand_landmarks[0]
                    hand_size = distance(p[0], p[9], width, height)
                    pinch = hand_size > 0 and distance(p[4], p[8], width, height) < hand_size * 0.35
                    pointing = p[8].y < p[6].y and p[12].y > p[10].y and not pinch
                    closed = p[8].y > p[6].y and p[12].y > p[10].y
                    if pointing or pinch:
                        cursor = (int(np.clip(p[8].x * width, 0, width - 1)), int(np.clip(p[8].y * height, 0, height - 1)))
                    if pointing and mouse is not None:
                        tx = np.interp(p[8].x, (0.15, 0.85), (0, screen_w - 1))
                        ty = np.interp(p[8].y, (0.15, 0.85), (0, screen_h - 1))
                        mouse_x += (tx - mouse_x) / 5
                        mouse_y += (ty - mouse_y) / 5
                        mouse.moveTo(mouse_x, mouse_y)
                    if closed and time.monotonic() - last_click > 0.5:
                        if button[0] <= cursor[0] <= button[2] and button[1] <= cursor[1] <= button[3]:
                            eraser = not eraser
                        elif mouse is not None:
                            mouse.click()
                        last_click = time.monotonic()
                    if pinch:
                        if previous is not None:
                            cv2.line(canvas, previous, cursor, (0, 0, 0) if eraser else (255, 200, 0), 50 if eraser else 8, cv2.LINE_AA)
                        previous = cursor
                    else:
                        previous = None
                    cv2.circle(frame, cursor, 8, (255, 255, 255), -1)
                else:
                    previous = None
                mask = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY) > 10
                frame[mask] = canvas[mask]
                cv2.rectangle(frame, button[:2], button[2:], (40, 40, 40), -1)
                cv2.putText(frame, 'BORRACHA' if eraser else 'LAPIS', (button[0] + 35, 52), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
                cv2.imshow('Desenho - Q sair / C limpar / E trocar', frame)
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    break
                if key == ord('c'):
                    canvas.fill(0)
                    previous = None
                if key == ord('e'):
                    eraser = not eraser
                    previous = None
    finally:
        if camera is not None:
            camera.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    try:
        main()
    except (RuntimeError, ValueError, OSError) as error:
        raise SystemExit(str(error)) from error
