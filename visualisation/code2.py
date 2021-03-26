#%%
import tkinter as tk
import pandas as pd
#%%
taille = 500
largeur = 600

def test(opt):
        print("hello")

def velo(variable):
    df1 = pd.read_json("JSON1.json") # Berracasa
    df2 = pd.read_json("JSON2.json") # Laverune
    df3 = pd.read_json("JSON3.json") # Celleneuve
    df = pd.concat([df1 , df2, df3], ignore_index = True)
    output_label = tk.Label()
    output_label.place(relx=0.25, rely=0.35, relwidth=0.5, relheight=0.4)
    if variable.get() == 'Berracasa':
       output_label['text'] = f"Le nombre de vélo passé le {df['dateObserved'][0][0:10]} est de {df['intensity'][0]}"
    if variable.get() == 'Laverune':
        output_label['text'] = f"Le nombre de vélo passé le {df['dateObserved'][2][0:10]} est de {df['intensity'][2]}"
    if variable.get() == 'Celleneuve':
        output_label['text'] = f"Le nombre de vélo passé le {df['dateObserved'][4][0:10]} est de {df['intensity'][4]}"




racine = tk.Tk()

#fenêtre
toile = tk.Canvas(racine, height=taille, width=largeur)
toile.pack()

#image de fond
image = tk.PhotoImage(file='C:/Users/Julie Alleau/Pictures/Saved Pictures/velomagg_tram.png')
image_label = tk.Label(racine, image=image)
image_label.place(relwidth=1, relheight=1)

#petit cadre vert
cadre = tk.Frame(racine, bg='#28b463', bd=5)
cadre.place(relx=0.5, rely=0.1, relwidth=0.75, relheight=0.1, anchor='n')

#menu déroulant
OptionList = [
"Berracasa",
"Laverune",
"Celleneuve"
] 

variable = tk.StringVar(racine)
variable.set(OptionList[0])

opt = tk.OptionMenu(racine, variable, *OptionList)
opt.config(width=90, font=('Helvetica', 12))
opt.place(relx=0.2, rely=0.1,relwidth=0.4, relheight=0.1)
opt = tk.OptionMenu(racine, variable, *OptionList)

##la ou on écrit
#entree = tk.Entry(cadre, font=40)
#entree.place(relwidth=0.65, relheight=1)

#bouton 
bouton = tk.Button(cadre, text="cliquer ici", font=40, command=lambda: velo(variable))
bouton.place(relx=0.7, relwidth=0.3, relheight=1)

#contour orange
cadre_inferieur = tk.Frame(racine, bg='#28b463', bd=10)
cadre_inferieur.place(relx=0.5, rely=0.25, relwidth=0.75, relheight=0.6, anchor='n')

#cadre blanc au milieu
label = tk.Label(cadre_inferieur)
label.place(relwidth=1, relheight=1)



racine.mainloop()
# %%
