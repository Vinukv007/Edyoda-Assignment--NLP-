# -*- coding: utf-8 -*-
"""SMS Spam Detection.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Vt9ONLDO4W-PgR_1OwT_NaHMf1P5Ufaa
"""

import pandas as pd
import numpy as np
import nltk
import re
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression

df=pd.read_csv('spam.csv',encoding='latin-1')
df.head()

# renaming columns and replacing spam or ham column with digits

df2=df[['v2','v1']]
df2.rename(columns={'v1':'type', 'v2':'message'}, inplace=True)

df2['type']=df2['type'].apply(lambda x:1 if x=='spam' else 0)
df2.head()

messages=df2.message.values

messages=[m.lower() for m in messages]
messages=[re.sub('\W+',' ', i) for i in messages]
messages=[re.sub('\s+',' ', i) for i in messages]

messages[:3]

nltk.download('stopwords')

sw=nltk.corpus.stopwords.words('english')

sw[:3]

msg_no_sw=[]
for msg in messages:
  pre_msg=[]
  for i in msg.split():
    if i not in sw:
      pre_msg.append(i)
  msg_no_sw.append(' '.join(pre_msg))

msg_no_sw[:3]

msg_no_sw=[re.sub('\d+','',m)for m in msg_no_sw]
msg_no_sw=[re.sub('\s\w{1,2}\s','',m)for m in msg_no_sw]
msg_no_sw=[re.sub('^\w{1,2}\s','',m)for m in msg_no_sw]
msg_no_sw=[re.sub('\s\w{1,2}$','',m)for m in msg_no_sw]
msg_no_sw=[re.sub('\s+',' ',m)for m in msg_no_sw]

msg_no_sw[:3]

from nltk.stem import PorterStemmer

ps=PorterStemmer()

new_msg=[]
for msg in msg_no_sw:
  pre_msg=[]
  for i in msg.split():
    pre_msg.append(ps.stem(i))
  new_msg.append(' '.join(pre_msg))

new_msg[:3]

cv=CountVectorizer()

x=cv.fit_transform(new_msg)
y=df2['type']

xtrain, xtest, ytrain, ytest=train_test_split(x,y, test_size=0.2,random_state=1, stratify=y)

lr=LogisticRegression()
lr.fit(xtrain, ytrain)
lr.score(xtest,ytest)

