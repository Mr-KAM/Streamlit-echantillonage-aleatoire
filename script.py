# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import streamlit as st
from math import*
import pandas as pd
from random import*
from io import BytesIO
from pyxlsb import open_workbook as open_xlsb
import matplotlib.pyplot as plt
from scipy.stats import describe
from PIL import Image

logo=Image.open("agrostat.ico")

st.set_page_config(page_title='AgroStat', page_icon = logo, layout = 'wide', initial_sidebar_state = 'auto')
st.title("Echantillonnage:📈")

taille_population=st.sidebar.number_input("Saisiser la taille de la population",min_value=30)

confiance=st.sidebar.number_input("Quel est la marge d'erreur que vous voulez?",min_value=0.1)/100


try:
	taille_echantillon=(taille_population*(1/confiance)*(1/confiance))/(taille_population+(1/confiance)*(1/confiance))
	# st.write("## La taille minimale de l'échantillon est:")
	if taille_population<=30:
		taille_echantillon=30
		st.write("# La taille minimale de l'échantillon est: ",round(taille_echantillon,0))
	else:
		st.write("## La taille minimale de l'échantillon est: ",round(taille_echantillon,0))
except: 
	st.write()
st.write("---")
# st.write("## Formule de calcul:")
# st.image("image5.png","Formule de calcule de la taille minimale de l'echantillon")
# st.write("- **n:** taille de l’échantillon\n - **N:** taille de la population mère\n - **e:** marge d’erreur")
# st.write("---")


Excel=st.sidebar.file_uploader("Selectionner une base de données Excel", type='xlsx')# Importation d'un fichier excel

echantillon=[]
aleatoire=[]
def echantilloner(data,nombre):
	global aleatoire
	global echantillon

	aleatoire=choices(range(len(data)),k=int(nombre))
	# st.write(aleatoire)
	echantillon=data.iloc[aleatoire]
	# st.write(echantillon)

def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='echantillon')
    workbook = writer.book
    worksheet = writer.sheets['echantillon']
    format1 = workbook.add_format({'num_format': '0.00'}) 
    worksheet.set_column('A:A', None, format1)  
    writer.save()
    processed_data = output.getvalue()
    return processed_data


if Excel is not None:
	try:
		liste_feuilles=pd.ExcelFile(Excel.getvalue()).sheet_names # 
		feuille=st.sidebar.selectbox("Selectionner la feuille de base de données",liste_feuilles)
		data_base=pd.read_excel(Excel.getvalue(),feuille)
		liste_colonnes=sorted(data_base)
		# slecetion de la colonnes des abscisses et des ordonnées
		colonneX=st.sidebar.selectbox("Choisissez la colonnes des abscisses (X):",liste_colonnes)
		colonneY=st.sidebar.selectbox("Choisissez la colonnes des ordonnées (Y):",liste_colonnes)

		st.write("### Base de données principale: N="+str(len(data_base)))
		st.write(" Taille minimale de l'echantillon: **n="+str(int(((len(data_base)*(1/confiance)*(1/confiance))/(len(data_base)+(1/confiance)*(1/confiance)))))+"**")
		st.write(data_base)

		taille_a_echantilloner=st.number_input("Taille à echantilloner",min_value=int(((len(data_base)*(1/confiance)*(1/confiance))/(len(data_base)+(1/confiance)*(1/confiance)))),max_value=len(data_base)-1)
		
		st.button("Echantillonnage aleatoire simple sur la base de donnée", on_click=echantilloner(data_base,taille_a_echantilloner))

	except:
		st.write("## ** Veuillez à la purification de la base de données**")

if len(aleatoire)>0 or len(echantillon)>0:
	st.write(aleatoire)
	st.write(echantillon)
	try:
		st.write("---")
		plot_data=pd.DataFrame({colonneX:echantillon[colonneX],colonneY:echantillon[colonneY]})
		st.write(plot_data)
		# plt.plot(colonneX, colonneY)
		# st.write(plt.plot(colonneX, colonneY))
		st.bar_chart(plot_data[colonneY])
		st.write("## Description:")
		st.write(describe(plot_data[colonneY]))
	except :
		st.sidebar.write("Choisissez de bonnees données pour le graphique")

	st.sidebar.download_button("⬇️Télécharger",data=to_excel(echantillon), file_name='Echantillon_aleatoire.xlsx')

