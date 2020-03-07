import pandas as pd
import  numpy as np
import matplotlib.pyplot as plt
import sys
import time
orig=pd.read_csv("C:\\Users\lenovo\Desktop\hairdryer_timeindexrev.csv")
orig['formulated_timeline']=pd.to_datetime(orig['formulated_timeline'])
orig=orig.set_index('formulated_timeline')
orig1=orig.resample('M').sum()#求和重采样
orig2=orig.resample('M').mean()#均值重采样
print(orig)
data=orig1['salescount']#本月总销量
data2=orig2['averagestar']#本月评分单件均值
Month_sale_star=pd.DataFrame()
Month_sale_star['salescount_M']=data
Month_sale_star['averagestar']=data2
print(Month_sale_star)
Month_sale_star.to_csv("C:\\Users\lenovo\Desktop\hairdryer_Sales_Star_M.csv")
Month_sale_star.plot()
plt.show()
