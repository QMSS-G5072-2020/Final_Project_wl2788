import requests
import os
import json
import pandas as pd
import numpy as np
from requests.exceptions import HTTPError
import re
import matplotlib.pyplot as plt


# Part 1 Get Data With API

## Function 1-Get dataset with specific game "platform" and "type"

def api_game(platform = 'pc', type = 'game'):
    
    """
    The function returns game giveways information from the Game Giveaway Tracker API with specific requirement for plateform and game type.

    Parameters 
    ---
    inputs:
        platform: string value that is the insert game platform, eg: pc, steam, epic-games-store, ubisoft, gog, icthio, ps4, etc.
        type: string value of game type, eg: game

    Returns
    ---
    output: 
        game_giveaway: pandas.DataFrame of the API
        
        Columns:
            _id: int64
            _title: object
            _worth: object
            _thumbnail: float64
            _image: object
            _description: object
            _instructions: object
            _open_giveaway_url: object
            _type: object
            _platforms: object
            _end_date: object
            _users: int64
            _status: bool
            _gamerpower_url: object
            _open_giveaway: object

    Example
    ---
    >>> df = api_game(type='game', platform= 'PC')
    >>> df.shape
    (1, 15)
    
    """
    assert isinstance(platform,str) #parameters should be string
    assert isinstance(type, str) #parameters should be string
    
    try:
        params = {'platform': platform, 'type': type}
        r = requests.get('https://www.gamerpower.com/api/giveaways', params = params)
        game_json=json.dumps(r.json(), indent=2)
        game_j = json.loads(game_json)
        game_giveaway = pd.DataFrame(game_j)
        return game_giveaway
    
        # Catch exception, however if the response was successful, no Exception will be raised
        r.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')

## Function 2: Get full dataset        
        
def api_game_full():
    
    """
    The function returns all game giveways information from the Game Giveaway Tracker API.

    Parameters
    ---
        
    Returns
    ---
    output: 
        game_df: pandas.DataFrame of the API with stated parameters
        
        Columns:
            _id: int64
            _title: object
            _worth: object
            _thumbnail: float64
            _image: object
            _description: object
            _instructions: object
            _open_giveaway_url: object
            _type: object
            _platforms: object
            _end_date: object
            _users: int64
            _status: bool
            _gamerpower_url: object
            _open_giveaway: object
            

    Example
    ---
    >>> df = api_game_full()
    >>> df.shape
    (84, 15)
    
    """
    try:
        r = requests.get('https://www.gamerpower.com/api/giveaways')
        game_json=json.dumps(r.json(), indent=2)
        game_j = json.loads(game_json)
        game_df = pd.DataFrame(game_j)
        return game_df
    
        # Catch exception, however if the response was successful, no Exception will be raised
        r.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
                

# Part 2 Functions With Full Dataset
## Function 1: Get descriptive statistics for each game type
        
def game_type(game_df):
    
    """
    The function is used to clean the data at first.
    Then return the new dataframe that contains number of games, user number mean, std, min, 25%, 50%, 75% and max value for each type.

    Parameters
    ---
    inputs: 
        game_df: pandas.DataFrame of the API which is generated in part1 function2.


    Returns
    ---
    output: 
        type_statistics: pandas.DataFrame descriptive statistics for each game type
        

    Example
    ---
    >>> game_df = api_game_full()
    >>> type_statistics=game_type(game_df)
    >>> type_statistics.shape
    (3, 8)
    
    """
    assert isinstance(game_df, pd.core.frame.DataFrame) # make sure input should be dataframe
    
    df=game_df.drop(['thumbnail', 'image', 'description','open_giveaway_url', 'end_date'], axis=1) # drop column and clean data
    g_type=df['type']
    g_users=df['users']
    g_list={'type': g_type, 'number of users': g_users}
    gt_df= pd.DataFrame(g_list)
    type_statistics=gt_df.groupby('type').describe()
    type_statistics=type_statistics.rename(columns={'count': 'number of games for this type'})

    return type_statistics        
        
        
## Function 2: Get Z score and its graph for users for each type
def zscore_plot(game_df):

    """
    The function is used to calculate Z score for number of users for each game type 
    Then get histogram graph for Z score

    Parameters
    ---
    inputs: 
        game_df: pandas.DataFrame of the API which is generated in part1 function2.


    Returns
    ---
    output: 
        a histogram plot for Z score of user number for each game type
              

    Example
    ---
    >>> game_df = api_game_full()
    >>> zscore_plot(game_df)
    a histogram plot shows up
    <matplotlib.axes._subplots.AxesSubplot at 0x11bca3ac0>
    
    """
    
    assert isinstance(game_df, pd.core.frame.DataFrame) # make sure input should be dataframe    
    
    g_type=game_df['type']
    g_users=game_df['users']
    g_list={'type': g_type, 'number of users': g_users}
    gt_df= pd.DataFrame(g_list)
    gt_df['user_zscore']=gt_df.groupby('type').transform(lambda x: (x-x.mean())/x.std())
    return gt_df['user_zscore'].hist()
        
        
## Function 3-Get number for specific game type
def type_number(game_df, type):
    
    """
    The function is used to allow people to choose one type of game
    Then check the number of games for this type

    Parameters
    ---
    inputs: 
        game_df: pandas.DataFrame of the API which is generated in part1 function2.
        type: string value of game type, please choose from 'Full Game','DLC & Loot','Early Access'.


    Returns
    ---
    output: 
        number: number of games for a specific game type
              

    Example
    ---
    >>> game_df = api_game_full()
    >>> type_number(game_df, 'Full Game')
    int: 21
    
    """    
    
    try: 
        if type not in ('Full Game','DLC & Loot','Early Access'): raise Error()
            
        df=game_df[game_df['type']==type]
        number=int(df['type'].value_counts())
    
        return number

    except:
        print('Please check your input values.')
        
