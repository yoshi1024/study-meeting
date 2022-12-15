#%%
#ライブラリのインポート
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
#%%
df_shutuba = pd.DataFrame()

for year in range(2010,2022):
    for month in range(1,13):
        #url_cal = 'https://nar.netkeiba.com/top/calendar.html?year={}&month={}&jyo_cd=48'.format(str(year),str(month))
        url_cal = 'https://race.netkeiba.com/top/calendar.html?year={}&month={}'.format(str(year),str(month))

        df_cal = pd.read_html(url_cal)[0]
        list_cal = [str(a) for a in sum(df_cal.values.tolist(), [])]
        list_day = [i.split()[0].zfill(2) for i in list_cal if '中山' in i]


        for day in list_day:
            for race_no in range(1,13):
                race_id = '{}48{}{}{}'.format(str(year), str(month).zfill(2), day, str(race_no).zfill(2))
                #url_race = 'https://nar.netkeiba.com/race/result.html?race_id={}&rf=race_list'.format(race_id)
                url_race = 'https://race.netkeiba.com/race/result.html?race_id={}&rf=race_list'.format(race_id)

                #url_past = 'https://nar.netkeiba.com/race/shutuba_past.html?race_id={}&rf=shutuba_submenu'.format(race_id)
                url_past = 'https://race.netkeiba.com/race/shutuba_past.html?race_id={}&rf=shutuba_submenu'.format(race_id)

                print(url_race)
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
# %%
df_result_past
# %%
#ライブラリのインポート
import pandas as pd

url_cal = 'https://race.netkeiba.com/top/calendar.html?rf=sidemenu'
df_cal = pd.read_html(url_cal)[0]
# %%
df_cal
# %%
list_cal = [str(a) for a in sum(df_cal.values.tolist(),[])]

# %%
list_day = [i.split()[0].zfill(2) for i in list_cal if '名古屋' in i]
