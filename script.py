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
    df = pd.read_csv(root + 'trip_data_1.csv',usecols=['medallion', ' pickup_datetime', ' dropoff_datetime',
       ' passenger_count', ' trip_time_in_secs', ' trip_distance',
       ' pickup_longitude', ' pickup_latitude', ' dropoff_longitude',
       ' dropoff_latitude'], nrows=1000000)
    df[' pickup_datetime'] = pd.to_datetime(df[' pickup_datetime'])
    df[' dropoff_datetime'] = pd.to_datetime(df[' dropoff_datetime'])
    df_1d = df[df[' pickup_datetime']<'2010-01-02 00:00:00']
    df_2d = df[df[' pickup_datetime']<'2010-01-02 00:10:00']
    df_1d = df_1d.loc[54:101]
    del df
    delta = 3
    for df in utils.dataloader_df(df_1d, buck_size = 10):
        last_consider = sh.last_consider_factory(df_2d, delta)
        last_series = df_1d.apply(last_consider, axis = 1)
        edges_series = utils.potential_ranges(last_series)
        output_shareable_edges = sh.output_shareable_edges_factory(df_2d, delta)
        for series in utils.dataloader_series(edges_series, buck_size = 240):
            split_series = utils.split_edges_series(series,4)
            pool = mp.Pool(4)
            results = pool.map(output_shareable_edges, split_series)
            pool.close()
            pool.join()
            out = sum(results,[])
            if len(out) > 0:
                with open('test.txt','a') as f:
                    for ele in out:
                        f.write(str(ele)+'\n')

if __name__ == "__main__":
    main()