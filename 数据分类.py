import pandas as pd
import numpy as np
data = pd.read_csv('数据预处理2.csv',encoding='gbk')
df1 = data.groupby(['大类编码','大类名称','中类编码','中类名称','小类编码','小类名称']).mean()
df1.to_csv('超市数据分类2.csv',encoding='gbk')
