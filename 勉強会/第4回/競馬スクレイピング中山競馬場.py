#%%
import pandas as pd
import time
from tqdm.notebook import tqdm

def scrape_race_results(race_id_list, pre_race_results={}):
    race_results = pre_race_results
    for race_id in tqdm(race_id_list):
        if race_id in race_results.keys():
            continue
        try:
            url = "https://db.netkeiba.com/race/" + race_id
            race_results[race_id] = pd.read_html(url)[0]
            time.sleep(1)
        except IndexError:
            continue
        except:
            break
    return race_results
# %%
race_id_list = []
for place in range(1, 11, 1):
    for kai in range(1, 6, 1):
        for day in range(1, 9, 1):
            for r in range(1, 13, 1):
                race_id = (
                    "2010"
                    + str(place).zfill(2)
                    + str(kai).zfill(2)
                    + str(day).zfill(2)
                    + str(r).zfill(2)
                )
                race_id_list.append(race_id)
                
#%%
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
# %%
race_id_list
# %%
results = scrape_race_results(race_id_list)
for key in results:
    results[key].index = [key] * len(results[key])
results = pd.concat([results[key] for key in results], sort=False)
# %%
import requests
from bs4 import BeautifulSoup
import time
from tqdm.notebook import tqdm
import re

def scrape_race_info(race_id_list):
    race_infos = {}
    for race_id in tqdm(race_id_list):
        try:
            url = "https://db.netkeiba.com/race/" + race_id
            html = requests.get(url)
            html.encoding = "EUC-JP"
            soup = BeautifulSoup(html.text, "html.parser")

            texts = (
                soup.find("div", attrs={"class": "data_intro"}).find_all("p")[0].text
                + soup.find("div", attrs={"class": "data_intro"}).find_all("p")[1].text
            )
            info = re.findall(r'＼w+', texts) #Qiitaでバックスラッシュを打つとバグるので大文字にしてあります。
            info_dict = {}
            for text in info:
                if text in ["芝", "ダート"]:
                    info_dict["race_type"] = text
                if "障" in text:
                    info_dict["race_type"] = "障害"
                if "m" in text:
                    info_dict["course_len"] = int(re.findall(r"＼d+", text)[0]) #ここも同様に大文字にしてます。
                if text in ["良", "稍重", "重", "不良"]:
                    info_dict["ground_state"] = text
                if text in ["曇", "晴", "雨", "小雨", "小雪", "雪"]:
                    info_dict["weather"] = text
                if "年" in text:
                    info_dict["date"] = text
            race_infos[race_id] = pd.DataFrame(info_dict)
            time.sleep(1)
        except IndexError:
            continue
        except Exception as e:
            print(e)
            break
    return race_infos

race_id_list = results.index.unique()
race_infos = scrape_race_info(race_id_list)
for key in race_infos:
    race_infos[key].index = [key] * len(race_infos[key])
race_infos = pd.concat([pd.DataFrame(race_infos[key], index=[key]) for key in race_infos])
results = results.merge(race_infos, left_index=True, right_index=True, how='left')