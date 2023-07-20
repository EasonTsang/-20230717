import numpy as np
import pandas as pd
import math

df1=pd.DataFrame(pd.read_excel('data1.xlsx',sheet_name=0))
df2=pd.DataFrame(pd.read_excel('data1.xlsx',sheet_name=1))

df1=df1.iloc[:,1:]
df2=df2.iloc[:,1:]

df1['总订货量']=df1.iloc[:,1:].sum(axis=1).reset_index(drop=True)
df2['总供货量']=df2.iloc[:,1:].sum(axis=1).reset_index(drop=True)
df2['周均供货量']=df2.iloc[:,1:241].sum(axis=1)/240

df=pd.DataFrame(df1['总订货量'])
df.insert(0,'总供货量',df2['总供货量'])
df.insert(0,'周均供货量',df2['周均供货量'])
df.insert(0, '订单完成率',df['总供货量']/df['总订货量'])
df.drop('总订货量',axis=1,inplace=True)
print(df)

def entropyWeight(data):
	data = np.array(data)
	# 归一化
	P = data / data.sum(axis=0)

	# 计算熵值
	E = np.nansum(-P * np.log(P) / np.log(len(data)), axis=0)

	# 计算权系数
	return (1 - E) / (1 - E).sum()

entropyWeight(df)
print(entropyWeight(df))

def topsis(data, weight=None):
	# 归一化
	data = data / np.sqrt((data ** 2).sum())

	# 最优最劣方案
	Z = pd.DataFrame([data.min(), data.max()], index=['负理想解', '正理想解'])

	# 距离
	weight = entropyWeight(data) if weight is None else np.array(weight)
	Result = data.copy()
	Result['正理想解'] = np.sqrt(((data - Z.loc['正理想解']) ** 2 * weight).sum(axis=1))
	Result['负理想解'] = np.sqrt(((data - Z.loc['负理想解']) ** 2 * weight).sum(axis=1))

	# 综合得分指数
	Result['综合得分指数'] = Result['负理想解'] / (Result['负理想解'] + Result['正理想解'])
	Result['排序'] = Result.rank(ascending=False)['综合得分指数']

	return Result, Z, weight

Result, Z, weight = topsis(df)
Result.to_excel('result.xlsx')
