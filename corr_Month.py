import pandas as pd
import  numpy as np
import matplotlib.pyplot as plt
from textblob import TextBlob
pd.set_option('display.max_columns',1000)
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth',1000)
data=pd.read_csv(r'C:\Users\lenovo\Desktop\2020_Weekend2_Problems\Problem_C_Data\Problem_C_Data\hair_dryer.tsv',sep='\t',header=0)
date = pd.read_csv(r'C:\Users\lenovo\Desktop\date.csv')
def verified_purchase_check(x):
    if x == 'Y':
        x = 1
    else:
        x = 0.1
    return x
def salescount(x):
    if x == 'Y':
        x = 1
    else:
        x = 0
    return x
def vine_check(x):
    if x == 'Y':
        x = 1.5
    else:
        x = 1
    return x

def review_to_score(text):
    if text=="Five Stars":
        score=5
    elif text == "Four Stars":
        score=4
    elif text=="Three Stars":
        score=3
    elif text=="Two Stars":
        score=2
    elif text=="One Star":
        score=1
    elif type(text)==str:
        blob = TextBlob(text)
        score=blob.sentiment.polarity*2.5+2.5
    else:
        score=2.5
    return score

data['review_date']=pd.to_datetime(data['review_date'])

data_quantified=pd.DataFrame()
data_quantified['review_date']=data['review_date']
data_quantified['date_delta']=(data['review_date']-data['review_date'][11469]).map(lambda x:x.days)#转换为数字格式的天数
data=data.set_index('review_date')
data_quantified=data_quantified.set_index('review_date')
data_quantified['star_rating']=data['star_rating']
data_quantified['review_headline_score']=list(map(review_to_score,data['review_headline']))#量化
data_quantified['review_body_score']=list(map(review_to_score,data['review_body']))#
data_quantified['vine_weigh'] = list(map(vine_check, data['vine']))  # 将vine的权重调整为两倍
data_quantified['verified_purchase_weigh'] = list(map(verified_purchase_check, data['verified_purchase']))  # 将未购买的评论调整未0.1
data_quantified['helpful_votes_weigh'] = 1 + data['helpful_votes']#+1将所有0投票的评论算进去
data_quantified['weigh'] = data_quantified['vine_weigh'] * data_quantified['verified_purchase_weigh'] #* data_quantified['helpful_votes_weigh']#总权重 weight 改为weigh
data_quantified['sales']=list(map(salescount, data['verified_purchase']))
data_quantified['star_rating_weighed']=data_quantified['star_rating']* data_quantified['weigh']
data_quantified['review']=(0.5*data_quantified['review_headline_score']+0.5*data_quantified['review_body_score'])/(0.28+0.55)
data_quantified['review_weighed']=data_quantified['review']*data_quantified['weigh']
data_quantified['fameindex']=data_quantified['review_weighed']*0.5+0.5*data_quantified['star_rating_weighed']
data_quantified['sales_cumsum']=data_quantified['sales'].cumsum()
data_quantified['fameindex_cumsum']=(data_quantified['fameindex']*data_quantified['sales']).cumsum()
data_quantified['star_cumsum']=(data_quantified['star_rating_weighed']*data_quantified['sales']).cumsum()#去除未付款者后进行计数
data_quantified['star_current']=data_quantified['star_cumsum']/data_quantified['sales_cumsum']#当前面板显示的星数
data_quantified['fameindex_current']=data_quantified['fameindex_cumsum']/data_quantified['sales_cumsum']#当前面板显示的星数
sales_sum=data_quantified.resample('M').sum()['sales']
data_M=data_quantified.resample('M').mean()
data_M['sales']=sales_sum#只有销量需要做每月累计，其他如评论和星级等只需做每单均值
corr_star_review=data_quantified['star_rating'].corr(data_quantified['review'])
print('Correlation index between star and review is :',corr_star_review)
data_M=data_M.reset_index()
data=data.reset_index()
data['review_date']=pd.to_datetime(data['review_date'])
data_M['delta_date']=(data_M['review_date'] - data['review_date'][11469]).map(lambda x:x.days)#转换为数字格式的天数

data_M['fameindex']=data_M['fameindex'].fillna(method='ffill')
data_M['fameindex_current']=data_M['fameindex_current'].fillna(method='ffill')

x=data_M['delta_date'].to_list()
x = np.array(x)
salesarray=sales_sum.to_list()
salesarray = np.array(salesarray)
fameindexarray=data_M['fameindex'].to_list()
fameindexarray = np.array(fameindexarray)
famecurrentarray=data_M['fameindex_current'].to_list()
famecurrentarray= np.array(famecurrentarray)
f1 = np.polyfit(x, salesarray, 5)
f2 = np.polyfit(x, fameindexarray, 5)
f3 = np.polyfit(x, famecurrentarray, 5)
sale_time = np.poly1d(f1)
fame_time=np.poly1d(f2)
fame_current_time=np.poly1d(f3)
print('Sale_time fitting polynomial is :\n', sale_time)
print('Fame_time fitting polinomial is :\n', fame_time)
print('Current fame-time fitting polinomial is :\n', fame_current_time)
data_M=data_M.set_index('review_date')
fig = plt.figure()
#plt.title('pacifier')
ax1=fig.add_subplot(3,1,1)
ax2=fig.add_subplot(3,1,2)
ax1.plot(data_M['sales'],label='Sales_time')
ax2.plot(data_M['fameindex'],label='Fameindex_time')
axpp=fig.add_subplot(3,1,3)
axpp.plot(data_M['fameindex_current'],label='Famecurrent_time')
ax1.legend()
ax2.legend()
axpp.legend()

fig2 = plt.figure()
plt.title('hair_dryer')
ax3=fig2.add_subplot(2,1,1)
ax4=fig2.add_subplot(2,1,2)
ax3.plot(x,salesarray,'o')
ax3.plot(x,sale_time(x),label='Sales_time')
ax4.plot(x, famecurrentarray,'o')
ax4.plot(x,fame_current_time(x),label='Famecurrent_time')
ax3.legend()
ax4.legend()
print(sale_time(4961))
print(fame_current_time(4961))
plt.show()

