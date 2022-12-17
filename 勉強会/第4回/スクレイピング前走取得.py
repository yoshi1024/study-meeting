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
