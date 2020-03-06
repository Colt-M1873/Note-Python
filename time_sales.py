import pandas as pd
import  numpy as np
import matplotlib.pyplot as plt
import sys
import time
orig=pd.read_csv("C:\\Users\lenovo\Desktop\hairdryer.csv")
#orig['review_date']=pd.to_datetime(orig['review_date'])
star_time=orig[['star_rating','review_date']]
sales_star_time=pd.DataFrame(columns=('formulated_timeline','salescount','totalstar','averagestar'))
origtimeline=orig['review_date'].tolist()
#print(origtimeline)
newtimeline=[]
j=-1
a=-1
for i in origtimeline:
    a+=1
    if i not in newtimeline:
        newtimeline.append(i)
        j = j + 1
        sales_star_time.loc[j,'formulated_timeline'] = star_time.loc[a, 'review_date']
        sales_star_time.loc[j,'salescount']=1
        sales_star_time.loc[j,'totalstar']=star_time.loc[a, 'star_rating']
    else :
        sales_star_time.loc[j,'salescount']+=1
        sales_star_time.loc[j,'totalstar']+=star_time.loc[a, 'star_rating']
print(sales_star_time.head(20))
sales_star_time['averagestar'] = sales_star_time.apply(lambda x: x['totalstar'] /   x['salescount'], axis=1)
sales_star_time['formulated_timeline']=pd.to_datetime(sales_star_time['formulated_timeline'])
print(sales_star_time)
# data=pd.Series(np.random.randn(1000),index=np.arange(1000))
# data = data.cumsum()
# data.plot()
# plt.show()
# data = pd.DataFrame(np.random.randn(10,4).cumsum(0) ,columns=['a','b','c','d'],index=np.arange(0,100,10)data.plot()plt.show())
# #sales_star_time.plot()
# plt.show()