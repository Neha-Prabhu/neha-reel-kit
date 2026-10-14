"""Face track of the rough cut -> build/faces.json [(t, x0, y0, x1, y1)] every 0.2 s (1080x1920 coords).
Used by kinetic captions (CAPTIONS["faces"]) and to pick which side a pop goes on.
  python tools/face_track.py reels/<name>/build/roughcut.mp4 reels/<name>/build/faces.json
Needs OpenCV 4.x (has Haar cascades; 5.x dropped them):
  pip install --target /tmp/cv4 "opencv-python-headless==4.12.0.88" "numpy<2.3"  then run with PYTHONPATH=/tmp/cv4"""
import json, sys
import cv2
src, out = sys.argv[1:3]
cap = cv2.VideoCapture(src); casc = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
res, i = [], 0
while True:
    ok, fr = cap.read()
    if not ok: break
    if i % 6 == 0:
        g = cv2.cvtColor(cv2.resize(fr, (540, 960)), cv2.COLOR_BGR2GRAY)
        f = casc.detectMultiScale(g, 1.1, 5, minSize=(70, 70))
        if len(f):
            x, y, w, h = [int(v) for v in max(f, key=lambda r: r[2] * r[3])]
            res.append((round(i / 30, 1), x * 2, y * 2, (x + w) * 2, (y + h) * 2))
        else: res.append((round(i / 30, 1), None, None, None, None))
    i += 1
json.dump(res, open(out, "w")); print(len(res), "samples ->", out)
