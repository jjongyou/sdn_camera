import pyrealsense2 as rs
import cv2
pipe = rs.pipeline()
profile = pipe.start()
try:
  for i in range(0, 100):
    frames = pipe.wait_for_frames()
    for f in frames:
      print(type(f))
      print(f.profile)
      cv2.imshow("cc", f)
finally:
    pipe.stop()
