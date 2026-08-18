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

st.title("🗺️ Mappa Italia: Scostamento Target PNIEC e Aree Idonee")
st.markdown("Seleziona una regione sulla mappa o dal menu per visualizzare l'appartenenza politica del Presidente, lo scostamento dal target in MW e la normativa sulle aree idonee.")

# 2. Download dinamico del GeoJSON delle regioni italiane (ISTAT/OpenPolis)
@st.cache_data
def load_geojson():
    url = "https://raw.githubusercontent.com/openpolis/geojson-italy/master/geojson/limits_IT_regions.geojson"
    response = requests.get(url)
    return response.json()

geojson_data = load_geojson()

# 3. Struttura Dati Aggiornata con Tabella Terna (Valori in MW)
data = {
    "regione": [
        "Abruzzo", "Basilicata", "Calabria", "Campania", "Emilia-Romagna", 
        "Friuli Venezia Giulia", "Lazio", "Liguria", "Lombardia", "Marche", 
        "Molise", "Piemonte", "Puglia", "Sardegna", "Sicilia", "Toscana", 
        "Trentino-Alto Adige/Südtirol", "Umbria", "Valle d'Aosta/Vallée d'Aoste", "Veneto"
    ],
    "presidente": [
        "Marco Marsilio", "Vito Bardi", "Roberto Occhiuto", "Vincenzo De Luca", "Michele De Pascale",
        "Massimiliano Fedriga", "Francesco Rocca", "Marco Bucci", "Attilio Fontana", "Francesco Acquaroli",
        "Francesco Roberti", "Alberto Cirio", "Michele Emiliano", "Alessandra Todde", "Renato Schifani", "Eugenio Giani",
        "Arno Kompatscher / Maurizio Fugatti", "Stefania Proietti", "Renzo Testolin", "Luca Zaia"
    ],
    "coalizione": [
        "Centrodestra", "Centrodestra", "Centrodestra", "Centrosinistra", "Centrosinistra",
        "Centrodestra", "Centrodestra", "Centrodestra", "Centrodestra", "Centrodestra",
        "Centrodestra", "Centrodestra", "Centrosinistra", "Centrosinistra", "Centrodestra", "Centrosinistra",
        "Autonomisti / Centrodestra", "Centrosinistra", "Autonomisti", "Centrodestra"
    ],
    "delta_mw": [
        -124, -182, -447, 91, 65, 
        314, 1428, -102, 697, -125, 
        -181, 422, -267, -599, -3, -302, 
        95, -193, -23, 377
    ],
    "installato_mw": [
        638, 697, 613, 1640, 2297, 1003, 3055, 238, 3923, 701, 
        156, 2262, 2610, 1336, 3393, 965, 543, 341, 40, 2612
    ],
    "target_mw": [
        763, 879, 1061, 1548, 2232, 689, 1628, 340, 3226, 825, 
        337, 1840, 2876, 1935, 3396, 1267, 449, 534, 63, 2236
    ]
}

df = pd.DataFrame(data)

# 4. Sidebar per selezione manuale alternativa
st.sidebar.header("🔍 Filtri & Selezione")
regione_selezionata_sidebar = st.sidebar.selectbox(
    "Seleziona direttamente una Regione:",
    options=["Tutte"] + list(df["regione"].unique())
)

# 5. Costruzione Mappa Choropleth Plotly con Scala Divergente (Rosso-Verde)
fig = px.choropleth_mapbox(
    df,
    geojson=geojson_data,
    locations="regione",
    featureidkey="properties.reg_name",
    color="delta_mw",
    color_continuous_scale="RdYlGn",     # Scala da Rosso a Verde
    color_continuous_midpoint=0,         # Forza lo zero al centro della scala (giallo/bianco)
    mapbox_style="carto-positron",
    zoom=4.8,
    center={"lat": 41.9, "lon": 12.5},
    opacity=0.8,
    hover_name="regione",
    hover_data={
        "presidente": True,
        "delta_mw": True,
        "installato_mw": True,
        "target_mw": True,
        "regione": False
    },
    labels={
        "delta_mw": "Scostamento dal Target (MW)",
        "presidente": "Presidente",
        "installato_mw": "Delta Installato [MW]",
        "target_mw": "Target Aree Idonee [MW]"
    }
)

fig.update_layout(
    margin={"r": 0, "t": 0, "l": 0, "b": 0},
    height=550,
    clickmode="event+select"
)

# 6. Layout a colonne
col_map, col_details = st.columns([1.3, 1])

with col_map:
    st.subheader("Mappa Italia - Scostamento Target (MW)")
    map_selection = st.plotly_chart(
        fig, 
        use_container_width=True, 
        on_select="rerun", 
        selection_mode="points"
    )

# 7. Intercettazione della selezione
selected_region_name = None

if map_selection and "selection" in map_selection and map_selection["selection"]["points"]:
    point = map_selection["selection"]["points"][0]
    if "location" in point:
        selected_region_name = point["location"]

if regione_selezionata_sidebar != "Tutte":
    selected_region_name = regione_selezionata_sidebar

# 8. Visualizzazione delle Informazioni Dettagliate
with col_details:
    st.subheader("📋 Scheda Informativa Regione")
    
    if selected_region_name:
        row = df[df["regione"] == selected_region_name].iloc[0]
        
        st.markdown(f"### **{row['regione']}**")
        
        # INFO 1: Appartenenza Politica
        st.info(
            f"**1. Presidente & Politica**\n\n"
            f"👤 **Presidente:** {row['presidente']}\n\n"
            f"🏛️ **Schieramento:** {row['coalizione']}"
        )
        
        # INFO 2: Scostamento in MW (Verde per anticipo, Rosso per ritardo)
        delta_val = row['delta_mw']
        if delta_val >= 0:
            st.success(
                f"**2. Avanzamento PNIEC (Dati Terna)**\n\n"
                f"✅ **In anticipo:** `+{delta_val} MW` rispetto al target progressivo\n\n"
                f"📊 **Target Periodo:** {row['target_mw']} MW | **Installato Netto:** {row['installato_mw']} MW"
            )
        else:
            st.error(
                f"**2. Avanzamento PNIEC (Dati Terna)**\n\n"
                f"⚠️ **In ritardo:** `{delta_val} MW` rispetto al target progressivo\n\n"
                f"📊 **Target Periodo:** {row['target_mw']} MW | **Installato Netto:** {row['installato_mw']} MW"
            )
        
        # INFO 3: Placeholder Legge Regionale
        st.write(
            f"**3. Legge Regionale Aree Idonee**\n\n"
            f"🔗 *(I link alle normative andranno mappati separatamente per le singole regioni)*"
        )
        
    else:
        st.write("👈 **Clicca su una regione nella mappa** oppure selezionala dal menu a sinistra per visualizzare i dettagli.")

# 9. Tabella Generale
st.markdown("---")
with st.expander("📊 Visualizza i dati Terna completi delle 20 regioni"):
    st.dataframe(
        df[["regione", "presidente", "installato_mw", "target_mw", "delta_mw"]],
        column_config={
            "regione": "Regione",
            "presidente": "Presidente",
            "installato_mw": st.column_config.NumberColumn("Installato gen 21-lug 26 (MW)", format="%d MW"),
            "target_mw": st.column_config.NumberColumn("Target Aree Idonee (MW)", format="%d MW"),
            "delta_mw": st.column_config.NumberColumn("Delta Scostamento (MW)", format="%d MW")
        },
        use_container_width=True,
        hide_index=True
    )
