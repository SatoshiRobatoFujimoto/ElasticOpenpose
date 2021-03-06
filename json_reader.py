import os
import sys
import glob
import math
import json
import pickle

POSE_COCO_BODY_PARTS =  {
  0 : "Nose",
  1 : "Neck",
  2 : "RShoulder",
  3 : "RElbow",
  4 : "RWrist",
  5 : "LShoulder",
  6 : "LElbow",
  7 : "LWrist",
  8 : "RHip",
  9 : "RKnee",
  10: "RAnkle",
  11: "LHip",
  12: "LKnee",
  13: "LAnkle",
  14: "REye",
  15: "LEye",
  16: "REar",
  17: "LEar",
  18: "Bkg"
}


def step1():
  n_d = {}

  """ reocer data from json """
  for name in sorted(glob.glob("../openpose/json/*.json")):
    o   = json.loads(open(name).read())
    mvs = o["people"] 
    for e, mv in enumerate(mvs):
      """ please insert merge algorithm """
      if n_d.get(e) is None:
        n_d[e] = []
      ps = mv["body_parts"]
      # print( ps )
      shot = {}
      for i in range(19):
        print(i,POSE_COCO_BODY_PARTS[i], ps[3*i:3*i+3] )
        shot[ POSE_COCO_BODY_PARTS[i] ] = ps[3*i:3*i+3]
      n_d[e].append( shot )

      
      print( shot )
  open("n_d.pkl", "wb").write( pickle.dumps(n_d) )

""" MMDのVMDをCSV化したものを、フレームごとのデータにす　"""
def step2():
  part_index = {}
  for name in glob.glob("*.utf8"):
    with open(name, "r") as f:
      next(f) 
      for line in f:
        line = line.strip()
        parts = line.split(",").pop(0)
        if part_index.get(parts) is None:
          part_index[parts] = len(part_index)
        ... #print(parts)
  open("part_index.pkl", "wb").write( pickle.dumps(part_index) ) 

  for name in glob.glob("*.utf8"):
    frame_part_param = {}
    with open(name, "r") as f:
      next(f) 
      for line in f:
        line = line.strip()
        es   = line.split(",")
        frame = es.pop(1)
        part  = part_index[es.pop(0)]

        if frame_part_param.get(frame) is None:
          frame_part_param[frame] = {}
        if frame_part_param[frame].get(part) is None:
          frame_part_param[frame][part] = es
        print(es)
    open("frame_part_param_{name}.pkl".format(name=name), "wb").write( pickle.dumps(frame_part_param) )
    print(name)

""" フレームの補完します """
def step3():
  for name in glob.glob("frame_part_param_*.pkl"):
    print(name)
    frame_part_param      = pickle.loads(open(name, "rb").read())
    fill_frame_part_param = {
    } 
    buffered              = None
    for i in range(0, 3000):
      i = "%d"%i
      if frame_part_param.get(i) is None: 
        fill_frame_part_param[i] = buffered
      else:
        buffered = frame_part_param[i]
        fill_frame_part_param[i] = frame_part_param[i]
    open("fill_%s"%name, "wb").write(pickle.dumps(fill_frame_part_param))

""" パーツの補完をする """
def step4():
  
  part_index = pickle.loads( open("part_index.pkl", "rb").read() )
  index_part = { index:part for part, index in part_index.items() }
  
  for name in glob.glob("fill_frame_part_param_*.csv.utf8.pkl"):
    frame_param_param = {}
    fill_frame_part_param = pickle.loads( open(name, "rb").read() )
    for index, part in index_part.items():
      print(index, part)
      buffer = None
      for frame, part_param in sorted( fill_frame_part_param.items(), key=lambda x:int(x[0]) ):
        #print(index, frame, part_param.get(index))
        
        if part_param.get(index) is None:
          ...
        else:
          buffer =  part_param.get(index)
        
        
        if frame_param_param.get(frame) is None:
          frame_param_param[frame] = {}
        if frame_param_param[frame].get(index) is None:
          frame_param_param[frame][index] = buffer


    for index, part in index_part.items():
      for frame, part_param in sorted( frame_param_param.items(), key=lambda x:int(x[0]) ):
        print(index, frame, part_param.get(index))


if __name__ == '__main__':
  if '--step1' in sys.argv:
    step1()
  
  if "--step2" in sys.argv:
    step2()

  if "--step3" in sys.argv:
    step3()

  if "--step4" in sys.argv:
    step4()
