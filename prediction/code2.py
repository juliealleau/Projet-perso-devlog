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
#la p-value est <0.5 donc c'est ok
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
#print(tab.shape)
#train=tab.iloc[:-30]
#test=tab.iloc[-30:]
#print(train.shape,test.shape)
# %%
from statsmodels.tsa.arima_model import ARIMA
#model=ARIMA(train['Total journée'],order=(5,0,2))
model=ARIMA(tab['Total journée'],order=(5,1,2))
model=model.fit()
model.summary()
# %%
#start=len(train)
#end=len(train)+len(test)-1
#pred=model.predict(start=start,end=end,typ='levels').rename('ARIMA Predictions')
#plt.plot(pred,color='turquoise', label='prédiction')
#plt.legend(loc = 'best')
#plt.xticks(rotation=45)
#plt.plot(tab['Total journée'].iloc[-30:], color='black', label='courbe initiale')
#plt.legend(loc = 'best')
#plt.show()

# %%
#from sklearn.metrics import mean_squared_error
#from math import sqrt
#tab['Total journée'].mean()
#rmse=sqrt(mean_squared_error(pred,tab['Total journée']))
#print(rmse)
# %%
from scipy import stats
resid = model.resid
stats.normaltest(resid)
#%%
from statsmodels.graphics.api import qqplot
fig = plt.figure(figsize=(12,8))
ax = fig.add_subplot(111)
fig = qqplot(resid, line='q', ax=ax, fit=True)


# %%
import statsmodels.api as sm
r,q,p = sm.tsa.acf(resid.values.squeeze(), fft=True, qstat=True)
data = np.c_[range(1,41), r[1:], q, p]
table = pd.DataFrame(data, columns=['lag', "AC", "Q", "Prob(>Q)"])
print(table.set_index('lag'))

predict_sunspots = model.predict('2021-03-27', dynamic=True)
print(predict_sunspots)


# %%
