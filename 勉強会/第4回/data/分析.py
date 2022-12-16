#%%
import pandas as pd
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from itertools import cycle
from sklearn.model_selection import train_test_split
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder

keiba_data = pd.read_csv('/Users/yoshida_ibuki/Documents/勉強会フォルダ/勉強会/勉強会/第4回/データ完全版.csv')

# %%
keiba_data
# %%
keiba_data.isnull().sum()
# %%
#欠損値処理
#keiba_data.drop(columns=["タイム"],inplace=True)
keiba_data.drop(columns=["着差"],inplace=True)
keiba_data.dropna(subset=["人気"],inplace=True)

keiba_data.dtypes
# %%

keiba_data["性別"]=keiba_data['性齢'].str[0:1].astype(str)
keiba_data["年齢"]=keiba_data['性齢'].str[1:].astype(int)

keiba_data
# %%
keiba_data["増減"]=keiba_data['馬体重'].str[3:].astype(str)
keiba_data["馬体重"]=keiba_data['馬体重'].str[:3].astype(int)
# %%
keiba_data["増減"] = keiba_data["増減"].str.replace('(','')
keiba_data["増減"] = keiba_data["増減"].str.replace(')','')
keiba_data["増減"] = keiba_data["増減"].str.replace('+','')
keiba_data["増減" ]= keiba_data['増減'].astype(int)

keiba_data
#%%
# rankの確認
keiba_data["着順"].unique()
delete_index = keiba_data.index[(keiba_data["着順"]=="中") | (keiba_data["着順"]=="失")|(keiba_data["着順"]=="10(降)") | (keiba_data["着順"]=="4(降)")|(keiba_data["着順"]=="12(降)") | (keiba_data["着順"]=="13(降)")|(keiba_data["着順"]=="5(降)")|(keiba_data["着順"]=="2(降)") | (keiba_data["着順"]=="3(降)")]
keiba_data.drop(delete_index,inplace=True)
keiba_data["着順"].unique()
keiba_data["着順" ]= keiba_data['着順'].astype(int)

# %%
keiba_data.isnull().sum()
keiba_data.dtypes
#%%
keiba_data["単勝"].unique()
keiba_data["単勝"]= keiba_data['単勝'].astype(float)

# %%
#labelencoderを使って、カテゴリ変数を変換。
le=LabelEncoder()
keiba_categorical = keiba_data[["性別","性齢","騎手","調教師"]].apply(le.fit_transform)
#keiba_categorical = keiba_categorical.rename(columns={"race_name":"race_name_c","filed":"field_c","gender":"gender_c","horse_name":"horse_name_c","course":"course_c","head_count":"head_count_c","trainerA":"trainerA_c","trainerB":"trainerB_c","jackie":"jackie_c"})
keiba_data = pd.concat([keiba_data,keiba_categorical],axis=1)
# %%
keiba_data.dtypes
# %%
keiba_data.drop(columns=["タイム"],inplace=True)
keiba_data.drop(columns=["馬名"],inplace=True)

# %%
# 1,2,3着かそれ以外かを分割して、２値分類問題にする。
keiba_data = keiba_data.assign(target = (keiba_data['着順'] <= 3).astype(int))
# %%
#!pip install lightgbm

!brew install libomp
!pip uninstall lightgbm
!pip install lightgbm
#%%
# trainデータおよびtestデータの分割と特徴量および目的変数の分割
import lightgbm as lgb
X = keiba_data.drop(['着順','target'], axis=1)
y = keiba_data['target']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=0)

#データの変換
lgb_train = lgb.Dataset(X_train, y_train)
lgb_eval = lgb.Dataset(X_test, y_test)
# %%
