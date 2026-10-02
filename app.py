"""Experimental posture reminder using ear and shoulder landmarks."""
import argparse
import math
import time
import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from common import model_path, open_camera

def posture_measure(points):
    """Normalized vertical distance; not a clinical posture score."""
    if any(p.visibility < 0.5 or not math.isfinite(p.y) for p in [points[i] for i in (7, 8, 11, 12)]):
        return None
    return (points[11].y + points[12].y - points[7].y - points[8].y) / 2

def main():
    parser = argparse.ArgumentParser(description='Lembrete experimental de postura / posture reminder')
    parser.add_argument('--camera', type=int, help='Indice da webcam')
    parser.add_argument('--limit', type=float, default=0.23, help='Limite personalizado (padrao: 0.23)')
    parser.add_argument('--mute', action='store_true', help='Desativar alerta sonoro')
    args = parser.parse_args()
    if not math.isfinite(args.limit) or not 0 < args.limit < 1:
        parser.error('--limit deve estar entre 0 e 1.')
    options = vision.PoseLandmarkerOptions(base_options=python.BaseOptions(model_asset_path=model_path('pose')), running_mode=vision.RunningMode.VIDEO)
    camera = None
    try:
        with vision.PoseLandmarker.create_from_options(options) as detector:
            camera = open_camera(args.camera)
            last_beep, timestamp = 0.0, 0
            while camera.isOpened():
                ok, frame = camera.read()
                if not ok:
                    print('A camera parou de fornecer imagens.')
                    break
                frame = cv2.flip(frame, 1)
                height, width = frame.shape[:2]
                image = mp.Image(image_format=mp.ImageFormat.SRGB, data=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                timestamp = max(timestamp + 1, int(time.monotonic() * 1000))
                result = detector.detect_for_video(image, timestamp)
                message, color = 'Posicione o corpo na camera', (220, 220, 220)
                if result.pose_landmarks:
                    points = result.pose_landmarks[0]
                    score = posture_measure(points)
                    if score is not None:
                        alert = score < args.limit
                        message = f'Distancia: {score:.2f} | Limite: {args.limit:.2f}'
                        color = (60, 60, 255) if alert else (80, 220, 80)
                        for i in (7, 8, 11, 12):
                            cv2.circle(frame, (int(points[i].x * width), int(points[i].y * height)), 5, color, -1)
                        if alert:
                            cv2.putText(frame, 'Confira sua postura', (20, height - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
                            if not args.mute and time.monotonic() - last_beep >= 2:
                                try:
                                    import winsound
                                    winsound.Beep(1000, 100)
                                except (ImportError, RuntimeError):
                                    pass
                                last_beep = time.monotonic()
                cv2.putText(frame, message, (15, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.65, color, 2)
                cv2.imshow('Monitor de Postura - Q para sair', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
    finally:
        if camera is not None:
            camera.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    try:
        main()
    except (RuntimeError, ValueError, OSError) as error:
        raise SystemExit(str(error)) from error
