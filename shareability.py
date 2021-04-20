import requests
import datetime
from functools import partial
import numpy as np
from tqdm import tqdm
import googlemaps
import config



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
      try:
        s = x.json()['durations'][0][1]
      except Exception as e:
        print(e)
        print(e.args)
        print('JSON Exception.  Node: ', (Node1.id, Node2.id), str(Node1.origin[0]) + ',' + str(Node1.origin[1]) + ";" + str(Node2.origin[0]) + ',' + str(Node2.origin[1]))
        print(x)
        return False
      if s is not None:
        tt_oi_oj = datetime.timedelta(seconds = s) 
      else:
        return False
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
        try:
          s = y.json()['durations'][0][1]
        except Exception as e:
          print(e)
          print(e.args)
          print('JSON Exception.  Node: ', str(Node2.origin[0]) + ',' + str(Node2.origin[1]) + ";" + str(Node1.dest[0]) + ',' + str(Node1.dest[1]))
          print(y)
          return False  
        if s is not None:
          tt_oj_di = datetime.timedelta(seconds = s)
        else:
          return False
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
          try:
            s = z.json()['durations'][0][1]
          except Exception as e:
            print(e)
            print(e.args)
            print('JSON Exception.  Node: ', str(Node1.dest[0]) + ',' + str(Node1.dest[1]) + ";" + str(Node2.dest[0]) + ',' + str(Node2.dest[1]))
            print(z)
            return False
          if s is not None:
            tt_di_dj = datetime.timedelta(seconds = s)
          else:
            return False
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
      try:
        s = x.json()['durations'][0][1]
      except Exception as e:
        print(e)
        print(e.args)
        print('JSON Exception.  Node: ', (Node1.id, Node2.id), str(Node1.origin[0]) + ',' + str(Node1.origin[1])+ ";" + str(Node2.origin[0]) + ',' + str(Node2.origin[1]))
        print(x)
        return False
      if s is not None:
        tt_oi_oj = datetime.timedelta(seconds = s)
      else:
        return False
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
          print(z)
          return False
        if z is not None:
          try:
            s = z.json()['durations'][0][1]
          except Exception as e:
            print(e)
            print(e.args)
            print('JSON Exception.  Node: ', (Node1.id, Node2.id), str(Node2.dest[0]) + ',' + str(Node2.dest[1]) + ";" + str(Node1.dest[0]) + ',' + str(Node1.dest[1]) )
            return False  
          if s is not None:
            tt_dj_di = datetime.timedelta(seconds = s)
          else:
            return False
        else:
          print('Return None.  Node: ', (Node1.id, Node2.id), str(Node2.dest[0]) + ',' + str(Node2.dest[1]) + ";" + str(Node1.dest[0]) + ',' + str(Node1.dest[1]) )
          return False
        
        if pt_i + tt_oi_oj + tt_oj_dj + tt_dj_di >= at_j + datetime_delta:
          return True
  print('-------- return False bc not shareable ---------')
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

def output_shareable_edges_factory(df, delta, gmap):
  return partial(output_shareable_edges, df, delta, gmap)

def output_shareable_edges(df, delta, gmap, potential_ranges_list):

  """ output a list of shareable edges
  """
  shareable_list = []
  for (i,j) in tqdm(potential_ranges_list):
    o1 = (df.loc[i][' pickup_longitude'],df.loc[i][' pickup_latitude'])
    d1 = (df.loc[i][' dropoff_longitude'],df.loc[i][' dropoff_latitude'])
    s1 = df.loc[i][' pickup_datetime']
    t1 = df.loc[i][' dropoff_datetime']

    n1 = Node(o1, d1, s1, t1, i)

    o2 = (df.loc[j][' pickup_longitude'],df.loc[j][' pickup_latitude'])
    d2 = (df.loc[j][' dropoff_longitude'],df.loc[j][' dropoff_latitude'])
    s2 = df.loc[j][' pickup_datetime']
    t2 = df.loc[j][' dropoff_datetime']

    n2 = Node(o2, d2, s2, t2, j)
    if gmap:
      canshare = shareable_super_gmap(n1, n2, delta)
    else:
      canshare = shareable_super(n1, n2, delta)
    if canshare:
      shareable_list.append((i,j))
  return shareable_list

