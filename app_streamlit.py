import streamlit as st
# #sur mac : commande à lancer pour faire run le serveur  : streamlit run /Users/augustinhannebert/Nextcloud/FAC/M2/S1/open_data/app_streamlit.py
# # #
# sur windows augustin: python -m streamlit  run c:/Users/augustin.hannebert/Documents/open_data/app_streamlit.py
# sur windows paul: python -m streamlit  run C:\Users\paulp\OneDrive\Documents\Open_data_M2\open_data\app_streamlit.py

import geopandas as gpd

#-------------------------------------------------------------------------------------------------
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import time
import matplotlib.pyplot as plt
import seaborn as sns



df = pd.read_csv("dataset_olympics (copie).csv", sep=";")

# Multipage setup
PAGES = {
    "Home": "home",
    "Data View": "data_view",
    "Country analysis": "country_analysis",
    "Sex analysis": "sex_analysis",
    "Athlete analysis": "athlete_analysis"
}
st.markdown("""
<style>
div.row-widget.stRadio > div{flex-direction:row;}
label[data-baseweb="radio"]{padding:10px; border-radius:10px; margin:5px; border:2px solid #ccc; display:flex; align-items:center; justify-content:center;}
label[data-baseweb="radio"]:hover{border-color:#ff4b4b;}
</style>
""", unsafe_allow_html=True)

st.sidebar.title('Navigation')
selection = st.sidebar.radio("Go to", list(PAGES.keys()))

# Home page
if selection == "Home":
    st.header("Les jeux olympics à travers les âges")
    st.write("Utilisez la barre de navigation pour décuvrir l'application")
    st.image("https://i.giphy.com/media/26ufmepVftH5Y2V7q/giphy.webp")  # Link to your logo or a welcome image
    # Ajouter un pied de page
    footer = """
    <style>
    .footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    background-color: white;
    color: black;
    text-align: center;
    }
    </style>
    <div class="footer">
    <p>Developed with ❤️ by Augustin Hannebert & Paul Peyrard 😎</p>
    </div>
    """
    st.markdown(footer, unsafe_allow_html=True)

# Data View page
elif selection == "Data View":
    st.header("Data Viewer")
    if st.checkbox("Charger les données"):
        # Créer un placeholder pour l'image
        placeholder = st.empty()
        
        # Afficher l'image temporaire dans le placeholder
        placeholder.image("https://cdn.dribbble.com/users/79654/screenshots/1436532/olympic_games_rings_loading.gif")
        
        # Attendre 3 secondes
        time.sleep(1.2)

        # Clear the placeholder (cela efface l'image)
        placeholder.empty()

        # Afficher le DataFrame après que l'image a disparu
        st.write(df)

