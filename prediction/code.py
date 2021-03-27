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
data2['date'] = data2.Datetime.dt.date
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
plt.plot(new_data['Total journée'])
#%% 
data_day = new_data.resample('d').max()
#data_array = data_day.values
#%%
#data_array_velo = data_array[:,0]
#data_array_couvre_feu = data_array[:,1]
#data_array_date = data_array[:,2]
#data_array_heure = data_array[:,3]
#data_array_confinement = data_array[:,4]
#
df = data_day.rename(columns = {'Total journée': 'y', 'date': 'ds'})

#%%
df['y'] = df['y'] - df['y'].shift(1)
df['y'].plot()

#%%
from fbprophet import Prophet
#%%
#train = df[(df['ds'] >= pd.to_datetime('2020-03-12')) & (df['ds'] <= pd.to_datetime('2021-03-01'))]
#test = df[(df['ds'] > pd.to_datetime('2021-03-01'))]
#train.shape
#test.shape
#%%
##c'est de la merde
#m = Prophet()
#m.fit(train)
#m.params
#future = m.make_future_dataframe(periods=127)
#future.tail
#forecast = m.predict(future)
#forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()
#fig1 = modele.plot(forecast)
#fig = m.plot_components(forecast)



future_confinement_df.tail(5)
#%%



modele = Prophet()
modele.add_regressor('Confinement')
modele.add_country_holidays(country_name = "FR" )
#modele.add_regressor('heure') 
#modele.add_regressor('couvre_feu') 
#modele.add_regressor('confinement')
modele.fit(df)
# %%
future = modele.make_future_dataframe(periods=5)

future_range = pd.date_range('2021-03-28', periods=5, freq='D')
future_confinement_df = pd.DataFrame({ 'future_date': future_range, 'future_confinement' : 0})
future_confinement_df['future_date'] = pd.to_datetime(future_confinement_df['future_date'])
future_confinement_df = future_confinement_df.set_index('future_date')

future_confinement_df.at['2021-03-28', 'future_confinement'] = 0
future_confinement_df.at['2021-03-29', 'future_confinement'] = 0
future_confinement_df.at['2021-03-30', 'future_confinement'] = 0
future_confinement_df.at['2021-03-31', 'future_confinement'] = 0
future_confinement_df.at['2021-04-01', 'future_confinement'] = 0

def confinement(ds):
    date = (pd.to_datetime(ds)).date()
    
    if df[date:].empty:
        return future_confinement_df[date:]['future_confinement'].values[0]
    else:
        return (df[date:]['Confinement']).values[0]
    
    return 0

future['Confinement'] = future['ds'].apply(confinement)
# %%
forecast = modele.predict(future)
forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()
fig = modele.plot_components(forecast)

#%%
fig1 = modele.plot(forecast)
# %%

#cette partie ne marche pas encore:
train = df.drop(df.index[-12 :])
future = df.loc[df["ds"] > train.iloc[len(train)-1]["ds"]["ds"]]
from sklearn.metrics import mean_absolute_error
import numpy as np
from numpy import array

#Nous formons le modèle

model = Prophet()
model.fit(train)

#Adapter le cadre de données utilisé pour les jours de prévision au format requis par Prophet.

future = list(future)
future = DataFrame(future)
future = future.rename(columns={0 : 'ds'})

# Nous faisons la prévision

forecast = model.predict(future)

# Nous calculons l’EAM entre les valeurs réelles et les valeurs prédites

y_true = df['y'][-12 :].values
y_pred = forecast['yhat'].values
mae = erreur_absolue_moyenne(y_true, y_pred)

# Nous traçons le résultat final pour une compréhension visuelle

y_true = np.stack(y_true).astype(float)
pyplot.plot(y_true, label="Actual")
pyplot.plot(y_pred, label='Predicted')
pyplot.legend()
pyplot.show()
print(mae)
# %%

# %%
