import pandas as pd
import numpy as np
data = pd.read_csv('预处理.csv',engine='python')
df1 = data.groupby(['大类编码','大类名称','中类编码','中类名称','小类编码','小类名称']).sum()
df1.to_csv('超市分类数据1.0.csv',encoding='utf-8-sig')
