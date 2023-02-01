import os
"""
用于处理数据库信息导入以及神经网络的训练
"""
def 姓氏():
    path = 'F:/数据库/姓氏/'
    point = {'基本信息' : 'base_information',
    '历代名人': "fam",
    '迁徙传播': "mig",
    '人口分布': "dis",
    '姓氏起源': "ori",
    '姓氏文化': "cul"}
    data = []
    for i in os.listdir(path):
        tmp = []
        now = os.listdir(path + i + '/')
        for k in point.keys():
            dir =  k + '.txt'
            print(dir)
            if(dir in now):
                file = open(path + i + '/' + dir , 'r' , encoding='utf-8')
                tmp.append(file.read())
                file.close()
            else:
                tmp.append("")
        data.append(SecondName(second_name = i, base_information=tmp[0],
                                fam = tmp[1],
                                mig=tmp[2],
                                dis=tmp[3],
                                ori=tmp[4],
                                cul=tmp[5]))
    SecondName.objects.bulk_create(data)

from Surname.models import  Province
province = ["河北省","山西省","吉林省","辽宁省","黑龙江省","陕西省","甘肃省","青海省","山东省","福建省",
            "浙江省","台湾省","河南省","湖北省","湖南省","江西省","江苏省","安徽省","广东省","海南省","四川省","贵州省","云南省"
            ,"内蒙古" , "北京" , "天津" , "重庆" ,"广西" , "新疆" , "西藏" , "澳门" , "香港","宁夏" , '上海']
data = []
for i in province:
    data.append(Province(name = i))

Province.objects.bulk_create(data)

from Surname.models import  Dynasty
dynasty = {
"夏朝":             [-2070,-1600],
"商（殷）朝":        [-1600,-1046],
"周朝":          [-1046,-256],
"春秋战国" :       [-770,-221],
"秦朝":         [-221,-206],
"汉朝":       [-202,263],
"三国时期":      [220,280],
"晋朝":          [265,420],
"南北朝":   [386,589],
"隋朝":        [581,618],
"唐朝":      [618,907],
"五代十国":       [907,960],
"宋朝":         [960,1279],
"元朝":     [1271,1368],
"明朝":      [1368,1644],
"清朝":           [1636,1912],
"中华民国" :    [1912,None],
"中华人民共和国":       [1945,None]
}
data = []
for a in dynasty.items():
    data.append(Dynasty(name=a[0] , begin=a[1][0] , end=a[1][1]))
Dynasty.objects.bulk_create(data)

from Surname.models import  Province , SecondName , Distribution
import numpy as np

n = SecondName.objects.all()
p = Province.objects.all()
data = []
for i in n:
    ratio = np.random.random(size=(p.count()))
    ratio =ratio / ratio.sum()
    n = 0
    for j in p:
        tmp = Distribution(ratio=ratio[n])
        tmp.save()
        tmp.姓氏.add(i)
        tmp.省份.add(j)
        tmp.save()
        n += 1

from Surname.models import SecondName
import pandas as pd
data = pd.read_csv('name.csv' , header = None)
all = []
Surname_all = {}
tmp = SecondName.objects.all()
for i in tmp:
    Surname_all[i.second_name] = i
for i in range(data.shape[0]):
    if data.iloc[i,0] in Surname_all:
        tmp = Surname_all[data.iloc[i,0]]
        for j in data.iloc[i,1:]:
            if j in Surname_all:
                tmp.father_surname.add(Surname_all[j])
        all.append(tmp)
print(all)

import pickle
import tensorflow.keras as keras
from tensorflow.keras import Sequential , Model
import tensorflow as tf
model = Sequential([
    keras.layers.Input((3)),
    keras.layers.Masking(),
    keras.layers.Embedding(3,256),
    keras.layers.Conv1D(1024 , 64 , 1 , padding = 'same'),
    keras.layers.LayerNormalization(),
    keras.layers.Activation('relu'),
    keras.layers.Conv1D(512 , 128 , 1 , padding = 'same'),
    keras.layers.LayerNormalization(),
    keras.layers.Activation('relu'),
    keras.layers.Conv1D(256 , 128 , 1 , padding = 'same'),
    keras.layers.LayerNormalization(),
    keras.layers.Activation('relu'),
    keras.layers.Conv1D(128 , 128 , 1 , padding = 'same'),
    keras.layers.LayerNormalization(),
    keras.layers.Activation('relu'),
    keras.layers.GlobalAveragePooling1D(),
    keras.layers.Dense(kind , 'softmax' )
])
model.build()
model.summary()
model.compile(loss ='sparse_categorical_crossentropy' ,
 optimizer = keras.optimizers.Adam(0.0002),metrics='acc')
model.fit(x = train_x , y = train_y , batch_size = 64 , epochs=100,validation_split=0.1)