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
            
            listofdfs.append(pd.read_json(fullname))

    return pd.concat(listofdfs)


def group_artist_rank(data, limit = 20, verbose = False):
    artistData = data.groupby('artistName').sum()
    artistData = artistData.sort_values('msPlayed', ascending=False)
    sample = artistData.head(limit)
    
    sample.reset_index(level=0, inplace=True)
    
    if verbose:
        print(sample)
    
    return sample


def group_by_time(data, limit = 31, verbose = False):
    timeData = data.groupby('date').sum()
    sample = timeData.head(limit) 
    
    sample.reset_index(level=0, inplace=True)
    
    if verbose:
        print(sample)
    
    return sample



def plot_bar_time(sample):
    dates = sample['date']
    y_pos = np.arange(len(dates))
    
    plt.bar(y_pos, sample['playTime_min'], align='center', color='coral')
    plt.xticks(y_pos, dates, rotation=90)
    plt.ylabel('Time Played (mins)')
    plt.title('Dates')
    
    hours = (int(np.max(sample['playTime_min']))/1000)%60
    
    while hours > 1:
        plt.axhline(hours*1000)
        hours -=1
    
    plt.show()



def plot_bar_frequency(sample):
    artists = sample['artistName']
    y_pos = np.arange(len(artists))
    
    plt.bar(y_pos, sample['playTime_min'], align='center', color='coral')
    plt.xticks(y_pos, artists, rotation=90)
    plt.ylabel('Time Played (mins)')
    plt.title('Artist')
    
    hours = (int(np.max(sample['playTime_min']))/1000)%60
    
    while hours > 1:
        plt.axhline(hours*1000)
        hours -=1
    
    plt.show()


def preprocess(data):
    # Transforms ms to hours:minutes:seconds
    data['playTime'] = data.msPlayed.apply(to_time_format)
    data['playTime_min'] = data.msPlayed.apply(to_mins)

    # Split to ease grouping by time    
    data[['date', 'time']] = data['endTime'].str.split(" ", expand=True)
    data = data.drop(columns =['endTime'])
    
    return data


# -----------------------------
# Support Functions
# -----------------------------

def to_time_format(millis, formattime ='%H:%M:%S'):
    return datetime.datetime.fromtimestamp(millis).strftime(formattime)

def to_mins(millis):
    return (int(millis)/(1000*60))%60
    
        

if __name__ == '__main__':
    test_path = '/Users/raulcoroban/Documents/Projects/Spotify Data'
    
    full_data = files_to_df(test_path)
    pro_data = preprocess(full_data)
    
    # Artist overall ranking
    data_artist = group_artist_rank(pro_data)
    plot_bar_frequency(data_artist)
    
    # Artists over the time (barplot)
    data_time = group_by_time(pro_data)
    plot_bar_time(data_time)
    
    # CUSTOM artist over time

    # Artists number of songs, albums    

    # Days of the week streaming time
        # - Check if all days are consecutive
        # - Add times
    
    # Days of the week streaming artists
    
    # Days of the week streaming CUSTOM artist
    
    # Months streaming time
    
    # Months streaming artists

    # Months streaming CUSTOM artist
    
    # Time played during the year (highlight lockdown)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    