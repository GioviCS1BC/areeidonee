import streamlit as st
import pandas as pd
import plotly.express as px
import requests

# 1. Configurazione
st.set_page_config(page_title="Monitoraggio Rinnovabili", layout="wide", initial_sidebar_state="expanded")
st.title("🗺️ Mappa Italia: Corsa alle Rinnovabili e Decreto Aree Idonee")
st.markdown("Questa mappa interattiva mostra in tempo reale chi è in ritardo e chi è in anticipo rispetto agli obiettivi vincolanti fissati per ciascuna regione.")

# 2. GeoJSON Originale di OpenPolis
@st.cache_data
def load_geojson():
    url = "https://raw.githubusercontent.com/openpolis/geojson-italy/master/geojson/limits_IT_regions.geojson"
    return requests.get(url).json()

geojson_data = load_geojson()

# 3. Dati Attuali
data = {
    "regione": [
        "Abruzzo", "Basilicata", "Calabria", "Campania", "Emilia-Romagna", 
        "Friuli-Venezia Giulia", "Lazio", "Liguria", "Lombardia", "Marche", 
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
        -124, -182, -447, 91, 65, 314, 1428, -102, 697, -125, 
        -181, 422, -267, -599, -3, -302, 95, -193, -23, 377
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
df["delta_perc"] = ((df["delta_mw"] / df["target_mw"]) * 100).round(1)

def categorizza_schieramento(coalizione):
    if "Centrodestra" in coalizione: return "Centrodestra"
    if "Centrosinistra" in coalizione: return "Centrosinistra"
    return "Autonomisti"

df["macro_area_politica"] = df["coalizione"].apply(categorizza_schieramento)

# 4. Caricamento Dati Storici dal nuovo file
@st.cache_data
def load_historical_data():
    try:
        # Leggiamo direttamente il foglio corretto
        df_hist = pd.read_excel('dataset_energie_rinnovabili.xlsx', sheet_name='Andamento_Storico_Politico')
        return df_hist
    except Exception as e:
        return None

df_storico = load_historical_data()

# 5. Interfaccia Sidebar
st.sidebar.header("⚙️ Opzioni Visualizzazione")
tipo_visualizzazione = st.sidebar.radio(
    "Mostra i dati sulla mappa come:",
    options=["Valore Assoluto (MW)", "Percentuale sul Target (%)"]
)

# 6. Mappa Leggera (px.choropleth base)
colonna_colore = "delta_mw" if tipo_visualizzazione == "Valore Assoluto (MW)" else "delta_perc"
etichetta_colore = "Scostamento (MW)" if tipo_visualizzazione == "Valore Assoluto (MW)" else "Scostamento (%)"

fig = px.choropleth(
    df,
    geojson=geojson_data,
    locations="regione",
    featureidkey="properties.reg_name",
    color=colonna_colore,
    color_continuous_scale="RdYlGn",
    color_continuous_midpoint=0,
    scope="europe",
    hover_name="regione",
    hover_data={"presidente": True, "delta_mw": True, "delta_perc": True, "regione": False},
    labels={
        "delta_mw": "Scostamento (MW)",
        "delta_perc": "Scostamento (%)",
        "presidente": "Governatore"
    }
)

fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0}, height=550)

# 7. Layout a colonne
col_map, col_details = st.columns([1.3, 1])

with col_map:
    map_selection = st.plotly_chart(fig, use_container_width=True, on_select="rerun", selection_mode="points")

# 8. Pannello Dettagli o Grafico Storico
with col_details:
    selected_region = None
    if map_selection and "selection" in map_selection and map_selection["selection"]["points"]:
        selected_region = map_selection["selection"]["points"][0].get("location")
        
    if selected_region:
        # Mostra i dettagli della regione selezionata
        row = df[df["regione"] == selected_region].iloc[0]
        st.markdown(f"### **Dettaglio: {row['regione']}**")
        st.write(f"👤 **Presidente:** {row['presidente']} (*{row['coalizione']}*)")
        st.write("---")
        
        delta_val = row['delta_mw']
        if delta_val >= 0:
            st.success(f"**Avanzamento**\n\n✅ **In anticipo:** `+{delta_val} MW` (+{row['delta_perc']}% sul target)")
        else:
            st.error(f"**Avanzamento**\n\n⚠️ **In ritardo:** `{delta_val} MW` ({row['delta_perc']}% sul target)")
        
        st.write(f"📊 **Target progressivo:** {row['target_mw']} MW")
        st.write(f"📈 **Installato netto:** {row['installato_mw']} MW")
            
    else:
        # Mostra il grafico storico se nessuna regione è cliccata
        st.markdown("### 📈 Spread: Centrodestra vs Centrosinistra")
        st.write("Andamento aggregato nel tempo dello scostamento in MW (Clicca su una regione per i dettagli singoli).")
        
        if df_storico is not None:
            # Creiamo il grafico a linee usando le colonne del nuovo dataset
            fig_line = px.line(
                df_storico, 
                x='Data', 
                y=['Centro-Destra (Totale MW)', 'Centro-Sinistra (Totale MW)'],
                color_discrete_map={
                    "Centro-Destra (Totale MW)": "#1f77b4", # Blu
                    "Centro-Sinistra (Totale MW)": "#d62728" # Rosso
                },
                labels={"value": "Scostamento (MW)", "variable": "", "Data": "Data Rilevazione"}
            )
            
            # Pulizia dei nomi nella legenda
            newnames = {'Centro-Destra (Totale MW)': 'Centrodestra', 'Centro-Sinistra (Totale MW)': 'Centrosinistra'}
            fig_line.for_each_trace(lambda t: t.update(name=newnames.get(t.name, t.name)))
            
            fig_line.add_hline(y=0, line_dash="dash", line_color="black")
            fig_line.update_layout(
                margin={"r": 0, "t": 10, "l": 0, "b": 0}, 
                height=350,
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            st.plotly_chart(fig_line, use_container_width=True)
        else:
            st.warning("⚠️ File 'dataset_energie_rinnovabili.xlsx' non trovato. Assicurati di averlo caricato su GitHub.")

# 9. Metriche Finali
st.markdown("---")
st.subheader("⚖️ Bilancio dell'Avanzamento")
st.write("Aggregazione dello scostamento complessivo (in MW) in base al colore politico della Giunta.")
bilancio = df.groupby("macro_area_politica")["delta_mw"].sum()

col1, col2, col3 = st.columns(3)
val_cdx = bilancio.get('Centrodestra', 0)
val_csx = bilancio.get('Centrosinistra', 0)
val_aut = bilancio.get('Autonomisti', 0)

col1.metric("🔵 Centrodestra", f"{val_cdx} MW", delta="In anticipo" if val_cdx >= 0 else "In ritardo", delta_color="normal" if val_cdx >= 0 else "inverse")
col2.metric("🔴 Centrosinistra", f"{val_csx} MW", delta="In anticipo" if val_csx >= 0 else "In ritardo", delta_color="normal" if val_csx >= 0 else "inverse")
col3.metric("⚪ Autonomisti", f"{val_aut} MW", delta="In anticipo" if val_aut >= 0 else "In ritardo", delta_color="normal" if val_aut >= 0 else "inverse")
