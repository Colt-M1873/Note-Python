import pandas as pd
data=pd.read_csv(r'C:\Users\lenovo\Desktop\2020_Weekend2_Problems\Problem_C_Data\Problem_C_Data\hair_dryer.tsv',sep='\t',header=0)
date = pd.read_csv(r'C:\Users\lenovo\Desktop\date.csv')
# 处理日期格式
def get_date(x):
    month, day, year = x.split('/')
    if int(day) < 10:
        day = '0' + day
    if int(month) < 10:
        month = '0' + month
    return year + month + day
data['review_date'] = list(map(get_date, data['review_date']))
date['date'] = list(map(get_date, date['date']))
#date['date'] = list(map(str, date['date']))  # str用于转成字符串

# # 得到data区间内的自然日序列
# date['date'] = list(map(str, date['date']))  # str用于转成字符串
data_star = data['star_rating'].groupby(data['star_rating']).count()  # 按评分分组并计数
#date = date[~(date['date'] < min(list(data['review_date'])))]
#date = date[~(date['date'] > max(list(data['review_date'])))]
date.columns = ['review_date']  # 截取data区间内的所有自然日
# ----------------------------------------------------------------------------------------------------------------------------
# 处理评论客户是否购买商品
data_verified_purchase_Y = data[data['verified_purchase'] == 'Y']  # 已购买商品的客户的评分
data_verified_purchase_N = data[~(data['verified_purchase'] == 'Y')]  # 未购买商品的客户的评分
# # 已购买商品的客户的评分分布
data_verified_purchase_Y_star = data_verified_purchase_Y['star_rating'].groupby(
    data_verified_purchase_Y['star_rating']).count()
# 已购买商品的客户的评分分布
data_verified_purchase_N_star = data_verified_purchase_N['star_rating'].groupby(
    data_verified_purchase_N['star_rating']).count()
#
# # ----------------------------------------------------------------------------------------------------------------------------
# # 处理客户身份是否是vine
data_vine_Y = data[data['vine'] == 'Y']  # 是vine数据
data_vine_N = data[~(data['vine'] == 'Y')]  # 不是vine数据
# vine客户的评论分布
data_vine_Y = data_vine_Y['star_rating'].groupby(data_vine_Y['star_rating']).count()
data_vine_N = data_vine_N['star_rating'].groupby(data_vine_N['star_rating']).count()
#
# 处理vine和verified_purchase
# 给未购买却评分的权重降至10%，给vine的权重调整为2
def dealwith_verified_purchase(x):
    if x == 'Y':
        x = 1
    else:
        x = 0.1
    return x
def dealwith_vine(x):
    if x == 'Y':
        x = 2
    else:
        x = 1
    return x
data['vine'] = list(map(dealwith_vine, data['vine']))  # 将vine的权重调整为两倍
data['verified_purchase'] = list(map(dealwith_verified_purchase, data['verified_purchase']))  # 将未购买的评论调整未0.1

# ----------------------------------------------------------------------------------------------------------------------------
# 讲对评论点击helpful的数量作为认同评分
data['helpful_votes'] = 1 + data['helpful_votes']#+1将所有0投票的评论算进去

data['star_rating_'] = data['star_rating'] * data['vine'] * data['verified_purchase'] * data['helpful_votes']  # 赋权评分
data['weight'] = data['vine'] * data['verified_purchase'] * data['helpful_votes']

star = data['star_rating_'].groupby(data['review_date']).sum()  # 每日得到的评分合计
volume = data_verified_purchase_Y['star_rating'].groupby(
    data_verified_purchase_Y['review_date']).count()  # 每日评论数目，销量的代理变量，不含未购买商品的评论
weight_daily = data['weight'].groupby(data['review_date']).sum()  # 每日评论总权重

star_ = star.cumsum()  # 累计评分合计
volume_ = volume.cumsum()  # 累计评论数
weight_daily_ = weight_daily.cumsum()  # 累计评分权重

Favorable_rate = star_ / weight_daily_
volume__ = pd.DataFrame([volume]).T
volume__ = volume__.reset_index()

Favorable_rate = pd.DataFrame([Favorable_rate]).T
Favorable_rate = Favorable_rate.reset_index()

result1 = pd.merge(Favorable_rate, volume__, on=['review_date'], how='left')
result1 = result1.fillna(0)
result1.columns = ['review_date', 'star_rating', 'Cumulative sales volume']
result1['Cumulative sales volume'] = result1['Cumulative sales volume'].cumsum()  #
result1 = pd.merge(date, result1, on='review_date', how='left')
result1 = result1.fillna(method='ffill')

# 得到每一类评分的累计数量
data1 = data[['star_rating', 'review_date']]
data1['count'] = 1
datanew = data1.groupby(['star_rating', 'review_date']).sum()
datanew = datanew.reset_index()

datanew = datanew.set_index(['review_date', 'star_rating'])
datanew = datanew.unstack()
datanew = datanew.fillna(0)
datanew.columns = ['1', '2', '3', '4', '5']
result2 = datanew.cumsum()  # 每一类评分累计
result2 = pd.merge(date, result2, on='review_date', how='left')
result2 = result2.fillna(method='ffill')

# 得到已购买商品的评论的每一类评分的累计数量
data1 = data_verified_purchase_Y[['star_rating', 'review_date']]
data1['count'] = 1
datanew = data1.groupby(['star_rating', 'review_date']).sum()
datanew = datanew.reset_index()
datanew = datanew.set_index(['review_date', 'star_rating'])
datanew = datanew.unstack()
datanew = datanew.fillna(0)
datanew.columns = ['1', '2', '3', '4', '5']
result3 = datanew.cumsum()  # 每一类评分累计
result3 = pd.merge(date, result3, on='review_date', how='left')
result3 = result3.fillna(method='ffill')

# 得到未购买商品的评论的每一类评分的累计数量
data1 = data_verified_purchase_N[['star_rating', 'review_date']]
data1['count'] = 1
datanew = data1.groupby(['star_rating', 'review_date']).sum()
datanew = datanew.reset_index()
datanew = datanew.set_index(['review_date', 'star_rating'])
datanew = datanew.unstack()
datanew = datanew.fillna(0)
datanew.columns = ['1', '2', '3', '4', '5']
result4 = datanew.cumsum()  # 每一类评分累计
result4 = pd.merge(date, result4, on='review_date', how='left')
result4 = result4.fillna(method='ffill')
result4 = result4.fillna(0)