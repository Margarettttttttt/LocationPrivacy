from faker import Faker
import googlemaps 
import config

gmaps = googlemaps.Client(key=config.API_key)
fake = Faker()

def obfuscated_coord(lat, lng, delta):
    ''' Output obfuscated coordinates and the walking time. 
    radius = 1 equals to 100km, sampled norma
    Heuristic: ~83m per min, so we want radius = 0.00083 * delta
    
    Constrain: walking time should be at most delta minutes
    '''
    r = 0.00083 * delta * 0.6
    valid_fake = False
    tries = 0
    while tries < 30:
        lat_fake = fake.coordinate(center=str(lat), radius = r)
        lng_fake = fake.coordinate(center=str(lng), radius = r)
        x = gmaps.distance_matrix((lat,lng), (lat_fake,lng_fake), mode='walking')
        try:
            dur = x['rows'][0]['elements'][0]['duration']['value']
            if dur < delta * 60:
                return (lat_fake, lng_fake), dur
        except Exception as e:
            print(e)
            print(e.args)
            print('Request Exception.  Node: ', str(Node1.dest[0]) + ',' + str(Node1.dest[1]) + ";" + str(Node2.dest[0]) + ',' + str(Node2.dest[1]))
            tries += 1
            continue
    return None 
