#任务1.1
""" import pandas as pd
import numpy as np """
""" data=pd.read_csv('超市数据.csv',engine='python',encoding='gbk')
data.pop('规格型号')
data.pop('单位')
data.pop('销售月份')
data.pop('商品编码')
data.index=data['顾客编号']
data.pop('顾客编号')
data.销售日期=pd.to_datetime(data['销售日期'],format='%Y%m%d',errors='coerce')
data.to_csv('预处理.csv',encoding='utf-8-sig') """
 
""" #任务1.2
data12=pd.read_csv('预处理.csv',engine='python')
df12=data12.groupby('大类名称').sum('销售金额')
sales=df12['销售金额']
sales.to_csv('大类商品销售金额.csv',encoding='utf-8-sig')
 
#任务1.3
df13=data12.groupby(['中类名称','是否促销']).sum('销售金额')
sales13=df13['销售金额']
sales13.to_csv('种类是否促销销售金额.csv',encoding='utf-8-sig')
 
 
#任务1.4
df14=data12.groupby('商品类型')
data14=df14.get_group('生鲜')
data141=df14.get_group('一般商品')
data141=data141.groupby('销售日期').sum('销售金额')
data14=data14.groupby('销售日期').sum('销售金额')
x=len(data14)
fresh=[]
ord=[]
sum14=0
sum141=0
lst14=data14['销售金额'].tolist()
lst141=data141['销售金额'].tolist()
for i in range(0,x):
    sum14=sum14+lst14[i]
    sum141=sum141+lst141[i]
    if (i+1)%7==0:
        fresh.append(sum14)
        ord.append(sum141)
        sum14=0
        sum141=0
data14=pd.DataFrame({'生鲜':fresh,'一般商品':ord},index=range(1,len(fresh)+1))
data14.to_csv('生鲜一般每周销售.csv',encoding='utf-8-sig')
 
#任务1.5
data12.销售日期=pd.to_datetime(data12['销售日期'],format='%Y/%m/%d')
data12['月']=data12['销售日期'].dt.month
df15=data12.groupby('月')
data15={}
for i in range(1,5):
    df151=df15.get_group(i)
    con = df151.groupby('顾客编号').sum('销售金额')
    day = df151.groupby(['顾客编号','销售日期']).size()
    day=day.groupby('顾客编号').size()
    data15['{:d}月消费天数'.format(i)] = day
    data15['{:d}月消费额'.format(i)]=con['销售金额']
    data15['{:d}月消费天数'.format(i)]=day
data15=pd.DataFrame(data15)
data15=data15.fillna(value=0)
data15.to_csv('客户每月销售金额及天数.csv',encoding='utf-8-sig') """
import pandas as pd
data_csv = pd.read_csv(r"超市数据源.csv", encoding='gbk')
print("原始数据数量" + str(len(data_csv)))
data_csv.drop_duplicates(inplace=True)
# how = 'any' 即去除所有的空值
data_csv = data_csv.dropna(how='any')
#单位标准化，减小精度对数据处理的干扰，故对数值进行标准化操作，保留5位小数；
data_csv["销售金额"] = data_csv["销售金额"].round(decimals=5)
#日期进行合法性验证，将日期转化为datetime类型，将非法日期剔除，最后使用去空值操作去除
# errors='coerce' 忽略不合法的值，置为null
data_csv["销售日期"] = pd.to_datetime(data_csv["销售日期"],format='%Y%m%d',errors='coerce')
print(data_csv.isnull().sum())
data_csv = data_csv.dropna(how='any')
#验证销售金额、单价和数量
data_csv_check = data_csv[data_csv["是否促销"]=='否'].eval('应付减实付 =(商品单价*销售数量 - 销售金额)')
print(data_csv_check[data_csv_check["应付减实付"] > 1]["大类名称"].value_counts())
#删除商品总额为零的数据
data_csv = data_csv.drop(data_csv[data_csv["销售金额"] == 0].index)  
#数据异常处理
xiaoshoujine_fushu = data_csv[data_csv["销售金额"] < 0]
xiaoshoushuliang_fushu = data_csv[data_csv["销售数量"] < 0]
print((xiaoshoujine_fushu == xiaoshoushuliang_fushu).sum())
for i in range (len(xiaoshoushuliang_fushu)):
    data_csv.drop(data_csv[
                        (data_csv["顾客编号"] == list(xiaoshoushuliang_fushu["顾客编号"])[i]) &
                        (data_csv["小类名称"] == list(xiaoshoushuliang_fushu["小类名称"])[i]) &
                        (abs(data_csv["销售金额"]) == abs(list(xiaoshoushuliang_fushu["销售金额"])[i]))
                    ].index, inplace=True)
#数据冗余处理
print("去冗余，交叉验证")
print(pd.crosstab(data_csv['小类编码'],data_csv["商品编码"],margins_name=True))
print("\n")
print(pd.crosstab(data_csv['小类编码'],data_csv["小类名称"],margins_name=True))
print(pd.crosstab(data_csv['中类编码'],data_csv["中类名称"],margins_name=True))
print(pd.crosstab(data_csv['大类编码'],data_csv["大类名称"],margins_name=True))

data_csv.to_csv(r"分类测试2.csv", index=False,index_label=False,encoding='gbk')
print("task1_2 completed")

