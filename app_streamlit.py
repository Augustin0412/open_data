import streamlit as st
# #sur mac : commande à lancer pour faire run le serveur  : streamlit run /Users/augustinhannebert/Nextcloud/FAC/M2/S1/open_data/app_streamlit.py
# # #
# sur windows augustin: python -m streamlit  run c:/Users/augustin.hannebert/Documents/open_data/app_streamlit.py
# sur windows paul: python -m streamlit  run C:\Users\paulp\OneDrive\Documents\Open_data_M2\open_data\app_streamlit.py


#-------------------------------------------------------------------------------------------------
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import time



df = pd.read_csv("dataset_olympics (copie).csv", sep=";")

PAGES = {
    "Page d'accueil": "home",
    "Vue Données": "data_view",
    "Analyse Pays": "country_analysis",
    "Analyse Sexes": "sex_analysis",
    "Analyse Athlètes": "athlete_analysis"
}
st.markdown("""
<style>
div.row-widget.stRadio > div{flex-direction:row;}
label[data-baseweb="radio"]{padding:10px; border-radius:10px; margin:5px; border:2px solid #ccc; display:flex; align-items:center; justify-content:center;}
label[data-baseweb="radio"]:hover{border-color:#ff4b4b;}
</style>
""", unsafe_allow_html=True)

st.markdown("""
    <style>
    .stCheckbox {
        display: flex;
        justify-content: start;
        padding: 5px;
        margin: 5px;
        background-color: #f0f2f6;
        border-radius: 10px;
    }
    .stCheckbox label {
        font-size: 16px;
        color: #0a58ca;
    }
    .stCheckbox input {
        accent-color: #0a58ca;
    }
    </style>
    """, unsafe_allow_html=True)


st.sidebar.title('Navigation')
selection = st.sidebar.radio("Aller à", list(PAGES.keys()))

if selection == "Page d'accueil":
    st.header("Les jeux olympics à travers les âges")
    st.write("Utilisez la barre de navigation pour découvrir l'application")
    st.image("https://i.giphy.com/media/26ufmepVftH5Y2V7q/giphy.webp") 
    
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

# Page d'accueil
elif selection == "Vue Données":
    st.header("Vue Données")
    if st.checkbox("Charger les données"):
        placeholder = st.empty()
        
        placeholder.image("https://cdn.dribbble.com/users/79654/screenshots/1436532/olympic_games_rings_loading.gif")
        
        time.sleep(1.2)

        placeholder.empty()

        st.write(df)

# Athlete Analysis page
elif selection == "Analyse Athlètes":
    st.header("Analyse de caracéristiques physiques des athlètes")

    #Nuage 3D age poids taille
    if st.checkbox('Nuage 3D : Age, poids, taille.'):
        st.subheader("Nuage 3D : Age, poids, taille.")
        st.write("Choississez les athlèthes que vous voulez comparer. Les variables sont leur poids, l'âge et la taille.")
        columns_to_copy = ['Name', 'Age', 'Height', 'Weight']
        df_copy = df[columns_to_copy].copy().drop_duplicates()
        df_copy = df_copy.dropna()

        columns_to_copy = ['Name', 'Age', 'Height', 'Weight']
        df_copy = df[columns_to_copy].copy().drop_duplicates(subset='Name')
        df_copy = df_copy.dropna()#.head(200)

        # liste déroulante
        selected_names = st.multiselect("Choisissez un ou plusieurs athlètes.", df_copy['Name'].unique(), default=None)

        if selected_names:
            filtered_df = df_copy[df_copy['Name'].isin(selected_names)]
            fig = px.scatter_3d(filtered_df, x='Age', y='Height', z='Weight', text='Name')
            st.plotly_chart(fig, use_container_width=True)
        else:
            filtered_df = df_copy
            st.image("https://media2.giphy.com/media/xPHPzwRnORKt9xPDDi/giphy.gif")  
    
    #scatter plot hommes femmes et age poids tailles    
    elif st.checkbox('Scatter Plot Interactif entre les hommes et les femmes selon leurs poids, taille, âge'):
        st.subheader("Scatter Plot Interactif")
        st.write("Visualisez les individus selon le poids, la taille ou l' âge. Confrontez les hommes et les femmes.")


        # Sélection du sexe
        selected_sex = st.selectbox("Sélectionnez le sexe:", ["Tous", "Hommes", "Femmes"])

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

        fig = px.scatter(
            df_filtered,
            x=col1,
            y=col2,
            color="Sex",
            color_discrete_map=color_discrete_map,
            opacity=0.5,
            size_max=60,
            labels={"Sex": "Sexe"}
        )

        st.plotly_chart(fig, use_container_width=True)
    
    #distribution des ages en fonction des gagants ou des perdants
    elif st.checkbox('Age Athlèthes'):
        st.header("Distribution de l'âge")
        st.write("Ici tu peux voir la distribution de l'âge de tes données.")
        st.write("Tu peux sélectionner Winners (gagnants) / Loosers (perdants) / Les deux")

        # Checkbox pour la victoire ou non
        filter_medal = st.checkbox("Gagnants", value=False)
        filter_no_medal = st.checkbox("Perdants", value=False)

        if filter_medal and filter_no_medal:
            filtered_df = df.copy()
        elif filter_medal:
            filtered_df = df[df['Win'] != 'Loose']
        elif filter_no_medal:
            filtered_df = df[df['Win'] == 'Loose']
        else:
            filtered_df = df.copy()


        fig = px.histogram(filtered_df, x='Age', title="Distribution de l'âge")
        fig.update_xaxes(title_text='Age')
        fig.update_yaxes(title_text='Nombre')

        st.plotly_chart(fig, use_container_width=True)

