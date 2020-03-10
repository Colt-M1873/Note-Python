import pandas as pd
import matplotlib.pyplot as plt
from textblob import TextBlob
#为使控制台输出完整----------------------------------------------------------------------------------------------------------------------
pd.set_option('display.max_columns',1000)
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth',1000)
#----------------------------------------------------------------------------------------------------------------------
data=pd.read_csv(r'C:\Users\lenovo\Desktop\2020_Weekend2_Problems\Problem_C_Data\Problem_C_Data\microwave.tsv',sep='\t')#, header=0
reviewheadlist=data['review_headline'].to_list()
reviewbodylist=data['review_body'].to_list()
print(reviewheadlist)
print(reviewbodylist)


#data['review_date']=pd.to_datetime(data['review_date'])#标准时转换
#data=data.set_index('review_date')
#data=data.resample('D').mean()
