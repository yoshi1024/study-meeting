#%%
import pandas as pd
import time
from tqdm.notebook import tqdm
import requests
from bs4 import BeautifulSoup
import time
from tqdm.notebook import tqdm
import re

race_id_list = []

for year in range(2010,2022):
    for kai in range(1, 6, 1):
        for day in range(1, 9, 1):
            for r in range(1, 13, 1):
                race_id = (
                    str(year).zfill(2)
                    + '06'
                    + str(kai).zfill(2)
                    + str(day).zfill(2)
                    + str(r).zfill(2)
                )
                race_id_list.append(race_id)

#%%
race_id_list[0]
#%%
df_shutuba = pd.DataFrame()
df_shutuba_1 = pd.DataFrame()

#race_id_list = race_id_list[0:10]

for race_id in tqdm(race_id_list):
    url_race = 'https://race.netkeiba.com/race/result.html?race_id={}&rf=race_list'.format(race_id)
    url_past = 'https://race.netkeiba.com/race/shutuba_past.html?race_id={}&rf=shutuba_submenu'.format(race_id)
    try:
        df_result = pd.read_html(url_race)[0]
        df_past = pd.read_html(url_past)[0]
        df_result_past = pd.merge(df_result, df_past, on='馬番')
        
        r = requests.get(url_race)
        soup = BeautifulSoup(r.content, 'html.parser')
        data1 = soup.find('div', class_='RaceData01').text
        df_result_past['距離'] = re.findall(r'\d+', data1)[2]
        df_result_past['フィールド'] = data1[data1.find('/')+2: data1.find('/')+3]
        df_result_past['馬場'] = data1[data1.find('馬場')+3: data1.find('馬場')+4]
    except:
        continue
    df_result_past['レースID'] = race_id
    df_shutuba= pd.concat([df_shutuba, df_result_past])
    #df_shutuba_1.append(df_result_past)

df_shutuba.to_csv('/Users/yoshida_ibuki/Documents/勉強会フォルダ/勉強会/勉強会/第4回/データ前走追加.csv',index=False)

# %%
df_result_past
# %%
df_shutuba
# %%
#いらないカラムを消す
df = df_shutuba.drop(['枠_x', '枠_y', '厩舎', '騎手斤量', '着差', '後3F', '印'], axis=1)
#特殊記号を消す
df['騎手'] = df['騎手'].str.replace('▲', '')
df['騎手'] = df['騎手'].str.replace('△', '')
df['騎手'] = df['騎手'].str.replace('☆', '')
df['騎手'] = df['騎手'].str.replace('★', '')
df['騎手'] = df['騎手'].str.replace('◇', '')

#1つのカラムに入っているデータを複数カラムに分ける
df_sex = df['性齢'].str.extract('([牝牡セ])(\d+)', expand=True)

#1つのカラムに入っているデータを複数カラムに分ける
df_sex = df['性齢'].str.extract('([牝牡セ])(\d+)', expand=True)
df['性'] = df_sex.loc[:, 0]
df['齢'] = df_sex.loc[:, 1]

df_weight = df['馬体重(増減)'].str.extract('(\d{3}).([+-0]\d*)', expand=True)
df['馬体重'] = df_weight.loc[:, 0]
df['体重増減'] = df_weight.loc[:, 1].str.replace('+', '', regex=True)

#「性齢」「馬体重（増減）」はいらないので消す
df = df.drop(['性齢', '馬体重(増減)'], axis=1)

#「前走」から必要なデータにわける
df_split = df['前走'].str.extract('(\d{4}.\d{2}.\d{2})\s(\w+)\s(\d*).*([ダ|芝])(\d+).*(\d:\d{2}.\d)\s(\w)\s(\d*)頭\s(\d*)番\s(\d*)人\s(\w+)\s(\d{2}[.]\d).+(\d{2}[.]\d).\s(\d{3}).([+-0]\d*).+\((-?\d*.\d{1})', expand=True)
#カラム名を指定
df_split.columns = ['日付', '場所', '着順', 'フィールド', '距離', 'タイム', '馬場', '出走馬数', '馬番', '人気', '騎手', '斤量', '後3F', '馬体重', '体重増減', '着差']
# %%
#文字列データを数値データにする
nagoya_mapping = {'中山': 1}
df_split['場所'] = df_split['場所'].map(nagoya_mapping)

field_mapping = {'芝': 1, 'ダ': 2, '障': 3}
df_split['フィールド'] = df_split['フィールド'].map(field_mapping)

condition_mapping = {'良': 1, '稍': 2, '重': 3, '不': 4}
df_split['馬場'] = df_split['馬場'].map(condition_mapping)

#騎手のユニーク値から辞書をつくる
jockey_mapping = dict(zip(df_split['騎手'].unique().tolist(), range(1, len(df_split['騎手'].unique().tolist()) + 1)))

#文字列から数値に変換する
df_split['騎手'] = df_split['騎手'].map(jockey_mapping)

#%%
#タイムを秒表記にする
base_time = pd.to_datetime('00:00.0', format='%M:%S.%f')

df_split['タイム'] = pd.to_datetime(df_split['タイム'], format='%M:%S.%f') - base_time
df_split['タイム'] = df_split['タイム'].dt.total_seconds()
# %%
df_split
# %%
