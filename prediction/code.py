#%%
#Importation des packages necessaire au code
import pandas as pd
from download import download
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
#%%
# Importation d'un fichier csv via une URL
url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQVtdpXMHB4g9h75a0jw8CsrqSuQmP5eMIB2adpKR5hkRggwMwzFy5kB-AIThodhVHNLxlZYm8fuoWj/pub?gid=2105854808&single=true&output=csv"
path_target = "./La_myriade_de_Totems_de_Montpellier_SaisiesFormulaire.csv"
print(path_target)
download(url, path_target, replace=True)  # if needed `pip install download`

# %%
#Création d'un dataframe nommé data
data = pd.read_csv("./La_myriade_de_Totems_de_Montpellier_SaisiesFormulaire.csv")
print(data)

# %%
#Réarrangement du tableau, suppression des données inutils
data.columns = ['Date', 'Heure', 'Total année', 'Total journée', 'a', 'b']
data2b = data.copy()
data2b.drop(['a','b'],1 , inplace = True)
data2b.drop([0,1], 0, inplace = True)
data2b.dropna(inplace = True)
print(data2b)
# %%
#data2.info()
data2b

#%%
data2=data2b.assign(Couvre_feu=0)
for i in data2.index:
  if data2['Heure'][i] > '18:00:00':
    data2['Couvre_feu'][i] = 1
# %%
#regroupement de date et heure
temps_regroupe = pd.to_datetime(data2['Date'] + ' ' + data2['Heure'], format='%d/%m/%Y %H:%M:%S')
temps_regroupe                        
# %%
data2['Datetime'] = temps_regroupe
data2
data2['hour'] = data2.Datetime.dt.hour
del data2['Heure']
del data2['Date']
data3 = data2.copy()
data3 = data2.set_index(['Datetime'])

# %%
data3

#%%
data4 = data3.copy()

#%%
data4.drop(['Total année'],1 , inplace = True)

#%%
print(data4)
#%%
data5 = data4.copy()
new_data=data5.assign(Confinement=0)
for i in range(1432):
  if new_data.index[i] >= pd.to_datetime('2020-03-17') and new_data.index[i] <= pd.to_datetime('2020-05-10'):
    new_data['Confinement'][i] = 1
  if new_data.index[i] >= pd.to_datetime('2020-10-29') and new_data.index[i] <= pd.to_datetime('2020-12-15'):
    new_data['Confinement'][i] = 1

#%%

#from numpy import cov
#covariance = cov(data3['Total journée'], data3['Total année'])
#print(covariance)
# %%
plt.xlabel('Date')
plt.ylabel('Nombre de velo')
plt.plot(new_data)

#%%
new_data2 = new_data.Datetime.dt.
#%%
from prophet import Prophet
m = Prophet()
m.fit(new_data)
# %%
future = m.make_future_dataframe(periods=365)
future.tail()

#%%
from gluonts.model.deepar import DeepAREstimator
estimateur = DeepAREstimator(freq=data_freq, prediction_length=7*24, trainer = Trainer(epochs=30, learning_rate=0.0001))
# %%
from gluonts.model.deepar import DeepAREstimator
from gluonts.trainer import Trainer
from gluonts.dataset.common import ListDataset
# %%