def shareable_first_gmap(Node1, Node2, delta):
  st_i = Node1.st 
  st_j = Node2.st
  at_i = Node1.at
  at_j = Node2.at
  gmaps = googlemaps.Client(key=config.API_key_new)
  datetime_delta = datetime.timedelta(minutes=delta)
  for d in range(delta+1):
    c = datetime.timedelta(minutes=d)
    pt_i = st_i + c
    try:
      x = gmaps.distance_matrix((Node1.origin[1],Node1.origin[0]), (Node2.origin[1],Node2.origin[0]), mode='driving')
    except Exception as e:
      print(e)
      print(e.args)
      print('Request Exception.  Node: ', (Node1.id, Node2.id), str(Node1.origin[0]) + ',' + str(Node1.origin[1]) + ";" + str(Node2.origin[0]) + ',' + str(Node2.origin[1]))
      return False
    if x is not None:
      try:
        s = x['rows'][0]['elements'][0]['duration']['value']
      except Exception as e:
        print(e)
        print(e.args)
        print('Query Exception (zero result).  Node: ', (Node1.id, Node2.id), str(Node1.origin[0]) + ',' + str(Node1.origin[1]) + ";" + str(Node2.origin[0]) + ',' + str(Node2.origin[1]))
        # print(x)
        # raise e
        return False
      if s is not None:
        tt_oi_oj = datetime.timedelta(seconds = s) 
      else:
        return False
    else:
      print('None object.  Node: ', (Node1.id, Node2.id), str(Node1.origin[0]) + ',' + str(Node1.origin[1]) + ";" + str(Node2.origin[0]) + ',' + str(Node2.origin[1]))
      return False
  
    if (pt_i + tt_oi_oj >= st_j) and (pt_i + tt_oi_oj <= st_j + datetime_delta):
      try:
        y = gmaps.distance_matrix((Node2.origin[1],Node2.origin[0]), (Node1.dest[1],Node1.dest[0]), mode='driving')
      except Exception as e:
        print(e)
        print(e.args)
        print('Request Exception.  Node: ', str(Node2.origin[0]) + ',' + str(Node2.origin[1]) + ";" + str(Node1.dest[0]) + ',' + str(Node1.dest[1]))
        return False  
      if y is not None:
        try:
          s = y['rows'][0]['elements'][0]['duration']['value']
        except Exception as e:
          print(e)
          print(e.args)
          print('Query Exception (zero result).  Node: ', str(Node2.origin[0]) + ',' + str(Node2.origin[1]) + ";" + str(Node1.dest[0]) + ',' + str(Node1.dest[1]))
          # print(y)
          # raise e
          return False  
        if s is not None:
          tt_oj_di = datetime.timedelta(seconds = s)
        else:
          return False
      else:
        print('None object.  Node: ', (Node1.id, Node2.id), str(Node2.origin[0]) + ',' + str(Node2.origin[1]) + ";" + str(Node1.dest[0]) + ',' + str(Node1.dest[1]))
        return False
      
      if pt_i + tt_oi_oj + tt_oj_di <= at_i + datetime_delta:
        try:
          z = gmaps.distance_matrix((Node1.dest[1],Node1.dest[0]),(Node2.dest[1],Node2.dest[0]), mode='driving')
        except Exception as e:
          print(e)
          print(e.args)
          print('Request Exception.  Node: ', str(Node1.dest[0]) + ',' + str(Node1.dest[1]) + ";" + str(Node2.dest[0]) + ',' + str(Node2.dest[1]))
          return False
        if z is not None:
          try:
            s = z['rows'][0]['elements'][0]['duration']['value']
          except Exception as e:
            print(e)
            print(e.args)
            print('Query Exception (zero result).  Node: ', str(Node1.dest[0]) + ',' + str(Node1.dest[1]) + ";" + str(Node2.dest[0]) + ',' + str(Node2.dest[1]))
            print(z)
            # raise e
            return False
          if s is not None:
            tt_di_dj = datetime.timedelta(seconds = s)
          else:
            return False
        else: 
          print('None object.  Node: ', (Node1.id, Node2.id), str(Node1.dest[0]) + ',' + str(Node1.dest[1]) + ";" + str(Node2.dest[0]) + ',' + str(Node2.dest[1]))
          return False
        
        if pt_i + tt_oi_oj + tt_oj_di + tt_di_dj >= at_j + datetime_delta:
          return True
    # except Exception as e:
      # print(e.args)
  return False

