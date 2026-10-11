"""Capture application UI with synthetic input; no physical camera or model inference."""
from pathlib import Path
import sys, math
from types import SimpleNamespace as Point
from unittest.mock import patch, MagicMock
import cv2,numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
import app,desenho
out=ROOT/'docs/assets'
class Camera:
 def __init__(self,n):self.n=n;self.i=0;self.released=False
 def isOpened(self):return self.i<self.n
 def read(self):
  self.i+=1
  frame=np.full((480,640,3),(31,25,19),dtype=np.uint8)
  for x in range(0,640,40):cv2.line(frame,(x,0),(x,479),(45,38,30),1)
  for y in range(0,480,40):cv2.line(frame,(0,y),(639,y),(45,38,30),1)
  return True,frame
 def release(self):self.released=True
class Detector:
 def __init__(self,kind,alert=False):self.kind=kind;self.i=0;self.alert=alert
 def __enter__(self):return self
 def __exit__(self,*args):pass
 def detect_for_video(self,*args):
  self.i+=1
  if self.kind=='hand':
   p=[Point(x=.4,y=.7) for _ in range(21)];p[9]=Point(x=.4,y=.42)
   x=.2+self.i/75*.6;y=.53+.15*math.sin(self.i/10)
   p[4]=Point(x=x+.005,y=y);p[8]=Point(x=x,y=y)
   return Point(hand_landmarks=[p])
  p=[Point(x=.5,y=.5,visibility=1) for _ in range(33)]
  for i,x in [(7,.44),(8,.56)]:p[i]=Point(x=x,y=.38 if self.alert else .25,visibility=1)
  for i,x in [(11,.30),(12,.70)]:p[i]=Point(x=x,y=.50 if self.alert else .55,visibility=1)
  return Point(pose_landmarks=[p])
def capture(module,name,kind,n,alert=False):
 camera=Camera(n);detector=Detector(kind,alert);saved=[]
 factory=module.vision.HandLandmarker if kind=='hand' else module.vision.PoseLandmarker
 with patch.object(module,'open_camera',return_value=camera),patch.object(factory,'create_from_options',return_value=detector),patch.object(cv2,'imshow',side_effect=lambda title,frame:saved.append(frame.copy())),patch.object(cv2,'waitKey',return_value=-1),patch.object(cv2,'destroyAllWindows'),patch.object(sys,'argv',['capture','--mute'] if kind=='pose' else ['capture']):module.main()
 assert camera.released and len(saved)==n
 assert cv2.imwrite(str(out/name),saved[-1])
 print(name,'rendered from application with synthetic landmarks; camera released')
capture(desenho,'drawing-test.png','hand',75)
capture(app,'posture-test.png','pose',1)
capture(app,'posture-alert-test.png','pose',1,True)
(out/'project-mark.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400"><rect x="50" y="100" width="300" height="240" rx="45" fill="#152431" stroke="#74ceff" stroke-width="14"/><path d="M125 100l25-45h100l25 45" fill="none" stroke="#74ceff" stroke-width="14"/><circle cx="200" cy="215" r="75" fill="none" stroke="#74ceff" stroke-width="16"/><circle cx="200" cy="215" r="37" fill="#74ceff"/><circle cx="302" cy="142" r="12" fill="#eef6fc"/></svg>',encoding='utf-8')
