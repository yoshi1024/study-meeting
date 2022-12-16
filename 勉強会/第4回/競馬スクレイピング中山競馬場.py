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
