import csv
import datetime
import random
import codecs
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# 文件名
filename = './data.csv'

# 生成模拟数据
# 把数据以UTF8编码写入文件
with codecs.open(filename,"w","utf-8") as file:         #这里写通过文件对象f读写文件内容的语句   上下文管理语句with
    wr = csv.writer(file)
    # 写入标题
    wr.writerow(['日期','营业额'])
    # 生成模拟的数据
    startdate = datetime.date(2018,1,1)
    # 生成365个数据，根据需要可以调整
    for i in range(365):
        # 生成数据，并写入csv文件
        amount = 300 + i * 5 + random.randrange(100) # 营业额
        wr.writerow([str(startdate),amount])
        # 生成下一天
        startdate = startdate + datetime.timedelta(days=1)

# 1.读取csv文件，加载数据
df_obj = pd.read_csv('./data.csv')
print(df_obj)

# 2. 缺失值的处理，丢弃
df_obj.dropna()

# 3. 生成每天营业额的折线图
plt.rcParams['font.sans-serif']='SimHei'             # 设置中文显示
plt.plot(df_obj['营业额'])
plt.plot(linestyle='--',color = "blue")                  # 画图
plt.title('该商店2018年每天的营业额情况')             # 表标题
plt.xlabel('日期')                                      # X轴标签
plt.ylabel('营业额')                                    # Y轴标签
plt.savefig('first.png')                               # 保存图片
plt.show()                                               # 显示折线图

# 4. 按月统计，生成柱状图
df_obj1 = df_obj[:]
df_obj1['month'] = df_obj1['日期'].map(lambda x:x[:x.rindex('-')])
# 按照month进行分组求和
df_obj1 = df_obj1.groupby(by='month').sum()
# print(df_obj1)
x = np.array(range(1,13))
width = 0.75 # 柱的宽度
plt.bar(x,df_obj1['营业额'],width,label="营业额",alpha=0.6)#图的透明度alpha
plt.legend()                                                # 添加图例，标签label="营业额"
plt.xlabel('日期')
plt.ylabel('营业额（元）')
plt.title('该商店2018年每天的营业额情况')
plt.savefig('second.png')
plt.show()




# 5.查找营业额最大的月份的数据，并保存到文件
m = df_obj1['营业额'].max()
# print(m)
df_obj2 = df_obj1[df_obj1['营业额'] == m]
# print(df_obj2)
# 将结果保存到文件
max_filename = './maxMonth.txt'                    # 创建max_filename文件和路径
with codecs.open(max_filename,"w","utf-8") as f:   # "w"：写模式，如果文件已存在，先清空原有内容--以写模式打开文件     #这里写通过文件对象f读写文件内容的语句
    wr = csv.writer(f)
    # 写入标题
    wr.writerow(['营业额最大月份'])
    # 写入数据
    wr.writerow([m])



print(df_obj1[:3]['营业额'])
#四个季度
a = df_obj1[:3]['营业额'].sum()
b= df_obj1[3:6]['营业额'].sum()
c= df_obj1[6:9]['营业额'].sum()
d = df_obj1[9:12]['营业额'].sum()
print(a,b,c,d)

# 绘制 饼状图
plt.figure(figsize=(6,6))                           # 将画布设定为正方形，则绘制的饼图是正圆
label=['第一季度','第二季度','第三季度','第四季度']# 定义饼图的文本标签
explode=[0.01,0.01,0.01,0.01]                       # 设定各项距离圆心n个半径
plt.pie([a,b,c,d],labels=label,autopct='%1.1f%%',explode=explode)
plt.title('2018年4个季度的营业额分布情况')       # 饼图标题
plt.savefig('03.png')
plt.show()



