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