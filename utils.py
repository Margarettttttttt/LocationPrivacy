def dataloader_df(df, buck_size = 10):
    n = len(df)
    num_buck = int(n * 1.0 / buck_size + 1) 
    split = np.split(df, num_buck)
    return split

