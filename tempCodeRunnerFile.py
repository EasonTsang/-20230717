# 计算得分并归一化
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
