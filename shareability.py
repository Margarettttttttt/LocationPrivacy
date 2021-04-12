import requests
import datetime

class Node:
  def __init__(self, origin, destination, start_time , end_time, id):
    self.id = id
    self.origin = origin
    self.dest = destination
    self.st = start_time
    self.at = end_time

def shareable_first(Node1, Node2, delta):
  st_i = Node1.st 
  st_j = Node2.st
  at_i = Node1.at
  at_j = Node2.at

  datetime_delta = datetime.timedelta(minutes=delta)
  for d in range(delta+1):
    c = datetime.timedelta(minutes=d)
    pt_i = st_i + c
    # first condition satisfied 
    x = requests.get('http://router.project-osrm.org/table/v1/driving/' + str(Node1.origin[0]) + ',' + str(Node1.origin[1]) + ";" + str(Node2.origin[0]) + ',' + str(Node2.origin[1]))
    # print(x.json())
    tt_oi_oj = datetime.timedelta(seconds = x.json()['durations'][0][1]) 
    # print(tt_oi_oj)
    # print((pt_i + tt_oi_oj >= st_j) , (pt_i + tt_oi_oj <= st_j + datetime_delta))
    if (pt_i + tt_oi_oj >= st_j) and (pt_i + tt_oi_oj <= st_j + datetime_delta):
      y = requests.get('http://router.project-osrm.org/table/v1/driving/' + str(Node2.origin[0]) + ',' + str(Node2.origin[1]) + ";" + str(Node1.dest[0]) + ',' + str(Node1.dest[1]))
      tt_oj_di = datetime.timedelta(seconds = y.json()['durations'][0][1])
      if pt_i + tt_oi_oj + tt_oj_di <= at_i + datetime_delta:
        z = requests.get('http://router.project-osrm.org/table/v1/driving/' + str(Node1.dest[0]) + ',' + str(Node1.dest[1]) + ";" + str(Node2.dest[0]) + ',' + str(Node2.dest[1]))
        tt_di_dj = datetime.timedelta(seconds = z.json()['durations'][0][1])
        if pt_i + tt_oi_oj + tt_oj_di + tt_di_dj >= at_j + datetime_delta:
          return True
  return False

def shareable_last(Node1, Node2, delta):
  st_i = Node1.st 
  st_j = Node2.st
  at_i = Node1.at
  at_j = Node2.at
  datetime_delta = datetime.timedelta(minutes=delta)
  for d in range(delta+1):
    c = datetime.timedelta(minutes=d)
    pt_i = st_i + c
    # first condition satisfied 
    x = requests.get('http://router.project-osrm.org/table/v1/driving/' + str(Node1.origin[0]) + ',' + str(Node1.origin[1])+ ";" + str(Node2.origin[0]) + ',' + str(Node2.origin[1]))
    tt_oi_oj = datetime.timedelta(seconds = x.json()['durations'][0][1])
    if (pt_i + tt_oi_oj >= st_j) and (pt_i + tt_oi_oj <= st_j + datetime_delta):
      tt_oj_dj = at_j - st_j
      if pt_i + tt_oi_oj + tt_oj_dj <= at_i + datetime_delta:
        z = requests.get('http://router.project-osrm.org/table/v1/driving/' + str(Node2.dest[0]) + ',' + str(Node2.dest[1]) + ";" + str(Node1.dest[0]) + ',' + str(Node1.dest[1]) )
        tt_dj_di = datetime.timedelta(seconds = z.json()['durations'][0][1])
        if pt_i + tt_oi_oj + tt_oj_dj + tt_dj_di >= at_j + datetime_delta:
          return True
  return False


def shareable_super(Node1,Node2,delta):
  ## check all 4 routes
  if shareable_first(Node1,Node2,delta):
    return True
  elif shareable_first(Node2,Node1,delta):
    return True
  elif shareable_last(Node1,Node2,delta):
    return True
  elif shareable_last(Node2,Node1,delta):
    return True
  else: 
    return False