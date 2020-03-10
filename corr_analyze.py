import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from textblob import TextBlob
#为使控制台输出完整----------------------------------------------------------------------------------------------------------------------
pd.set_option('display.max_columns',1000)
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth',1000)
#----------------------------------------------------------------------------------------------------------------------
data=pd.read_csv(r'C:\Users\lenovo\Desktop\2020_Weekend2_Problems\Problem_C_Data\Problem_C_Data\hair_dryer.tsv',sep='\t',header=0)
date = pd.read_csv(r'C:\Users\lenovo\Desktop\date.csv')
def dealwith_vine(x):
    if x == 'Y':
        x = 1.5
    else:
        x = 1
    return x
def salescount(x):
    if x == 'Y':
        x = 1
    else:
        x = 0
    return x
def dealwith_verified_purchase(x):
    if x == 'Y':
        x = 1
    else:
        x = 0.2
    return x

data_quantified=pd.DataFrame()#新DF，用于存储量化后的data数据
data_quantified['review_date']=data['review_date']
data_quantified['star_rating']=data['star_rating']
data_quantified['vine_weigh'] = list(map(dealwith_vine, data['vine']))  # 将vine的权重调整为两倍
data_quantified['verified_purchase_weigh'] = list(map(dealwith_verified_purchase, data['verified_purchase']))  # 将未购买的评论调整未0.1
data_quantified['helpful_votes_weigh'] = (data['helpful_votes'])*0.1+1#+1将所有0投票的评论算进去
data_quantified['star_weigh'] = data_quantified['vine_weigh'] * data_quantified['verified_purchase_weigh'] #总权重 weight 改为weigh
data_quantified['star_rating_weighed']=data_quantified['star_rating']* data_quantified['star_weigh']
data_quantified['sales']=list(map(salescount, data['verified_purchase']))
data_quantified['review_date']=pd.to_datetime(data['review_date'])#标准时转换
data_quantified=data_quantified.set_index('review_date')
data_quantified['sales_cumsum']=data_quantified['sales'].cumsum()
data_quantified['star_cumsum']=(data_quantified['star_rating_weighed']*data_quantified['sales']).cumsum()#去除未付款者后进行计数
data_quantified['star_current']=data_quantified['star_cumsum']/data_quantified['sales_cumsum']
#print(data_quantified)
sales_sum=data_quantified.resample('M').sum()['sales']
data_M=data_quantified.resample('M').mean()
corr_star_sale=sales_sum.corr(data_M['star_rating'])
corr_star_weighed_sale=sales_sum.corr(data_M['star_rating_weighed'])
#print(sales_sum)
print(corr_star_sale)
print(corr_star_weighed_sale)
data_M['sales']=sales_sum
data_M=data_M.reset_index()
data['review_date']=pd.to_datetime(data['review_date'])
data_M['delta_date']=(data_M['review_date'] - data['review_date'][11469]).map(lambda x:x.days)#转换为数字格式的天数

x=data_M['delta_date'].to_list()
y=sales_sum.to_list()
x = np.array(x)
print('x is :\n',x)
y = np.array(y)
f1 = np.polyfit(x, y, 5)
print('f1 is :\n',f1)
sale_time = np.poly1d(f1)
print('p1 is :\n', sale_time)
#data_M_mean['sales'].plot()
#plt.show()
fig = plt.figure()
ax1=fig.add_subplot(2,1,1)
ax2=fig.add_subplot(2,1,2)
ax1.plot(data_M['sales'])
#ax2.plot(data_M_mean['star_current'])
ax2.plot(x,y)
plt.show()
#print(data_M_mean)
#print(weighed_mean)
#print(sales_sum)



