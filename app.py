import json

import pandas as pd
import matplotlib.pyplot as plt
import plotly
from flask import Flask, jsonify
from flask import render_template
import json
import plotly.express as px
import plotly.io as pio


app = Flask(__name__)

df=pd.read_csv("colis-1.csv")
fourrnisseur_list = df["fournisseur_id"].tolist()

fournisseur_liste_saisie=[]

# entrer la valeur :
x = int(input("What is the fournisseur id ? "))

# mettre une condition sur le choix de la valeur x
if x in fourrnisseur_list:
     print('your choice for the fournisseur id is true \n')

else :

    print('retry ! your choice is wrong ')

#calculer le nombre de fournisseur id
###### pourcentage des colis livres
h=df['fournisseur_id'].value_counts()
#convertir h to a dataframe
h_frame=h.to_frame()
#obtenir resultat de la valeur  de fournisseur qui corresspond au fournisseur id saisie  par l'utilisateur
resultat=h_frame.loc[x, 'fournisseur_id']

# faire une copie de df mais avec les valeurs emis par l'utilisateur
df2=df.loc[df['fournisseur_id'] == x]
y=df2['etat'].value_counts()
data_frame=y.to_frame()

per=data_frame.loc['colis livrée', 'etat']
per1=per*(100/resultat)
u=round(per1)
resultat_liste=[]

###pourcentage des colis retournée
per2=data_frame.loc['colis retournée', 'etat']
per3=per2*(100/resultat)
u1=round(per3)
resultat_liste_retourne=[]

###### top 5 chers colis par fournisseurs
e=df.loc[df['fournisseur_id'] == x]
df_copy=e.copy()
c=['adresse', 'anomalie', 'cod', 'code_postal',
      'date_creation', 'delegation', 'designation', 'etat', 'gouvernorat',
      'hauteur', 'largeur', 'latitude', 'localite', 'longeur', 'longitude',
      'mode_paiement','nom_c', 'poids', 'prenom_c', 'remarque',
       'service', 'tel_c_1', 'tel_c_2', 'personnel_id']
df_copy.drop(c, inplace=True, axis=1)
df3 = df_copy.sort_values(["nb_p"], ascending=False)
df3_liste=df3['nb_p'].values.tolist()
#df3_liste[0:6]




@app.route('/')
def index():
    return 'welcome to our rest api '


@app.route('/plot')
def plot() :
    #plt.title("gouvernorat Distribution")
    #plt.xlabel("gouvernorat ")
    #plt.ylabel("gouvernorat Value Count")
    #vc = df2['gouvernorat'].value_counts()
    #vc.plot.bar(rot=90)
    vc = df2['gouvernorat'].value_counts()
    barchart = px.bar(
        data_frame=vc,


        opacity=0.9,  # set opacity of markers (from 0 to 1)
        orientation="v",  # 'v','h': orientation of the marks
        )
    pio.show(barchart)

    graph1JSON= json.dumps(barchart, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('index.html', graph1JSON=graph1JSON)



@app.route('/liste_fournisseurs', methods=['GET'] )
def get () :
    return jsonify({'fournisseur_liste':fourrnisseur_list})



@app.route('/choix_fournisseurs_id',methods=['POST','GET'])
def accept():
   fournisseur_liste_saisie.append(x)
   return jsonify({'accepted':fournisseur_liste_saisie})



@app.route('/resultat_coulis_livres',methods=['POST','GET'])
def get_resultat():
    resultat_liste.append(u)
    return jsonify({'resultat pourcentage de colis livrées': resultat_liste})

@app.route('/resultat_coulis_retournes',methods=['POST','GET'])
def get_resultat_coulis_retourne():
    resultat_liste_retourne.append(u1)
    return jsonify({'resultat pourcentage de colis retournes':resultat_liste_retourne})

@app.route('/top5',methods=['GET'])
def get_top5() :
    return jsonify({'les top 5 chers par ce fournisseur ': df3_liste[0:6]})




if __name__== "__main__":
    app.run(host='localhost', port=5000)

