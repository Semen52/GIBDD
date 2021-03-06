# coding: utf8
import pandas
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager
from scipy import stats
from sklearn.preprocessing import scale
from sklearn import svm
from sklearn.decomposition import PCA
from utils import *

OUTLIER_FRACTION = 0.01

"""
Script
"""

raw_data = load_data_from_csv('data\parsered1.csv', False)

# print raw_data[['date', 'num_dtp', 'num_death', 'num_hurt']] #[raw_data['num_death'] > 4]#| data_gibdd['num_hurt'] > 35]
# print data_gibdd[['date', 'num_death', 'num_hurt']][data_gibdd['num_hurt'] > 35]
# exit()
# dates = raw_data['date']
# print dates
dtp_data = raw_data[['date', 'num_dtp', 'num_death', 'num_hurt']]
dtp_data = dtp_data.sort_index(by=['date'])
dtp_data = dtp_data.set_index('date')

NCOLS = dtp_data.shape[1]
dtp_data.plot(subplots=True, figsize=(10, 2 * NCOLS), title="DTP data on subplots", )
plt.legend(loc="best")
plt.show()

pandas.rolling_mean(dtp_data['num_dtp'], window=30).plot(style='-g', grid=True)
# dtp_data_num.plot() #kind='barh'
plt.show()

'''

# Для обучения модели оставим только численные параметры, кроме даты и ссылки.
# Запишем их в массив NumPy data_params, попутно преобразовав к типу float64.
# Шкалируем данные так, чтобы все признаки лежали в диапазоне от -1 до 1.
data_params = np.array(raw_data.values[:, 1:8], dtype="float64")
data_params = scale(data_params)

# Далее выделяем 2 главных компонента в данных, чтоб их можно было отобразить.
# Тут нам пригодилась библиотека Scikit-learn Principal Component Analysis (PCA).
# Также нам не помешает сохранить число сводок
X = PCA(n_components=2).fit_transform(data_params)
days_num = X.shape[0]

# Создаем экземпляр классификатора с гауссовым ядром и «скармливаем» ему данные.
clf = svm.OneClassSVM(kernel="rbf")
clf.fit(X)

# Порог определяется статистически, как такое расстояние
# до разделяющей поверхности, что у OUTLIER_FRACTION
# (в нашем случае у одного) процента выборки оно больше
# (т.е в нашем случае, threshold — это 1%-перцентиль массива
# расстояний до разделяющей поверхности).
dist_to_border = clf.decision_function(X).ravel()
threshold = stats.scoreatpercentile(dist_to_border,
            100 * OUTLIER_FRACTION)
is_inlier = dist_to_border > threshold

# Отображение
xx, yy = np.meshgrid(np.linspace(-7, 7, 500), np.linspace(-7, 7, 500))
n_inliers = int((1. - OUTLIER_FRACTION) * days_num)
n_outliers = int(OUTLIER_FRACTION * days_num)
Z = clf.decision_function(np.c_[xx.ravel(), yy.ravel()])
Z = Z.reshape(xx.shape)
plt.title("Outlier detection")
plt.contourf(xx, yy, Z, levels=np.linspace(Z.min(), threshold, 7),
                         cmap=plt.cm.Blues_r)
a = plt.contour(xx, yy, Z, levels=[threshold],
                            linewidths=2, colors='red')
plt.contourf(xx, yy, Z, levels=[threshold, Z.max()],
                         colors='orange')
b = plt.scatter(X[is_inlier == 0, 0], X[is_inlier == 0, 1], c='white')
c = plt.scatter(X[is_inlier == 1, 0], X[is_inlier == 1, 1], c='black')
plt.axis('tight')
plt.legend([a.collections[0], b, c],
           ['learned decision function', 'outliers', 'inliers'],
           prop=matplotlib.font_manager.FontProperties(size=11))
plt.xlim((-7, 7))
plt.ylim((-7, 7))
plt.show()

print 'Снаружи'
data_inlier = data_gibdd[is_inlier == 0]
print data_inlier
# save_data_to_csv(data=data_gibdd[is_inlier == 0])
data_inlier.to_csv('data\\anomaly.csv', sep=';', encoding='utf-8')
# print 'Внутри'
# print data_gibdd[is_inlier == 1]

'''