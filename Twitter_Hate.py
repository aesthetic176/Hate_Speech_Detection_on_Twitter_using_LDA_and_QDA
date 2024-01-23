# -*- coding: utf-8 -*-
"""moneesh.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1hx9qwnMCatvOwOmyYcSfx_LUfJ3CETqr
"""

data_path = r"/content/train_E6oV3lV.csv"

pip install scikit-plot

pip install pandas-profiling

# Commented out IPython magic to ensure Python compatibility.
import pandas_profiling
import nltk
import numpy as np
import pandas as pd
import re
import matplotlib.pyplot as plt
import seaborn as sb
from nltk.corpus import stopwords
import warnings
warnings.filterwarnings("ignore")
#import unidecode
from wordcloud import WordCloud
from nltk.stem import WordNetLemmatizer
nltk.download('wordnet')
from nltk.stem import PorterStemmer
nltk.download('punkt')
from nltk.tokenize import word_tokenize
import matplotlib.animation as animation
import operator
import plotly.express as px
from collections import Counter
# %matplotlib inline

import pandas as pd
data_frame = pd.read_csv(data_path)

def print_data_information():
  print("Dimention of the data set:",data_frame.shape)
  print("Tweets with NA value:",data_frame['tweet'].isna().sum())
  print("Labels with NA values:",data_frame['label'].isna().sum())
  print("Printing top 10 values of the data set")
  print("*****************************************")
  print(data_frame.head())

print_data_information()

pip install unidecode

#Code for removing slang words
d = {'luv':'love','wud':'would','lyk':'like','wateva':'whatever','ttyl':'talk to you later',
               'kul':'cool','fyn':'fine','omg':'oh my god!','fam':'family','bruh':'brother',
               'cud':'could','fud':'food'} ## Need a huge dictionary
lemmatizer = WordNetLemmatizer()

def preprocess_data_frame():
  data_frame['clean_tweet'] = data_frame['tweet'].apply(lambda x : ' '.join([tweet for tweet in x.split()if not tweet.startswith("@")])) #Remove @
  data_frame['clean_tweet'] = data_frame['clean_tweet'].apply(lambda x : ' '.join([tweet for tweet in x.split() if not tweet == '\d*'])) #Remove numbers
  #data_frame['clean_tweet'] = data_frame['clean_tweet'].apply(lambda x : ' '.join([unidecode.unidecode(word) for word in x.split()]))   #Remove greek symbols
  data_frame['clean_tweet'] = data_frame['clean_tweet'].apply(lambda x : ' '.join([word for word in x.split() if not word == 'h(m)+' ])) #Remove hm*
  data_frame['clean_tweet'] = data_frame['clean_tweet'].apply(lambda x : ' '.join(d[word] if word in d else word for word in x.split())) #Replace slang words
  data_frame['clean_tweet'] = data_frame['clean_tweet'].apply(lambda x : ' '.join([lemmatizer.lemmatize(word) for word in x.split()]))  #Lemmatization

preprocess_data_frame()

data_frame

data_frame['label'].value_counts()

fig = plt.figure(figsize=(5,5))
sns.countplot(x='label', data = data_frame)

fig = plt.figure(figsize=(7,7))
colors = ("red", "gold")
wp = {'linewidth':2, 'edgecolor':"black"}
tags = data_frame['label'].value_counts()
explode = (0.1, 0.1)
tags.plot(kind='pie',autopct = '%1.1f%%', shadow=True, colors = colors, startangle =90,
         wedgeprops = wp, explode = explode, label='')
plt.title('Distribution of sentiments')

#Tokenization
corpus = []
#ps = PorterStemmer()
for i in range(0,31962):
    tweet = data_frame['clean_tweet'][i]
    tweet = tweet.lower()
    tweet = tweet.split()
    #tweet = [ps.stem(word) for word in tweet if not word in set(stopwords.words('english'))]
    tweet = ' '.join(tweet)
    corpus.append(tweet)

len(corpus)

pip install wordcloud

normal_words = ' '.join([word for word in data_frame['clean_tweet'][data_frame['label'] == 0]])
wordcloud = WordCloud(width = 800, height = 500, max_font_size = 110,max_words = 100).generate(normal_words)
print('Normal words')
plt.figure(figsize= (12,8))
plt.imshow(wordcloud, interpolation = 'bilinear',cmap='viridis')
plt.axis('off')

