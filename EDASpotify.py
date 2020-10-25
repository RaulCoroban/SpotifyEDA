# -*- coding: utf-8 -*-
"""
Spyder Editor


"""

import os
import fnmatch
import datetime

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------
# CORE Functions
# -----------------------------
def files_to_df(path, pattern = 'StreamingHistory*'):
    listofdfs = []
    
    for path,dirs,files in os.walk(path):
        for f in fnmatch.filter(files, pattern):
            fullname = os.path.abspath(os.path.join(path,f))
            #df = json.load(open(fullname))
            
            listofdfs.append(pd.read_json(fullname))

    return pd.concat(listofdfs)


def group_artist(data, limit = 20, verbose = False):
    artistData = data.groupby('artistName').sum()
    artistData = artistData.sort_values('msPlayed', ascending=False)
    sample = artistData.head(limit)
    
    sample.reset_index(level=0, inplace=True)
    
    if verbose:
        print(sample)
    
    return sample


def plot_bar_frequency(sample):
    artists = sample['artistName']
    y_pos = np.arange(len(artists))
    
    plt.bar(y_pos, sample['msPlayed'], align='center', color='coral')
    plt.xticks(y_pos, artists, rotation=90)
    plt.ylabel('Time Played')
    plt.title('Artist')
    
    plt.show()


def preprocess(data):
    # Transforms ms to hours:minutes:seconds
    data['playTime'] = data.msPlayed.apply(to_time)
    
    return data


# -----------------------------
# Support Functions
# -----------------------------

def to_time(millis):
    return datetime.datetime.fromtimestamp(millis).strftime('%H:%M:%S')
        

if __name__ == '__main__':
    test_path = '/Users/raulcoroban/Documents/Projects/Spotify Data'
    
    full_data = files_to_df(test_path)
    pro_data = preprocess(full_data)
    
    # Group by artist
    data_artist = group_artist(pro_data)
    plot_bar_frequency(data_artist)
    

    # Group by day or month