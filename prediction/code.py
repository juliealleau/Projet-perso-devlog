#%%
#Importation des packages necessaires au code
import pandas as pd
from download import download
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# Importation d'un fichier csv via une URL
url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQVtdpXMHB4g9h75a0jw8CsrqSuQmP5eMIB2adpKR5hkRggwMwzFy5kB-AIThodhVHNLxlZYm8fuoWj/pub?gid=2105854808&single=true&output=csv"
path_target = "./La_myriade_de_Totems_de_Montpellier_SaisiesFormulaire.csv"
print(path_target)
download(url, path_target, replace=True)  

#Création d'un dataframe nommé data
data = pd.read_csv("./La_myriade_de_Totems_de_Montpellier_SaisiesFormulaire.csv")
#print(data)


#Réarrangement du tableau, suppression des données inutiles
data.columns = ['Date', 'Heure', 'Total année', 'Total journée', 'a', 'b']
data2b = data.copy()
data2b.drop(['a', 'b'], 1, inplace=True)
data2b.drop([0, 1], 0, inplace=True)
data2b.dropna(inplace=True)
print(data2b)

#Info sur le tableau
#data2.info()


#ajout d'une colonne couvre feu
data2 = data2b.assign(Couvre_feu=0)
for i in data2.index:
  if data2['Heure'][i] > '18:00:00':
    data2['Couvre_feu'][i] = 1


#regroupement de 'date' et 'heure'
temps_regroupe = pd.to_datetime(data2['Date'] + ' ' + data2['Heure'], format='%d/%m/%Y %H:%M:%S')                        
data2['Datetime'] = temps_regroupe
data2['date'] = data2.Datetime.dt.date
data2['hour'] = data2.Datetime.dt.hour
del data2['Heure']
del data2['Date']
data3 = data2.copy()
data3 = data2.set_index(['Datetime'])


#suppression de la colonne 'Total année'
data4 = data3.copy()
data4.drop(['Total année'], 1, inplace=True)

#ajout d'une colonne confinement
data5 = data4.copy()
new_data = data5.assign(Confinement=0)
for i in range(1432):
  if new_data.index[i] >= pd.to_datetime('2020-03-17') and new_data.index[i] <= pd.to_datetime('2020-05-10'):
    new_data['Confinement'][i] = 1
  if new_data.index[i] >= pd.to_datetime('2020-10-29') and new_data.index[i] <= pd.to_datetime('2020-12-15'):
    new_data['Confinement'][i] = 1

#graphe du nombre de vélos par jour
plt.xlabel('Date')
plt.ylabel('Nombre de velo')
plt.plot(new_data['Total journée'])

#Renommer colonne pour utiliser fbprophet
df = new_data.rename(columns={'Total journée': 'y'})
df['ds'] = new_data.index

#%%

#Test de Dickey-Fulle pour tester la stationnarité du modèle
from statsmodels.tsa.stattools import adfuller

print('Resulat du test de Dickey-Fuller:')
test_DF = adfuller(df['y'], autolag='AIC')
sortie_test = pd.Series(test_DF[0:4], index=['Statistique de test', 'p-value', 'retard utilisé', "nombre d'observation utilisé"])
for key,value in test_DF[4].items():
  sortie_test['Valeur critique (%s)'%key] = value
print(sortie_test)

#La p-value est de 0.006 < 0.05 donc c'est stationnaire

###################Prédiction##################

#%%
#Ajout du modèle et de variables explicatives 
from fbprophet import Prophet
modele = Prophet()
modele.add_regressor('Confinement')
modele.add_regressor('Couvre_feu')
modele.add_country_holidays(country_name="FR" )

#Ajustement du modèle
modele.fit(df)

#Création des futures dates et des nouvelles colonnes 'confinement' et 'couvre_feu'.
future = modele.make_future_dataframe(periods=23*3, freq='H')
future_range = pd.date_range('2021-04-02', periods=23*3, freq='H')
ds = pd.to_datetime(future['ds'], format='%d/%m/%Y %H:%M:%S')
future['heure'] = future.ds.dt.hour

#confinement
future_confinement_df = pd.DataFrame({'future_date': future_range, 'future_confinement': 0})
future_confinement_df['future_date'] = pd.to_datetime(future_confinement_df['future_date'])
future_confinement_df = future_confinement_df.set_index('future_date')

def confinement(ds):
    date = (pd.to_datetime(ds)).date()
    
    if df[date:].empty:
        return future_confinement_df[date:]['future_confinement'].values[0]
    else:
        return (df[date:]['Confinement']).values[0]
    
    return 0

future['Confinement'] = future['ds'].apply(confinement)

#couvre feu
future_couvre_feu_df = pd.DataFrame({'future_date': future_range, 'future_couvre_feu': 0})
future_couvre_feu_df['future_date'] = pd.to_datetime(future_couvre_feu_df['future_date'])
future_couvre_feu_df = future_couvre_feu_df.set_index('future_date')


for i in range(0, len(future)):  
  if future['heure'][i] < 6:
    future.at[i, 'Couvre_feu'] = 1
for i in range(0, len(future)):
  if future['heure'][i] >= 18:
    future.at[i, 'Couvre_feu'] = 1  
for i in range(0, len(future)):
  if future['heure'][i] >= 6 and future['heure'][i] <= 17:
    future.at[i, 'Couvre_feu'] = 0


#prévision 
forecast = modele.predict(future)
forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()
fig1 = modele.plot(forecast)
plt.savefig("fig1.png", dpi=1000)

#tracé de la tendance, la saisonnalité quotidienne, la saisonnalité hebdomadaire et des autres variables explicatives de la série temporelle.
fig = modele.plot_components(forecast) 
plt.savefig("composants.png", dpi=1000)

#récupération de la prédiction du 2021-04-02
for i in range(0, len(forecast)):
  if forecast['ds'][i] >= pd.to_datetime('2021-04-02 08:00:00') and forecast['ds'][i] <= pd.to_datetime('2021-04-02 10:00:00'):
    print(forecast[['ds', 'yhat']].iloc[i])
#%%

#################################  essai du modèle sur les données existante  #################################
train = df.drop(df.index[-40:])
future2 = df.loc[(df['ds'] > df.index[-41:][0])]

from sklearn.metrics import mean_absolute_error
import numpy as np
from numpy import array

model = Prophet()
model.fit(train)


#Adapter le cadre de données utilisé pour les jours de prévision au format requis par Prophet.
future = list(future2)
future = pd.DataFrame(future)
future = future2.rename(columns={0: 'ds'})

# Prévision
forecast = model.predict(future)

# MAE entre les valeurs réelles et les valeurs prédites
y_true = df['y'][-40:].values
y_pred = forecast['yhat'].values
mae = mean_absolute_error(y_true, y_pred)
print("L'erreur absolue moyenne est de ", mae)

# Plot du résultat final pour une compréhension visuelle
y_true = np.stack(y_true).astype(float)

fig2 = plt.figure(figsize=(7,5))
plt.plot(y_true, label="Actual")
plt.plot(y_pred, label='Predicted')
plt.legend()
plt.xlabel('Date')
plt.ylabel('Nombre de vélo')
plt.title("Erreur absolue moyenne entre les 2 courbes")
plt.xlim([-1, 41])
plt.ylim([-1, 2000])
plt.show()
fig2.savefig("difference.png", dpi=1000)


# %%
