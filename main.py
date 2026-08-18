import streamlit as st
import pandas as pd
import plotly.express as px
import requests

# 1. Configurazione della pagina Streamlit
st.set_page_config(
    page_title="Monitor Aree Idonee & PNIEC Regioni",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🗺️ Mappa Italia: Aree Idonee, PNIEC e Politica Regionale")
st.markdown("Seleziona una regione sulla mappa o dal menu per visualizzare l'appartenenza politica del Presidente, il gap di GW rispetto agli obiettivi PNIEC e la normativa sulle aree idonee.")

# 2. Download dinamico del GeoJSON delle regioni italiane (ISTAT/OpenPolis)
@st.cache_data
def load_geojson():
    url = "https://raw.githubusercontent.com/openpolis/geojson-italy/master/geojson/limits_IT_regions.geojson"
    response = requests.get(url)
    return response.json()

geojson_data = load_geojson()

# 3. Struttura Dati con le 20 Regioni
# (Nota: I dati sui GW e i link alle leggi possono essere aggiornati nel tempo)
data = {
    "regione": [
        "Lombardia", "Lazio", "Campania", "Sicilia", "Veneto", 
        "Emilia-Romagna", "Piemonte", "Puglia", "Toscana", "Calabria", 
        "Sardegna", "Liguria", "Marche", "Abruzzo", "Friuli Venezia Giulia", 
        "Trentino-Alto Adige/Südtirol", "Umbria", "Basilicata", "Molise", "Valle d'Aosta/Vallée d'Aoste"
    ],
    "presidente": [
        "Attilio Fontana", "Francesco Rocca", "Vincenzo De Luca", "Renato Schifani", "Luca Zaia",
        "Michele De Pascale", "Alberto Cirio", "Michele Emiliano", "Eugenio Giani", "Roberto Occhiuto",
        "Alessandra Todde", "Marco Bucci", "Francesco Acquaroli", "Marco Marsilio", "Massimiliano Fedriga",
        "Arno Kompatscher / Maurizio Fugatti", "Stefania Proietti", "Vito Bardi", "Francesco Roberti", "Renzo Testolin"
    ],
    "coalizione": [
        "Centrodestra (Lega)", "Centrodestra (FdI)", "Centrosinistra (PD)", "Centrodestra (FI)", "Centrodestra (Lega)",
        "Centrosinistra (PD)", "Centrodestra (FI)", "Centrosinistra (PD)", "Centrosinistra (PD)", "Centrodestra (FI)",
        "Centrosinistra (M5S/PD)", "Centrodestra (Civica/CDX)", "Centrodestra (FdI)", "Centrodestra (FdI)", "Centrodestra (Lega)",
        "Autonomisti / Centrodestra", "Centrosinistra (Civica/CSX)", "Centrodestra (FI)", "Centrodestra (FI)", "Autonomisti (UV)"
    ],
    "orientamento": [
        "Centrodestra", "Centrodestra", "Centrosinistra", "Centrodestra", "Centrodestra",
        "Centrosinistra", "Centrodestra", "Centrosinistra", "Centrosinistra", "Centrodestra",
        "Centrosinistra", "Centrodestra", "Centrodestra", "Centrodestra", "Centrodestra",
        "Autonomisti", "Centrosinistra", "Centrodestra", "Centrodestra", "Autonomisti"
    ],
    "target_pniec_gw": [8.5, 6.2, 5.0, 10.4, 6.3, 6.3, 5.8, 7.2, 4.1, 4.5, 6.2, 1.5, 2.8, 2.4, 2.1, 1.8, 1.6, 2.2, 0.9, 0.4],
    "installato_attuale_gw": [4.2, 2.4, 2.8, 5.1, 3.3, 3.9, 3.1, 6.2, 2.2, 2.9, 2.3, 0.5, 1.4, 1.2, 1.1, 1.2, 0.9, 1.8, 0.7, 0.2],
    "legge_aree_idonee_nome": [
        "Proposta L.R. Aree Idonee Lombardia", "Delibera Giunta Lazio FER", "D.D. Campania Aree Idonee",
        "DDG Sicilia Aree Idonee", "L.R. Veneto Aree Idonee", "L.R. 5/2026 Emilia-Romagna",
        "L.R. Piemonte Aree Idonee", "DGR Puglia FER", "L.R. Toscana Aree Idonee",
        "DGR Calabria Aree Idonee", "L.R. 5/2024 (Sardegna)", "L.R. Liguria FER",
        "L.R. Marche Aree Idonee", "L.R. Abruzzo Aree Idonee", "L.R. FVG Aree Idonee",
        "Delibera Prov. Autonoma Aree Idonee", "L.R. Umbria Aree Idonee", "L.R. Basilicata FER",
        "L.R. Molise Aree Idonee", "L.R. VdA Aree Idonee"
    ],
    "legge_aree_idonee_url": [
        "https://www.regione.lombardia.it", "https://www.regione.lazio.it", "https://www.regione.campania.it",
        "https://www.regione.sicilia.it", "https://www.regione.veneto.it", "https://www.regione.emilia-romagna.it",
        "https://www.regione.piemonte.it", "https://www.regione.puglia.it", "https://www.regione.toscana.it",
        "https://www.regione.calabria.it", "https://www.regione.sardegna.it", "https://www.regione.liguria.it",
        "https://www.regione.marche.it", "https://www.regione.abruzzo.it", "https://www.regione.fvg.it",
        "https://www.provincia.tn.it", "https://www.regione.umbria.it", "https://www.regione.basilicata.it",
        "https://www.regione.molise.it", "https://www.regione.vda.it"
    ]
}

df = pd.DataFrame(data)

# Calcolo del ritardo/gap in GW rispetto al PNIEC
df["ritardo_pniec_gw"] = (df["target_pniec_gw"] - df["installato_attuale_gw"]).round(2)
df["percentuale_completamento"] = ((df["installato_attuale_gw"] / df["target_pniec_gw"]) * 100).round(1)

# 4. Sidebar per selezione manuale alternativa
st.sidebar.header("🔍 Filtri & Selezione")
regione_selezionata_sidebar = st.sidebar.selectbox(
    "Seleziona direttamente una Regione:",
    options=["Tutte"] + list(df["regione"].unique())
)

# 5. Costruzione Mappa Choropleth Plotly
fig = px.choropleth_mapbox(
    df,
    geojson=geojson_data,
    locations="regione",
    featureidkey="properties.reg_name",
    color="ritardo_pniec_gw",
    color_continuous_scale="Reds",
    mapbox_style="carto-positron",
    zoom=4.8,
    center={"lat": 41.9, "lon": 12.5},
    opacity=0.7,
    hover_name="regione",
    hover_data={
        "presidente": True,
        "coalizione": True,
        "ritardo_pniec_gw": ":.2f GW",
        "target_pniec_gw": ":.2f GW",
        "regione": False
    },
    labels={
        "ritardo_pniec_gw": "Gap PNIEC (GW)",
        "presidente": "Presidente",
        "coalizione": "Coalizione"
    }
)

fig.update_layout(
    margin={"r": 0, "t": 0, "l": 0, "b": 0},
    height=550,
    clickmode="event+select"
)

# 6. Layout a colonne (Mappa a sinistra, Dettaglio 3 Info a destra)
col_map, col_details = st.columns([1.3, 1])

with col_map:
    st.subheader("Mappa Italia - Ritardo Rinnovabili (GW)")
    map_selection = st.plotly_chart(
        fig, 
        use_container_width=True, 
        on_select="rerun", 
        selection_mode="points"
    )

# 7. Intercettazione della selezione (Click sulla mappa o Sidebar)
selected_region_name = None

# Verifica se l'utente ha cliccato sulla mappa
if map_selection and "selection" in map_selection and map_selection["selection"]["points"]:
    point = map_selection["selection"]["points"][0]
    if "location" in point:
        selected_region_name = point["location"]

# Se l'utente usa il menu sidebar, la sidebar ha la precedenza
if regione_selezionata_sidebar != "Tutte":
    selected_region_name = regione_selezionata_sidebar

# 8. Visualizzazione delle 3 Informazioni Dettagliate
with col_details:
    st.subheader("📋 Scheda Informativa Regione")
    
    if selected_region_name:
        row = df[df["regione"] == selected_region_name].iloc[0]
        
        st.markdown(f"### **{row['regione']}**")
        
        # INFO 1: Appartenenza Politica
        st.info(
            f"**1. Presidente & Politica**\n\n"
            f"👤 **Presidente:** {row['presidente']}\n\n"
            f"🏛️ **Coalizione / Partito:** {row['coalizione']}"
        )
        
        # INFO 2: Ritardo PNIEC in GW
        st.warning(
            f"**2. Ritardo PNIEC (Rinnovabili)**\n\n"
            f"⚠️ **Gap da installare:** `{row['ritardo_pniec_gw']} GW` mancanti al 2030\n\n"
            f"📊 **Target totale PNIEC:** {row['target_pniec_gw']} GW | **Attuale:** {row['installato_attuale_gw']} GW\n\n"
            f"📈 **Avanzamento:** {row['percentuale_completamento']}%"
        )
        
        # INFO 3: Link Legge Regionale Aree Idonee
        st.success(
            f"**3. Legge Regionale Aree Idonee**\n\n"
            f"📜 **Normativa:** {row['legge_aree_idonee_nome']}\n\n"
            f"🔗 [Apri il testo ufficiale / Portale regionale]({row['legge_aree_idonee_url']})"
        )
        
    else:
        st.write("👈 **Clicca su una regione nella mappa** oppure selezionala dal menu a sinistra per visualizzare i 3 dettagli.")

# 9. Tabella Generale Comparativa in fondo alla pagina
st.markdown("---")
with st.expander("📊 Visualizza la tabella completa delle 20 regioni"):
    st.dataframe(
        df[["regione", "presidente", "coalizione", "target_pniec_gw", "installato_attuale_gw", "ritardo_pniec_gw", "legge_aree_idonee_nome"]],
        column_config={
            "regione": "Regione",
            "presidente": "Presidente",
            "coalizione": "Schieramento",
            "target_pniec_gw": st.column_config.NumberColumn("Target PNIEC (GW)", format="%.1f GW"),
            "installato_attuale_gw": st.column_config.NumberColumn("Installato (GW)", format="%.1f GW"),
            "ritardo_pniec_gw": st.column_config.NumberColumn("Ritardo (GW)", format="%.2f GW"),
            "legge_aree_idonee_nome": "Riferimento Normativo"
        },
        use_container_width=True,
        hide_index=True
    )
