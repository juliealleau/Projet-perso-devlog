
# %%
import tkinter as tk
import pandas as pd
from download import download


# %%
#taille de la fenêtre
taille = 1100
largeur = 1200


# %%
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

url = "https://data.montpellier3m.fr/sites/default/files/ressources/MMM_EcoCompt_X2H20042634.json"
path_target5 = "./JSON4.json"
print(path_target5)
download(url, path_target5, replace=True)

url = "https://data.montpellier3m.fr/sites/default/files/ressources/MMM_EcoCompt_X2H20042635.json"
path_target6 = "./JSON5.json"
print(path_target6)
download(url, path_target6, replace=True)

url = "https://data.montpellier3m.fr/sites/default/files/ressources/MMM_EcoCompt_X2H20063161.json"
path_target7 = "./JSON6.json"
print(path_target7)
download(url, path_target7, replace=True)

url = "https://data.montpellier3m.fr/sites/default/files/ressources/MMM_EcoCompt_X2H20063162.json"
path_target8 = "./JSON7.json"
print(path_target8)
download(url, path_target8, replace=True)

url = "https://data.montpellier3m.fr/sites/default/files/ressources/MMM_EcoCompt_X2H20063163.json"
path_target9 = "./JSON8.json"
print(path_target9)
download(url, path_target9, replace=True)

url = "https://data.montpellier3m.fr/sites/default/files/ressources/MMM_EcoCompt_XTH19101158.json"
path_target10 = "./JSON9.json"
print(path_target10)
download(url, path_target10, replace=True)

url = "https://data.montpellier3m.fr/sites/default/files/ressources/MMM_EcoCompt_X2H20063164.json"
path_target11 = "./JSON10.json"
print(path_target11)
download(url, path_target11, replace=True)

url = "https://www.montpellier3m.fr/sites/default/files/velomagg_tram.png"
path_target4 = "./image.png"
print(path_target4)
download(url, path_target4, replace=True) 


df1 = pd.read_json("JSON1.json") # Berracasa
df2 = pd.read_json("JSON2.json") # Laverune
df3 = pd.read_json("JSON3.json") # Celleneuve
df4 = pd.read_json("JSON4.json") # Lattes 2
df5 = pd.read_json("JSON5.json") # Lattes 1
df6 = pd.read_json("JSON6.json") # Vieille-Poste
df7 = pd.read_json("JSON7.json") # Gerhardt
df8 = pd.read_json("JSON8.json") # Delmas 1
df9 = pd.read_json("JSON9.json") # Albert 1er
df10 = pd.read_json("JSON10.json") # Delmas 2
df = pd.concat([df1, df2, df3, df4, df5, df6, df7, df8, df9, df10], ignore_index = True)


# %%
def velo(variable):
    df1 = pd.read_json("JSON1.json") # Berracasa
    df2 = pd.read_json("JSON2.json") # Laverune
    df3 = pd.read_json("JSON3.json") # Celleneuve
    df4 = pd.read_json("JSON4.json") # Lattes 2
    df5 = pd.read_json("JSON5.json") # Lattes 1
    df6 = pd.read_json("JSON6.json") # Vieille-Poste
    df7 = pd.read_json("JSON7.json") # Gerhardt
    df8 = pd.read_json("JSON8.json") # Delmas 1
    df9 = pd.read_json("JSON9.json") # Albert 1er
    df10 = pd.read_json("JSON10.json") # Delmas 2
    df = pd.concat([df1, df2, df3, df4, df5, df6, df7, df8, df9, df10], ignore_index = True)
    output_label = tk.Label(font=("Helvetica", 15))
    output_label.place(relx=0.20, rely=0.35, relwidth=0.6, relheight=0.4)
    if variable.get() == 'Berracasa':
        output_label['text'] = f"Le nombre de vélos passés le {df['dateObserved'][0][0:10]} est de {df['intensity'][0]}"
    if variable.get() == 'Laverune':
        output_label['text'] = f"Le nombre de vélos passés le {df['dateObserved'][2][0:10]} est de {df['intensity'][2]}"
    if variable.get() == 'Celleneuve':
        output_label['text'] = f"Le nombre de vélos passés le {df['dateObserved'][4][0:10]} est de {df['intensity'][4]}"
    if variable.get() == 'Lattes 2':
        output_label['text'] = f"Le nombre de vélos passés le {df['dateObserved'][0][0:10]} est de {df['intensity'][6]}"
    if variable.get() == 'Lattes 1':
        output_label['text'] = f"Le nombre de vélos passés le {df['dateObserved'][0][0:10]} est de {df['intensity'][8]}"
    if variable.get() == 'Vieille-Poste':
        output_label['text'] = f"Le nombre de vélos passés le {df['dateObserved'][0][0:10]} est de {df['intensity'][10]}"
    if variable.get() == 'Gerhardt':
        output_label['text'] = f"Le nombre de vélos passés le {df['dateObserved'][0][0:10]} est de {df['intensity'][12]}"
    if variable.get() == 'Delmas 1':
        output_label['text'] = f"Le nombre de vélos passés le {df['dateObserved'][0][0:10]} est de {df['intensity'][14]}"
    if variable.get() == 'Albert 1er':
        output_label['text'] = f"Le nombre de vélos passés le {df['dateObserved'][0][0:10]} est de {df['intensity'][16]}"
    if variable.get() == 'Delmas 2':
        output_label['text'] = f"Le nombre de vélos passés le {df['dateObserved'][0][0:10]} est de {df['intensity'][18]}"


# %%
racine = tk.Tk()
#fenêtre
toile = tk.Canvas(racine, height=taille, width=largeur)
toile.pack()

#image de fond
image = tk.PhotoImage(file='image.png')
image_label = tk.Label(racine, image=image)
image_label.place(relwidth=1, relheight=1)

#petit cadre vert
cadre = tk.Frame(racine, bg='#28b463', bd=5)
cadre.place(relx=0.5, rely=0.1, relwidth=0.75, relheight=0.1, anchor='n')

#menu déroulant
OptionList = [
"Choisissez un lieu",
"Berracasa",
"Laverune",
"Celleneuve",
"Lattes 2",
"Lattes 1",
"Vieille-Poste",
"Gerhardt",
"Delmas 1",
"Albert 1er",
"Delmas 2"
] 

variable = tk.StringVar(racine)
variable.set(OptionList[0])

opt = tk.OptionMenu(racine, variable, *OptionList)
opt.config(width=90, font=('Helvetica', 15))
opt.place(relx=0.2, rely=0.1,relwidth=0.4, relheight=0.1)

#bouton 
bouton = tk.Button(cadre, text="cliquer ici", font=40, command=lambda: velo(variable))
bouton.place(relx=0.7, relwidth=0.3, relheight=1)

#contour vert
cadre_inferieur = tk.Frame(racine, bg='#28b463', bd=10)
cadre_inferieur.place(relx=0.5, rely=0.25, relwidth=0.75, relheight=0.6, anchor='n')

#cadre blanc au milieu
label = tk.Label(cadre_inferieur)
label.place(relwidth=1, relheight=1)


racine.mainloop()


# %%