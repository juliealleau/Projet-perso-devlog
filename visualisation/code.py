#%%
import tkinter as tk
import pandas as pd
from download import download

url = "https://data.montpellier3m.fr/sites/default/files/ressources/MMM_EcoCompt_X2H20042633.json"
path_target1 = "./JSON1.json"
print(path_target1)
download(url, path_target1, replace=True) 

url = "https://data.montpellier3m.fr/sites/default/files/ressources/MMM_EcoCompt_X2H20042632.json"
path_target2 = "./JSON2.json"
print(path_target2)
download(url, path_target2, replace=True) 

url = "https://data.montpellier3m.fr/sites/default/files/ressources/MMM_EcoCompt_X2H19070220.json"
path_target3 = "./JSON3.json"
print(path_target3)
download(url, path_target3, replace=True) 

#%%
df1 = pd.read_json("JSON1.json") # Berracasa
df2 = pd.read_json("JSON2.json") # Laverune
df3 = pd.read_json("JSON3.json") # Celleneuve
df = pd.concat([df1 , df2, df3], ignore_index = True)

#%%
taille = 500
largeur = 600

####creation fonction 
def fonction(entree):
    print("vous avez entré:", entree)

##def forma_reponse(velos):
#    #station = 
#    #velo_libre = 
#
#    return str(station) + ' ' + (velo_libre)
#
#
#def velo(station):
#    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQVtdpXMHB4g9h75a0jw8CsrqSuQmP5eMIB2adpKR5hkRggwMwzFy5kB-AIThodhVHNLxlZYm8fuoWj/pub?gid=2105854808&single=true&output=csv"
#    parametre = {}
#    reponse = requests.get(url, params=parametre)
#    velos = reponse.json()
#
#    label['text'] = forma_reponse(velos)


####Fenêtre et graphisme 
#création de la fenêtre

racine = tk.Tk()

#fenêtre
toile = tk.Canvas(racine, height=taille, width=largeur)
toile.pack()

#image de fond
image = tk.PhotoImage(file='C:/Users/Julie Alleau/Pictures/Saved Pictures/velomagg_tram.png')
image_label = tk.Label(racine, image=image)
image_label.place(relwidth=1, relheight=1)

#petit cadre orange
cadre = tk.Frame(racine, bg='#28b463', bd=5)
cadre.place(relx=0.5, rely=0.1, relwidth=0.75, relheight=0.1, anchor='n')

#la ou on écrit
entree = tk.Entry(cadre, font=40)
entree.place(relwidth=0.65, relheight=1)

#bouton 
bouton = tk.Button(cadre, text="cliquer ici", font=40, command=lambda: velo(entree.get()))
bouton.place(relx=0.7, relwidth=0.3, relheight=1)

#contour orange
cadre_inferieur = tk.Frame(racine, bg='#28b463', bd=10)
cadre_inferieur.place(relx=0.5, rely=0.25, relwidth=0.75, relheight=0.6, anchor='n')

#cadre blanc au milieu
label = tk.Label(cadre_inferieur)
label.place(relwidth=1, relheight=1)



racine.mainloop()

