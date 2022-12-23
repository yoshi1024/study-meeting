#%%
import pandas as pd
import time
import numpy as np
import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup
import time
from tqdm.notebook import tqdm
import seaborn as sns
from itertools import cycle
from sklearn.model_selection import train_test_split
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
import re
from sklearn.metrics import precision_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix
from pandas.plotting import scatter_matrix
import warnings # 実行に関係ない警告を無視
warnings.filterwarnings('ignore')
import lightgbm as lgb #LightGBM
from sklearn import datasets
from sklearn.metrics import log_loss # モデル評価用(logloss)     
from sklearn.metrics import roc_auc_score # モデル評価用(auc)

df_2010_2021 = pd.read_csv('/Users/yoshida_ibuki/Documents/勉強会フォルダ/勉強会/勉強会/第4回/データ前走追加.csv')
df_2022 = pd.read_csv('/Users/yoshida_ibuki/Documents/勉強会フォルダ/勉強会/勉強会/第4回/データ前走追加2022.csv')
# %%
df_2010_2021
# %%
df_2022
# %%  merge　２０２１：８１７１6件　２０２２：６５２０件

# %%  前処理　人気・オッズの列を削除

# %% 機械学習
