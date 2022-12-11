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

df['都道府県コード'] = df['都道府県コード'].astype(int)
df['人口（男）'] = df['人口（男）'].astype(int)
df['人口（総数）'] = df['人口（総数）'].astype(int)

df_touhoku = df[df.都道府県コード < 8]

%matplotlib inline
import matplotlib.pyplot as plt

plt.bar(df_touhoku['都道府県名'], df_touhoku['人口（総数）'])

pip install japanize-matplotlib

import japanize_matplotlib
import matplotlib.pyplot as plt

plt.bar(df_touhoku['都道府県名'], df_touhoku['人口（総数）'])

plt.scatter(
pd.Series(df['人口（男）'],dtype='int'),
pd.Series(df['人口（女）'],dtype='int'))

pd.Series(df['人口（男）'],dtype='int')

plt.scatter(
pd.Series(df['人口（男）'],dtype='int'),
pd.Series(df['人口（女）'],dtype='int'))

plt.title('Population')
plt.xlabel('man')
plt.ylabel('woman')

plt.show()

# 箱ひげ図
plt.boxplot(df['人口（男）'])
plt.show()

plt.hist(df['人口（男）'])
plt.show()