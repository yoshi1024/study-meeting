df <- read.csv('./1212data/lesson1.csv',fileEncoding = 'sjis')

#注釈の列を削除
library(dplyr) 
df <- select(df, -注)

#都道府県名がないデータは除外
df <- df[df$西暦.年.== 2015,]

#欠損している行を削除
df <- na.omit(df)

df <- df[
    (df$都道府県コード!='00') &
    (df$都道府県コード!='0A') &
    (df$都道府県コード!='0B'),
]

df$都道府県コード <- as.numeric(df$都道府県コード)

df$人口.総数. <- as.numeric(df$人口.総数.)
df$人口.男. <- as.numeric(df$人口.男.)
df$人口.女. <- as.numeric(df$人口.女.)

df_touhoku <- df[df$都道府県コード < 8 ,]

# ggplot2パッケージ呼び出し
library(ggplot2)

# 作図
ggplot(data = df_touhoku, aes(x = 都道府県名, y = 人口.総数.)) + 
  geom_bar(stat = "identity") 

plot(df[,'人口.男.'],df[,'人口.女.'])

ggplot(data = df, mapping = aes(x = df[,'人口.男.'], y = df[,'人口.女.'])) +
  geom_point()

boxplot(df$人口.男.)

hist(df$人口.男.)