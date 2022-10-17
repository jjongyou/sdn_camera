# Test 1 - Fail
#import pathlib
#filepath = sorted(pathlib.Path('.').glob('SocketCAN.cpp'))
#print(filepath)

# Test 2 - Fail 
#import glob
#filepath = glob.glob('/SocketCAN.cpp', recursive=True)
#print(filepath)

# Test 3 - Success, 모든 파일 전부다 다찾음
import os
def findfile(name, path):
  for dirpath, dirname, filename in os.walk(path):
    if name in filename:
      print(os.path.join(dirpath, name))
      # return os.path.join(dirpath, name)

# filepath = findfile("SocketCAN.cpp", "/")
# print(filepath)
findfile("SocketCAN.cpp", "/")
