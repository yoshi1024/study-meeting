import pandas as pd

#データの読み込み
df = pd.read_csv('./1212data/lesson1.csv',encoding = 'shift_jis')

#注釈の列を削除
df = df.drop('注', axis=1)

#都道府県データのみ抽出
#都道府県名がないデータは除外

df = df.dropna(subset=['都道府県名'])

df = df[df['西暦（年）'] == 2015]

#都道府県データのみ抽出
df = df[~df['都道府県コード'].isin(['00','0A','0B'])]