elif selection == "Athlete analysis":
    st.header("Analyse de caracéristiques physiques des athlètes")

    #Nuage 3D age poids taille
    if st.checkbox('Nuage 3D : Age, poids, taille.'):
        st.subheader("Nuage 3D : Age, poids, taille.")
        st.write("Choississez les athlèthes que vous voulez comparer. Les variables sont leur poids, l'âge et la taille.")
        columns_to_copy = ['Name', 'Age', 'Height', 'Weight']
        df_copy = df[columns_to_copy].copy().drop_duplicates()
        df_copy = df_copy.dropna()

        # Sélectionnez les colonnes et supprimez les doublons et les valeurs nulles
        columns_to_copy = ['Name', 'Age', 'Height', 'Weight']
        df_copy = df[columns_to_copy].copy().drop_duplicates(subset='Name')
        df_copy = df_copy.dropna()#.head(200)

        # Page Streamlit
        selected_names = st.multiselect("Choisissez un ou plusieurs athlètes.", df_copy['Name'].unique(), default=None)

        # Filtrer le DataFrame en fonction des noms sélectionnés
        if selected_names:
            filtered_df = df_copy[df_copy['Name'].isin(selected_names)]
            fig = px.scatter_3d(filtered_df, x='Age', y='Height', z='Weight', text='Name')
            st.plotly_chart(fig, use_container_width=True)
        else:
            filtered_df = df_copy
            st.image("https://media2.giphy.com/media/xPHPzwRnORKt9xPDDi/giphy.gif")  
    
    #scatter plot hommes femmes et age poids tailles    
    elif st.checkbox('Scatter Plot Interactif entre les hommes et les femmes selon leurs poids, taille, âge'):
        # # Scatter plot
        st.subheader("Scatter Plot Interactif")
        st.write("Visualisez les individus selon le poids, la taille ou l' âge. Confrontez les hommes et les femmes.")


            # Sélection du sexe
        selected_sex = st.selectbox("Sélectionnez le sexe:", ["Tous", "Hommes", "Femmes"])

        # Filtrer les données basées sur le sexe sélectionné
        if selected_sex == "Hommes":
            df_filtered = df[df['Sex'] == 'M']
            color_discrete_map = {'M': 'blue'}
        elif selected_sex == "Femmes":
            df_filtered = df[df['Sex'] == 'F']
            color_discrete_map = {'F': 'pink'}
        else:
            df_filtered = df
            color_discrete_map = {'F': 'pink', 'M': 'blue'} # Utilisez un dictionnaire pour mapper les couleurs

        # Sélection des variables pour l'axe x et y
        col1 = st.selectbox("Choisissez la première variable", ['Age', 'Height', 'Weight'])
        col2 = st.selectbox("Choisissez la seconde variable", ['Age', 'Height', 'Weight'], index=1)

        # Création du scatter plot avec Plotly
        fig = px.scatter(
            df_filtered,
            x=col1,
            y=col2,
            color="Sex",
            color_discrete_map=color_discrete_map, # Utilisez la cartographie des couleurs ici
            opacity=0.5,
            size_max=60,
            labels={"Sex": "Sexe"} # Traduire la légende
        )

        # Affichage du scatter plot
        st.plotly_chart(fig, use_container_width=True)
    
    #distribution des ages en fonction des gagants ou des perdants
    elif st.checkbox('Age des athlèthes'):
        # age distribution ________________________________________
        st.header("Age Distribution")
        st.write("Here you can view the age distribution of your data.")
        st.write("You can select winners / lossers / both")

        # Widget checkbox pour filtrer par médaille
        filter_medal = st.checkbox("Winners", value=False)

        # Widget checkbox pour filtrer par non médaille
        filter_no_medal = st.checkbox("Loosers", value=False)

        # Filtrer les données en fonction des cases à cocher
        if filter_medal and filter_no_medal:
            filtered_df = df.copy()
        elif filter_medal:
            filtered_df = df[df['Win'] != 'Loose']
        elif filter_no_medal:
            filtered_df = df[df['Win'] == 'Loose']
        else:
            filtered_df = df.copy()



        # Créer un histogramme des âges
        fig = px.histogram(filtered_df, x='Age', title='Age Distribution')
        fig.update_xaxes(title_text='Age')
        fig.update_yaxes(title_text='Count')

        # Page Streamlit
        st.plotly_chart(fig, use_container_width=True)

elif selection == 'Country analysis':
    st.header('Country Analysis')
    st.subheader('Particiations des pays')
    st.write('Quels sont les pays ayant le plus participés aux jeux ? ')

    # Calculer les 10 premiers pays les plus fréquemment présents
    # Calculer les pays les plus fréquemment présents
    top_countries = df.groupby('Team').size().sort_values(ascending=False)
    top_countries = top_countries.rename('Count')

    # Widget slider pour choisir le nombre de pays à afficher
    num_countries_to_show = st.slider("Choisissez le nombre de pays à afficher", min_value=1, max_value=25, value=3)

    # Prendre les premiers num_countries_to_show pays
    top_countries = top_countries.head(num_countries_to_show)

    # Créer un histogramme à partir des données du tableau avec une couleur personnalisée
    fig = px.bar(top_countries.reset_index(), x='Team', y='Count', labels={'index': 'Country', 'Team': 'Count'}, title=f'Top {num_countries_to_show} des pays ayant le plus de participations')
    fig.update_xaxes(title_text='Country')
    fig.update_yaxes(title_text='Nombre')

    # Page Streamlit
    st.plotly_chart(fig, use_container_width=True)

