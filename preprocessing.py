import numpy as np
import pandas as pd
import math

df1=pd.DataFrame(pd.read_excel('data1.xlsx',sheet_name=0))
df2=pd.DataFrame(pd.read_excel('data1.xlsx',sheet_name=1))
print(df1)
df1=df1.iloc[:,1:]
df2=df2.iloc[:,1:]

df1['总订货量']=df1.iloc[:,1:].sum(axis=1).reset_index(drop=True)
df2['总供货量']=df2.iloc[:,1:].sum(axis=1).reset_index(drop=True)
df2['周均供货量']=df2.iloc[:,1:241].sum(axis=1)/240
print(df1)
df=pd.DataFrame(df1['总订货量'])
df.insert(0,'总供货量',df2['总供货量'])
df.insert(0,'周均供货量',df2['周均供货量'])
df.insert(0, '订单完成率',df['总供货量']/df['总订货量'])

print(df)
#dfshangquan