## Function 4-Get longest or shortest title        
def title_max_min(game_df, calculation):
    
    """
    The function is used to get longest or shortest title

    Parameters
    ---
    inputs: 
        game_df: pandas.DataFrame of the API which is generated in part1 function2
        calculation: string value, if you enter 'max', you will get longest title, if you enter 'min', that would be shortest title


    Returns
    ---
    output: 
        game title: string value of longest or shortest game title
              

    Example
    ---
    >>> game_df = api_game_full()
    >>> title_max_min(game_df, 'min')
    'Free Kalaban (PC)'
    
    """    
    
    assert isinstance(game_df, pd.core.frame.DataFrame) # make sure input should be dataframe   
    assert isinstance(calculation, str) # make sure input should be string
    assert calculation in ('max', 'min')
    
    if calculation=='max':
        max_length = -1
        for title in game_df['title']: 
            if len(title) > max_length: 
                max_length = len(title) 
                game_title= title
        return game_title
    
    if calculation =='min':
        min_length = 1000
        for title in game_df['title']: 
            if len(title) < min_length: 
                min_length = len(title) 
                game_title = title
        return game_title
    
## Function 5: Check the length of title for each game type    
def title_length_type(game_df):
    
    """
    The function is used to get length (max, min, average) of game name for each game type

    Parameters
    ---
    inputs: 
        game_df: pandas.DataFrame of the API which is generated in part1 function2


    Returns
    ---
    output: 
        df: dataframe that contains min, max, mean of title length for 3 game types
              

    Example
    ---
    >>> game_df = api_game_full()
    >>> df=title_length_type(game_df)
    >>> df.shape
    (3, 3)
    
    """        
    
    assert isinstance(game_df, pd.core.frame.DataFrame) # make sure input should be dataframe   
    
    g_type=game_df['type']
    g_title=game_df['title'].str.len()
    g_list={'type': g_type, 'title length': g_title}
    gt_df= pd.DataFrame(g_list)
    df=gt_df.groupby('type').agg(['min', 'max', 'mean'])
    
    return df


## Function 6 Get descriptive statistics of users for each platform
def game_platform(game_df):
    
    """
    The function is used to clean the data at first.
    Then return the new dataframe that contains number of games, user number mean, std, min, 25%, 50%, 75% and max value for each game platform.

    Parameters
    ---
    inputs: 
        game_df: pandas.DataFrame of the API which is generated in part1 function2.


    Returns
    ---
    output: 
        type_statistics: pandas.DataFrame descriptive statistics for each game platform
        

    Example
    ---
    >>> game_df = api_game_full()
    >>> type_statistics=game_platform(game_df)
    >>> type_statistics.shape
    (19, 8)
    
    """
    
    assert isinstance(game_df, pd.core.frame.DataFrame) # make sure input should be dataframe

    
    df=game_df.drop(['thumbnail', 'image', 'description','open_giveaway_url', 'end_date'], axis=1) # drop column and clean data
    g_platforms=game_df['platforms']
    g_users=game_df['users']
    g_list={'platform': g_platforms, 'number of users': g_users}
    gt_df= pd.DataFrame(g_list)
    type_statistics=gt_df.groupby('platform').describe()
    type_statistics=type_statistics.rename(columns={'count': 'number of games for this platform'})
    
    return type_statistics



## Function 7 Get dataframe with rank of worth
def worth_new(game_df, ascending):
    
    """
    The function is used to remove the N/A value and useless symbol at first.
    Then change the datatype of "worth" from string to float
    Then return a new dataframe with rank of "worth" from high to low or low to high
    

    Parameters
    ---
    inputs: 
        game_df: pandas.DataFrame of the API which is generated in part1 function2.
        ascending: boolean：True or False

    Returns
    ---
    output: 
        df_worth: pandas.DataFrame with worth ranking
        

    Example
    ---
    >>> game_df = api_game_full()
    >>> df_worth=worth_new(game_df, True)
    >>> df_worth.shape
    (27, 16)
    
    """
    
    assert isinstance(game_df, pd.core.frame.DataFrame) # make sure input should be dataframe
    assert isinstance(ascending, bool) # make sure input should be boolean
    
    df_worth=game_df[game_df['worth']!='N/A'] #delete missing value

    worth_new=[]
    for worth in df_worth['worth']:    
        s=float(worth.replace('$', ''))
        worth_new.append(s)
    
    df_worth['worth_new']=worth_new
    df_worth=df_worth.sort_values(by='worth_new',ascending=ascending)
    
    return df_worth


## Function 8 Check relationship between number of users and game worth with scatter plot

def worth_plot(df_worth):
    
    """
    The function is used to check relationship between number of users and game worth with scatter plot

    Parameters
    ---
    inputs: 
        df_worth: pandas.DataFrame with worth ranking from part 2 function 7

    Returns
    ---
    output: 
        a scatter plot with number of users and game worth 
              
    Example
    ---
    >>> df_worth=worth_new(game_df, True)
    >>> worth_plot(df_worth)
    a scatter plot shows up
    
    """
    
    assert isinstance(df_worth, pd.core.frame.DataFrame) # make sure input should be dataframe
    
    plt.scatter(df_worth['worth_new'], df_worth['users'], alpha=0.5)

    m, b = np.polyfit(df_worth['worth_new'], df_worth['users'], 1)
    plt.plot(df_worth['worth_new'], m*df_worth['worth_new'] + b, color='g')

    plt.xlabel('game worth')
    plt.ylabel('Users')

    plt.show()





        
        
        
        
        
        