normal_words = ' '.join([word for word in data_frame['clean_tweet'][data_frame['label'] == 1]])
wordcloud = WordCloud(width = 800, height = 500, max_font_size = 110,max_words = 100).generate(normal_words)
print('Normal words')
plt.figure(figsize= (12,8))
plt.imshow(wordcloud, interpolation = 'bilinear')
plt.axis('off')

#Techniques to convert the tweets into Bag-of-Words, TF-IDF, and Word Embeddings
#Building various classifiers: -
#TF-IDF approach
from sklearn.feature_extraction.text import TfidfVectorizer
tfidf_vectorizer = TfidfVectorizer(max_features = 500,max_df=0.90, min_df=2,stop_words='english')
# TF-IDF feature matrix
X1 = tfidf_vectorizer.fit_transform(corpus).toarray()
Y1 = data_frame.loc[:,'label'].values

from sklearn.model_selection import train_test_split
X1_train, X1_test, Y1_train, Y1_test = train_test_split(X1, data_frame['label'], test_size = 0.2)

#QDA
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis

rf = QuadraticDiscriminantAnalysis()
rf.fit(X1_train, Y1_train)
y_pred = rf.predict(X1_test)
print(pd.crosstab(Y1_test,y_pred,rownames=['Actual'],colnames=['Predicted']))
print(classification_report(Y1_test, y_pred))

import scikitplot as skplt

Y_test_probs = rf.predict_proba( X1_test)

skplt.metrics.plot_roc_curve(Y1_test, Y_test_probs,
                       title="Hate and Non-Hate ROC Curve", figsize=(12,6));

cm_Qda= confusion_matrix(Y1_test, y_pred)
cm_Qda

import seaborn as sns
sns.set(rc= {"figure.figsize": (8, 6)})

cm = confusion_matrix(Y1_test, y_pred)
class_label = ["NON-HATE","HATE", ]
df_cm = pd.DataFrame(cm, index=class_label,columns=class_label)
ax = sns.heatmap(df_cm, annot=True, fmt='d')
bottom, top = ax.get_ylim()
ax.set_ylim(bottom + 0.5, top - 0.5)
plt.title("Confusion Matrix")
plt.xlabel("Predicted Label")
plt.ylabel("True Label")
plt.show()

true = np.random.randint(0, 10, size=100)
pred = np.random.randint(0, 10, size=100)
target_names = [ "NON-HATE","HATE", ]

clf_report = classification_report(Y1_test,
                                   y_pred,
                                   target_names=target_names,
                                   output_dict=True)

ax = sns.heatmap(pd.DataFrame(clf_report).iloc[:-1, :].T, annot=True)
bottom, top = ax.get_ylim()
ax.set_ylim(bottom + 0.5, top - 0.5)

from sklearn.model_selection import train_test_split
X1_train1, X1_test1, Y1_train1, Y1_test1 = train_test_split(X1, data_frame['label'], test_size = 0.2)

#LDA
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

rf = LinearDiscriminantAnalysis()
rf.fit(X1_train1, Y1_train1)
y_pred1 = rf.predict(X1_test1)
print(pd.crosstab(Y1_test1,y_pred,rownames=['Actual'],colnames=['Predicted']))
print(classification_report(Y1_test1, y_pred1))

import scikitplot as skplt

Y_test_probs1 = rf.predict_proba( X1_test1)

skplt.metrics.plot_roc_curve(Y1_test1, Y_test_probs1,
                       title="Hate and Non-Hate ROC Curve", figsize=(12,6));

cm_lda= confusion_matrix(Y1_test1, y_pred1)
cm_lda

import seaborn as sns
sns.set(rc= {"figure.figsize": (8, 6)})

cm = confusion_matrix(Y1_test1, y_pred1)
class_label = ["NON-HATE", "HATE"]
df_cm = pd.DataFrame(cm, index=class_label,columns=class_label)
ax = sns.heatmap(df_cm, annot=True, fmt='d')
bottom, top = ax.get_ylim()
ax.set_ylim(bottom + 0.5, top - 0.5)
plt.title("Confusion Matrix")
plt.xlabel("Predicted Label")
plt.ylabel("True Label")
plt.show()

true = np.random.randint(0, 10, size=100)
pred = np.random.randint(0, 10, size=100)
target_names = ["NON-HATE", "HATE"]

clf_report = classification_report(Y1_test1,
                                   y_pred1,
                                   target_names=target_names,
                                   output_dict=True)

ax = sns.heatmap(pd.DataFrame(clf_report).iloc[:-1, :].T, annot=True)
bottom, top = ax.get_ylim()
ax.set_ylim(bottom + 0.5, top - 0.5)