elif selection == "Sex analysis":
    st.header('Analyses entre les hommes et les femmes')
    st.write('Choisissez les analyses qui peuvent vous intéresser')
    if st.checkbox('participation des hommes et des femmes'):
        st.subheader("Participation des hommes et des femmes")
        # Sélectionner la saison (été, hiver, ou les deux)

        selected_seasons = st.multiselect("Choisissez les saisons qui vous intéressent.", ["Summer", "Winter"],  default=["Summer", "Winter"])
        if selected_seasons == []:
            st.image("https://media.tenor.com/TaSMM2QzA30AAAAd/pick-one-decide.gif")
        else:            
            # Filtrer les données en fonction de la saison choisie
            filtered_df = df.copy()
            filtered_df = df[df['Season'].isin(selected_seasons) if selected_seasons else df]

            # Slider pour sélectionner la période d'étude (année minimale et maximale)
            year_range = st.slider("Selectionnez la période", min_value=filtered_df['Year'].min(), max_value=filtered_df['Year'].max(), value=(filtered_df['Year'].min(), filtered_df['Year'].max()))

            # Filtrer les données en fonction de la période choisie avec le slider
            min_year, max_year = year_range
            filtered_df = filtered_df[(filtered_df['Year'] >= min_year) & (filtered_df['Year'] <= max_year)]

            # Calculer la parité homme/femme par année
            gender_counts = filtered_df.groupby('Year')['Sex'].value_counts().unstack(fill_value=0)
            gender_counts['Total'] = gender_counts['M'] + gender_counts['F']

            # Créer un plot avec deux courbes (femmes en rose et hommes en bleu)
            fig = px.line(gender_counts, x=gender_counts.index, y=['F', 'M'], title='Gender Parity Over Time')
            bool=True
            # Personnaliser les couleurs des courbes
            fig.update_xaxes(title_text='Year')
            fig.update_yaxes(title_text='Count')

            st.plotly_chart(fig, use_container_width=True)
            
        
    elif st.checkbox('évolution de la parité'):#évolution parité 
        st.subheader('La parité au cours du temps')
        # Filter the data for the specified years and group by 'Year', 'NOC', and 'Sex'
        filtered_df = df[df['Year'].isin([1936, 1956, 1976, 1996, 2016])]
        counts_NOC = filtered_df.groupby(['Year', 'NOC', 'Sex'])['ID'].nunique().reset_index()

        # Pivot to get separate columns for Male and Female
        counts_NOC = counts_NOC.pivot_table(index=['Year', 'NOC'], columns='Sex', values='ID', fill_value=0).reset_index()

        # Calculate the 'Total' and filter for NOCs with at least 50 athletes
        counts_NOC['Total'] = counts_NOC['M'] + counts_NOC['F']
        counts_NOC = counts_NOC[counts_NOC['Total'] > 49]

        # Rename columns for clarity
        counts_NOC.rename(columns={'M': 'Male', 'F': 'Female'}, inplace=True)

        # Convert 'Year' to a categorical type for better color mapping in Plotly
        counts_NOC['Year'] = counts_NOC['Year'].astype(str)

        # Plotting with Plotly Express
        fig = px.scatter(counts_NOC, x='Male', y='Female', color='Year', 
                        title='Participation des hommes vs participation des femmes.',
                        trendline='ols') # Ordinary Least Squares regression line

        # Customizing the layout of the plot
        fig.update_layout(
            xaxis_title="Nombre d'athlètes masculins",
            yaxis_title="Nombre d'athlèthes féminins",
            legend_title="Année",
            legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
        )

        # Add a 1:1 line to indicate parity
        fig.add_shape(type="line", x0=0, y0=0, x1=max(counts_NOC['Total']), y1=max(counts_NOC['Total']),
                    line=dict(color="Black", width=2, dash="dash"))

        # Show plot in Streamlit
        st.plotly_chart(fig, use_container_width=True)
    
