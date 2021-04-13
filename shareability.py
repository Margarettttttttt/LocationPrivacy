import requests
import datetime
from functools import partial
import numpy as np
from tqdm import tqdm


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
    try:
      x = requests.get('http://router.project-osrm.org/table/v1/driving/' + str(Node1.origin[0]) + ',' + str(Node1.origin[1]) + ";" + str(Node2.origin[0]) + ',' + str(Node2.origin[1]))
    except Exception as e:
      print(e)
      print(e.args)
      print('Exception.  Node: ', (Node1.id, Node2.id), str(Node1.origin[0]) + ',' + str(Node1.origin[1]) + ";" + str(Node2.origin[0]) + ',' + str(Node2.origin[1]))
      return False
    if x is not None:
      tt_oi_oj = datetime.timedelta(seconds = x.json()['durations'][0][1]) 
    else:
      print('None object.  Node: ', (Node1.id, Node2.id), str(Node1.origin[0]) + ',' + str(Node1.origin[1]) + ";" + str(Node2.origin[0]) + ',' + str(Node2.origin[1]))
      return False
  
    if (pt_i + tt_oi_oj >= st_j) and (pt_i + tt_oi_oj <= st_j + datetime_delta):
      try:
        y = requests.get('http://router.project-osrm.org/table/v1/driving/' + str(Node2.origin[0]) + ',' + str(Node2.origin[1]) + ";" + str(Node1.dest[0]) + ',' + str(Node1.dest[1]))
      except Exception as e:
        print(e)
        print(e.args)
        print('Exception.  Node: ', str(Node2.origin[0]) + ',' + str(Node2.origin[1]) + ";" + str(Node1.dest[0]) + ',' + str(Node1.dest[1]))
        return False  
      if y is not None:
        tt_oj_di = datetime.timedelta(seconds = y.json()['durations'][0][1])
      else:
        print('None object.  Node: ', (Node1.id, Node2.id), str(Node2.origin[0]) + ',' + str(Node2.origin[1]) + ";" + str(Node1.dest[0]) + ',' + str(Node1.dest[1]))
        return False
      
      if pt_i + tt_oi_oj + tt_oj_di <= at_i + datetime_delta:
        try:
          z = requests.get('http://router.project-osrm.org/table/v1/driving/' + str(Node1.dest[0]) + ',' + str(Node1.dest[1]) + ";" + str(Node2.dest[0]) + ',' + str(Node2.dest[1]))
        except Exception as e:
          print(e)
          print(e.args)
          print('Exception.  Node: ', str(Node1.dest[0]) + ',' + str(Node1.dest[1]) + ";" + str(Node2.dest[0]) + ',' + str(Node2.dest[1]))
          return False
        if z is not None:
          tt_di_dj = datetime.timedelta(seconds = z.json()['durations'][0][1])
        else: 
          print('None object.  Node: ', (Node1.id, Node2.id), str(Node1.dest[0]) + ',' + str(Node1.dest[1]) + ";" + str(Node2.dest[0]) + ',' + str(Node2.dest[1]))
          return False
        
        if pt_i + tt_oi_oj + tt_oj_di + tt_di_dj >= at_j + datetime_delta:
          return True
    # except Exception as e:
      # print(e.args)
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
    try:
      x = requests.get('http://router.project-osrm.org/table/v1/driving/' + str(Node1.origin[0]) + ',' + str(Node1.origin[1])+ ";" + str(Node2.origin[0]) + ',' + str(Node2.origin[1]))
    except Exception as e:
      print(e)
      print(e.args)
      print('Exception.  Node: ', (Node1.id, Node2.id), str(Node1.origin[0]) + ',' + str(Node1.origin[1])+ ";" + str(Node2.origin[0]) + ',' + str(Node2.origin[1]))
      return False
    if x is not None:
      tt_oi_oj = datetime.timedelta(seconds = x.json()['durations'][0][1])
    else:
      print('Return None.  Node: ', (Node1.id, Node2.id), str(Node1.origin[0]) + ',' + str(Node1.origin[1])+ ";" + str(Node2.origin[0]) + ',' + str(Node2.origin[1]))
      return False
  
    if (pt_i + tt_oi_oj >= st_j) and (pt_i + tt_oi_oj <= st_j + datetime_delta):
      tt_oj_dj = at_j - st_j
      if pt_i + tt_oi_oj + tt_oj_dj <= at_i + datetime_delta:
        try:
          z = requests.get('http://router.project-osrm.org/table/v1/driving/' + str(Node2.dest[0]) + ',' + str(Node2.dest[1]) + ";" + str(Node1.dest[0]) + ',' + str(Node1.dest[1]) )
        except Exception as e:
          print(e)
          print(e.args)
          print('Exception.  Node: ', (Node1.id, Node2.id), str(Node2.dest[0]) + ',' + str(Node2.dest[1]) + ";" + str(Node1.dest[0]) + ',' + str(Node1.dest[1]) )
          return False
        if z is not None:
          tt_dj_di = datetime.timedelta(seconds = z.json()['durations'][0][1])
        else:
          print('Return None.  Node: ', (Node1.id, Node2.id), str(Node2.dest[0]) + ',' + str(Node2.dest[1]) + ";" + str(Node1.dest[0]) + ',' + str(Node1.dest[1]) )
          return False
        
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

def last_consider_factory(df, delta):
  return partial(last_consider, df, delta)

def last_consider(df, delta, row):
  n = len(df)
  datetime_delta = datetime.timedelta(minutes=delta)
  st = row[' pickup_datetime']
  last = np.argmin(df[' pickup_datetime'] <= st + datetime_delta * 2)
  if last == 0:
    last = n
  return last

def output_shareable_edges_factory(df, delta):
  return partial(output_shareable_edges, df, delta)

def output_shareable_edges(df, delta, potential_ranges_list):
  """ output a list of shareable edges
  """
  shareable_list = []
  for (i,j) in tqdm(potential_ranges_list):
    o1 = (df.loc[i][' pickup_longitude'],df.loc[0][' pickup_latitude'])
    d1 = (df.loc[i][' dropoff_longitude'],df.loc[0][' dropoff_latitude'])
    s1 = df.loc[i][' pickup_datetime']
    t1 = df.loc[i][' dropoff_datetime']

    n1 = Node(o1, d1, s1, t1, i)

    o2 = (df.loc[j][' pickup_longitude'],df.loc[1][' pickup_latitude'])
    d2 = (df.loc[j][' dropoff_longitude'],df.loc[1][' dropoff_latitude'])
    s2 = df.loc[j][' pickup_datetime']
    t2 = df.loc[j][' dropoff_datetime']

    n2 = Node(o2, d2, s2, t2, j)
    if shareable_super(n1, n2, delta):
      shareable_list.append((i,j))
  return shareable_list