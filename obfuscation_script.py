import importlib
import multiprocessing as mp
import pandas as pd
import numpy as np
import requests
import datetime
import time
from tqdm import tqdm
import shareability as sh
from functools import partial
import utils

def main():
    root = ''
    df = pd.read_csv(root + 'obfuscated_trips_duration_included.csv',usecols=[
       ' fake_pickup_latitude',' fake_pickup_longitude', ' fake_dropoff_latitude',
       ' fake_dropoff_longitude', 'fake_pickup_datetime', 'fake_dropoff_datetime'])
    df['fake_pickup_datetime'] = pd.to_datetime(df['fake_pickup_datetime'])
    df['fake_dropoff_datetime'] = pd.to_datetime(df['fake_dropoff_datetime'])
    df_1d = df[~df['fake_dropoff_datetime'].isnull()]
    df_2d = df_1d
    # df_1d = df_1d.loc[54:101]
    del df
    delta = 3
    count = 0
    df_loader = utils.dataloader_df(df_1d, buck_size = 10)
    del df_1d
    for df in df_loader:
        last_consider = sh.last_consider_factory(df_2d, delta, obfuscated = True)
        last_series = df.apply(last_consider, axis = 1)
        edges_series = utils.potential_ranges(last_series)
        output_shareable_edges = sh.output_shareable_edges_factory(df_2d, delta, obfuscated = True)
        # if count == 0:
        #     count = 1
        #     edges_series = edges_series[edges_series.apply(lambda x : False if (x[0]==54 and x[1]<=579) else True )]
        #     print(edges_series.head())
        for series in utils.dataloader_series(edges_series, buck_size = 30):
            split_series = utils.split_edges_series(series,3)
            pool = mp.Pool(3)
            print('----------starting parallelization----------')
            results = pool.map(output_shareable_edges, split_series)
            pool.close()
            pool.join()
            print('----------ending parallelization----------')
            out = sum(results,[])
            if len(out) > 0:
                with open('edges_gmaps.txt','a') as f:
                    for ele in out:
                        f.write(str(ele)+'\n')
                    print('Update: wrote down some edges up to ' + str(ele))

if __name__ == "__main__":
    main()