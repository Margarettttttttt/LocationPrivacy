def dataloader_df(df, buck_size = 10):
    """
    Spliting the dataframe of interest into chunks with size of buck_size.
    Return a list of the splited dataframes
    """
    n = len(df)
    num_buck = int(n * 1.0 / buck_size + 1) 
    split = np.split(df, num_buck)
    return split

def potential_ranges(last):
    """return a list of tuples corresponding to the index of the dataframe
    """
    ranges_series = pd.Series([(i, j) for (i,c) in last for j in range(i+1,c) ])
    # print(ranges_series)
    return ranges_series