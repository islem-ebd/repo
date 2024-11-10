import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import plotly.express as px

# Configuration de la page Streamlit
st.set_page_config(page_title="Prédiction des Mandats Minute", layout="wide")

# Application du style CSS pour un aspect professionnel
st.markdown("""
    <style>
    .main {
        background-color: #003366;  /* Bleu marine pour l'arrière-plan */
    }
    h1, h2, h3 {
        color: #FFD700;  /* Jaune doré pour les titres */
        font-weight: bold;
    }
    .stButton>button {
        background-color: #FFD700;  /* Jaune doré pour les boutons */
        color: #003366;  /* Texte en bleu marine */
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #FFC300;  /* Jaune plus clair au survol */
    }
    .stTextInput, .stTextArea, .stSelectbox, .stNumberInput {
        background-color: #ffffff; /* Fond blanc pour les champs */
        border-radius: 5px; /* Coins arrondis */
        border: 1px solid #003366; /* Bordure bleu marine */
    }
    </style>
    """, unsafe_allow_html=True)

# Affichage du logo de la Poste Tunisienne
logo_path = r"C:\Users\Islem\Desktop\prediction_delais\logo poste tunisienne.png"
try:
    st.image(logo_path, width=150, caption="La Poste Tunisienne")
except Exception as e:
    st.error(f"Erreur lors du chargement de l'image : {str(e)}")

# Titre principal
st.title("Prédiction des Mandats Minute - Poste Tunisienne")

# Sidebar pour le chargement des fichiers
st.sidebar.header("Charger des Données")
uploaded_file = st.sidebar.file_uploader("Charger un fichier CSV ou Excel", type=["csv", "xlsx", "xls"])

# Initialisation de la variable pour stocker les données
data = None

# Chargement des données si un fichier est téléchargé
if uploaded_file is not None:
    if uploaded_file.name.endswith('.csv'):
        data = pd.read_csv(uploaded_file)
    else:
        data = pd.read_excel(uploaded_file)

    st.sidebar.success("Données chargées avec succès.")

# Entrée des paramètres pour la prédiction avec texte en bleu marin et police plus fine
st.markdown("""
    <h2 style='color: #003366; font-family: "Arial", sans-serif; font-weight: normal; font-size: 20px;'>
    Entrez les informations demandées ci-dessous pour obtenir une estimation de la durée de traitement.
    </h2>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    montant_mandat = st.number_input("Montant du Mandat (DT)", min_value=0.0, format="%.2f", help="Entrez le montant en dinars tunisiens.")
    date_emission = st.date_input("Date d'Émission", value=datetime.today(), help="Sélectionnez la date d'émission du mandat.")

with col2:
    type_mandat = st.selectbox("Type de Mandat", ["M1406", "MCRBT", "MEXP", "MSERV"], help="Sélectionnez le type de mandat.")
    type_identite_expediteur = st.selectbox("Type d'Identité de l'Expéditeur", ["CIN", "Passeport", "Carte de Séjour"], help="Sélectionnez le type d'identité de l'expéditeur.")
    notes = st.text_area("Commentaires supplémentaires", placeholder="Ajoutez des notes ou informations supplémentaires.")





# Fonction de prédiction simulée (à remplacer par le modèle réel)
def predict_dur_class(input_df):
    return np.random.randint(1, 11, size=input_df.shape[0])  # Remplacez cette ligne par votre modèle de prédiction

# Bouton pour déclencher la prédiction
if st.button("Prédire la Durée du Mandat"):
    with st.spinner("Calcul des prédictions en cours..."):
        # Création d'un DataFrame avec les données d'entrée
        input_data = pd.DataFrame({
            "Montant": [montant_mandat],
            "CodeTypeMandat": [type_mandat],
            "Date d'Émission": [date_emission],
            "TypeIdentiteExp": [type_identite_expediteur],
            "Commentaires": [notes]
        })
        
        # Calcul de la prédiction
        prediction = predict_dur_class(input_data)
        
        # Affichage du résultat
        st.success(f"La durée prédite du mandat est : {prediction[0]} jours.")
        
        # Affichage des détails de la prédiction dans un tableau
        st.subheader("Détails de la Prédiction")
        result_df = input_data.assign(Durée_Prédit=prediction)
        st.dataframe(result_df.style.set_table_attributes('style="color: #003366;"'))

        # Graphique de la durée prédite par type de mandat
        fig = px.bar(result_df, x="CodeTypeMandat", y="Durée_Prédit", title="Durée Prédite par Type de Mandat")
        st.plotly_chart(fig)

# Options d'analyse supplémentaires dans la barre latérale
st.sidebar.header("Analyse des Données")
st.sidebar.markdown("Utilisez les options ci-dessous pour analyser les données chargées.")

# Filtrer les données par type de mandat et afficher les graphiques
if data is not None:
    if 'CodeTypeMandat' in data.columns:
        mandat_types = data['CodeTypeMandat'].unique()
        selected_type = st.sidebar.selectbox("Filtrer par Type de Mandat", mandat_types)

        # Filtrer les données
        filtered_data = data[data['CodeTypeMandat'] == selected_type]
        st.subheader(f"Analyse des Mandats pour le type {selected_type}")

        # Supprimer les colonnes sensibles
        columns_to_drop = ['Exp_NumPieceIdentite', 'Exp_NumGSM', 'Benef_NumGSM', 'Benef_NumPieceIDentite', 
                           'Mand_BenCinDatelivraison', 'Mand_BenCinLieuDelivrance', 'Mand_BenDateNaissance']
        filtered_data = filtered_data.drop(columns=columns_to_drop, errors='ignore')

        # Graphiques de distribution des montants
        fig1 = px.histogram(filtered_data, x="Mand_Montant", title="Distribution des Montants des Mandats")
        st.plotly_chart(fig1)

        # Graphiques de distribution des durées
        fig2 = px.histogram(filtered_data, x="Mand_Duree", title="Distribution des Durées des Mandats")
        st.plotly_chart(fig2)

        # Graphique de la distribution du type d'identité de l'expéditeur
        if 'Mand_TypeIdentiteExp' in filtered_data.columns:
            fig3 = px.histogram(filtered_data, x="Mand_TypeIdentiteExp", title="Distribution des Types d'Identité de l'Expéditeur")
            st.plotly_chart(fig3)

        # Option pour télécharger les résultats
        if st.sidebar.button("Télécharger les Résultats"):
            result_csv = result_df.to_csv(index=False)
            st.sidebar.download_button("Télécharger le fichier CSV des résultats", result_csv, "resultats.csv", "text/csv")
    else:
        st.sidebar.error("La colonne 'CodeTypeMandat' est manquante dans les données.")
else:
    st.sidebar.warning("Aucun fichier chargé. Veuillez d'abord charger un fichier pour utiliser les options d'analyse.")
