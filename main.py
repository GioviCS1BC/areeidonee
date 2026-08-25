import streamlit as st
import pandas as pd
import plotly.express as px
import requests

# 1. Configurazione della pagina Streamlit
st.set_page_config(
    page_title="Monitoraggio Obiettivi Rinnovabili Regioni",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Titoli e descrizioni
st.title("🗺️ Mappa Italia: Corsa alle Rinnovabili e Decreto Aree Idonee")
st.markdown(
    "Questa mappa interattiva mostra in tempo reale **chi è in ritardo e chi è in anticipo** "
    "sull'installazione di nuovi impianti a fonti rinnovabili (fotovoltaico ed eolico) "
    "rispetto agli obiettivi vincolanti fissati per ciascuna regione."
)

# 2. Download dinamico del GeoJSON
@st.cache_data
def load_geojson():
    url = "https://raw.githubusercontent.com/openpolis/geojson-italy/master/geojson/limits_IT_regions.geojson"
    response = requests.get(url)
    return response.json()

geojson_data = load_geojson()

# 3. Struttura Dati (Tabella Terna)
data = {
    "regione": [
        "Abruzzo", "Basilicata", "Calabria", "Campania", "Emilia-Romagna", 
        "Friuli-Venezia Giulia", "Lazio", "Liguria", "Lombardia", "Marche", 
        "Molise", "Piemonte", "Puglia", "Sardegna", "Sicilia", "Toscana", 
        "Trentino-Alto Adige", "Umbria", "Valle d'Aosta", "Veneto"
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

# Calcolo percentuale e classificazione politica
df["delta_perc"] = ((df["delta_mw"] / df["target_mw"]) * 100).round(1)

def categorizza_schieramento(coalizione):
    if "Centrodestra" in coalizione:
        return "Centrodestra"
    elif "Centrosinistra" in coalizione:
        return "Centrosinistra"
    else:
        return "Autonomisti"

df["macro_area_politica"] = df["coalizione"].apply(categorizza_schieramento)

# Indicatore complessivo Italia
totale_delta_italia = 940
st.info(
    f"🇮🇹 **Situazione Nazionale:** L'Italia nel suo complesso ha installato **29.063 MW** dall'inizio del 2021. "
    f"Rispetto al target atteso ad oggi, il Paese è attualmente **in anticipo di {totale_delta_italia} MW** sulla tabella di marcia."
)

# 4. Sidebar (Filtri e Opzioni)
st.sidebar.header("🔍 Ricerca Regione")
regione_selezionata_sidebar = st.sidebar.selectbox(
    "Cerca o seleziona una Regione:",
    options=["Nessuna"] + list(df["regione"].unique())
)

st.sidebar.markdown("---")
st.sidebar.header("⚙️ Opzioni Visualizzazione")
tipo_visualizzazione = st.sidebar.radio(
    "Mostra i dati sulla mappa come:",
    options=["Valore Assoluto (MW)", "Percentuale sul Target (%)"]
)

# 5. Costruzione Mappa Dinamica
if tipo_visualizzazione == "Valore Assoluto (MW)":
    colonna_colore = "delta_mw"
    etichetta_colore = "Scostamento (MW)"
    hover_dati = {
        "presidente": True,
        "delta_mw": True,
        "delta_perc": False,
        "installato_mw": False,
        "target_mw": False,
        "regione": False
    }
else:
    colonna_colore = "delta_perc"
    etichetta_colore = "Scostamento (%)"
    hover_dati = {
        "presidente": True,
        "delta_perc": True,
        "delta_mw": False,
        "installato_mw": False,
        "target_mw": False,
        "regione": False
    }

fig = px.choropleth_mapbox(
    df,
    geojson=geojson_data,
    locations="regione",
    featureidkey="properties.reg_name",
    color=colonna_colore,
    color_continuous_scale="RdYlGn",
    color_continuous_midpoint=0,
    mapbox_style="carto-positron",
    zoom=4.8,
    center={"lat": 41.9, "lon": 12.5},
    opacity=0.8,
    hover_name="regione",
    hover_data=hover_dati,
    labels={
        "delta_mw": "Scostamento (MW)",
        "delta_perc": "Scostamento (%)",
        "presidente": "Governatore"
    }
)

fig.update_layout(
    margin={"r": 0, "t": 0, "l": 0, "b": 0},
    height=550,
    clickmode="event+select",
    coloraxis_colorbar_title_text=etichetta_colore
)

# 6. Layout a colonne
col_map, col_details = st.columns([1.3, 1])

with col_map:
    st.subheader(f"Mappa Italia - {tipo_visualizzazione}")
    map_selection = st.plotly_chart(
        fig, 
        use_container_width=True, 
        on_select="rerun", 
        selection_mode="points"
    )

# 7. Intercettazione Selezione
selected_region_name = None

if map_selection and "selection" in map_selection and map_selection["selection"]["points"]:
    point = map_selection["selection"]["points"][0]
    if "location" in point:
        selected_region_name = point["location"]

if regione_selezionata_sidebar != "Nessuna":
    selected_region_name = regione_selezionata_sidebar

# 8. Visualizzazione Dettagli o Spiegazione Utente
with col_details:
    if selected_region_name:
        row = df[df["regione"] == selected_region_name].iloc[0]
        
        st.markdown(f"### **Dettaglio: {row['regione']}**")
        
        st.write(
            f"👤 **Presidente:** {row['presidente']} "
            f"(*( {row['coalizione']} )*)"
        )
        st.write("---")
        
        delta_val = row['delta_mw']
        delta_perc = row['delta_perc']
        
        if delta_val >= 0:
            st.success(
                f"**Avanzamento Nuove Rinnovabili**\n\n"
                f"✅ **In anticipo:** `+{delta_val} MW` (+{delta_perc}% sul target)\n\n"
                f"📊 **Target progressivo:** {row['target_mw']} MW\n\n"
                f"📈 **Installato netto:** {row['installato_mw']} MW"
            )
        else:
            st.error(
                f"**Avanzamento Nuove Rinnovabili**\n\n"
                f"⚠️ **In ritardo:** `{delta_val} MW` ({delta_perc}% sul target)\n\n"
                f"📊 **Target progressivo:** {row['target_mw']} MW\n\n"
                f"📉 **Installato netto:** {row['installato_mw']} MW"
            )
            
        st.write("---")
        st.write("🔗 *Riferimento normativo Aree Idonee in fase di aggiornamento.*")
        
    else:
        st.markdown("### Come leggere i dati")
        st.write(
            "I colori sulla mappa indicano lo scostamento tra quanto la singola regione avrebbe "
            "dovuto installare fino ad oggi e quanto ha effettivamente realizzato."
        )
        st.info(
            "🟢 **I colori verdi** indicano le regioni in anticipo: hanno già installato "
            "più Megawatt di quelli richiesti."
        )
        st.warning(
            "🔴 **I colori rossi** indicano le regioni in ritardo: sono indietro rispetto "
            "al percorso assegnato dallo Stato."
        )
        st.markdown("👈 **Clicca su una regione sulla mappa** per i numeri esatti.")

# --- NUOVA SEZIONE: BILANCIO POLITICO ---
st.markdown("---")
st.subheader("⚖️ Bilancio dell'Avanzamento per Schieramento Politico")
st.write("Aggregazione del ritardo o anticipo complessivo (in MW) in base al colore politico della Giunta Regionale.")

bilancio = df.groupby("macro_area_politica")["delta_mw"].sum().reset_index()

val_cdx = bilancio.loc[bilancio['macro_area_politica'] == 'Centrodestra', 'delta_mw'].sum()
val_csx = bilancio.loc[bilancio['macro_area_politica'] == 'Centrosinistra', 'delta_mw'].sum()
val_aut = bilancio.loc[bilancio['macro_area_politica'] == 'Autonomisti', 'delta_mw'].sum()

col_cdx, col_csx, col_aut = st.columns(3)

with col_cdx:
    st.metric(
        label="🔵 Regioni di Centrodestra", 
        value=f"{val_cdx} MW",
        delta="In anticipo" if val_cdx >= 0 else "In ritardo",
        delta_color="normal" if val_cdx >= 0 else "inverse"
    )

with col_csx:
    st.metric(
        label="🔴 Regioni di Centrosinistra", 
        value=f"{val_csx} MW",
        delta="In anticipo" if val_csx >= 0 else "In ritardo",
        delta_color="normal" if val_csx >= 0 else "inverse"
    )

with col_aut:
    st.metric(
        label="⚪ Autonomisti (Valle d'Aosta)", 
        value=f"{val_aut} MW",
        delta="In anticipo" if val_aut >= 0 else "In ritardo",
        delta_color="normal" if val_aut >= 0 else "inverse"
    )

# 9. Tabella Generale
st.markdown("---")
with st.expander("📊 Tabella analitica completa delle 20 regioni (Dati Terna)"):
    st.dataframe(
        df[["regione", "presidente", "installato_mw", "target_mw", "delta_mw", "delta_perc"]],
        column_config={
            "regione": "Regione",
            "presidente": "Presidente",
            "installato_mw": st.column_config.NumberColumn("Installato Reale (MW)", format="%d MW"),
            "target_mw": st.column_config.NumberColumn("Target Previsto (MW)", format="%d MW"),
            "delta_mw": st.column_config.NumberColumn("Scostamento (MW)", format="%d MW"),
            "delta_perc": st.column_config.NumberColumn("Scostamento (%)", format="%.1f %%")
        },
        use_container_width=True,
        hide_index=True
    )