# Country Analysis Page
elif selection == 'Analyse Pays':
    st.header('Analyse des Pays')
    st.subheader('Particiations des pays')
    st.write('Quels sont les pays ayant le plus participés aux jeux ? ')

    # les pays les + fréquentés, en fonction du taux de victoire
    country_wins = df.groupby(['Team', 'Win']).size().unstack().fillna(0)

    # Slider
    num_countries_to_show = st.slider("Choisissez le nombre de pays à afficher", min_value=1, max_value=25, value=3)

    top_countries = country_wins.sum(axis=1).sort_values(ascending=False).head(num_countries_to_show)

    country_wins = country_wins.loc[top_countries.index]

    fig = px.bar(country_wins, labels={'value': 'Nombre', 'variable': 'Statut'}, title=f'Top {num_countries_to_show} des pays ayant le plus de participations',     color_discrete_map={'Win': 'green', 'Loose': 'red'})
    fig.update_xaxes(title_text='Pays')
    fig.update_yaxes(title_text='Nombre')
    fig.update_layout(barmode='stack')

    st.plotly_chart(fig, use_container_width=True)

# Page Analyse des sexes
elif selection == "Analyse Sexes":
    st.header('Analyses entre les hommes et les femmes')
    st.write('Choisissez les analyses qui peuvent vous intéresser')

    # Participation homme et femme
    if st.checkbox('Participation des hommes et des femmes'):
        st.subheader("Participation des hommes et des femmes")

        # liste déroulante
        selected_seasons = st.multiselect("Choisissez les saisons qui vous intéressent.", ["Summer", "Winter"],  default=["Summer", "Winter"])
        if selected_seasons == []:
            st.image("https://media.tenor.com/TaSMM2QzA30AAAAd/pick-one-decide.gif")
        else:            
            filtered_df = df.copy()
            filtered_df = df[df['Season'].isin(selected_seasons) if selected_seasons else df]

            # Slider
            year_range = st.slider("Selectionnez la période", min_value=filtered_df['Year'].min(), max_value=filtered_df['Year'].max(), value=(filtered_df['Year'].min(), filtered_df['Year'].max()))

            min_year, max_year = year_range
            filtered_df = filtered_df[(filtered_df['Year'] >= min_year) & (filtered_df['Year'] <= max_year)]

            gender_counts = filtered_df.groupby('Year')['Sex'].value_counts().unstack(fill_value=0)
            gender_counts['Total'] = gender_counts['M'] + gender_counts['F']

            fig = px.line(gender_counts, x=gender_counts.index, y=['F', 'M'], title='Parité des genres dans le temps')
            bool=True

            fig.update_xaxes(title_text='Année')
            fig.update_yaxes(title_text='Nombre')

            st.plotly_chart(fig, use_container_width=True)
            
    # Evolution de la parité
    elif st.checkbox('Evolution de la parité'): 
        st.subheader('La parité au cours du temps')

        filtered_df = df[df['Year'].isin([1936, 1956, 1976, 1996, 2016])]
        counts_NOC = filtered_df.groupby(['Year', 'NOC', 'Sex'])['ID'].nunique().reset_index()

        counts_NOC = counts_NOC.pivot_table(index=['Year', 'NOC'], columns='Sex', values='ID', fill_value=0).reset_index()

        counts_NOC['Total'] = counts_NOC['M'] + counts_NOC['F']
        counts_NOC = counts_NOC[counts_NOC['Total'] > 49]

        counts_NOC.rename(columns={'M': 'Male', 'F': 'Female'}, inplace=True)

        counts_NOC['Year'] = counts_NOC['Year'].astype(str)

        fig = px.scatter(counts_NOC, x='Male', y='Female', color='Year', 
                        title='Participation des hommes vs participation des femmes.',
                        trendline='ols',
                        hover_data="NOC")

        fig.update_layout(
            xaxis_title="Nombre d'athlètes masculins",
            yaxis_title="Nombre d'athlèthes féminins",
            legend_title="Année",
            legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
        )

        fig.add_shape(type="line", x0=0, y0=0, x1=max(counts_NOC['Total']), y1=max(counts_NOC['Total']),
                    line=dict(color="Black", width=2, dash="dash"))

        st.plotly_chart(fig, use_container_width=True)
    