def shareable_last_gmap(Node1, Node2, delta):
  gmaps = googlemaps.Client(key=config.API_key_new)
  st_i = Node1.st 
  st_j = Node2.st
  at_i = Node1.at
  at_j = Node2.at
  datetime_delta = datetime.timedelta(minutes=delta)
  for d in range(delta+1):
    c = datetime.timedelta(minutes=d)
    pt_i = st_i + c
    try:
      x = gmaps.distance_matrix((Node1.origin[1],Node1.origin[0]),(Node2.origin[1],Node2.origin[0]), mode='driving')
    except Exception as e:
      print(e)
      print(e.args)
      print('Exception.  Node: ', (Node1.id, Node2.id), str(Node1.origin[0]) + ',' + str(Node1.origin[1])+ ";" + str(Node2.origin[0]) + ',' + str(Node2.origin[1]))
      return False
    if x is not None:
      try:
        s = x['rows'][0]['elements'][0]['duration']['value']
      except Exception as e:
        print(e)
        print(e.args)
        print('Query Exception (zero result).  Node: ', (Node1.id, Node2.id), str(Node1.origin[0]) + ',' + str(Node1.origin[1])+ ";" + str(Node2.origin[0]) + ',' + str(Node2.origin[1]))
        # print(x) 
        # raise e
        return False
      if s is not None:
        tt_oi_oj = datetime.timedelta(seconds = s)
      else:
        return False
    else:
      print('Return None.  Node: ', (Node1.id, Node2.id), str(Node1.origin[0]) + ',' + str(Node1.origin[1])+ ";" + str(Node2.origin[0]) + ',' + str(Node2.origin[1]))
      return False
  
    if (pt_i + tt_oi_oj >= st_j) and (pt_i + tt_oi_oj <= st_j + datetime_delta):
      tt_oj_dj = at_j - st_j
      if pt_i + tt_oi_oj + tt_oj_dj <= at_i + datetime_delta:
        try:
          z = gmaps.distance_matrix((Node2.dest[1],Node2.dest[0]),(Node1.dest[1],Node1.dest[0]) , mode='driving')
        except Exception as e:
          print(e)
          print(e.args)
          print('Exception.  Node: ', (Node1.id, Node2.id), str(Node2.dest[0]) + ',' + str(Node2.dest[1]) + ";" + str(Node1.dest[0]) + ',' + str(Node1.dest[1]) )
          # print(z)
          return False
        if z is not None:
          try:
            s = z['rows'][0]['elements'][0]['duration']['value']
          except Exception as e:
            print(e)
            print(e.args)
            print('Query Exception (zero result).  Node: ', (Node1.id, Node2.id), str(Node2.dest[0]) + ',' + str(Node2.dest[1]) + ";" + str(Node1.dest[0]) + ',' + str(Node1.dest[1]) )
            # raise e
            return False  
          if s is not None:
            tt_dj_di = datetime.timedelta(seconds = s)
          else:
            return False
        else:
          print('Return None.  Node: ', (Node1.id, Node2.id), str(Node2.dest[0]) + ',' + str(Node2.dest[1]) + ";" + str(Node1.dest[0]) + ',' + str(Node1.dest[1]) )
          return False
        
        if pt_i + tt_oi_oj + tt_oj_dj + tt_dj_di >= at_j + datetime_delta:
          return True
  return False

def shareable_super_gmap(Node1,Node2,delta):
  ## check all 4 routes
  if shareable_first_gmap(Node1,Node2,delta):
    return True
  elif shareable_first_gmap(Node2,Node1,delta):
    return True
  elif shareable_last_gmap(Node1,Node2,delta):
    return True
  elif shareable_last_gmap(Node2,Node1,delta):
    return True
  else: 
    return False