

!pip install bing-image-downloader
!mkdir images

from bing_image_downloader import downloader
downloader.download("people with mask in covid crisis",limit = 30,output_dir='images',adult_filter_off=True)
downloader.download("male athlete faces",limit = 30,output_dir='images',adult_filter_off=True,force_replace=True)

import os
import matplotlib.pyplot as plt
import numpy as np
from skimage.io import imread
from skimage.transform import resize
target = []
images = []
flat_data = []
DATADIR = '/content/images'
CATEGORIES = ['people with mask in covid crisis','male athlete faces']
for category in CATEGORIES:
  class_num = CATEGORIES.index(category)
  path = os.path.join(DATADIR,category)
  for img in os.listdir(path):
    img_array = imread(os.path.join(path,img))
    img_resized = resize(img_array,(150,150,3))
    flat_data.append(img_resized.flatten())
    images.append(img_resized)
    target.append(class_num)
flat_data = np.array(flat_data)
target = np.array(target)
images = np.array(images)

from sklearn.model_selection import train_test_split
x_train,x_test,y_train,y_test = train_test_split(flat_data,target,test_size = 0.3,random_state=109)

from sklearn.model_selection import GridSearchCV
from sklearn import svm
param_grid = [
              {'C':[1,10,100,1000],'kernel':['linear']},
              {'C':[1,10,100,1000],'gamma':[0.001,.0001],'kernel':['rbf']},
]
svc = svm.SVC(probability = True)
clf = GridSearchCV(svc,param_grid)
clf.fit(x_train,y_train)

y_pred = clf.predict(x_test)
y_pred

y_test

from sklearn.metrics import accuracy_score,confusion_matrix

accuracy_score(y_pred,y_test)

confusion_matrix(y_pred,y_test)

import pickle 
pickle.dump(clf,open('img_model.p','wb'))

model = pickle.load(open('img_model.p','rb'))

flat_data = []
url = input('Enter your URL')
img = imread(url)
img_resized = resize(img,(150,150,3))
flat_data.append(img_resized.flatten())
flat_data = np.array(flat_data)
print(img.shape)
plt.imshow(img_resized)
y_out = model.predict(flat_data)
y_out = CATEGORIES[y_out[0]]
print(f'PREDICTED OUTPUT:{y_out}')

!pip install streamlit
!pip install pyngrok
from pyngrok import ngrok


%%writefile app.py
import streamlit as st
import numpy as np
from skimage.io import imread
from skimage.transform import resize
import pickle 
from PIL import Image
st.title('Image Classifier using Machine Learning')
st.text('Upload the Image') 

 
model= pickle.load(open('img_model.p','rb'))
 
uploaded_file = st.file_upload('Choose an image...', type='jpg')
if uploaded_file is not None:
   img = Image.open(uploaded_file)
   st_image(img,caption='Uploaded Image')
 
   if st.button('PREDICT'):
     CATEGORIES = ['people with mask in covid crisis','male athlete faces']
     st.write('Result....')
     flat_data=[]
     img = np.array(img)
     img_resized = resize(img,(150,150,3))
     flat_data.append(img_resized.flatten())
     flat_data = np.array(flat_data)
     plt.imshow(img_resized)
     y_out = model.predict(flat_data)
     y_out = CATEGORIES[y_out[0]]
     st.write(f'PREDICTED OUTPUT:{y_out}')
     q  = model.predict_proba(flat_data)
     for index, item in enumerate(CATEGORIES):
       st.write(f'{item} : {q[0][index]*100}%')


!nohup streamlit run app.py &
url = ngrok.connect(port='8501')
url
