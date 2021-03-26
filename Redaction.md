titre:
auteur:
date:
1 tableau 

2 stationnariter 
-> rolling statistics :
tracer la moyenne mobile ou la variance mobile et voir si elle varie avec le temps. Plus d'une technique visuelle

-> ADCF test
L'hypothese nulle est que le la statistique de test est non stationnaire.

Ce qui distingue ARMA et ARIMA, c'est la différenciation. Un modèle ARMA est un modèle stationnaire; Si votre modèle n'est pas stationnaire, vous pouvez atteindre la stationnarité en prenant une série de différences. Le «I» dans le modèle ARIMA signifie intégré; C'est une mesure du nombre de différences non saisonnières nécessaires pour atteindre la stationnarité. Si aucune différenciation n'est impliquée dans le modèle, il devient alors simplement un ARMA.

Un modèle avec une dième différence à ajuster et un modèle ARMA (p, q) est appelé un processus ARIMA d'ordre (p, d, q). Vous pouvez sélectionner p, d et q avec un large éventail de méthodes, y compris AIC, BIC et les autocorrélations empiriques (Petris, 2009).