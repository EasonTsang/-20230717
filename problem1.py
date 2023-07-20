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

# 中间型指标 -> 极大型指标
def dataDirection_2(datas, x_best):
    temp_datas = datas - x_best
    M = np.max(abs(temp_datas))
    answer_datas = 1 - abs(datas - x_best) / M  # 套公式
    return answer_datas

df['订单完成率']=dataDirection_2(df['订单完成率'],1)
print(df)

# # 正向化矩阵标准化
# def temp2(datas):
#     K = np.power(np.sum(pow(datas, 2), axis=1), 0.5)
#     for i in range(0, K.size):
#         for j in range(0, datas[i].size):
#             datas[i, j] = datas[i, j] / K[i]  # 套用矩阵标准化的公式
#     return datas

# df=temp2(df)
# print(df)

# # 计算得分并归一化
# def temp3(answer2):
#     list_max = np.array(
#         [np.max(answer2[0, :]), np.max(answer2[1, :]), np.max(answer2[2, :])])  # 获取每一列的最大值
#     list_min = np.array(
#         [np.min(answer2[0, :]), np.min(answer2[1, :]), np.min(answer2[2, :])])  # 获取每一列的最小值
#     max_list = []  # 存放第i个评价对象与最大值的距离
#     min_list = []  # 存放第i个评价对象与最小值的距离
#     answer_list = []  # 存放评价对象的未归一化得分
#     for k in range(0, np.size(answer2, axis=1)):  # 遍历每一列数据
#         max_sum = 0
#         min_sum = 0
#         for q in range(0, 3):  # 有三个指标
#             max_sum += np.power(answer2[q, k] - list_max[q], 2)  # 按每一列计算Di+
#             min_sum += np.power(answer2[q, k] - list_min[q], 2)  # 按每一列计算Di-
#         max_list.append(pow(max_sum, 0.5))
#         min_list.append(pow(min_sum, 0.5))
#         answer_list.append(min_list[k] / (min_list[k] + max_list[k]))  # 套用计算得分的公式 Si = (Di-) / ((Di+) +(Di-))
#         max_sum = 0
#         min_sum = 0
#     answer = np.array(answer_list)  # 得分归一化
#     return (answer / np.sum(answer))
# print(temp3(df['周均供货量']))

# df['周均供货量']=temp3(df['周均供货量'])
# df['订单完成率']=temp3(df['订单完成率'])
# df['总供货量']=temp3(df['总供货量'])

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

 