#%%
#Importation des packages necessaire au code
import pandas as pd
from download import download
import numpy as np
import matplotlib.pyplot as plt
#%%
# Importation d'un fichier csv via une URL
url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQVtdpXMHB4g9h75a0jw8CsrqSuQmP5eMIB2adpKR5hkRggwMwzFy5kB-AIThodhVHNLxlZYm8fuoWj/pub?gid=2105854808&single=true&output=csv"
path_target = "./La\ myriade\ de\ Totems\ de\ Montpellier\ -\ SaisiesFormulaire.csv"
print(path_target)
download(url, path_target, replace=True)  # if needed `pip install download`

# %%
#Création d'un dataframe nommé data
data = pd.read_csv('./La\\ myriade\\ de\\ Totems\\ de\\ Montpellier\\ -\\ SaisiesFormulaire.csv')
print(data)

# %%
#Réarrangement du tableau, suppression des données inutils
data.columns = ['Date', 'Heure', 'Total année', 'Total journée', 'a', 'b']
data2 = data.copy()
data2.drop(['a','b'],1 , inplace = True)
data2.drop([0,1], 0, inplace = True)
data2.dropna(inplace = True)
print(data2)
# %%
#data2.info()
data2

#%%
data2=data2.assign(Couvre_feu=0)
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
moyenne_mobile = new_data.rolling(window='31d').mean()
std_mobile = new_data.rolling(window='31d').std()
print(moyenne_mobile, std_mobile)

# %%
Courbe_initiale = plt.plot(new_data['Total journée'], color='turquoise', label='Courbe initiale')
moyenne = plt.plot(moyenne_mobile['Total journée'], color='purple', label='moyenne mobile')
std = plt.plot(std_mobile['Total journée'], color='salmon', label='écart-type mobile')
plt.legend(loc = 'best')
plt.title('Moyenne et écart-type mobile')
plt.show()
# %%
from statsmodels.tsa.stattools import adfuller

# %%
print('Resulat du test de Dickey-Fuller:')
test_DF = adfuller(new_data['Total journée'], autolag='AIC')

sortie_test = pd.Series(test_DF[0:4], index=['Statistique de test', 'p-value', 'retard utilisé', "nombre d'observation utilisé"])
for key,value in test_DF[4].items():
  sortie_test['Valeur critique (%s)'%key] = value

print(sortie_test)

#%%
def test_stationnarité(serie_tempo):
  moy_mob = serie_tempo.rolling(window='31d').mean()
  std_mob = serie_tempo.rolling(window='31d').std()

  Courbe_initiale = plt.plot(serie_tempo, color='turquoise', label='Courbe initiale')
  moyenne = plt.plot(serie_tempo, color='purple', label='moyenne mobile')
  std = plt.plot(serie_tempo, color='salmon', label='écart-type mobile')
  plt.legend(loc = 'best')
  plt.title('Moyenne et écart-type mobile')
  plt.show()

  print('Resulat du test de Dickey-Fuller:')
  test_DF = adfuller(serie_tempo, autolag='AIC')
  sortie_test = pd.Series(test_DF[0:4], index=['Statistique de test', 'p-value', 'retard utilisé', "nombre d'observation utilisé"])
  for key,value in test_DF[4].items():
    sortie_test['Valeur critique (%s)'%key] = value
  print(sortie_test)
# %%
#from statsmodels.tsa.seasonal import seasonal_decompose
#decomposition = seasonal_decompose(new_data['Total journée'], period=5)
#
#tendance = decomposition.trend
#saisonnalité = decomposition.seasonal
#erreur = decomposition.resid
#
#plt.subplot(411)
#plt.plot(new_data['Total journée'], color='turquoise', label='Courbe initiale')
#plt.legend(loc = 'best')
#plt.subplot(412)
#plt.plot(tendance, color='purple', label='tendance')
#plt.legend(loc = 'best')
#plt.subplot(413)
#plt.plot(saisonnalité, color='salmon', label='saisonnalité')
#plt.legend(loc = 'best')
#plt.subplot(414)
#plt.plot(erreur, color='black', label='erreur')
#plt.legend(loc = 'best')
#plt.tight_layout()
#
## %%
#decompositionData = erreur
#decompositionData.dropna(inplace=True)
#test_stationnarité(decompositionData)
# %%
from pmdarima import auto_arima
tab = new_data.resample('d').max()
stepwise_fit = auto_arima(tab['Total journée'], trace=True, suppress_warnings=True)
# %%
print(tab.shape)
train=tab.iloc[:-30]
test=tab.iloc[-30:]
print(train.shape,test.shape)
# %%
from statsmodels.tsa.arima_model import ARIMA
model=ARIMA(train['Total journée'],order=(5,0,2))
model=model.fit()
model.summary()
# %%
start=len(train)
end=len(train)+len(test)-1
pred=model.predict(start=start,end=end,typ='levels').rename('ARIMA Predictions')
plt.plot(pred,color='turquoise', label='prédiction')
plt.legend(loc = 'best')
plt.xticks(rotation=45)
plt.plot(tab['Total journée'].iloc[-30:], color='black', label='courbe initiale')
plt.legend(loc = 'best')
plt.show()

# %%
from sklearn.metrics import mean_squared_error
from math import sqrt
tab['Total journée'].mean()
rmse=sqrt(mean_squared_error(pred,tab['Total journée']))
print(rmse)
# %%
