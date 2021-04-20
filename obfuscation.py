from faker import Faker
import googlemaps 
import config
import pandas as pd

gmaps = googlemaps.Client(key=config.API_key_new)
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
    while tries < 10:
        lat_fake = fake.coordinate(center=str(lat), radius = r)
        lng_fake = fake.coordinate(center=str(lng), radius = r)
        x = gmaps.distance_matrix((lat,lng), (lat_fake,lng_fake), mode='walking')
        try:
            dur = x['rows'][0]['elements'][0]['duration']['value']
            if dur < delta * 60:
                print(tries)
                return pd.Series([lat_fake, lng_fake, dur])
            else:
                tries += 1
                continue
        except Exception as e:
            print(e)
            print(e.args)
            print('Request Exception.  Node: '+ str(lat) + ',' + str(lng) + '---->' + str(lat_fake)+str(lng_fake))
            tries += 1
            continue
    return pd.Series([0.00,0.00, 0]) 

def main():
    root = ''
    df = pd.read_csv(root + 'trip_data_1.csv',usecols=['medallion', ' pickup_datetime', ' dropoff_datetime',
       ' passenger_count', ' trip_time_in_secs', ' trip_distance',
       ' pickup_longitude', ' pickup_latitude', ' dropoff_longitude',
       ' dropoff_latitude'], nrows=1000000)
    df[' pickup_datetime'] = pd.to_datetime(df[' pickup_datetime'])
    df[' dropoff_datetime'] = pd.to_datetime(df[' dropoff_datetime'])
    df = df[df[' pickup_datetime']<'2010-01-01 00:15:00']
    # df = df.iloc[:996]
    print(len(df))
    # df_2d = df[df[' pickup_datetime']<'2010-01-01 01:10:00']
    delta = 3
    obfuscated_pickup = df.apply(lambda x : obfuscated_coord(x.loc[' pickup_latitude'],x.loc[' pickup_longitude'],delta ), axis=1)
    obfuscated_dropoff = df.apply(lambda x : obfuscated_coord(x.loc[' dropoff_latitude'],x.loc[' dropoff_longitude'],delta ), axis=1)
    obfuscated_pickup.columns = [' fake_pickup_latitude',' fake_pickup_longitude', 'pickup_walking_time']
    obfuscated_dropoff.columns = [' fake_dropoff_latitude',' fake_dropoff_longitude', 'dropoff_walking_time']

    df = df.join(obfuscated_pickup).join(obfuscated_dropoff)
    df.to_csv('obfuscated_trips.csv')
    print(df.head(2))

if __name__ == "__main__":
    main()