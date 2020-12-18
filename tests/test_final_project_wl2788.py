from final_project_wl2788 import __version__
from final_project_wl2788 import final_project_wl2788
import requests
import os
import json
import pandas as pd
import numpy as np
from requests.exceptions import HTTPError
import re
import matplotlib.pyplot as plt


def test_version():
    assert __version__ == '0.1.0'
    
def test_api_game():
    df = final_project_wl2788.api_game(type='game', platform= 'PC')
    assert type(df) == pd.core.frame.DataFrame    
      
def test_api_game_full():
    df = final_project_wl2788.api_game_full()
    assert type(df) == pd.core.frame.DataFrame    
    
def test_game_type():
    df=final_project_wl2788.game_type(game_df)
    assert type(df) == pd.core.frame.DataFrame   

def test_type_number():
    actual = final_project_wl2788.type_number(game_df, 'Full Game')
    expected = 21
    assert actual == expected    
    
def test_title_max_min():
    actual = final_project_wl2788.title_max_min(game_df, 'min')
    expected = 'Free Kalaban (PC)'
    assert actual == expected
    
def test_title_length_type():
    df=final_project_wl2788.title_length_type(game_df)
    assert type(df) == pd.core.frame.DataFrame
    
    
def test_game_platform():
    df=final_project_wl2788.game_platform(game_df)
    assert type(df) == pd.core.frame.DataFrame
    
def test_worth_new():
    df=final_project_wl2788.worth_new(game_df, True)
    assert type(df) == pd.core.frame.DataFrame    
    
    
    
    
    
    
    
    
    
    
    
    
    